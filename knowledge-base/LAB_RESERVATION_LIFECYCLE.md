# Lab reservation lifecycle — SONiC / AresONE / Arista (optional)

Extends the [UHD RS-FEC pattern](./UHD_RS_FEC_RESERVATION.md) to switches and AresONE chassis.
**All features are OFF by default** in `architect/lab_reservation_lifecycle.yaml`.

---

## Backup-first workflow (required)

Never upload experimental drivers or change inventory without a snapshot.

```bash
cd /root/Apps/LAAS/scripts

# 1. Full backup (inventory, topologies, drivers, connections)
python3 lab_staging_workflow.py backup

# 2. Local self-test (dispatch maps, manifest interfaces — no Velocity changes)
python3 lab_staging_workflow.py selftest

# 3. Optional deploy (backup + selftest + upload)
python3 lab_staging_workflow.py deploy --sonic --hogan --apply

# 4. Rollback driver assignments if Velocity breaks
python3 lab_staging_workflow.py restore-drivers \
  --from /root/Apps/velocity/architect/backups/<timestamp>_pre-deploy
```

Latest backup pointer: `architect/latest_staging_backup.json`

Full lab backup (same data, no staging marker): `python3 velocity_backup_lab.py`

---

## Platform capabilities

| Platform | Driver | Reservation L1 action | Speed / FEC | Status |
|----------|--------|----------------------|-------------|--------|
| **UHD Connect** | `UHD-Connect-Mgmt` v1.2.3 `Configurable` | `setConfig` → `setup` (400G manual RS-FEC) | REST `/config` | **Production** (`uhd.enabled: true`) |
| **SONiC** | `SONiC-RoCE-Mgmt` v1.2.0 `Configurable` | `setConfig` → `setup` (baseline JSON per speed) | `config load baseline_{N}G.json` | **Optional** — needs on-switch baselines |
| **AresONE Hogan** | `IXIA-Chassis-Mgmt` v1.3.0 `Management` | `setup` / `verifyReady` (ownership + link poll) | No chassis speed change | **Optional** — verify-only |
| **Arista EOS** | `Arista_driver_06_19` iTest | VLAN only today | `speed forced` via SSH (future) | **Not implemented** |

---

## Enabling SONiC speed-mode on reserve (future)

1. Provision baselines on switches: `/etc/sonic/baselines/baseline_400G.json`, etc.
2. Edit `architect/lab_reservation_lifecycle.yaml`:

```yaml
enabled: true
sonic:
  enabled: true
  default_speed_gbps: 400
```

3. `python3 lab_staging_workflow.py backup`
4. `python3 lab_staging_workflow.py deploy --sonic --apply`
5. `python3 velocity_orchestrate_ai_lab.py build-topology --name 2SW-Arista-Leaf --force`  
   (TBML `useDefaultConfig` for SONiC devices — wire when enabling)

Fix interface mismatch before enable: inventory `CONFIGURABLE` must match driver `Configurable`.

---

## Enabling AresONE link verify (future)

1. Assign **Hogan REST** driver (`IXIA-Chassis-Mgmt`) to AresONE devices (not SSH-only).
2. Set `aresone.enabled: true` in lifecycle YAML.
3. Deploy Hogan v1.3.0+ via `lab_staging_workflow.py deploy --hogan --apply`.

`setup` optionally calls `takeOwnership` on `defaultPorts`; `verifyReady` polls `linkCheck`.

---

## Interface mismatch rule

Velocity shows *"Resource and driver interfaces do not match"* when inventory and driver catalog disagree.
This **blocks** `setConfig` / reservation automation. Always verify:

```bash
python3 -c "
from velocity_core_api import VelocityCoreClient, load_config
# ... compare device.interface vs driver.interface in catalog
"
```

---

## Self-test

```bash
python3 lab_driver_selftest.py
```

Checks: UHD `setConfig`, SONiC `Configurable` manifest + `ALLOWED_CALLS`, Hogan lifecycle methods, config files present.

---

## Related files

| Path | Role |
|------|------|
| `architect/lab_reservation_lifecycle.yaml` | Feature flags |
| `LAAS/scripts/lab_staging_workflow.py` | Backup / deploy / rollback CLI |
| `LAAS/scripts/sonic_topology_reservation.py` | SONiC CONFIGURABLE + config asset |
| `LAAS/scripts/hogan_topology_reservation.py` | AresONE verifyReady hook |
| `Drivers/Community/rp_sonic.l2.switch.driver/` | SONiC driver v1.2.0 |
| `Drivers/Community/rp_ixos_hogan.mgmt.driver/` | Hogan driver v1.3.0 |
