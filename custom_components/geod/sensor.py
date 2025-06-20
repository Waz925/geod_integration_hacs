import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


class GEODBalanceSensor(Entity):
    def __init__(self, wallet_address, api_key):
        self._wallet_address = wallet_address
        self._api_key = api_key
        self._state = None
        self._attr_name = "GEOD Token Balance"
        self._attr_unique_id = f"geod_balance_{wallet_address[-6:]}"
        self._attr_unit_of_measurement = "GEOD"

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._attr_unit_of_measurement

    async def async_update(self):
        url = (
            "https://api.polygonscan.com/api"
            f"?module=account&action=tokenbalance"
            f"&contractaddress=0xAC0F66379A6d7801D7726d5a943356A172549Adb"
            f"&address={self._wallet_address}&tag=latest&apikey={self._api_key}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if data.get("status") == "1":
                    self._state = round(int(data["result"]) / 1e18, 4)
                else:
                    self._state = None


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    wallet = config_entry.data.get("wallet_address")
    api_key = config_entry.data.get("polygonscan_api_key")
    async_add_entities([GEODBalanceSensor(wallet, api_key)], True)
