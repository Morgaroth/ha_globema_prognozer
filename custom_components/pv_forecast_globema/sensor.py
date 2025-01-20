"""Sensor platform for PV Forecast Globema."""
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__package__ + __name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up sensors for PV Forecast Globema."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        GlobemaSensor(sensor_data["name"], coordinator)
        for sensor_data in coordinator.data
    ]
    async_add_entities(sensors, True)


class GlobemaSensor(SensorEntity):
    """Representation of a PV Forecast Globema sensor."""

    def __init__(self, name, coordinator):
        """Initialize the sensor."""
        self._name = f"PV Forecast {name}"
        self.coordinator = coordinator
        self._data = next(
            (item for item in coordinator.data if item["name"] == name), {}
        )
        self._state = self._data.get("today")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return self.coordinator.data

    async def async_update(self):
        """Fetch new data for the sensor."""
        await self.coordinator.async_request_refresh()
        for item in self.coordinator.data:
            if item["name"] == self._name.split("PV Forecast ")[1]:
                self._state = item["today"]
                self._data = item
                break