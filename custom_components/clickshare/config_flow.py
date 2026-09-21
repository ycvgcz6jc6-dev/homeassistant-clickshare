from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .const import DOMAIN, CONF_PORT, CONF_VERIFY_SSL, CONF_API_VERSION
from .api import ClickShareClient, ClickShareAuthError, ClickShareError

class ClickShareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            version = user_input[CONF_API_VERSION]
            port = user_input[CONF_PORT]
            client = ClickShareClient(
                user_input[CONF_HOST],
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                port,
                user_input[CONF_VERIFY_SSL],
                version,
            )
            try:
                await client.probe()
            except ClickShareAuthError:
                errors["base"] = "invalid_auth"
            except ClickShareError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_HOST]}-{version}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"ClickShare {user_input[CONF_HOST]}",
                    data=user_input
                )

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_USERNAME, default="admin"): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_API_VERSION, default="v2"): vol.In(["v2", "v1"]),
            vol.Required(CONF_PORT, default=4003): int,
            vol.Required(CONF_VERIFY_SSL, default=False): bool,
        })
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
