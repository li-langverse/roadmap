# Li philosophy

Principles that guide language design, ecosystem packages, and agent coordination. Normative compiler rules live in [`lic`](https://github.com/li-langverse/lic); this file is the human- and agent-facing voice.

## Three pillars (order is binding)

1. **Mathematical provability** — `lic build` is the proof certificate.
2. **Easy syntax** — Nim-like surface, Python 3.14 types (no `Any`).
3. **Fast execution** — LLVM, SIMD, OpenMP **after** proof.

When pillars conflict, provability wins.

## Composability

Li treats every substantial feature — webservers, benchmark runners, package tools — as a **small, composable API**, not a monolithic binary. Other programs and agents must be able to `import` a library, call `serve` / `stop` / `ready` (or domain-equivalent verbs), and tear down services without copy-paste. Package `src/lib.li` is canonical; `src/main.li` is a thin demo only. Composable surfaces still carry proof contracts under strict-by-default.

**Implementation detail (lic):** [composable-by-default.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/composable-by-default.md)

## Strict by default

Proof, security, and performance gates run at maximum unless explicitly relaxed in `li.toml` `[gates]` or documented env downgrades. See [engineering-standards.md](ecosystem/engineering-standards.md).
