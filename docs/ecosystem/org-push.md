# Pushing lic / lip / lit to li-langverse

Automation: [`scripts/push-li-langverse-repos.sh`](../../scripts/push-li-langverse-repos.sh).

## Prerequisites (human)

1. Fine-grained PAT or `gh auth login` scoped to **`li-langverse`**.
2. Store token outside git (e.g. local `.env.github` — **never commit**).
3. Set `LI_DOWNSTREAM_DISPATCH_TOKEN` on **`lic`** for `notify-downstream.yml`.

## Agent steps

```bash
./scripts/build.sh
./scripts/check-master-plan-gates.sh
./scripts/push-li-langverse-repos.sh   # when remotes configured
```

## Exit gate (8-sync)

- `lic`, `lip`, `lit` on GitHub with green CI (Linux + macOS).
- Tag `lic` v* → downstream `ecosystem-upstream` workflow fires on **lip**.
