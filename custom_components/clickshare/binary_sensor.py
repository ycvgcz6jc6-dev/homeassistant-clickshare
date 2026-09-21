from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import ClickShareEntity

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ClickShareOnline(c, entry), ClickShareSharing(c, entry)])

class ClickShareOnline(ClickShareEntity, BinarySensorEntity):
    _attr_name = "REST API"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_online"
    @property
    def is_on(self):
        return self.coordinator.last_update_success

class ClickShareSharing(ClickShareEntity, BinarySensorEntity):
    _attr_name = "Sharing active"
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_sharing"
    @property
    def is_on(self):
        # Conservative generic inference from advertised resources.
        # Unknown remains None rather than fabricating a state.
        resources = self.coordinator.data.get("resources", {})
        keys = ("sharing", "presenting", "presentation", "activeSources", "activeSource")
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k in keys:
                        if isinstance(v, bool): return v
                        if isinstance(v, list): return bool(v)
                        if isinstance(v, (int, str)): return bool(v)
                    r = walk(v)
                    if r is not None: return r
            elif isinstance(x, list):
                for v in x:
                    r = walk(v)
                    if r is not None: return r
            return None
        return walk(resources)
