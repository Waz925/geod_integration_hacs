from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, config_entry, async_add_entities):
    async_add_entities([GEODBalanceSensor()], True)

class GEODBalanceSensor(Entity):
    def __init__(self):
        self._state = None
        self._attr_name = "GEOD Token Balance"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        # Fetch balance (stub)
        self._state = 123.45
