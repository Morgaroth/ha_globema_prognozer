# """Sensor platform for Prognozer."""
# import logging
#
# import requests
# from homeassistant.components.sensor import SensorEntity
#
# API_URL = "https://prognozer.globema.pl/api/layers/20005/geojson?outputFormat=application/json"
#
# TRACKED_KEYS = [
#     "nazwa",
#     "kod_teryt",
#     "slonce_dzis_proc",
#     "slonce_jutro_proc",
#     "slonce_pojutrze_proc",
#     "slonce_prosum_dzis_proc",
#     "slonce_prosum_jutro_proc",
#     "slonce_prosum_pojutrze_proc",
# ]
#
# _LOGGER: logging.Logger = logging.getLogger(__package__)
#
#
# def fetch_data():
#     response = requests.get(API_URL)
#     response.raise_for_status()
#     data = response.json()
#     sensors = []
#
#     for feature in data["features"]:
#         # if feature['id'] != 'wojewodztwo.43':
#         #     continue
#         properties = feature["properties"]
#
#         # Create a filtered dictionary with only the positive keys
#         filtered_data = {key: properties[key] for key in TRACKED_KEYS if key in properties}
#         sensors.append(filtered_data)
#
#     logging.info(f"Created [{len(sensors)}] from {data}")
#
#     return sensors
#
#
# async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
#     """Set up the sensor platform."""
#     sensors = fetch_data()
#     entities = [GlobemaForecastSensor(data["nazwa"], data) for data in sensors]
#     async_add_entities(entities, True)
#
#
# class GlobemaForecastSensor(SensorEntity):
#     """Representation of a Prognozer sensor."""
#
#     def __init__(self, name, data):
#         """Initialize the sensor."""
#         self._name = f"PV Forecast for {name.capitalize()}"
#         self._state = data.get("slonce_dzis_proc")  # Use `slonce_dzis_proc` as the main state
#         self._data = data
#
#     @property
#     def name(self):
#         """Return the name of the sensor."""
#         return self._name
#
#     @property
#     def state(self):
#         """Return the state of the sensor."""
#         return self._state
#
#     @property
#     def extra_state_attributes(self):
#         """Return additional attributes."""
#         return self._data
#
#     async def async_update(self):
#         """Update the sensor."""
#         # Normally, update logic would be here if needed.
#         pass

"""Sensor platform for PV Forecast Globema."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up sensors for PV Forecast Globema."""
    config = hass.data[DOMAIN][entry.entry_id]

    # Create a list of sensors
    sensors = [
        GlobemaSensor("Today Solar Potential", "slonce_dzis_proc", 58.0),
        GlobemaSensor("Tomorrow Solar Potential", "slonce_jutro_proc", 19.6),
    ]
    async_add_entities(sensors, True)

class GlobemaSensor(SensorEntity):
    """Representation of a PV Forecast Globema sensor."""

    def __init__(self, name, key, initial_value):
        """Initialize the sensor."""
        self._name = name
        self._key = key
        self._state = initial_value

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"pv_forecast_{self._key}"

    async def async_update(self):
        """Fetch new data and update the state."""
        # Simulate fetching new data
        # Replace this with your actual API call or data processing logic
        self._state += 1  # Simulate data change for testing
