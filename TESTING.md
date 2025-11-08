# Testing Guide for Indra V2H Home Assistant Integration

## Prerequisites

1. **Home Assistant Installation**: Ensure Home Assistant is installed and running
2. **Indra Account**: Have your Indra Smart Portal email and password ready
3. **Network Access**: Ensure Home Assistant can reach the Indra API (internet connection required)

## Installation Steps

### 1. Copy Integration to Home Assistant

Copy the `indra_v2h` folder to your Home Assistant `custom_components` directory:

**For Home Assistant OS/Supervised:**
```bash
# SSH into your Home Assistant instance
# Navigate to config directory
cd /config
mkdir -p custom_components
# Copy the indra_v2h folder here
```

**For Home Assistant Core (Docker/venv):**
```bash
# Navigate to your Home Assistant config directory
# Typically: ~/.homeassistant or /config
cd ~/.homeassistant  # or your config path
mkdir -p custom_components
# Copy the indra_v2h folder here
```

**For Home Assistant Container:**
```bash
# Mount your config directory and copy files there
# Or use volume mounts to access the config directory
```

### 2. Verify File Structure

Ensure your directory structure looks like this:
```
<config>/custom_components/indra_v2h/
├── __init__.py
├── config_flow.py
├── const.py
├── coordinator.py
├── entity.py
├── manifest.json
├── README.md
├── select.py
├── sensor.py
└── services.yaml
```

### 3. Restart Home Assistant

**Important**: You must restart Home Assistant completely (not just reload) for custom integrations to be recognized.

- **Home Assistant OS**: Go to Settings > System > Hardware > Restart
- **Docker**: `docker restart homeassistant`
- **Systemd**: `sudo systemctl restart home-assistant`

## Configuration Testing

### 1. Add the Integration

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration** (bottom right)
3. Search for "Indra V2H"
4. If it doesn't appear:
   - Check the logs (see Troubleshooting below)
   - Verify the files are in the correct location
   - Ensure Home Assistant was fully restarted

### 2. Configure Credentials

1. Enter your Indra Smart Portal **Email**
2. Enter your Indra Smart Portal **Password**
3. Click **Submit**

**Expected Behavior:**
- If credentials are valid: Integration should be created successfully
- If credentials are invalid: You'll see an error message

**Common Issues:**
- "Cannot connect": Check internet connection, verify API is accessible
- "Invalid auth": Double-check email and password
- Integration doesn't appear: Check logs for import errors

## Verification Checklist

After successful configuration, verify the following:

### 1. Check Entities Are Created

Go to **Settings** > **Devices & Services** > **Indra V2H**

You should see:
- **Device**: "Indra V2H Charger"
- **Entities**:
  - `sensor.indra_v2h_power` - Power sensor (kW)
  - `sensor.indra_v2h_energy` - Energy sensor (kWh)
  - `sensor.indra_v2h_status` - Status sensor
  - `sensor.indra_v2h_model` - Model info
  - `sensor.indra_v2h_serial` - Serial number
  - `sensor.indra_v2h_firmware` - Firmware version
  - `select.indra_v2h_mode` - Mode selector

### 2. Check Entity States

Go to **Developer Tools** > **States** and search for `indra_v2h`:

- Verify entities exist
- Check if they have values (may show "unknown" initially)
- Wait 60 seconds for first update

### 3. Test Mode Selection

1. Go to **Settings** > **Devices & Services** > **Indra V2H**
2. Find the **Indra V2H Mode** select entity
3. Click on it and try changing the mode
4. Verify the mode changes in the Indra Smart Portal

**Test Modes:**
- `idle` - Should stop all charging/discharging
- `charge` - Should start charging
- `discharge` - Should start discharging
- `schedule` - Should return to scheduled mode

### 4. Test Services

Go to **Developer Tools** > **Services**:

**Test `indra_v2h.set_mode`:**
```yaml
service: indra_v2h.set_mode
data:
  mode: charge
```

**Test `indra_v2h.set_schedule`:**
```yaml
service: indra_v2h.set_schedule
data:
  mode: charge
  start_time: "22:00:00"
  end_time: "06:00:00"
```

Click **Call Service** and check:
- No errors in the response
- Mode actually changes (verify in portal or via select entity)

### 5. Check Logs

Go to **Settings** > **System** > **Logs** and filter for `indra_v2h`:

Look for:
- Successful data updates: `Updating Indra V2H data`
- Any error messages
- API communication logs

## Troubleshooting

### Integration Not Appearing

**Check:**
1. Files are in `custom_components/indra_v2h/` (not `custom_components/custom_components/indra_v2h/`)
2. All required files exist (especially `manifest.json`)
3. Home Assistant was fully restarted (not just reloaded)
4. Check logs for import errors

**Logs to Check:**
```bash
# In Home Assistant logs, look for:
- "Unable to import indra_v2h"
- "No module named 'pyindrav2h'"
- Syntax errors
```

### "Cannot Connect" Error

**Possible Causes:**
1. Internet connection issue
2. Indra API is down
3. Firewall blocking API access
4. Incorrect API method names in code

**Fix:**
- Check internet connectivity
- Verify you can access Indra Smart Portal in browser
- Check logs for specific API errors
- May need to adjust API method calls (see API Verification below)

### Entities Show "Unknown"

**Possible Causes:**
1. API returning different data structure than expected
2. Coordinator not updating
3. Device not connected

**Fix:**
- Check logs for API response structure
- Verify coordinator is updating (check logs every 60 seconds)
- May need to adjust sensor code to match actual API response

### Mode Changes Not Working

**Possible Causes:**
1. Incorrect API method names
2. Device not responding
3. Mode already set to that value

**Fix:**
- Check logs for API errors
- Verify device is online in Indra Smart Portal
- Try different mode to test

## API Verification

The integration assumes certain API methods exist. You may need to verify/adjust:

**Expected Methods:**
- `client.get_device()` - Returns device info
- `client.get_statistics()` - Returns usage statistics
- `client.set_mode(mode)` - Sets charger mode
- `client.set_schedule()` - Returns to schedule mode

**To Verify API:**
1. Install pyindrav2h in a Python environment:
   ```bash
   pip install pyindrav2h
   ```
2. Test the API:
   ```python
   from pyindrav2h import IndraClient
   
   client = IndraClient("your_email", "your_password")
   device = client.get_device()  # Check what this returns
   stats = client.get_statistics()  # Check what this returns
   print(device)
   print(stats)
   ```
3. Adjust the integration code if the API structure differs

## Manual API Testing

Test the pyindrav2h library directly:

```bash
# Install the library
pip install pyindrav2h

# Test CLI (if available)
indracli device
indracli statistics
indracli charge
```

Compare the output with what the integration expects.

## Next Steps After Testing

Once basic functionality works:

1. **Create Automations**: Test automations based on heat pump usage
2. **Monitor Data**: Watch sensor values over time
3. **Test Edge Cases**: Test with device offline, invalid modes, etc.
4. **Performance**: Monitor coordinator update frequency and API response times

## Reporting Issues

If you encounter issues:

1. Check the logs (Settings > System > Logs)
2. Note the exact error messages
3. Check the pyindrav2h library version
4. Verify your Home Assistant version
5. Document steps to reproduce

## Notes

- The integration polls every 60 seconds - changes may not be immediate
- Some API methods may need adjustment based on actual pyindrav2h library structure
- The `set_schedule` service is a placeholder - actual schedule times may need to be set via Indra Smart Portal

