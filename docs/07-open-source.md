# Open-source checklist

A checklist for a public repo, and its status for this repo. Each item has a level:

- 🛑 **Blocker:** harm that cannot be undone once the repo is public. Fix before the next push.
- ⚠️ **Warning:** looks careless, or costs work later. Fix soon.
- 📝 **Note:** worth knowing. No action needed.

The steps come from the `opening-a-repo` skill in the `opensource` plugin. Its audit file has
the exact scan commands.

**Status on 2026-11-14:** the repo is already public (since 2026-11-13). 0 secrets. 1 open
item: who owns the code. Everything else is done or listed below.

## 1. Decide

| Check | Level | This repo |
|---|---|---|
| A named maintainer answers issues | 🛑 | ✅ lethuan127, best effort, stated in `SECURITY.md` |
| The license is chosen, and the owner may release the code | 🛑 | ❓ MIT. **Confirm:** you own this code, and no employer claims work made on its time |
| The support level is written down | ⚠️ | ✅ "best effort" in `CONTRIBUTING.md` and `SECURITY.md` |

## 2. Audit: the tree and the full history

A clean tree proves nothing. Old commits keep every deleted line.

| Check | Level | This repo |
|---|---|---|
| No secrets in any commit (keys, tokens, `.env`, private keys) | 🛑 | ✅ 15 commits searched, 0 hits. No scanner installed; a manual search ran |
| No customer or personal data in fixtures, tests or docs | 🛑 | ✅ Fixtures use made-up data. The eval phone number and names are fake |
| No real company or customer names | 🛑 | ✅ Fixed on 2026-11-14 with option B: `main` was squashed to one commit and force pushed. See "Decision" |
| No third-party code without a license | 🛑 | ✅ All code written here. cc-skills had no license, so nothing was copied |
| Dependency licenses fit the outbound license | 🛑 | ✅ Python standard library, plus `openpyxl` (MIT) |
| No internal hostnames, ticket IDs or channel names | ⚠️ | ✅ None found |
| Commit author emails are ones you want public | ⚠️ | 📝 One personal Gmail address. Keep it, or use GitHub's noreply address for new commits |
| Commit messages name no customer or incident | ⚠️ | ✅ Clean |

## 3. Prepare the files

| Check | Level | This repo |
|---|---|---|
| `LICENSE` with the exact SPDX text and the right owner | 🛑 | ✅ Added to the root and to the plugin folder. It was missing before |
| `README` says what it is, its status, how to install | ⚠️ | ✅ English and Vietnamese |
| `CONTRIBUTING.md`: setup, test commands, scope | ⚠️ | ✅ Added |
| `SECURITY.md`: a private way to report a problem | ⚠️ | ✅ Added. Needs private reporting turned on in GitHub settings |
| Issue forms that ask only for what you need | ⚠️ | ✅ `bug.yml` and `feature.yml`. Both warn that the page is public |
| CI that runs without secrets, so fork pull requests pass | ⚠️ | ✅ `check.yml`: unit tests, manifests, skill names, dead links |
| Code of conduct | 📝 | Skipped. One maintainer, no community yet. A code with nobody to read reports is worse than none |

## 4. GitHub settings

| Check | Level | This repo |
|---|---|---|
| Description and topics | ⚠️ | ✅ Set on 2026-11-14. 8 topics, plus a social preview image |
| Private vulnerability reporting on | ⚠️ | ✅ On |
| Secret scanning and push protection on | ⚠️ | ✅ On |
| Branch protection on `main` requires CI | 📝 | Skipped. One maintainer pushes to `main` directly |
| Wiki turned off, if unused | 📝 | ✅ Off |

## 5. After publishing: sustain

| Check | Level | This repo |
|---|---|---|
| Clone the public URL and scan what landed | ⚠️ | ✅ Done on 2026-11-14: 1 commit, 0 company names, checks pass |
| A fixed time to read new issues | ⚠️ | Plan: once a week. Feedback from `send-feedback` lands as issues |
| Releases follow version numbers, with notes | 📝 | The "Versions" part of the plugin README |

## Decision: the company name in old commits

**Chosen: B, by lethuan127, on 2026-11-14.** Before that, 2 early commits described the employer by name. The facts came from the
company's public website, so nothing secret leaked. But a reader can link the plugin to the
company and to the Product Owner.

| Option | Cost | Note |
|---|---|---|
| **A. Fresh repo** (recommended) | 10 minutes | Delete the GitHub repo, create it again, push one squashed commit. Old clones and forks keep the old history, but the repo is 1 day old with no stars, so there are likely none |
| B. Force push a squashed `main` | 5 minutes | GitHub keeps the old commits reachable by hash for a while. The `opening-a-repo` skill advises against it |
| C. Accept | 0 | Record who accepted it and when, in this file |

**Risk left after B:** GitHub may still show the old commits to anyone who has their hash. To
remove them for good, ask GitHub Support to purge the cached views and unreachable objects of
this repo.
