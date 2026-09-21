from __future__ import annotations
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .api import ClickShareError

_LOGGER = logging.getLogger(__name__)

class ClickShareCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client):
        self.client = client
        super().__init__(
            hass, _LOGGER, name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL)
        )

    async def _async_update_data(self):
        try:
            data = await self.client.probe()
            # If Swagger/OpenAPI is available, collect advertised read-only
            # resources. This is intentionally capped.
            if self.client.openapi:
                data["resources"] = await self.client.read_advertised_gets()
            return data
        except ClickShareError as exc:
            raise UpdateFailed(str(exc)) from exc
