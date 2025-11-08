"""Sensor entities for Indra V2H integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import IndraV2HDataUpdateCoordinator
from .entity import IndraV2HEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Indra V2H sensor entities."""
    coordinator: IndraV2HDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        IndraV2HPowerSensor(coordinator),
        IndraV2HEnergySensor(coordinator),
        IndraV2HStatusSensor(coordinator),
        IndraV2HDeviceInfoSensor(coordinator, "model"),
        IndraV2HDeviceInfoSensor(coordinator, "serial"),
        IndraV2HDeviceInfoSensor(coordinator, "firmware"),
    ]

    async_add_entities(sensors)


class IndraV2HPowerSensor(IndraV2HEntity, SensorEntity):
    """Sensor for current power usage."""

    _attr_name = "Indra V2H Power"
    _attr_unique_id = "indra_v2h_power"
    _attr_native_unit_of_measurement = UnitOfPower.KILO_WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> float | None:
        """Return the current power value."""
        if not self.coordinator.data:
            return None
        
        statistics = self.coordinator.data.get("statistics", {})
        # Extract power value from statistics
        # Based on v2hdevice.py: powerToEv is in stats["data"]["powerToEv"]
        data = statistics.get("data", {})
        power = data.get("powerToEv")
        if power is not None:
            # Convert from W to kW
            return float(power) / 1000.0
        return None


class IndraV2HEnergySensor(IndraV2HEntity, SensorEntity):
    """Sensor for energy consumption."""

    _attr_name = "Indra V2H Energy"
    _attr_unique_id = "indra_v2h_energy"
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:counter"

    @property
    def native_value(self) -> float | None:
        """Return the energy value."""
        if not self.coordinator.data:
            return None
        
        statistics = self.coordinator.data.get("statistics", {})
        # Extract energy value from statistics
        # Based on v2hdevice.py: activeEnergyToEv and activeEnergyFromEv are available
        data = statistics.get("data", {})
        # Use activeEnergyToEv (charging) or activeEnergyFromEv (discharging)
        energy = data.get("activeEnergyToEv") or data.get("activeEnergyFromEv")
        if energy is not None:
            # Convert from Wh to kWh
            return float(energy) / 1000.0
        return None


class IndraV2HStatusSensor(IndraV2HEntity, SensorEntity):
    """Sensor for device status."""

    _attr_name = "Indra V2H Status"
    _attr_unique_id = "indra_v2h_status"
    _attr_icon = "mdi:information"

    @property
    def native_value(self) -> str | None:
        """Return the device status."""
        if not self.coordinator.data:
            return None
        
        statistics = self.coordinator.data.get("statistics", {})
        # Based on v2hdevice.py: state is in stats["state"]
        state = statistics.get("state")
        if state:
            return str(state)
        
        # Fallback to mode if state not available
        mode = statistics.get("mode")
        if mode:
            return str(mode)
        
        return "unknown"


class IndraV2HDeviceInfoSensor(IndraV2HEntity, SensorEntity):
    """Sensor for device information."""

    def __init__(
        self,
        coordinator: IndraV2HDataUpdateCoordinator,
        info_type: str,
    ) -> None:
        """Initialize device info sensor."""
        super().__init__(coordinator)
        self._info_type = info_type
        self._attr_name = f"Indra V2H {info_type.capitalize()}"
        self._attr_unique_id = f"indra_v2h_{info_type}"
        self._attr_icon = "mdi:information-outline"

    @property
    def native_value(self) -> str | None:
        """Return the device info value."""
        if not self.coordinator.data:
            return None
        
        device = self.coordinator.data.get("device", {})
        # Device data is a list, get first item
        if isinstance(device, list) and len(device) > 0:
            device_info = device[0]
            value = device_info.get(self._info_type)
            if value is not None:
                return str(value)
        elif isinstance(device, dict):
            value = device.get(self._info_type)
            if value is not None:
                return str(value)
        return None

