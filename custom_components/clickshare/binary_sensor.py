from homeassistant.components.binary_sensor import BinarySensorEntity,BinarySensorDeviceClass
from .const import DOMAIN
from .entity import ClickShareEntity
async def async_setup_entry(hass,e,add):add([Online(hass.data[DOMAIN][e.entry_id],e)])
class Online(ClickShareEntity,BinarySensorEntity):
 _attr_name="REST API";_attr_device_class=BinarySensorDeviceClass.CONNECTIVITY
 def __init__(self,c,e):super().__init__(c,e);self._attr_unique_id=f"{e.unique_id}_online"
 @property
 def is_on(self):return self.coordinator.last_update_success

