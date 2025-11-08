"""Base entity for Indra V2H integration."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import IndraV2HDataUpdateCoordinator


class IndraV2HEntity(CoordinatorEntity):
    """Base entity for Indra V2H devices."""

    def __init__(
        self,
        coordinator: IndraV2HDataUpdateCoordinator,
        device_id: str | None = None,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_id = device_id or "indra_v2h_charger"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Indra V2H Charger",
            manufacturer="Indra",
            model="V2H Charger",
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
        )

