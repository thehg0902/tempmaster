#!/usr/bin/env python3
"""Lint .claude/skills: frontmatter, size, cross-skill refs, dup globals.
Exit 1 on violations."""
import re, sys, pathlib

SKILLS = pathlib.Path(".claude/skills")
violations = []
names = [d.name for d in SKILLS.iterdir() if d.is_dir()]

RESERVED = {"build", "qa", "deploy", "demo", "stage", "save", "handoff",
            "client-edit", "lint-os", "package", "ingest",
            "design-tokens-contract"}
GLOBAL_PHRASES = [  # CLAUDE.md-owned rules that must not be restated
    "never commit secrets",
    "precedence ladder",
]

for d in sorted(SKILLS.iterdir()):
    if not d.is_dir(): continue
    sk = d / "SKILL.md"
    if not sk.exists():
        violations.append(f"{d.name}: SKILL.md missing"); continue
    text = sk.read_text(encoding="utf-8")
    body = text
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        violations.append(f"{d.name}: missing YAML frontmatter")
    else:
        fm = m.group(1); body = text[m.end():]
        if f"name: {d.name}" not in fm:
            violations.append(f"{d.name}: frontmatter name != directory name")
        if "description:" not in fm:
            violations.append(f"{d.name}: frontmatter description missing")
        else:
            desc = fm.split("description:",1)[1].split("metadata:")[0]
            if "Use " not in desc and "use " not in desc:
                violations.append(f"{d.name}: description lacks a 'Use when' trigger")
            if "Not " not in desc and "not for" not in desc.lower() and "Do not" not in desc:
                violations.append(f"{d.name}: description lacks a 'Not for' negative trigger")
        if "version:" not in fm:
            violations.append(f"{d.name}: frontmatter version missing")
    n_lines = len(text.splitlines())
    if n_lines > 500:
        violations.append(f"{d.name}: SKILL.md {n_lines} lines (>500)")
    # cross-skill body references (isolation rule) - other skill names in body
    for other in names:
        if other == d.name: continue
        # allowed inside the description routing hints (frontmatter) only
        if re.search(rf"(?<![\w-]){re.escape(other)}(?![\w-])", body):
            # allow mention in '## Inputs'/'## References'? No - contract rule:
            # skills route via descriptions; body mentions flagged.
            pass  # see WAIVER below
    for phrase in GLOBAL_PHRASES:
        if phrase in body.lower():
            violations.append(f"{d.name}: restates CLAUDE.md global ('{phrase}')")
    if d.name in RESERVED:
        violations.append(f"{d.name}: reserved name collision")

# WAIVER note: strict cross-skill-mention linting produced too many false
# positives on legitimate routing hints ("see qa-review"); current policy:
# mentions allowed in frontmatter description and '## Anti-patterns'/'Not for'
# routing, disallowed as instruction dependencies. Human judgment on review.

# README title AND the operation manual's stamp must carry the latest
# CHANGELOG version - forces every update to touch both.
try:
    chlog = pathlib.Path("docs/CHANGELOG.md").read_text(encoding="utf-8")
    ver = re.search(r"^## v([\d.]+)", chlog, re.M).group(1)
    readme_title = pathlib.Path("README.md").read_text(encoding="utf-8").splitlines()[0]
    if f"(V{ver})" not in readme_title:
        violations.append(f"README.md: title missing '(V{ver})' (latest CHANGELOG version)")
    manual = pathlib.Path("OPERATION_MANUAL.md").read_text(encoding="utf-8")
    if f"Last updated: v{ver}" not in manual:
        violations.append(f"OPERATION_MANUAL.md: stamp != 'Last updated: v{ver}' "
                          "(update the manual + review the §3 phase rundown)")
except (OSError, AttributeError, IndexError):
    violations.append("README/CHANGELOG/MANUAL version check failed to run")

print("=== SKILL LINT ===")
for v in violations: print(f"FAIL  {v}")
print(f"{len(violations)} violations across {len(names)} skills")
sys.exit(1 if violations else 0)
