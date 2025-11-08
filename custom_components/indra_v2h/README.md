# Indra V2H Home Assistant Integration

A Home Assistant custom integration for controlling and monitoring Indra V2H (Vehicle-to-Home) chargers using the `pyindrav2h` library.

## Features

- **Device Monitoring**: Real-time sensors for power, energy, and device status
- **Mode Control**: Select entity to change charger modes (idle, charge, discharge, loadmatch, exportmatch, schedule)
- **Custom Services**: Services for setting modes and schedules programmatically
- **Automatic Updates**: Coordinator polls device data every 60 seconds

## Installation

### Manual Installation

1. Copy the `indra_v2h` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/indra_v2h/
   ```

2. Restart Home Assistant

3. Go to **Settings** > **Devices & Services** > **Add Integration**

4. Search for "Indra V2H" and follow the setup wizard

5. Enter your Indra Smart Portal credentials:
   - Email
   - Password

### HACS Installation

**Option 1: Add as Custom Repository (Recommended)**

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three dots (⋮) in the top right
4. Select **Custom repositories**
5. Add repository:
   - Repository: `https://github.com/yourusername/indra-v2h-home-assistant` (replace with your repo URL)
   - Category: **Integration**
6. Click **Add**
7. Search for "Indra V2H" in HACS
8. Click **Download**
9. Restart Home Assistant
10. Go to **Settings** > **Devices & Services** > **Add Integration** and configure

**Option 2: Manual HACS Installation**

1. Ensure HACS is installed in Home Assistant
2. Download the latest release from GitHub
3. Extract and copy `custom_components/indra_v2h/` to your Home Assistant config
4. Restart Home Assistant
5. Configure via **Settings** > **Devices & Services**

## Configuration

The integration uses a config flow. After installation:

1. Navigate to **Settings** > **Devices & Services**
2. Find "Indra V2H" in your integrations
3. Click **Configure** to update credentials if needed

## Entities

### Sensors

- **Indra V2H Power**: Current power usage (kW)
- **Indra V2H Energy**: Total energy consumption (kWh)
- **Indra V2H Status**: Current device status
- **Indra V2H Model**: Device model information
- **Indra V2H Serial**: Device serial number
- **Indra V2H Firmware**: Firmware version

### Select

- **Indra V2H Mode**: Select the charger operating mode
  - `idle`: No charging/discharging
  - `charge`: Charge the vehicle
  - `discharge`: Discharge from vehicle to home
  - `loadmatch`: Match home load
  - `exportmatch`: Match export to grid
  - `schedule`: Return to scheduled mode

## Services

### `indra_v2h.set_mode`

Set the charger mode programmatically.

**Service Data:**
```yaml
mode: charge  # Options: idle, charge, discharge, loadmatch, exportmatch, schedule
```

**Example:**
```yaml
service: indra_v2h.set_mode
data:
  mode: discharge
```

### `indra_v2h.set_schedule`

Set a schedule for the charger (placeholder for future implementation).

**Service Data:**
```yaml
mode: charge  # Optional, default: charge
start_time: "22:00:00"  # Optional
end_time: "06:00:00"  # Optional
```

**Example:**
```yaml
service: indra_v2h.set_schedule
data:
  mode: charge
  start_time: "22:00:00"
  end_time: "06:00:00"
```

## Automations

### Example: Charge During Low Tariff

```yaml
automation:
  - alias: "Charge V2H during low tariff"
    trigger:
      - platform: time
        at: "00:30:00"
    action:
      - service: indra_v2h.set_mode
        data:
          mode: charge
```

### Example: Discharge During High Demand

```yaml
automation:
  - alias: "Discharge V2H during peak"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - service: indra_v2h.set_mode
        data:
          mode: discharge
```

### Example: Schedule Based on Heat Pump Usage

```yaml
automation:
  - alias: "V2H discharge when heat pump on"
    trigger:
      - platform: state
        entity_id: sensor.heat_pump_power
        above: 2000  # Watts
    condition:
      - condition: state
        entity_id: sensor.octopus_energy_rate
        above: 0.30  # High tariff
    action:
      - service: indra_v2h.set_mode
        data:
          mode: discharge
```

## Integration with Other Components

### Octopus Energy Integration

Combine with the official Octopus Energy integration to optimize charging based on tariff rates:

```yaml
automation:
  - alias: "Charge when tariff is low"
    trigger:
      - platform: numeric_state
        entity_id: sensor.octopus_energy_current_rate
        below: 0.10  # p/kWh
    action:
      - service: indra_v2h.set_mode
        data:
          mode: charge
```

### Grant Aerona3 Heat Pump

Use with the Grant Aerona3 heat pump integration to coordinate heating and V2H charging:

```yaml
automation:
  - alias: "Discharge V2H when heat pump needs power"
    trigger:
      - platform: state
        entity_id: climate.grant_aerona3
        to: "heat"
    condition:
      - condition: numeric_state
        entity_id: sensor.octopus_energy_current_rate
        above: 0.25
    action:
      - service: indra_v2h.set_mode
        data:
          mode: discharge
```

## Troubleshooting

### Integration Not Appearing

- Ensure the `custom_components` directory exists
- Check that all files are in the correct location
- Restart Home Assistant completely
- Check the logs for errors: **Settings** > **System** > **Logs**

### Authentication Errors

- Verify your Indra Smart Portal credentials are correct
- Check that your account has API access enabled
- Review the integration logs for specific error messages

### Mode Changes Not Working

- Check the device is online and connected
- Verify the current mode in the Indra Smart Portal
- Review Home Assistant logs for API errors

## Limitations

- The `set_schedule` service is a placeholder. Actual schedule times may need to be configured via the Indra Smart Portal
- The integration polls data every 60 seconds - real-time updates may be delayed
- This is an unofficial integration and may break if Indra updates their API

## Future Enhancements

- Advanced scheduling with time-based rules
- Predictive modeling for optimal charge/discharge times
- Integration with Octopus Energy tariff data
- Custom Lovelace cards for visualization
- Support for multiple V2H chargers

## Support

This is a community project. For issues or feature requests, please create an issue in the repository.

**Note**: Please do not contact Indra Support for issues with this integration. Indra are unable to assist with unofficial API integrations.

## Acknowledgments

This integration is built on top of the excellent [`pyindrav2h`](https://pypi.org/project/pyindrav2h/) library by [creatingwake](https://github.com/creatingwake). Without their work reverse-engineering the Indra API and creating the Python library, this Home Assistant integration would not be possible.

This integration was vibe coded with [Cursor](https://cursor.sh), an AI-powered code editor.

Special thanks to:
- **creatingwake** - Author of the `pyindrav2h` library that provides the core API functionality
- **Cursor** - AI-powered development environment used to build this integration
- Home Assistant community for integration patterns and examples

## License

This integration is provided as-is for community use.

