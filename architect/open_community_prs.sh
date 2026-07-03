#!/usr/bin/env bash
# Open Community driver PR to Spirent/Velocity-assets using Keysight corporate GitHub.
# Prereq: gh auth login (Keysight SSO) or GH_TOKEN in ~/.cursor/agent-stack.env
set -euo pipefail

CORP_GITHUB_USER="${CORP_GITHUB_USER:-rakeshbitsindri}"
CORP_EMAIL="${CORP_EMAIL:-rakesh.kumar@keysight.com}"
KEYSIGHT_SSO="https://github.com/enterprises/Keysight-Technologies-Copilot/sso"

if ! gh auth status >/dev/null 2>&1; then
  if [[ -f /root/.cursor/agent-stack.env ]]; then
    # shellcheck disable=SC1091
    set -a && source /root/.cursor/agent-stack.env && set +a
  fi
  if [[ -n "${GH_TOKEN:-}" ]]; then
    echo "$GH_TOKEN" | gh auth login --hostname github.com --with-token
  else
    echo "GitHub not authenticated."
    echo "  1) Keysight SSO: $KEYSIGHT_SSO"
    echo "  2) Device login:  gh auth login --hostname github.com --web"
    echo "  Or add GH_TOKEN (repo scope) to ~/.cursor/agent-stack.env"
    exit 1
  fi
fi

LOGIN="$(gh api user -q .login)"
echo "Authenticated as: $LOGIN ($CORP_EMAIL)"

VELOCITY=/root/Apps/velocity
cd "$VELOCITY"

# Fork upstream under corporate account if needed
if ! git remote get-url fork >/dev/null 2>&1; then
  gh repo fork Spirent/Velocity-assets --remote=true --remote-name=fork
fi

export GIT_AUTHOR_NAME="Rakesh Kumar"
export GIT_AUTHOR_EMAIL="$CORP_EMAIL"
export GIT_COMMITTER_NAME="Rakesh Kumar"
export GIT_COMMITTER_EMAIL="$CORP_EMAIL"

git push -u fork community

gh pr create \
  --repo Spirent/Velocity-assets \
  --base main \
  --head "${LOGIN}:community" \
  --title "Community drivers: UHD RS-FEC, SONiC speed mode, Hogan AresONE lifecycle" \
  --body-file "$VELOCITY/architect/PR_COMMUNITY_DRIVERS.md"

echo ""
echo "Velocity PR: https://github.com/Spirent/Velocity-assets/pulls"

# LAAS staging scripts (optional — rakeshbitsindri/Apps or Keysight fork)
APPS=/root/Apps
if [[ -d "$APPS/.git" ]]; then
  cd "$APPS"
  if git remote get-url origin | grep -q github.com; then
    git push -u origin community 2>/dev/null || true
    gh pr create \
      --repo "$(git remote get-url origin | sed -n 's#.*github.com[:/]\([^/]*\/[^/.]*\).*#\1#p')" \
      --base main \
      --head community \
      --title "LAAS lab staging workflow for Community driver FEC/speed testing" \
      --body "$(cat <<EOF
## Summary
- lab_staging_workflow.py — backup-first deploy and rollback
- lab_driver_selftest.py — local driver dispatch tests
- SONiC/Hogan topology hooks + UHD FEC in reservation service

Written and debugged by $CORP_EMAIL
Co-authored-by: Cursor
EOF
)" 2>/dev/null && echo "LAAS PR created." || echo "LAAS PR skipped."
  fi
fi
