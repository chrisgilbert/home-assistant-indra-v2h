"""Data update coordinator for Indra V2H."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class IndraV2HDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Indra V2H data."""

    def __init__(self, hass: HomeAssistant, client) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="Indra V2H",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.client = client
        self.device_data = {}
        self.statistics_data = {}

    async def _async_update_data(self):
        """Fetch data from Indra V2H API."""
        try:
            # Fetch device info and statistics (these are now async)
            device_data = await self.client.get_device()
            statistics_data = await self.client.get_statistics()
            
            self.device_data = device_data if device_data else {}
            self.statistics_data = statistics_data if statistics_data else {}
            
            return {
                "device": self.device_data,
                "statistics": self.statistics_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Indra V2H API: {err}") from err

