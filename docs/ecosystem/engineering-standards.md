# Engineering standards (agents: mandatory)

<!-- DOC-ecosystem-engineering-standards -->

**Agents do not get to improvise on quality.** Style and structure have freedom; **functionality**, **security**, and **performance** are **strictly engineered**.

Read with [agent-coordination.md](agent-coordination.md) and [vision-and-roadmap.md](vision-and-roadmap.md).

---

## The three gates (always)

Every PR, package, and phase must satisfy **all three**:

| Gate | Meaning | Evidence |
|------|---------|----------|
| **Functionality** | Matches spec/REQ; correct for stated inputs; no silent wrong answers | `li-tests` / `lit` green; **T-** ids in manifest; contracts discharged when phase requires |
| **Security** | No known CVE class unmitigated for this repo; no trusted creep; config safe-by-default | [Security testing](https://github.com/li-langverse/lic/blob/main/docs/testing/security.md); repo exploit/fuzz suites; `nginx_mitigations` / `webserver-bugs` where HTTP |
| **Performance** | No unmeasured hot paths; regressions investigated | Benchmarks tier appropriate to repo; policy e.g. ≤2× oracle or ≤1.2× C++ where plan says |

**Forbidden:** “It compiles, ship it” without the row’s evidence. **Forbidden:** disabling security/perf CI to go green without a tracked **PH-** / issue and user approval.

---

## Security — CVE discipline

**Always test against known CVE classes relevant to the repo.**

| Repo type | Catalog / harness |
|-----------|-------------------|
| **`lic`** (compiler) | [`security/cve-catalog.json`](https://github.com/li-langverse/lic/blob/main/security/cve-catalog.json), [`cwe-to-li-tests.toml`](https://github.com/li-langverse/lic/blob/main/security/cwe-to-li-tests.toml), `li-tests/run_security.sh`, fuzz nightly |
| **`lis`** (httpd) | [`tier5_http` exploits](https://github.com/li-langverse/lis/tree/main/benchmarks/tier5_http/exploits), `nginx_mitigations.toml`, [webserver-bugs.toml](https://github.com/li-langverse/lic/blob/main/security/webserver-bugs.toml) |
| **New official package** | Copy security templates from `scripts/templates/github-repo/`; add rows to catalog when introducing a new attack surface |

**On every security-sensitive change:**

1. Search catalog for CWE/CVE class (smuggling, overflow, race, weak crypto, …).
2. Add or extend **T-** test / exploit TOML / fuzz seed.
3. Map to **REQ-** or **li_invariant** in plan or `PUBLISH.md`.
4. Run **`scripts/ci-security.sh`** (or repo `./scripts/ci.sh` if it includes security).

Agents: if a CVE class is **not** in the catalog, **add a stub row** in the same PR that implements the fix.

---

## Performance — measured only

| Rule | Detail |
|------|--------|
| No perf refactor without baseline | CSV or bench row in PR description |
| Regressions | Investigate before merge; document in CHANGELOG if intentional |
| Agent workloads | Prefer concurrent streams, tail latency, proof-friendly bounds — see [li-httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md) |
| SIMD/parallel | Tier 1 benches; master plan **≤1.2× C++** where stated |

---

## Coverage tiers

| Scope | Line coverage | Enforced by |
|-------|---------------|-------------|
| **`std/**` in `lic`** | **100%** | `scripts/check-stdlib-coverage.sh`; `.cursor/rules/li-stdlib.mdc` |
| **`lip publish` / official `li-*`** | **≥80%** | `lit test --coverage`; `li.toml` `min_coverage` |
| **Compiler `li-tests`** | Conformance + CVE map | Manifest outcomes, not a single % gate |
| **Experimental monorepo package** | SHOULD ≥80% before org promote | [governance](governance.md) promotion checklist |

Lowering any tier requires human approval and a tracked **PH-** / issue.

---

## Functionality — spec-first

| Rule | Detail |
|------|--------|
| Normative spec before code | REQ/PH in master plan or package traceability |
| AI-first UX | OpenAI-compatible routes, streaming, cancellation, trace IDs where product says agent |
| Config | Typed + `validate-config`; no string-eval config |
| Breaking change | Semver + migration note + downstream notification |

---

## Learn from other ecosystems (required design step)

Before implementing a **new ecosystem feature** (package manager, HTTP proxy, registry, test runner, …):

1. **Survey** — name 2–4 references (e.g. Cargo, npm, nginx, Envoy, LiteLLM, Go modules).
2. **Extract** — algorithms, UX patterns, security mitigations worth keeping.
3. **Adapt** — stitch into Li: must satisfy **easy + AI-first + provable + fast**; reject what needs `Any`/runtime magic.
4. **Document** — short “Learned from” subsection in phase plan or `docs/adr/` / package `docs/traceability.md`.

**Examples (intent, not copy-paste):**

| Li component | Learn from | Keep | Reject |
|--------------|------------|------|--------|
| `lip` lockfile | Cargo, npm | Reproducible pins, integrity | Opaque lifecycle scripts |
| li-httpd routing | nginx, Envoy | Prefix trees, upstream LB | `if`/`rewrite`, Lua |
| li-httpd limits | APISIX, LiteLLM | Stream timeouts, token buckets | Unbounded body pass-through |
| `lit` coverage | pytest + cargo tarpaulin | 80% gate on publish | Flaky timing-only tests |

**Nginx** remains **oracle + CVE checklist** for httpd — not a code port ([li-httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md)).

---

## What agents may decide freely

- Naming inside a package (if traceability ids updated)
- Refactors that **preserve** all three gates and proof obligations
- Doc wording, examples, test layout

## What agents must escalate

- Lowering coverage, skipping CVE tests, or weakening bench thresholds
- New `trusted.lean` axioms
- New org repos, secrets, branch protection
- Changing **language pillars** or master plan phase order

---

## Checklist (copy per task)

- [ ] Vision change reflected in **master plan** or package docs (see [vision-and-roadmap.md](vision-and-roadmap.md))
- [ ] **Functionality:** tests + spec ids
- [ ] **Security:** relevant CVE classes covered
- [ ] **Performance:** bench or explicit N/A with reason
- [ ] **Learned from** other ecosystems documented
- [ ] Downstream pins notified if `lic` / API changed
- [ ] `.li-agent-coord.json` claims updated
