"""The Indra V2H integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_EMAIL, CONF_PASSWORD, DOMAIN, MODES
from .coordinator import IndraV2HDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SELECT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Indra V2H from a config entry."""
    try:
        from .client import IndraV2HClient

        # Create client with credentials from config entry
        client = IndraV2HClient(entry.data[CONF_EMAIL], entry.data[CONF_PASSWORD])
        
        # Create coordinator
        coordinator = IndraV2HDataUpdateCoordinator(hass, client)
        
        # Fetch initial data
        await coordinator.async_config_entry_first_refresh()
        
        # Store coordinator in hass data
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = coordinator
        
        # Set up platforms
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        # Register services (services.yaml is auto-loaded, but we register handlers)
        await async_setup_services(hass, coordinator)
        
        return True
    except Exception as err:
        _LOGGER.error("Error setting up Indra V2H integration: %s", err)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


async def async_setup_services(hass: HomeAssistant, coordinator: IndraV2HDataUpdateCoordinator) -> None:
    """Set up custom services."""
    
    async def set_mode_service(call):
        """Service to set charger mode."""
        mode = call.data.get("mode")
        if mode not in MODES:
            _LOGGER.error("Invalid mode: %s", mode)
            return
        
        try:
            await coordinator.client.set_mode(mode)
            
            await coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error setting mode: %s", err)
    
    async def set_schedule_service(call):
        """Service to set schedule times."""
        start_time = call.data.get("start_time")
        end_time = call.data.get("end_time")
        mode = call.data.get("mode", "charge")
        
        _LOGGER.info(
            "Setting schedule: mode=%s, start=%s, end=%s",
            mode, start_time, end_time
        )
        
        # For now, this is a placeholder for future schedule implementation
        # The pyindrav2h library may need schedule-specific methods
        try:
            # Return to schedule mode - actual schedule times may need
            # to be set via the Indra Smart Portal or future API methods
            await coordinator.client.set_schedule()
            await coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error setting schedule: %s", err)
    
    # Register services
    hass.services.async_register(DOMAIN, "set_mode", set_mode_service)
    hass.services.async_register(DOMAIN, "set_schedule", set_schedule_service)

