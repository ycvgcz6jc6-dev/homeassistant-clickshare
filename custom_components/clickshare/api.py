from __future__ import annotations
import asyncio,json,ssl,base64
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
class ClickShareError(Exception): pass
class ClickShareAuthError(ClickShareError): pass
class ClickShareClient:
 def __init__(self,host,username,password,port=4003,verify_ssl=False,api_version="v2"):
  self.host,self.username,self.password,self.port,self.verify_ssl,self.api_version=host,username,password,port,verify_ssl,api_version
  self.openapi={}
 @property
 def base_url(self): return f'{"https" if self.api_version=="v2" else "http"}://{self.host}:{self.port}'
 def _sync(self,method,path,body=None):
  token=base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
  h={"Authorization":f"Basic {token}","Accept":"application/json"}
  d=None
  if body is not None: d=json.dumps(body).encode();h["Content-Type"]="application/json"
  ctx=ssl._create_unverified_context() if self.base_url.startswith("https") and not self.verify_ssl else None
  try:
   with urlopen(Request(self.base_url+path,data=d,headers=h,method=method),timeout=8,context=ctx) as r:
    raw=r.read()
    try:return json.loads(raw)
    except:return raw.decode(errors="replace")
  except HTTPError as e:
   if e.code in (401,403): raise ClickShareAuthError(str(e))
   raise ClickShareError(str(e))
  except (URLError,OSError,TimeoutError) as e: raise ClickShareError(str(e))
 async def get(self,path): return await asyncio.to_thread(self._sync,"GET",path)
 async def load_openapi(self):
  if self.api_version!="v2": return {}
  for p in ("/api-docs/v2/openapi.json","/api-docs/v2/swagger.json","/api-docs/v2"):
   try:
    d=await self.get(p)
    if isinstance(d,dict) and "paths" in d:self.openapi=d;return d
   except ClickShareError: pass
  return {}
 async def probe(self):
  r={"api_version":self.api_version,"host":self.host}
  if self.api_version=="v2":
   await self.load_openapi();r["openapi_available"]=bool(self.openapi)
   try:r["buttons"]=await self.get("/v2/configuration/buttons")
   except ClickShareError:r["buttons"]=None
  return r
 async def read_advertised_gets(self,limit=40):
  if not self.openapi: await self.load_openapi()
  out={}
  for p,ops in self.openapi.get("paths",{}).items():
   if "get" not in ops or "{" in p or not p.startswith("/v2/"):continue
   try:out[p]=await self.get(p)
   except ClickShareError as e:out[p]={"_error":str(e)}
   if len(out)>=limit:break
  return out

