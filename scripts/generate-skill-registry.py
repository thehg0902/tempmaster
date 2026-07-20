#!/usr/bin/env python3
"""Generate docs/REGISTRY.md from skill frontmatter. Never hand-edit it."""
import re, pathlib

SKILLS = pathlib.Path(".claude/skills")
rows = []
for d in sorted(SKILLS.iterdir()):
    sk = d / "SKILL.md"
    if not d.is_dir() or not sk.exists(): continue
    text = sk.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    def grab(key, default="-"):
        mm = re.search(rf"{key}:\s*(.+)", fm)
        return mm.group(1).strip() if mm else default
    desc = re.search(r"description:\s*(.+?)(?=\nmetadata:|\Z)", fm, re.S)
    desc = re.sub(r"\s+", " ", desc.group(1)).strip() if desc else "-"
    meta = re.search(r"metadata:\s*\{(.*?)\}", fm)
    meta = meta.group(1) if meta else ""
    ver = re.search(r"version:\s*([\d.]+)", meta)
    cat = re.search(r"category:\s*(\w+)", meta)
    tier = re.search(r"tier:\s*(\w+)", meta)
    rows.append((d.name, tier.group(1) if tier else "-",
                 cat.group(1) if cat else "-",
                 ver.group(1) if ver else "-", desc))

out = ["# Skill Registry (auto-generated - do not hand-edit)",
       "", "Regenerate: `python3 scripts/generate-skill-registry.py`", "",
       "| skill | tier | category | version | description |",
       "|---|---|---|---|---|"]
for name, tier, cat, ver, desc in sorted(rows, key=lambda r: (r[1], r[0])):
    out.append(f"| {name} | {tier} | {cat} | {ver} | {desc} |")
pathlib.Path("docs").mkdir(exist_ok=True)
pathlib.Path("docs/REGISTRY.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote docs/REGISTRY.md ({len(rows)} skills)")
