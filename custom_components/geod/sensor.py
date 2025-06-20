import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

GEOD_TOKEN_DECIMALS = 1e18

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    wallet = config_entry.data.get("wallet_address")
    api_key = config_entry.data.get("polygonscan_api_key")
    sensor = GEODBalanceSensor(wallet, api_key)
    async_add_entities([sensor], True)

    async def handle_manual_refresh(call):
        await sensor.async_update()
        sensor.async_write_ha_state()

    hass.services.async_register("geod", "refresh_geod_data", handle_manual_refresh)

class GEODBalanceSensor(Entity):
    def __init__(self, wallet, api_key):
        self._wallet = wallet
        self._api_key = api_key
        self._state = None
        self._attr_name = "GEOD Token Balance"
        self._attr_unit_of_measurement = "GEOD"
        self._attr_icon = "mdi:currency-usd"

    @property
    def name(self):
        return "GEOD Token Balance"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        url = (
            "https://api.polygonscan.com/api"
            "?module=account"
            "&action=tokenbalance"
            "&contractaddress=0xAC0F66379A6d7801D7726d5a943356A172549Adb"
            f"&address={self._wallet}"
            "&tag=latest"
            f"&apikey={self._api_key}"
        )
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    data = await resp.json()
                    result = int(data.get("result", "0")) / GEOD_TOKEN_DECIMALS
                    self._state = round(result, 2)
        except Exception:
            self._state = None
