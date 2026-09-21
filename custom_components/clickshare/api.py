from __future__ import annotations
import asyncio
import json
import ssl
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import base64

class ClickShareError(Exception):
    pass

class ClickShareAuthError(ClickShareError):
    pass

@dataclass
class ApiResponse:
    status: int
    data: Any
    headers: dict[str, str]

class ClickShareClient:
    """Small async wrapper around ClickShare REST.

    V2 is HTTPS on TCP 4003. Basic authentication uses the same credentials
    as the Web Configurator. The client deliberately does not hard-code
    undocumented control endpoints. It reads the Base Unit OpenAPI document
    when available and only exposes operations that the unit advertises.
    """
    def __init__(self, host: str, username: str, password: str,
                 port: int = 4003, verify_ssl: bool = False,
                 api_version: str = "v2"):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.verify_ssl = verify_ssl
        self.api_version = api_version
        self.openapi: dict[str, Any] = {}

    @property
    def base_url(self):
        scheme = "https" if self.api_version == "v2" else "http"
        return f"{scheme}://{self.host}:{self.port}"

    def _sync_request(self, method: str, path: str, body=None,
                      accept="application/json") -> ApiResponse:
        url = self.base_url + path
        token = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()
        headers = {
            "Authorization": f"Basic {token}",
            "Accept": accept,
        }
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        req = Request(url, data=data, headers=headers, method=method)
        context = None
        if url.startswith("https://") and not self.verify_ssl:
            context = ssl._create_unverified_context()
        try:
            with urlopen(req, timeout=8, context=context) as resp:
                raw = resp.read()
                content_type = resp.headers.get("Content-Type", "")
                if "json" in content_type or raw[:1] in (b"{", b"["):
                    try:
                        payload = json.loads(raw.decode())
                    except Exception:
                        payload = raw.decode(errors="replace")
                else:
                    payload = raw.decode(errors="replace")
                return ApiResponse(resp.status, payload, dict(resp.headers))
        except HTTPError as exc:
            if exc.code in (401, 403):
                raise ClickShareAuthError(f"Authentication failed ({exc.code})") from exc
            raise ClickShareError(f"HTTP {exc.code}: {exc.reason}") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise ClickShareError(str(exc)) from exc

    async def request(self, method, path, body=None):
        return await asyncio.to_thread(self._sync_request, method, path, body)

    async def get(self, path):
        return (await self.request("GET", path)).data

    async def patch(self, path, body):
        return (await self.request("PATCH", path, body)).data

    async def post(self, path, body=None):
        return (await self.request("POST", path, body)).data

    async def load_openapi(self):
        """Try common Swagger/OpenAPI JSON locations on the Base Unit."""
        if self.api_version != "v2":
            return {}
        candidates = [
            "/api-docs/v2/openapi.json",
            "/api-docs/v2/swagger.json",
            "/api-docs/v2",
        ]
        for path in candidates:
            try:
                data = await self.get(path)
                if isinstance(data, dict) and ("paths" in data or "openapi" in data or "swagger" in data):
                    self.openapi = data
                    return data
            except ClickShareError:
                continue
        return {}

    def supports(self, path: str, method: str = "get") -> bool:
        paths = self.openapi.get("paths", {})
        return path in paths and method.lower() in paths[path]

    async def probe(self):
        """Validate credentials and collect a useful initial snapshot."""
        result = {"api_version": self.api_version, "host": self.host}
        if self.api_version == "v2":
            await self.load_openapi()
            result["openapi_available"] = bool(self.openapi)
            # Officially documented by Barco and safe/read-only.
            try:
                result["buttons"] = await self.get("/v2/configuration/buttons")
            except ClickShareError:
                result["buttons"] = None
        else:
            # V1 differs by firmware/model. Validate HTTP/auth without
            # pretending V2 endpoints apply.
            try:
                result["root"] = await self.get("/")
            except ClickShareError:
                result["root"] = None
        return result

    async def read_advertised_gets(self, limit=40):
        """Read safe GET resources advertised by the unit's own V2 OpenAPI.

        This makes diagnostics useful across firmware/model revisions without
        inventing endpoints. Failures are isolated per resource.
        """
        if not self.openapi:
            await self.load_openapi()
        out = {}
        for path, ops in self.openapi.get("paths", {}).items():
            if "get" not in ops or "{" in path:
                continue
            if not path.startswith("/v2/"):
                continue
            try:
                out[path] = await self.get(path)
            except ClickShareError as exc:
                out[path] = {"_error": str(exc)}
            if len(out) >= limit:
                break
        return out
