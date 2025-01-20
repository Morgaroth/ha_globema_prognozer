"""Sensor platform for Prognozer."""
import requests
from homeassistant.components.sensor import SensorEntity

API_URL = "https://prognozer.globema.pl/api/layers/20005/geojson?outputFormat=application/json"

TRACKED_KEYS = [
    "nazwa",
    "kod_teryt",
    "slonce_dzis_proc",
    "slonce_jutro_proc",
    "slonce_pojutrze_proc",
    "slonce_prosum_dzis_proc",
    "slonce_prosum_jutro_proc",
    "slonce_prosum_pojutrze_proc",
]

def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    sensors = []

    for feature in data["features"]:
        if feature['id'] != 'wojewodztwo.43':
            continue
        properties = feature["properties"]
        # Create a filtered dictionary with only the positive keys
        filtered_data = {key: properties[key] for key in TRACKED_KEYS if key in properties}
        sensors.append(filtered_data)

    return sensors


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    sensors = fetch_data()
    entities = [GlobemaForecastSensor(data["nazwa"], data) for data in sensors]
    async_add_entities(entities, True)


class GlobemaForecastSensor(SensorEntity):
    """Representation of a Prognozer sensor."""

    def __init__(self, name, data):
        """Initialize the sensor."""
        self._name = f"PV Forecast for {name.capitalize()}"
        self._state = data.get("slonce_dzis_proc")  # Use `slonce_dzis_proc` as the main state
        self._data = data

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
        return self._data

    async def async_update(self):
        """Update the sensor."""
        # Normally, update logic would be here if needed.
        pass
