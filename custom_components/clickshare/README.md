# Barco ClickShare for Home Assistant — 0.1.0

Custom integration focused on local, real ClickShare interfaces.

## Supported architecture
- V2: C-5, C-10, CX-20, CX-30, CX-50 Gen1/Gen2, ClickShare Bar Core/Pro.
- V1 mode is present as a compatibility foundation for CS-100/Huddle, CSE-200/200+/800, but V1 model-specific entities still require validation against a real unit/API document.
- V2 uses HTTPS TCP 4003.
- The integration attempts to read the Base Unit's own OpenAPI/Swagger definition and only polls GET endpoints advertised by that unit.
- Official `/v2/configuration/buttons` support.
- No invented reboot/standby/settings endpoints: active controls will be added only when confirmed from the target unit's OpenAPI document.

## Install
Copy `custom_components/clickshare` to `/config/custom_components/clickshare`, restart Home Assistant, then:
Settings > Devices & services > Add integration > Barco ClickShare.

Before setup, in ClickShare Configurator:
Wi-Fi & Network > Services > Remote control via API = enabled.

V2 credentials are the Web Configurator credentials. Change default credentials before production use.

## Why some controls are intentionally absent
Barco changes resources by product generation and firmware. This first build discovers the unit's actual OpenAPI resources instead of shipping decorative or guessed controls. The REST diagnostics sensor exposes discovered endpoint names/values for the next mapping pass.

## SSE
Barco V2 firmware 2.12.0.12+ supports Server-Sent Events for GET resources. Polling is used in 0.1.0 for maximum compatibility; SSE is the planned next transport once validated on the target Base Unit.

## SNMP
Barco documents SNMPv3 and enterprise OID `.1.3.6.1.4.1.7312`, including current uptime, total uptime, temperature and high-temperature threshold. SNMP is intentionally not bundled in 0.1.0 because HA/Python SNMP dependencies vary; it can be added after REST validation.

## First field test
After installing, send the model, firmware, and the attributes of `sensor.<clickshare>_rest_diagnostics`.
That tells us exactly which resources your Base Unit advertises, allowing model-safe entities for standby/reboot/network/features/peripherals/etc.
