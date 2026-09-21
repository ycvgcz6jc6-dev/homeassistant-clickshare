from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

class ClickShareEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.entry = entry
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.unique_id or entry.entry_id)},
            "manufacturer": "Barco",
            "name": entry.title,
            "configuration_url": f"https://{entry.data['host']}",
        }
