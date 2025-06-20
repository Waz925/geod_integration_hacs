"""GEOD Token Integration."""
from .const import DOMAIN
from .sensor import async_setup_entry
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    await async_setup_entry(hass, config_entry)
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    return True
