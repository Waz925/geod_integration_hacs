"""GEOD Token Integration."""
from .const import DOMAIN

async def async_setup_entry(hass, config_entry):
    from .sensor import async_setup_entry as sensor_setup
    await sensor_setup(hass, config_entry, lambda: None)
    return True
