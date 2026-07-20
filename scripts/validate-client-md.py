#!/usr/bin/env python3
"""Validate client/client.md. Exit 1 on blockers.

v2 (paste-based) model: Creative / Overrides / Business Profile Paste /
Auto sections, everything optional; the ONLY blocker is no business name
found anywhere. Backward compatible: files with the old v1.1 headers
(## Business / ## Contact) validate under the v1.1 required-sections
rules. Optional arg: a different file to validate (for tests)."""
import re, sys, pathlib

CLIENT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "client/client.md")

V11_REQUIRED = ["Business", "Contact", "Services", "Pages", "Brand",
                "Audience", "Mood", "Stack"]
V11_OPTIONAL = ["Links", "Testimonials", "Photos", "Competitors",
                "Style references", "Special requests", "Autonomy"]
STACK_KEYS = {
    "animation": {"gsap", "css-only", "none"},
    "3d": {"yes", "no"},
    "booking": {"calendly", "none"},
    "forms": {"formspree", "none"},
    "email-marketing": {"brevo", "none"},
    "analytics": {"ga4", "plausible", "none"},
    "hero-media": {"video", "loop", "intro-loop", "scroll-scrub",
                   "image-sequence", "static", "propose"},
    "framework": {"vanilla", "react-cdn", "tailwind-cdn"},
}

if not CLIENT.exists():
    print("BLOCKER: client/client.md missing"); sys.exit(1)

text = CLIENT.read_text(encoding="utf-8")
# {curly-brace} operator comments: stripped globally BEFORE any parsing
# (schema v1.6.0) - never content, valid in both v1.1 and v2 formats.
text = re.sub(r"\{[^{}]*\}", "", text)
sections = {}
for m in re.finditer(r"^## (.+?)\s*$", text, re.M):
    start = m.end()
    nxt = re.search(r"^## ", text[start:], re.M)
    sections[m.group(1).strip()] = text[start:start + nxt.start() if nxt else len(text)].strip()

blockers, soft = [], []


def strip_comments(body):
    return re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()


def parse_pages_markup(pages_body):
    """`home | hero / menu | menu-list` -> summary string (shared v1.1/v2)."""
    pages_line = next((l for l in pages_body.splitlines() if "|" in l), "")
    if not pages_line:
        return ""
    line = re.sub(r"^[-*]?\s*(?:Pages:)?\s*", "", pages_line.strip())
    parsed = []
    for group in line.split("/"):
        tokens = [t.strip() for t in group.split("|")]
        page, secs = tokens[0], [t for t in tokens[1:] if t]
        if not page:  # empty page name / '|' before any page: SOFT, interpret
            if parsed:
                parsed[-1][1].extend(secs)
                soft.append(f"Pages markup: empty page name - folding sections {secs} into '{parsed[-1][0]}'")
            elif secs:
                parsed.append([secs[0], secs[1:]])
                soft.append(f"Pages markup: '|' before any page - treating '{secs[0]}' as the page")
            continue
        parsed.append([page, secs])
    return "; ".join(f"{p} ({', '.join(s)})" if s else p for p, s in parsed)


def check_stack_flags(stack_body, missing_is_soft=True):
    found = {}
    for line in stack_body.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            if v.strip():  # empty value = scaffold line, treat as unset
                found[k.strip().lstrip("-* ").lower()] = v.strip()
    # Free text (interpretation principle): unrecognized values and missing
    # keys are SOFT, never blockers. 'placeholder' is universal.
    for k, allowed in STACK_KEYS.items():
        v = found.get(k)
        if v is None:
            if missing_is_soft:
                soft.append(f"Stack flag '{k}' missing - defaulting to 'propose'")
        elif v not in allowed and v != "placeholder":
            soft.append(f"unrecognized value '{v}' for flag '{k}' - will interpret and recommend (DECISIONS.md)")


VIBE_DIR = pathlib.Path("client/assets-intake/vibe")
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}


def check_vibe(body):
    """Referenced vibe images must exist; unlisted ones get a note.
    Everything SOFT - vibe is pure optional context. -> summary or ''"""
    refs = re.findall(r"(?:vibe/)?([\w][\w .\-]*\.(?:png|jpe?g|webp|gif|avif))",
                      strip_comments(body), re.I)
    for r in refs:
        if not (VIBE_DIR / r).exists():
            soft.append(f"Vibe reference '{r}' not found in client/assets-intake/vibe/")
    on_disk = sorted(f.name for f in VIBE_DIR.iterdir()
                     if f.suffix.lower() in IMG_EXT) if VIBE_DIR.exists() else []
    for f in on_disk:  # committed with the repo (v1.3.2): keep them small
        kb = (VIBE_DIR / f).stat().st_size // 1024
        if kb > 500:
            soft.append(f"vibe image '{f}' is {kb}KB - compress to ~500KB "
                        "(it is committed to git)")
    unlisted = [f for f in on_disk if f not in refs]
    if unlisted:
        soft.append("vibe images not listed under ## Vibe (still viewed at "
                    f"Phase 2): {', '.join(unlisted)}")
    if refs or on_disk:
        return f"{len(refs)} referenced, {len(on_disk)} image(s) on disk"
    return ""


def find_name_in_overrides(body):
    # [ \t]* not \s* : \s would eat the newline and swallow the NEXT
    # scaffold line as the value ("- Name:\n- Phone:" -> "- Phone:")
    m = re.search(r"^[-*]?[ \t]*Name[ \t]*:[ \t]*(.+)$", body, re.M | re.I)
    if m and strip_comments(m.group(1)) and "TODO" not in m.group(1):
        return m.group(1).strip()
    return ""


def find_plausible_name_in_paste(body):
    """First non-trivial line of the paste is treated as a plausible
    business name candidate (GBP dumps start with the listing title)."""
    for line in body.splitlines():
        line = line.strip().lstrip("-*# ").strip()
        if not line or line.lower().startswith(("http", "www.")):
            continue
        if re.fullmatch(r"[\d\W]+", line):  # ratings/phone/punctuation-only
            continue
        return line
    return ""


# ---- format detection -------------------------------------------------
is_v11 = "Business" in sections or "Contact" in sections
mode = "v1.1 (legacy)" if is_v11 else "v2 (paste-based)"
pages_summary = ""
vibe_summary = check_vibe(sections.get("Vibe", ""))  # both formats
parsed_n = confirmed_n = unconfirmed_n = questions_n = 0

if is_v11:
    for s in V11_REQUIRED:
        body = sections.get(s)
        if body is None:
            blockers.append(f"required section '## {s}' missing")
        elif "TODO" in body or not body:
            blockers.append(f"required section '## {s}' incomplete (contains TODO or empty)")
    for s in V11_OPTIONAL:
        body = sections.get(s, "")
        if not body or "TODO" in body:
            soft.append(f"optional section '## {s}' missing or TODO")
    pages_summary = parse_pages_markup(sections.get("Pages", ""))
    check_stack_flags(sections.get("Stack", ""))
else:
    creative = strip_comments(sections.get("Creative", ""))
    overrides = strip_comments(sections.get("Overrides", ""))
    paste = strip_comments(sections.get("Business Profile Paste", ""))
    auto_key = next((k for k in sections if k.startswith("Auto")), None)
    auto = strip_comments(sections.get(auto_key, "")) if auto_key else ""

    # BLOCKER only if: no name in Overrides AND no plausible name in Paste
    # AND Auto empty.
    name = find_name_in_overrides(overrides)
    paste_name = find_plausible_name_in_paste(paste)
    if not name and not paste_name and not auto:
        blockers.append("no business name found anywhere (Overrides Name:, "
                        "Business Profile Paste, or Auto) - cannot start")

    # Creative answers present? (a bullet with text after its colon)
    has_creative = any(
        re.search(r":\s*\S", l) or (l.strip() and ":" not in l)
        for l in creative.splitlines())
    if not has_creative:
        soft.append("Creative section empty - will proceed on niche-playbook "
                    "defaults; answers there most improve voice and design")
    if not paste:
        soft.append("Business Profile Paste empty - falling back to "
                    "v1.1-style manual mode using Overrides only")
    elif not auto:
        soft.append("Paste present but Auto empty - run client-enrichment "
                    "(Phase 0) to parse it")

    pages_summary = parse_pages_markup(overrides)
    if not re.search(r"^[ \t]*[-*]?[ \t]*(animation|3d|booking|forms|email-marketing|analytics|hero-media|framework)[ \t]*:[ \t]*\S",
                     overrides, re.M | re.I):
        soft.append("no Stack flags in Overrides - all default to 'propose'")
    else:
        check_stack_flags(overrides, missing_is_soft=False)

    # Fact summary from Auto tags
    parsed_n = len(re.findall(r"^\s*-\s.*\[(?:paste|override)\]", auto, re.M))
    confirmed_n = len(re.findall(r"\[confirmed\]", auto))
    unconfirmed_n = len(re.findall(r"\[unconfirmed\]", auto))
    qfile = pathlib.Path("state/QUESTIONS.md")
    if qfile.exists():
        qtext = re.sub(r"<!--.*?-->", "", qfile.read_text(encoding="utf-8"), flags=re.S)
        questions_n = len(re.findall(r"^\s*-\s*\[ \]", qtext, re.M))

print("=== CLIENT.MD VALIDATION ===")
print(f"FORMAT   {mode}")
for b in blockers: print(f"BLOCKER  {b}")
for s in soft:     print(f"SOFT     {s}")
if pages_summary: print(f"PAGES    {pages_summary}")
if vibe_summary: print(f"VIBE     {vibe_summary}")
if not is_v11:
    print(f"FACTS    {parsed_n} parsed, {confirmed_n} confirmed, "
          f"{unconfirmed_n} unconfirmed, {questions_n} open questions")
print(f"{len(blockers)} blockers, {len(soft)} soft gaps")
sys.exit(1 if blockers else 0)
