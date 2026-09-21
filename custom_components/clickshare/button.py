from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN
from .entity import ClickShareEntity

async def async_setup_entry(hass, entry, async_add_entities):
    c = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ClickShareRefresh(c, entry)])

class ClickShareRefresh(ClickShareEntity, ButtonEntity):
    _attr_name = "Refresh"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.unique_id}_refresh"
    async def async_press(self):
        await self.coordinator.async_request_refresh()
