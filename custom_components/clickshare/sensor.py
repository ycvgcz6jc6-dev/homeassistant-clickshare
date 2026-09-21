from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import ClickShareEntity
async def async_setup_entry(hass,e,add):add([Api(hass.data[DOMAIN][e.entry_id],e),Buttons(hass.data[DOMAIN][e.entry_id],e)])
class Api(ClickShareEntity,SensorEntity):
 _attr_name="API version";_attr_entity_category=EntityCategory.DIAGNOSTIC
 def __init__(self,c,e):super().__init__(c,e);self._attr_unique_id=f"{e.unique_id}_api"
 @property
 def native_value(self):return self.coordinator.data.get("api_version")
class Buttons(ClickShareEntity,SensorEntity):
 _attr_name="Buttons connected"
 def __init__(self,c,e):super().__init__(c,e);self._attr_unique_id=f"{e.unique_id}_buttons"
 @property
 def native_value(self):
  b=self.coordinator.data.get("buttons");return sum(1 for x in b if isinstance(x,dict) and x.get("connected")) if isinstance(b,list) else None
 @property
 def extra_state_attributes(self):return {"buttons":self.coordinator.data.get("buttons")}

