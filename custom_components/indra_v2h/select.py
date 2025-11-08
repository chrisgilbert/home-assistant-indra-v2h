"""Select entity for Indra V2H mode selection."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, MODES
from .coordinator import IndraV2HDataUpdateCoordinator
from .entity import IndraV2HEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Indra V2H select entity."""
    coordinator: IndraV2HDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([IndraV2HModeSelect(coordinator)])


class IndraV2HModeSelect(IndraV2HEntity, SelectEntity):
    """Select entity for charger mode."""

    _attr_name = "Indra V2H Mode"
    _attr_unique_id = "indra_v2h_mode"
    _attr_options = MODES
    _attr_icon = "mdi:power-settings"

    @property
    def current_option(self) -> str | None:
        """Return the current selected mode."""
        if not self.coordinator.data:
            return None
        
        statistics = self.coordinator.data.get("statistics", {})
        # Based on v2hdevice.py: mode is in stats["mode"]
        mode = statistics.get("mode")
        if mode:
            # Convert library mode to our mode format
            mode_lower = mode.lower()
            if mode_lower in MODES:
                return mode_lower
            # Map library modes to our modes
            mode_map = {
                "loadmatch": "loadmatch",
                "idle": "idle",
                "schedule": "schedule",
                "charge": "charge",
                "discharge": "discharge",
                "exportmatch": "exportmatch",
            }
            if mode_lower in mode_map:
                return mode_map[mode_lower]
        
        return MODES[0]  # Default to first mode if unknown

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option not in MODES:
            _LOGGER.error("Invalid mode: %s", option)
            return

        try:
            # Use the client's set_mode method (now async)
            await self.coordinator.client.set_mode(option)
            
            # Force coordinator update to reflect new state
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error setting mode to %s: %s", option, err)
            raise

