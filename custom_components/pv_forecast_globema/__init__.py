from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later  # Direct import

from custom_components.pv_forecast_globema.const import CONF_FILTER_THE_STUFF, DOMAIN


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the PV Forecast Globema integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up PV Forecast Globema from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Log the configuration option
    filter_the_stuff = entry.data.get(CONF_FILTER_THE_STUFF, False)
    async_call_later(
        0, lambda: hass.components.logger.getLogger(__name__).info(
            f"Filter the Stuff: {'Enabled' if filter_the_stuff else 'Disabled'}"
        )
    )
    return True
