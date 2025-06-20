import aiohttp
from datetime import datetime
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

GEOD_CONTRACT = "0xAC0F66379A6d7801D7726d5a943356A172549Adb"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    wallet = config_entry.data["wallet_address"]
    api_key = config_entry.data["polygonscan_api_key"]
    balance_sensor = GEODBalanceSensor(wallet, api_key)
    delta_sensor = GEODTokensReceivedTodaySensor(balance_sensor)

    async_add_entities([balance_sensor, delta_sensor], True)

    async def handle_refresh(call):
        await balance_sensor.async_update()
        balance_sensor.async_write_ha_state()
        delta_sensor.update_tokens_received()
        delta_sensor.async_write_ha_state()

    hass.services.async_register(DOMAIN, "refresh_balance", handle_refresh)

class GEODBalanceSensor(Entity):
    def __init__(self, wallet_address, api_key):
        self._wallet_address = wallet_address
        self._api_key = api_key
        self._state = None
        self._attr_name = "GEOD Token Balance"
        self._attr_unique_id = f"geod_balance_{wallet_address[-6:]}"
        self._attr_unit_of_measurement = "GEOD"
        self._last_updated = None

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
    def extra_state_attributes(self):
        return {
            "last_updated": self._last_updated
        }

    async def async_update(self):
        url = (
            "https://api.polygonscan.com/api"
            f"?module=account&action=tokenbalance"
            f"&contractaddress={GEOD_CONTRACT}"
            f"&address={self._wallet_address}&tag=latest&apikey={self._api_key}"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if data.get("status") == "1":
                    self._state = round(int(data["result"]) / 1e18, 4)
                    self._last_updated = datetime.utcnow().isoformat()
                else:
                    self._state = None

class GEODTokensReceivedTodaySensor(Entity):
    def __init__(self, balance_sensor):
        self._balance_sensor = balance_sensor
        self._attr_name = "GEOD Tokens Received Today"
        self._attr_unique_id = f"geod_received_today_{balance_sensor._wallet_address[-6:]}"
        self._attr_unit_of_measurement = "GEOD"
        self._midnight_balance = None
        self._state = None

    @property
    def name(self):
        return self._attr_name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def state(self):
        return self._state

    def update_tokens_received(self):
        now = datetime.utcnow()
        if self._midnight_balance is None or now.hour == 0:
            self._midnight_balance = self._balance_sensor.state
        if self._midnight_balance is not None and self._balance_sensor.state is not None:
            self._state = round(float(self._balance_sensor.state) - float(self._midnight_balance), 4)
