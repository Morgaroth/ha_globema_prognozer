import logging

import aiohttp

API_URL = "https://prognozer.globema.pl/api/layers/20005/geojson?outputFormat=application/json"
_LOGGER = logging.getLogger(__package__ + __name__)


async def fetch_data():
    """Fetch data from the Prognozer API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            response.raise_for_status()
            raw_data = await response.json()

            # Process the data into a usable format
            sensors_data = []
            for feature in raw_data.get("features", []):
                properties = feature.get("properties", {})
                sensors_data.append({
                    "area": properties.get("nazwa"),
                    "today": properties.get("slonce_dzis_proc"),
                    "tomorrow": properties.get("slonce_jutro_proc"),
                    "day_after": properties.get("slonce_pojutrze_proc"),
                })

            return sensors_data
