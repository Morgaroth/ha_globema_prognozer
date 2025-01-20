from homeassistant import config_entries
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from custom_components.pv_forecast_globema.const import DOMAIN


class PVForecastGlobemaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PV Forecast Globema."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="PV Forecast Globema", data=user_input)

        # Configuration schema
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional("filter_the_stuff", default=False): cv.boolean,
                }
            ),
        )
