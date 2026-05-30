# Li ecosystem overview

<!-- DOC-ecosystem-overview -->

Li ships as a **language** ([`li-langverse/li-language`](https://github.com/li-langverse/li-language)) plus **packages** you build and publish under the same org. The org’s ambition is to be the **go-to open ecosystem for HPC, scientific computing, and AI** — see [vision north star](vision-and-roadmap.md#north-star--go-to-ecosystem-agents-read-first).

## Three tools

| Tool | Repo | Role | Status |
|------|------|------|--------|
| **`lic`** | [li-language](https://github.com/li-langverse/li-language) | Compile and prove your code | Available |
| **`lit`** | [**lip**](https://github.com/li-langverse/lip) | Tests and ≥80% line coverage gate | Bootstrap (phase 8e) |
| **`lip`** | [**lip**](https://github.com/li-langverse/lip) | Dependencies, lockfile, registry publish | Bootstrap (phase 8b–8d) |

Package manager and test tooling live in **[`li-langverse/lip`](https://github.com/li-langverse/lip)** (sibling repo to `li-language`).

## Creating a package today

Use the scaffold script (same layout `lip` will expect later):

```bash
./scripts/li-new-package my-lib --kind library
./scripts/li-new-package my-app --kind binary --official
```

Official / standard packages belong in **[`li-langverse`](https://github.com/li-langverse)** on GitHub. See [Creating packages](https://github.com/li-langverse/lic/blob/main/docs/guide/creating-packages.md) and [Governance](governance.md).

## Agents working in parallel

**New agents — read in order:** [engineering-standards.md](engineering-standards.md) (strict functionality / security / performance) → [vision-and-roadmap.md](vision-and-roadmap.md) → [agent-coordination.md](agent-coordination.md) (`.li-agent-coord.json`, claims).

## Language + ecosystem evolving together

Compiler changes flow downstream via **`li-toolchain.toml`**, release dispatch, and CI. See **[language-evolution.md](language-evolution.md)** and [upstream-notifications.md](upstream-notifications.md).

## Bootstrap lip / lit locally

```bash
git clone https://github.com/li-langverse/lip.git   # after org push
cd lip && LI_REPO=../li-language ./scripts/ci.sh
```

## Plans

| Topic | Document |
|-------|----------|
| **Algorithms & libraries (HPC → gaming → drug → CAD → cinematic)** | [algorithms-and-libraries-plan.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/algorithms-and-libraries-plan.md) |
| World Studio (shell + profiles) | [world-studio-vision.md](https://github.com/li-langverse/lic/blob/main/docs/game-dev/world-studio-vision.md) |
| Scaffold + `li.toml` | [Package scaffold plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-package-scaffold.md) |
| `lip` + `lit` | [Package manager plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-package-manager-lip.md) |
| Org + traceability | [Ecosystem governance](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-ecosystem-governance.md) |
| Official packages | [official-packages.md](official-packages.md) |
