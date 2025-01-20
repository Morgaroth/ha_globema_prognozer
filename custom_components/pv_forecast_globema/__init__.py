from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, CONF_FILTER_THE_STUFF
from .sensor import fetch_data


async def async_setup(hass: HomeAssistant, config: dict):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    async def _update_method():
        return await fetch_data()

    coordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name="PV Forecast Globema",
        update_method=_update_method,
        update_interval=timedelta(hours=1),
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN]["coordinator"] = coordinator

    # Filter sensors based on user selection
    selected_sensors = entry.data.get("selected_sensors", [])
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "selected_sensors": selected_sensors,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if entry.entry_id in hass.data[DOMAIN]:
        await hass.config_entries.async_unload_platforms(entry, ["sensor"])
        hass.data[DOMAIN].pop(entry.entry_id)
    return True
