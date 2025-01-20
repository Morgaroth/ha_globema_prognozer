from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
import voluptuous as vol
from .const import DOMAIN
from .sensor import fetch_data

class PVForecastGlobemaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.available_options = []

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="PV Forecast Globema", data=user_input)

        # Fetch options directly using fetch_data
        try:
            data = await fetch_data()
            self.available_options = [item["name"] for item in data]
        except Exception as e:
            self.available_options = []
            self.hass.components.logger.getLogger(__name__).error(
                "Failed to fetch options: %s", e
            )

        # Fallback in case no options are available
        if not self.available_options:
            return self.async_abort(reason="no_data_available")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "selected_sensors",
                        default=[],
                    ): vol.All(
                        cv.ensure_list,
                        vol.In(self.available_options),
                    )
                }
            ),
        )
