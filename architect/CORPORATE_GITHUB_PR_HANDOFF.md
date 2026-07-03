# Corporate GitHub PR handoff — Velocity Community drivers

## Auth status (nginx-eagle)

- **Logged in:** `rakesh-kumar_keysight` (Rakesh Kumar, rakesh.kumar+keysight@keysight.com)
- **Enterprise:** Keysight-Copilot / Keysight-Technologies-Copilot SSO

## Blocker — Enterprise Managed User (EMU)

GitHub returns **403** for this account:

| Action | Result |
|--------|--------|
| Fork `Spirent/Velocity-assets` | Unauthorized (EMU cannot access) |
| Create personal repo | Not allowed for EMU |
| Create `Keysight-Copilot/*` repo | No `CreateRepository` permission |
| Push to `rakeshbitsindri/Apps` | Permission denied (EMU) |

`Spirent/Velocity-assets` is **pull-only** for this account.

## Branch ready locally

```
cd /root/Apps/velocity
git checkout community
git log origin/main..community --oneline
```

Commits:
- UHD Connect driver + RS-FEC knowledge
- Community drivers (SONiC, Hogan, Ixia SSH) + lifecycle docs
- Test-ready version pins + zips

Patches: `architect/community-pr-patches/`

## Option A — Personal GitHub (`rakeshbitsindri`)

PR opened as **ninja915** (pre-rename): https://github.com/Spirent/Velocity-assets/pull/72  
After username change, fork URL becomes `rakeshbitsindri/Velocity-assets` (see `GITHUB_USERNAME_RAKESHBITSINDRI.md`).

```bash
git clone https://github.com/rakeshbitsindri/Velocity-assets.git
cd Velocity-assets
git remote add upstream https://github.com/Spirent/Velocity-assets.git
git fetch upstream
git checkout -b community
git push -u origin community

gh pr create --repo Spirent/Velocity-assets --base main --head rakeshbitsindri:community \
  --title "Community drivers: UHD RS-FEC, SONiC speed mode, Hogan AresONE lifecycle" \
  --body-file architect/PR_COMMUNITY_DRIVERS.md
```

Web UI: https://github.com/Spirent/Velocity-assets/compare/main...rakeshbitsindri:community?expand=1

## Option B — Keysight admin

Ask Keysight GitHub admin to:

1. Create `Keysight-Copilot/Velocity-assets` (mirror/fork of Spirent)
2. Grant `rakesh-kumar_keysight` push access
3. Push `community` branch and open cross-org PR to Spirent (if policy allows)

## Option C — Spirent Developer Community zip upload

Import zips from `architect/drivers_bundle/zips/` via Velocity UI (no git PR required for lab testing):

- `rp_uhd_connect.mgmt.driver.zip` — UHD-Connect-Mgmt v1.2.3
- `rp_sonic.l2.switch.driver.zip` — SONiC-RoCE-Mgmt v1.2.0
- `rp_ixos_hogan.mgmt.driver.zip` — IXIA-Chassis-Mgmt v1.3.0
- `rp_ixia_chassis.mgmt.driver.zip` — IXIA-Chassis-SSH v1.0.1

## Author

Written and debugged by rakesh.kumar@keysight.com  
Co-authored-by: Cursor
