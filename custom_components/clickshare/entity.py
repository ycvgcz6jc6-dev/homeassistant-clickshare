from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
class ClickShareEntity(CoordinatorEntity):
 _attr_has_entity_name=True
 def __init__(self,c,e):
  super().__init__(c);self.entry=e;self._attr_device_info={"identifiers":{(DOMAIN,e.unique_id or e.entry_id)},"manufacturer":"Barco","name":e.title}

