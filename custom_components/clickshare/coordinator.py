from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator,UpdateFailed
from .const import DOMAIN,DEFAULT_SCAN_INTERVAL
from .api import ClickShareError
_LOGGER=logging.getLogger(__name__)
class ClickShareCoordinator(DataUpdateCoordinator):
 def __init__(self,hass,client):
  self.client=client
  super().__init__(hass,_LOGGER,name=DOMAIN,update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL))
 async def _async_update_data(self):
  try:
   d=await self.client.probe()
   if self.client.openapi:d["resources"]=await self.client.read_advertised_gets()
   return d
  except ClickShareError as e:raise UpdateFailed(str(e)) from e

