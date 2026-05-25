# li-httpd compiler prerequisites (P0)

li-httpd **M1 `.li` code** does not start until these **`lic`** gates pass. Infra in **`lis`** can proceed in parallel.

| ID | Work | Repo | Plan |
|----|------|------|------|
| P0-lean | VC + Lean on `lic build` (real discharge) | `lic` | Master plan 2e–2f |
| P0-bytes | `std` bytes, stringview, Reader/Writer | `lic` | [li-httpd plan](https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-16-li-httpd-plan.md) w0-bytes-io |
| P0-net | `raises Net`, trusted syscall RFC | `lic` | httpd plan |
| P0-async | async/await + epoll/kqueue | `lic` | w1-async-reactor |
| P0-http | HTTP/1.1 parser proofs | `lic` | w2-http11 |

**Coverage:** `std/**` = **100%**; published `li-*` = **≥80%** ([engineering-standards.md](engineering-standards.md)).

**lis status:** [implementation-status](https://github.com/li-langverse/lis/blob/main/docs/implementation-status.md) (infra harness complete).

**Org mirrors:** See [httpd-repo-canonical.md](httpd-repo-canonical.md) for `li-httpd` vs legacy `net.httpd` (recommendation only; no deletes until WP-D3 human gate).
