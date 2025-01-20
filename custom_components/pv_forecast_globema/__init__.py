import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.pv_forecast_globema.const import CONF_FILTER_THE_STUFF, DOMAIN
from custom_components.pv_forecast_globema.data_fetcher import fetch_data
from custom_components.pv_forecast_globema.sensor import GlobemaSensor

_LOGGER = logging.getLogger(__package__ + __name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the PV Forecast Globema integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up sensors for PV Forecast Globema."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        GlobemaSensor(sensor_data["area"], coordinator) for sensor_data in coordinator.data
    ]
    async_add_entities(sensors, True)
