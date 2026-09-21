from __future__ import annotations
import json
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import ClickShareEntity

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ClickShareApiSensor(c, entry),
        ClickShareButtonsSensor(c, entry),
        ClickShareDiagnosticsSensor(c, entry),
    ])

class ClickShareApiSensor(ClickShareEntity, SensorEntity):
    _attr_name = "API version"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_api"
    @property
    def native_value(self):
        return self.coordinator.data.get("api_version", "unknown")

class ClickShareButtonsSensor(ClickShareEntity, SensorEntity):
    _attr_name = "Buttons connected"
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_buttons"
    @property
    def native_value(self):
        buttons = self.coordinator.data.get("buttons")
        if not isinstance(buttons, list):
            return None
        return sum(1 for b in buttons if isinstance(b, dict) and b.get("connected"))
    @property
    def extra_state_attributes(self):
        buttons = self.coordinator.data.get("buttons")
        return {"buttons": buttons} if buttons is not None else {}

class ClickShareDiagnosticsSensor(ClickShareEntity, SensorEntity):
    _attr_name = "REST diagnostics"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_diagnostics"
    @property
    def native_value(self):
        resources = self.coordinator.data.get("resources", {})
        return f"{len(resources)} resources"
    @property
    def extra_state_attributes(self):
        # HA attributes should stay reasonably sized. Keep endpoint names and
        # compact values; detailed raw JSON is available in coordinator logs.
        resources = self.coordinator.data.get("resources", {})
        compact = {}
        for k, v in list(resources.items())[:40]:
            s = json.dumps(v, default=str)
            compact[k] = s[:1000]
        return {
            "openapi_available": self.coordinator.data.get("openapi_available"),
            "resources": compact,
        }
