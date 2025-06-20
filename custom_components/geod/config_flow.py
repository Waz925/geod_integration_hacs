from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class GeodConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="GEOD Wallet", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("wallet_address"): str,
                vol.Required("polygonscan_api_key"): str
            })
        )
