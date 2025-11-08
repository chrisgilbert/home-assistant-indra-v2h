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
        
        # Register services if not already registered
        if not hasattr(hass.data[DOMAIN], "_services_registered"):
            await async_setup_services(hass)
            hass.data[DOMAIN]["_services_registered"] = True
        
        return True
    except Exception as err:
        _LOGGER.error("Error setting up Indra V2H integration: %s", err)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Unregister services if no more entries
        if DOMAIN in hass.data and len([k for k in hass.data[DOMAIN].keys() if k != "_services_registered"]) == 0:
            hass.services.async_remove(DOMAIN, "set_mode")
            hass.services.async_remove(DOMAIN, "set_schedule")
            hass.data[DOMAIN].pop("_services_registered", None)
    
    return unload_ok


def _get_coordinator_for_service(hass: HomeAssistant, call) -> IndraV2HDataUpdateCoordinator | None:
    """Get the coordinator for a service call."""
    if DOMAIN not in hass.data:
        return None
    
    # Try to get coordinator from entity_id if provided
    entity_id = call.data.get("entity_id")
    if entity_id:
        # Extract entry_id from entity registry if possible
        from homeassistant.helpers import entity_registry as er
        
        entity_registry = er.async_get(hass)
        if registry_entry := entity_registry.async_get(entity_id):
            entry_id = registry_entry.config_entry_id
            if entry_id and entry_id in hass.data[DOMAIN]:
                return hass.data[DOMAIN][entry_id]
    
    # Otherwise, use the first coordinator
    coordinators = [v for k, v in hass.data[DOMAIN].items() if k != "_services_registered"]
    if coordinators:
        return coordinators[0]
    
    return None


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up custom services."""
    
    async def set_mode_service(call):
        """Service to set charger mode."""
        coordinator = _get_coordinator_for_service(hass, call)
        if not coordinator:
            _LOGGER.error("No Indra V2H coordinator found")
            return
        
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
        coordinator = _get_coordinator_for_service(hass, call)
        if not coordinator:
            _LOGGER.error("No Indra V2H coordinator found")
            return
        
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

