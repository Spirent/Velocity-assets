# Velocity AI Cobalt Lab — Knowledge Base

Operational reference for staging, wiring, topology validation, and reservations on the HBG PM AI Lab Velocity instance.

**Velocity UI:** https://10.36.111.156/velocity/login  
**Scripts root:** `/root/Apps/LAAS/scripts`  
**Architect artifacts:** `/root/Apps/velocity/architect`  
**Credentials:** `/root/Apps/LAAS/scripts/velocity.config.json` (do not commit; rotate if exposed)

---

## Documents in this folder

| Document | Purpose |
|----------|---------|
| [MASTER_RUNBOOK.md](./MASTER_RUNBOOK.md) | **Start here** — full chronology, architecture, procedures, reasoning, and incident fixes from June 2026 lab bring-up |
| [REST_API_REFERENCE.md](./REST_API_REFERENCE.md) | Velocity REST endpoints with request/response examples (`curl` + Python) |
| [COMMAND_REFERENCE.md](./COMMAND_REFERENCE.md) | One-page CLI cheat sheet for orchestrator, wiring, and validation scripts |
| [TOPOLOGY_CATALOG_SNAPSHOT.md](./TOPOLOGY_CATALOG_SNAPSHOT.md) | Current topology UUIDs, validity status, and hardware scope |
| [INVENTORY_WIRING_REFERENCE.md](./INVENTORY_WIRING_REFERENCE.md) | Two-layer connection model, OCS/DAC/direct-DAC maps, RL aliases, expected connection counts |
| [UHD_RS_FEC_RESERVATION.md](./UHD_RS_FEC_RESERVATION.md) | **UHD Connect** — CONFIGURABLE interface, config asset, RS-FEC on reserve, repair commands |

---

## Related repo docs (outside this folder)

| Path | Purpose |
|------|---------|
| `architect/laas_staging_roadmap.md` | PM AI Lab LaaS plan execution checklist |
| `architect/velocity_reservation_api_runbook.md` | Reservation create/export/release |
| `architect/ai_lab_reservation_policies.yaml` | Duration, concurrency, wiring gates |
| `architect/ai_lab_connection_manifest.yaml` | OCS triplet ↔ endpoint matrix |
| `architect/velocity_wiring_gate_checklist.md` | CLOS-4SW-Full gate criteria |
| `architect/ai_lab_backup_topology_plan.md` | M08-absent backup templates |
| `/root/.cursor/plans/velocity_reservation_api_aba2b75f.plan.md` | Reservation service implementation plan |

---

## When something breaks — fast path

```bash
cd /root/Apps/LAAS/scripts

# 1. Auth + connectivity
python3 velocity_orchestrate_ai_lab.py check

# 2. Refresh GUID index from live inventory
python3 velocity_orchestrate_ai_lab.py audit-inventory

# 3. Re-apply inventory FIXED wiring (dry-run first)
python3 velocity_connect_inventory_ports.py --dry-run --full-lab
python3 velocity_connect_inventory_ports.py --apply --full-lab

# 4. Rebind topology TBML to current inventory GUIDs + Arista *-RL canvas names
python3 velocity_orchestrate_ai_lab.py refresh-topologies --include-backup

# 5. Validate
python3 velocity_validate_topologies.py --include-backup
```

If topologies show **"Resource is disabled"** → stale AresONE GUIDs in TBML; run step 4 after step 2.  
If topologies show **BAD_CONNECTION** on M05→A3 → canvas must use `Arista-03-RL`, not `Arista-03` (see MASTER_RUNBOOK §5).

---

*Last updated: 2026-06-23 (post lab sanitize + topology validity fix)*
