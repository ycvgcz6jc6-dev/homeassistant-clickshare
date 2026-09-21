from .const import DOMAIN,PLATFORMS,CONF_PORT,CONF_VERIFY_SSL,CONF_API_VERSION
from .api import ClickShareClient
from .coordinator import ClickShareCoordinator
async def async_setup_entry(hass,entry):
 client=ClickShareClient(entry.data["host"],entry.data["username"],entry.data["password"],entry.data.get(CONF_PORT,4003),entry.data.get(CONF_VERIFY_SSL,False),entry.data.get(CONF_API_VERSION,"v2"))
 c=ClickShareCoordinator(hass,client);await c.async_config_entry_first_refresh()
 hass.data.setdefault(DOMAIN,{})[entry.entry_id]=c
 await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS);return True
async def async_unload_entry(hass,entry):
 ok=await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
 if ok:hass.data[DOMAIN].pop(entry.entry_id,None)
 return ok

