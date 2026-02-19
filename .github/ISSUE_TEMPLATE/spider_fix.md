---
name: Spider fix
about: Report and track fixes for a specific retailer spider
title: "[Spider Fix] <spider_name>: <short issue summary>"
labels: ["spider", "bug"]
assignees: []
---

## Spider
- Spider name: `<spider_name>`
- Retailer/site: `<site>`
- Mode(s): `<api | bootstrap | html>`

## Problem summary
Describe the failure clearly.

## Current behavior
- Item count: `<count>`
- Status/result: `<e.g., 403, 401, captcha, empty parse, timeout>`
- First observed: `<date/time + timezone>`

## Expected behavior
Describe expected output (for example, non-zero items for category/search run).

## Reproduction
```bash
# Exact command(s)
common-scrapy crawl <spider_name> -a <args> -a max_pages=1 -O /tmp/<spider_name>.jsonl
```

## Logs / evidence
Paste key log lines and errors.

```text
<paste relevant log excerpt>
```

## Suspected cause
- [ ] Internal API request shape/auth changed
- [ ] Bootstrap state not present / changed
- [ ] HTML structure changed
- [ ] Bot protection / geo / proxy issue
- [ ] Other: `<details>`

## Proposed fix plan
1. Validate internal API (URL, headers, auth/session requirements)
2. Update bootstrap extraction if present (`__NEXT_DATA__` / `__APOLLO_STATE__` / custom)
3. Patch HTML fallback selectors/parsing
4. Re-test (`api`, `bootstrap`, `html`) with `max_pages=1`
5. Update README sample/output if needed

## Acceptance criteria
- [ ] Spider runs without crash
- [ ] At least one mode returns non-zero items in current test environment
- [ ] Output fields are normalized (`item_id`, `title`, `url`, price fields, etc.)
- [ ] README/examples are updated if behavior changed

## Environment
- Branch/commit: `<git rev-parse --short HEAD>`
- VPN state: `<connected/disconnected + city>`
- Proxy setting: `<PROXY set/unset>`
- Runtime notes: `<anything relevant>`
