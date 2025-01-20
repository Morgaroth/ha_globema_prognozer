import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from custom_components.pv_forecast_globema.const import CONF_FILTER_THE_STUFF, DOMAIN
from custom_components.pv_forecast_globema.data_fetcher import fetch_data
from custom_components.pv_forecast_globema.sensor import GlobemaSensor

_LOGGER = logging.getLogger(__package__ + __name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the PV Forecast Globema integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up PV Forecast Globema from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Set up DataUpdateCoordinator
    async def _update_method():
        return await fetch_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="PV Forecast Globema",
        update_method=_update_method,
        update_interval=timedelta(hours=1),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    sensors = [
        GlobemaSensor(sensor_data["area"], coordinator) for sensor_data in coordinator.data
    ]
    async_add_entities(sensors, True)
    return True
