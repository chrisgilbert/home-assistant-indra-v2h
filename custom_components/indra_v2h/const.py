"""Constants for the Indra V2H integration."""

DOMAIN = "indra_v2h"

# Charger modes
MODE_IDLE = "idle"
MODE_CHARGE = "charge"
MODE_DISCHARGE = "discharge"
MODE_LOADMATCH = "loadmatch"
MODE_EXPORTMATCH = "exportmatch"
MODE_SCHEDULE = "schedule"

# Available modes for select entity
MODES = [
    MODE_IDLE,
    MODE_CHARGE,
    MODE_DISCHARGE,
    MODE_LOADMATCH,
    MODE_EXPORTMATCH,
    MODE_SCHEDULE,
]

# Configuration keys
CONF_EMAIL = "email"
CONF_PASSWORD = "password"

# Update intervals
UPDATE_INTERVAL = 60  # seconds

# Device attributes
ATTR_DEVICE_ID = "device_id"
ATTR_MODE = "mode"
ATTR_POWER = "power"
ATTR_ENERGY = "energy"
ATTR_STATUS = "status"

