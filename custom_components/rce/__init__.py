from homeassistant.core import HomeAssistant

DOMAIN = "pv_forecast_globema"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the PV Forecast Globema integration."""
    return True
