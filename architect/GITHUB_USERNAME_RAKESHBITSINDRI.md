# GitHub username: rakeshbitsindri

Personal account rename from `ninja915` → `rakeshbitsindri`.

## 1. Rename on GitHub (required — one-time, web UI)

https://github.com/settings/admin → **Change username** → `rakeshbitsindri`

GitHub redirects old URLs; repos move automatically (`ninja915/Velocity-assets` → `rakeshbitsindri/Velocity-assets`).

Open PR [#72](https://github.com/Spirent/Velocity-assets/pull/72) should keep working after rename.

## 2. Already updated on nginx-eagle

| Item | New value |
|------|-----------|
| Velocity `fork` remote | `https://github.com/rakeshbitsindri/Velocity-assets.git` |
| Apps `origin` remote | `https://github.com/rakeshbitsindri/Apps.git` |
| `open_community_prs.sh` | `CORP_GITHUB_USER=rakeshbitsindri` |
| `~/.cursor/agent-stack.env` | `GITHUB_USERNAME=rakeshbitsindri` |

## 3. After rename — refresh CLI

```bash
gh auth refresh -h github.com -s user,repo,read:org
gh api user -q .login   # expect: rakeshbitsindri

cd /root/Apps/velocity
git push -u fork community

cd /root/Apps
git push -u origin community
```

## 4. Verify

```bash
curl -s https://api.github.com/users/rakeshbitsindri | jq .login
gh pr view 72 --repo Spirent/Velocity-assets --json headRefName,headRepositoryOwner
```

Written and debugged by rakesh.kumar@keysight.com
