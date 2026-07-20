#!/usr/bin/env python3
"""Agency OS automated QA gate. Run from repo root. Exit 1 on any FAIL."""
import re, sys, pathlib

ROOT = pathlib.Path(".")
SITE = ROOT / "site"
fails, warns = [], []

def fail(msg): fails.append(msg)
def warn(msg): warns.append(msg)

# scan all of site/ recursively (root page, shared/, every page folder)
html_files = sorted(SITE.rglob("*.html"))
css_files  = sorted(SITE.rglob("*.css"))
js_files   = sorted(SITE.rglob("*.js"))

if not html_files:
    fail("no HTML files in site/ - nothing to QA")

for f in html_files + css_files + js_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    if "[PLACEHOLDER" in text: fail(f"{f}: unresolved [PLACEHOLDER]")
    if re.search(r"\bTODO\b", text): fail(f"{f}: leftover TODO")
    if "lorem ipsum" in text.lower(): fail(f"{f}: lorem ipsum")

for f in html_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    # local refs exist - resolved relative to each file's own folder, so
    # "../assets/..." from a page folder and "assets/..." from site/ root
    # both pass when the target exists. Folder refs (about/) hit index.html.
    for m in re.finditer(r'(?:src|href)="([^"#][^":]*?)"', text):
        ref = m.group(1)
        if ref.startswith(("http", "mailto:", "tel:", "//", "data:")): continue
        target = (f.parent / ref).resolve()
        if target.is_dir(): target = target / "index.html"
        if not target.exists():
            fail(f"{f}: broken local ref -> {ref}")
    # img alt + intrinsic size (CLS)
    for m in re.finditer(r"<img\b[^>]*>", text):
        tag = m.group(0)
        if "alt=" not in tag: fail(f"{f}: <img> missing alt")
        if "width=" not in tag or "height=" not in tag:
            warn(f"{f}: <img> missing width/height (CLS) -> {tag[:60]}")
    # single h1
    n_h1 = len(re.findall(r"<h1\b", text))
    if n_h1 != 1: fail(f"{f}: {n_h1} <h1> tags (need exactly 1)")
    if "<main" not in text: warn(f"{f}: no <main> landmark")
    # viewport meta
    if "viewport" not in text: fail(f"{f}: missing viewport meta")
    # stylesheet link order per file-structure contract:
    # tokens.css -> base.css -> the page's own style.css
    sheets = [s.split("/")[-1] for s in
              re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', text)
              + re.findall(r'<link[^>]+href="([^"]+)"[^>]+rel="stylesheet"', text)]
    order = [s for s in sheets if s in ("tokens.css", "base.css", "style.css")]
    if order and order != [s for s in ("tokens.css", "base.css", "style.css") if s in order]:
        fail(f"{f}: stylesheet order {order} (contract: tokens -> base -> style)")

# hardcoded colors outside tokens.css; per-page CSS health
for f in css_files:
    if f.name == "tokens.css": continue
    text = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"#[0-9a-fA-F]{3,8}\b|rgb\(", text):
        fail(f"{f}: hardcoded color '{m.group(0)}' (use var(--token))"); break
    if f.name == "style.css":  # per-page css: small + token-driven
        kb = f.stat().st_size // 1024
        if kb > 20:
            warn(f"{f}: {kb}KB page css (>20KB suggests shared/ leakage)")
        if text.strip() and "var(" not in text:
            warn(f"{f}: no var( usage - bypassing design tokens?")

# header/footer drift across page folders. Pages at different depths
# legitimately differ in relative href/src prefixes (../), so normalize
# those away before comparing - only real content drift warns.
def block(tag, text):
    m = re.search(rf"<{tag}\b.*?</{tag}>", text, re.S)
    if not m: return None
    b = re.sub(r"\s+", " ", m.group(0))
    return re.sub(r'((?:src|href)=")(?:\.\./)+', r"\1", b)
if len(html_files) > 1:
    base = html_files[0].read_text(encoding="utf-8", errors="replace")
    for tag in ("header", "footer"):
        ref_block = block(tag, base)
        for f in html_files[1:]:
            other = block(tag, f.read_text(encoding="utf-8", errors="replace"))
            if ref_block and other and ref_block != other:
                warn(f"{f}: <{tag}> differs from {html_files[0]} (drift?)")

# page-weight audit vs hosting-profile budgets (the "dip detector").
# Profile from client.md 'Hosting plan:' - business/cloud/cdn = cdn
# profile, anything else / unknown = the tighter no-cdn set (fail-safe).
def hosting_profile():
    try:
        txt = (ROOT / "client" / "client.md").read_text(encoding="utf-8")
        txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)  # docs comments lie
        txt = re.sub(r"\{[^{}]*\}", "", txt)              # {operator comments}
        m = re.search(r"^[-*]?[ \t]*Hosting plan[ \t]*:[ \t]*(.+)$", txt, re.M | re.I)
        v = m.group(1).strip().lower() if m else ""
        if v and ("business" in v or "cloud" in v or "cdn" in v):
            return "cdn"
    except OSError:
        pass
    return "no-cdn"

PROFILE = hosting_profile()
MB = 1024 * 1024
PAGE_CAP, HERO_CAP = (1.5 * MB, 4 * MB) if PROFILE == "cdn" else (1.0 * MB, 3 * MB)

for f in html_files:
    text = f.read_text(encoding="utf-8", errors="replace")
    refs = set(re.findall(r'(?:src|href|poster)="([^"#][^":]*?)"', text))
    for ss in re.findall(r'srcset="([^"]+)"', text):
        for part in ss.split(","):
            if part.strip(): refs.add(part.strip().split()[0])
    weights, video_bytes = [], 0
    for ref in refs:
        if ref.startswith(("http", "mailto:", "tel:", "//", "data:")): continue
        target = (f.parent / ref).resolve()
        if not target.exists() or target.is_dir(): continue
        size = target.stat().st_size
        if target.suffix.lower() in (".mp4", ".webm", ".mov"):
            video_bytes += size          # video capped separately, not in page weight
        else:
            weights.append((size, ref))
    total = sum(s for s, _ in weights)
    top3 = ", ".join(f"{r} ({s // 1024}KB)" for s, r in sorted(weights, reverse=True)[:3])
    if total > PAGE_CAP:
        fail(f"{f}: page weight {total / MB:.2f}MB > {PAGE_CAP / MB:.1f}MB cap "
             f"[{PROFILE}]; heaviest: {top3}")
    elif total > PAGE_CAP * 0.8:
        warn(f"{f}: page weight {total / MB:.2f}MB is >80% of the "
             f"{PAGE_CAP / MB:.1f}MB cap [{PROFILE}]; heaviest: {top3}")
    if video_bytes > HERO_CAP:
        fail(f"{f}: video weight {video_bytes / MB:.1f}MB > {HERO_CAP / MB:.0f}MB cap [{PROFILE}]")
    elif video_bytes > HERO_CAP * 0.8:
        warn(f"{f}: video weight {video_bytes / MB:.1f}MB is >80% of cap [{PROFILE}]")

# media log consistency. Cell indices assume the 9-column contract table
# with leading pipe: split("|") -> [ '', id, date, type, model, prompt,
# credits, approved, file, status, '' ] so cells[8] = file column.
log = ROOT / "state" / "MEDIA_LOG.md"
if log.exists():
    for line in log.read_text().splitlines():
        if "| generated" in line or "| in-use" in line:
            cells = [c.strip() for c in line.split("|")]
            if len(cells) > 8 and cells[8] not in ("-", "") and not (ROOT / cells[8]).exists():
                fail(f"MEDIA_LOG: file missing on disk -> {cells[8]}")

print("=== QA CHECK ===")
for w in warns: print(f"WARN  {w}")
for x in fails: print(f"FAIL  {x}")
print(f"{len(fails)} fail, {len(warns)} warn")
sys.exit(1 if fails else 0)
