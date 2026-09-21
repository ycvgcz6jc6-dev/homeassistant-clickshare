DOMAIN = "clickshare"
CONF_VERIFY_SSL = "verify_ssl"
CONF_API_VERSION = "api_version"
CONF_PORT = "port"

DEFAULT_PORT_V2 = 4003
DEFAULT_PORT_V1 = 4000
DEFAULT_VERIFY_SSL = False
DEFAULT_SCAN_INTERVAL = 30

PLATFORMS = ["sensor", "binary_sensor", "button"]

# V2 endpoints confirmed/documented by Barco public material or discovered
# from the unit's own OpenAPI document.
V2_BUTTONS = "/v2/configuration/buttons"
V2_DOC = "/api-docs/v2"
