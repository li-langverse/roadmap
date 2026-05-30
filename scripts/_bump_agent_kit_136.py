from pathlib import Path

p = Path(__file__).resolve().parents[1] / "agent-kit/manifest.toml"
t = p.read_text(encoding="utf-8")
t = t.replace('version = "1.3.5"', 'version = "1.3.6"', 1)
if "agent-self-unblock" not in t:
    t = t.replace(
        '  "skills/audit-plan-completion",\n  "skills/run-local-ci-gha-quota",',
        '  "skills/audit-plan-completion",\n  "skills/agent-self-unblock",\n  "skills/run-goal-directed-loop",\n  "skills/run-local-ci-gha-quota",',
    )
p.write_text(t, encoding="utf-8")
print("manifest 1.3.6")
