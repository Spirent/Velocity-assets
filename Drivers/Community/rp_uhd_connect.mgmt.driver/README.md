# UHD Connect Management Driver (Velocity)

Author: rakesh.kumar@keysight.com  
Written and debugged by rakesh.kumar@keysight.com  
Co-authored-by: Cursor

Python Management driver for Keysight **UHD Connect** appliances on KCOS.

## Official API documentation (on-box)

Replace `{ip}` with the appliance management IP (e.g. `10.36.87.102`).

| Resource | URL |
|----------|-----|
| Getting Started UI | `https://{ip}/` |
| **UHD Connect API** (Redoc) | `https://{ip}/uhd_connect/redoc.html` |
| Connect OpenAPI JSON | `https://{ip}/uhd_connect/openapi.json` |
| Sample configs | `https://{ip}/samples.tar.gz` |
| **Ixia-C / BGP API** (Redoc) | `https://{ip}/ixiac/redoc.html` |
| Ixia-C OpenAPI JSON | `https://{ip}/ixiac/openapi.json` |

### Two REST surfaces

1. **Connect API** — base `https://{ip}/connect/api/v1`
   - Configures front-panel ports, VLAN/VxLAN connections, layer-1 profiles.
   - OpenAPI documents `GET/PUT /config`.
   - Metrics and switchover are documented in Getting Started / samples:
     - `POST /metrics/operations/query` — per-port stats + **`link_status`** (`link_up` / `link_down`)
     - `POST /metrics/operations/clear`
     - `POST /control/operations/switchover` — `{"enable": true|false}`

2. **Ixia-C API** — base `https://{ip}/` (Open Traffic Generator model)
   - Used for internal BGP service instances (`/config`, `/control/protocols`, `/results/metrics`).
   - Required only for the `samples/with_bgp/` workflow; not used by this Velocity driver today.

## Driver endpoints used

| Velocity op | REST call |
|-------------|-----------|
| `getPorts`, `linkCheck`, `healthcheck` | `POST …/metrics/operations/query` |
| `getProperties` | `GET …/config` (+ metrics for live ports) |
| `setup` | `POST …/config` — 400G manual RS-FEC on `defaultPort` |
| `verifyReady` | poll `link_status` on configured port |
| `teardown` | restore pre-reservation config snapshot |
| `applyLayer1Profile` | `POST …/config` — explicit RS-FEC apply |
| `probe` | metrics query reachability |

## Reservation lifecycle (UHD-AresONE-S)

Velocity **Configurable** driver + **CONFIGURABLE** inventory. On reserve, Velocity calls `setConfig` → `setup` → `verifyReady` when the template config asset and topology `useDefaultConfig` are wired (see `knowledge-base/UHD_RS_FEC_RESERVATION.md`).

LAAS `reserve-topology` and `uhd-ensure-fec` provide a fallback if UI reserve skips FEC.

**Do not** POST `/connect/api/v1/config` from LAAS/curl while the device is unlocked or during refresh — that locks `tf2-uhdc-e2e` in Velocity.

Upload driver v1.2.3+ before using lifecycle from Velocity UI:

```bash
cd /root/Apps/LAAS/scripts
python3 velocity_upload_python_drivers.py --uhd-only --apply
```

## Velocity procedures

- `getProperties`, `getPorts`, `getHealth`, `healthcheck`, `linkCheck`, `probe`
- `setup`, `verifyReady`, `teardown`, `applyLayer1Profile` — L1 RS-FEC reservation lifecycle
- `takeOwnership` / `releaseOwnership` — no-ops (no ownership API on UHD Connect)
- `getLldpNeighbors` — empty (L1 fabric appliance)

## Port naming

Front-panel ports **1–32** (plus internal port 33 on some builds). Velocity `status` maps
`metrics.link_status`: `link_up` → `online`, `link_down` → `offline`.

Configured logical names (e.g. `vlan_port_1`) come from active `/config` when present.

## Lab devices

| Name | IP | Velocity driver |
|------|-----|-----------------|
| `tf2-uhdc-e2e` | 10.36.87.102 | `UHD-Connect-Mgmt` (`deec16db-583e-4740-b471-aec837234244`) |
| `tf2-o3` | 10.36.70.7 | same |

## Velocity registration

- Driver UUID: `deec16db-583e-4740-b471-aec837234244`
- Template: `UHD Connect` (`1ddc5167-cff6-4aa0-ba68-cb189de13d2b`) — interface must be **MANAGEMENT**
