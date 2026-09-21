from homeassistant.components.button import ButtonEntity
from .const import DOMAIN
from .entity import ClickShareEntity
async def async_setup_entry(hass,e,add):add([Refresh(hass.data[DOMAIN][e.entry_id],e)])
class Refresh(ClickShareEntity,ButtonEntity):
 _attr_name="Refresh"
 def __init__(self,c,e):super().__init__(c,e);self._attr_unique_id=f"{e.unique_id}_refresh"
 async def async_press(self):await self.coordinator.async_request_refresh()

