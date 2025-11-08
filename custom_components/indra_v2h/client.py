"""Client wrapper for pyindrav2h library."""
from __future__ import annotations

import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)


class IndraV2HClient:
    """Wrapper for pyindrav2h library to provide consistent API."""

    def __init__(self, email: str, password: str) -> None:
        """Initialize the client."""
        self.email = email
        self.password = password
        self._connection = None
        self._client = None
        self._device = None
        
        # Import and create connection
        try:
            from pyindrav2h.connection import Connection
            from pyindrav2h.v2hclient import v2hClient
            
            self._connection = Connection(email, password)
            self._client = v2hClient(self._connection)
            _LOGGER.info("Initialized pyindrav2h client")
        except ImportError as err:
            _LOGGER.error("Failed to import pyindrav2h: %s", err)
            raise

    async def refresh(self) -> None:
        """Refresh device info and statistics."""
        if self._client is None:
            raise RuntimeError("Client not initialized")
        await self._client.refresh()
        self._device = self._client.device

    async def get_device(self) -> dict[str, Any]:
        """Get device information."""
        if self._client is None:
            raise RuntimeError("Client not initialized")
        
        # Refresh if needed
        if self._device is None:
            await self._client.refresh_device()
            self._device = self._client.device
        
        # Return device data
        if self._device and hasattr(self._device, 'data'):
            return self._device.data
        
        return {}

    async def get_statistics(self) -> dict[str, Any]:
        """Get device statistics."""
        if self._client is None:
            raise RuntimeError("Client not initialized")
        
        # Refresh if needed
        if self._device is None:
            await self._client.refresh_stats()
            self._device = self._client.device
        else:
            await self._device.refresh_stats()
        
        # Return statistics data
        if self._device and hasattr(self._device, 'stats'):
            return self._device.stats
        
        return {}

    async def set_mode(self, mode: str) -> None:
        """Set the charger mode."""
        await self._set_mode_async(mode)

    async def _set_mode_async(self, mode: str) -> None:
        """Set the charger mode (async implementation)."""
        if self._device is None:
            await self._client.refresh_device()
            self._device = self._client.device
        
        if mode == "idle":
            await self._device.idle()
        elif mode == "loadmatch":
            await self._device.load_match()
        elif mode == "schedule":
            await self._device.schedule()
        elif mode == "charge":
            await self._device.select_charger_mode("CHARGE")
        elif mode == "discharge":
            await self._device.select_charger_mode("DISCHARGE")
        elif mode == "exportmatch":
            # Use select_charger_mode with EXPORT_MATCH mode
            # Note: This may need to be verified with the actual library
            await self._device.select_charger_mode("EXPORT_MATCH")
        else:
            raise ValueError(f"Unknown mode: {mode}")

    async def set_schedule(self) -> None:
        """Return to scheduled mode."""
        await self.set_mode("schedule")

    @property
    def device(self):
        """Get the device object."""
        return self._device
