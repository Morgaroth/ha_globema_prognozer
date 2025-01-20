from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN


async def fetch_data():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://prognozer.globema.pl/api/layers/20005/geojson?outputFormat=application/json") as response:
            response.raise_for_status()
            raw_data = await response.json()
            return [
                {
                    "name": item["properties"]["nazwa"],
                    "today": item["properties"].get("slonce_dzis_proc"),
                    "tomorrow": item["properties"].get("slonce_jutro_proc"),
                    "day_after": item["properties"].get("slonce_pojutrze_proc"),
                }
                for item in raw_data.get("features", [])
            ]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    selected_sensors = hass.data[DOMAIN][entry.entry_id]["selected_sensors"]

    sensors = [
        GlobemaSensor(sensor_data["name"], coordinator)
        for sensor_data in coordinator.data
        if sensor_data["name"] in selected_sensors
    ]
    async_add_entities(sensors, True)


class GlobemaSensor(SensorEntity):
    def __init__(self, name, coordinator):
        self._name = f"PV Forecast {name}"
        self.coordinator = coordinator
        self._data = next((item for item in coordinator.data if item["name"] == name), {})
        self._state = self._data.get("today")

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._data

    async def async_update(self):
        await self.coordinator.async_request_refresh()
