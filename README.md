# Indra V2H Home Assistant Integration

A Home Assistant custom integration for controlling and monitoring Indra V2H (Vehicle-to-Home) chargers using the `pyindrav2h` library.

## Features

- **Device Monitoring**: Real-time sensors for power, energy, and device status
- **Mode Control**: Select entity to change charger modes (idle, charge, discharge, loadmatch, exportmatch, schedule)
- **Custom Services**: Services for setting modes and schedules programmatically
- **Automatic Updates**: Coordinator polls device data every 60 seconds

## Installation

### HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three dots (⋮) in the top right
4. Select **Custom repositories**
5. Add repository:
   - Repository: `https://github.com/YOUR_USERNAME/YOUR_REPO` (replace with your repo URL)
   - Category: **Integration**
6. Click **Add**
7. Search for "Indra V2H" in HACS
8. Click **Download**
9. Restart Home Assistant
10. Go to **Settings** > **Devices & Services** > **Add Integration** and configure

### Manual Installation

1. Copy the `custom_components/indra_v2h` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services** > **Add Integration**
4. Search for "Indra V2H" and follow the setup wizard
5. Enter your Indra Smart Portal credentials (email and password)

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

## Documentation

For detailed documentation, see [custom_components/indra_v2h/README.md](custom_components/indra_v2h/README.md)

## Acknowledgments

This integration is built on top of the excellent [`pyindrav2h`](https://pypi.org/project/pyindrav2h/) library by [creatingwake](https://github.com/creatingwake). Without their work reverse-engineering the Indra API and creating the Python library, this Home Assistant integration would not be possible.

This integration was vibe coded with [Cursor](https://cursor.sh), an AI-powered code editor.

Special thanks to:
- **creatingwake** - Author of the `pyindrav2h` library that provides the core API functionality
- **Cursor** - AI-powered development environment used to build this integration
- Home Assistant community for integration patterns and examples

## Support

This is a community project. For issues or feature requests, please create an issue in the repository.

**Note**: Please do not contact Indra Support for issues with this integration. Indra are unable to assist with unofficial API integrations.

## License

This integration is provided as-is for community use.

