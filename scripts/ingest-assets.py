#!/usr/bin/env python3
"""Agency OS asset ingest (/ingest). Matches files in
client/assets-intake/slots/ against SHOPPING_LIST.md, processes each per
its treatment (contracts/asset-slots.md), places outputs under site/assets/,
updates SHOPPING_LIST checkboxes + MEDIA_LOG rows, prints a report.

ADAPTIVE OPTIMIZATION (v1.4.1): quality-first within the performance
budget. Free transforms always run (resize cap, WebP, faststart,
poster); LOSSY levels use a ladder - start high, step down ONLY if the
asset exceeds its budget. Budgets are profile-aware: the client.md
`Hosting plan:` line selects cdn (hostinger-business) or no-cdn
(hostinger-premium / unknown - fail-safe tighter) budgets.

Tooling: images use cwebp, else Pillow, else PENDING commands. Video +
scrub + posters need only ffmpeg (it encodes WebP directly).
Idempotent: slots already marked [x] are skipped unless --force.
"""
import json, re, shutil, subprocess, sys, pathlib

ROOT = pathlib.Path(".")
SLOTS = ROOT / "client" / "assets-intake" / "slots"
LIST = SLOTS / "SHOPPING_LIST.md"
MEDIA_LOG = ROOT / "state" / "MEDIA_LOG.md"
OUT_VIDEO = ROOT / "site" / "assets" / "video"
OUT_IMAGES = ROOT / "site" / "assets" / "images"
MAX_W = 1440
FORCE = "--force" in sys.argv

processed, pending, missing, unexpected, flags = [], [], [], [], []


def hosting_profile():
    """cdn (hostinger-business/cloud or explicit cdn) vs no-cdn (default:
    the tighter, fail-safe budget set - see performance skill)."""
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
KB, MB = 1024, 1024 * 1024
BUDGET = {
    "cdn":    {"image": 300 * KB, "poster": 200 * KB,
               "vid_target": int(2.5 * MB), "vid_cap": 4 * MB, "scrub": 10 * MB},
    "no-cdn": {"image": 200 * KB, "poster": 150 * KB,
               "vid_target": 2 * MB, "vid_cap": 3 * MB, "scrub": 8 * MB},
}[PROFILE]


def which(tool): return shutil.which(tool) is not None


def has_pillow():
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True, capture_output=True)


def png_has_alpha(p):
    d = p.read_bytes()
    return len(d) > 25 and (d[25] in (4, 6) or (d[25] == 3 and b"tRNS" in d))


def parse_list(text):
    slots = []
    for m in re.finditer(
            r"^## +(\S+)\s+\[( |x)\] *filled.*?\n(?:folder:.*\n)?treatment: *(.+)$",
            text, re.M):
        slots.append({"name": m.group(1), "filled": m.group(2) == "x",
                      "treatment": m.group(3).split()[0].lower()})
    return slots


def treatment_of(slot):
    n = slot["name"]
    if re.search(r"-scrub\.\w+$", n): return "scroll-scrub"
    if re.search(r"-intro\.\w+$", n): return "intro-loop"
    if re.search(r"-loop\.\w+$", n):  return slot.get("treatment") or "loop"
    if n.endswith(".png"): return "alpha-or-image"
    if re.search(r"\.(jpe?g|webp)$", n): return "image"
    return slot.get("treatment") or "image"


def report_kept(name, level, size, budget):
    print(f"  kept {level} - {size // KB}KB, budget {budget // KB}KB [{PROFILE} profile]")


def encode_image(src, out, q):
    """One encode attempt at quality q. True = encoded, None = no tool."""
    if which("cwebp"):
        run(["cwebp", "-q", q, "-resize", MAX_W, 0, src, "-o", out])
        return True
    if has_pillow():
        from PIL import Image
        im = Image.open(src)
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)),
                           Image.LANCZOS)
        im.save(out, "WEBP", quality=q, method=6)  # EXIF dropped by default
        print(f"  pillow webp q{q} -> {out}")
        return True
    return None


def do_image(src, name):
    OUT_IMAGES.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".png" and png_has_alpha(src):
        out = OUT_IMAGES / src.name          # alpha: passthrough, never flatten
        shutil.copy2(src, out)
        ok = png_has_alpha(out)
        print(f"  alpha preserved: {'YES' if ok else 'NO - INVESTIGATE'}")
        return str(out.relative_to(ROOT)).replace("\\", "/") if ok else False
    budget = BUDGET["poster"] if "poster" in src.stem else BUDGET["image"]
    out = OUT_IMAGES / (src.stem + ".webp")
    for q in (90, 82, 75):                    # quality-first ladder
        r = encode_image(src, out, q)
        if r is None:
            pending.append((name, f"cwebp -q {q} -resize {MAX_W} 0 '{src}' -o '{out}'"
                                  "  (or: pip install pillow)"))
            return False
        size = out.stat().st_size
        if size <= budget:
            report_kept(name, f"q{q}", size, budget)
            return str(out.relative_to(ROOT)).replace("\\", "/")
    flags.append(f"{name}: {out.stat().st_size // KB}KB at q75 exceeds "
                 f"{budget // KB}KB budget [{PROFILE}] - resize/crop the source?")
    return str(out.relative_to(ROOT)).replace("\\", "/")


def do_video(src, name):
    if not which("ffmpeg"):
        pending.append((name, f"ffmpeg -i '{src}' -an -c:v libx264 -crf 23 "
                              f"-movflags +faststart -vf scale=-2:1080 "
                              f"'{OUT_VIDEO / name}'"))
        return False
    OUT_VIDEO.mkdir(parents=True, exist_ok=True)
    OUT_IMAGES.mkdir(parents=True, exist_ok=True)
    out = OUT_VIDEO / name
    kept = None
    for crf in (20, 23, 26):                  # CRF ladder: target, then cap
        run(["ffmpeg", "-y", "-i", src, "-an", "-c:v", "libx264", "-crf", crf,
             "-movflags", "+faststart", "-vf", "scale=-2:1080", out])
        size = out.stat().st_size
        if crf == 20 and size <= BUDGET["vid_target"]:
            kept = (f"CRF20", size); break
        if crf >= 23 and size <= BUDGET["vid_cap"]:
            kept = (f"CRF{crf}", size); break
    size = out.stat().st_size
    if kept:
        report_kept(name, kept[0], kept[1],
                    BUDGET["vid_target"] if kept[0] == "CRF20" else BUDGET["vid_cap"])
    else:
        flags.append(f"{name}: {size / MB:.1f}MB at CRF26 exceeds "
                     f"{BUDGET['vid_cap'] / MB:.0f}MB cap [{PROFILE}] - cut the clip")
    # poster: intro videos freeze on their FIRST frame, loops on the last
    poster = OUT_IMAGES / f"{src.stem}-poster.webp"
    frame_args = [] if "intro" in src.stem else ["-sseof", "-0.1"]
    run(["ffmpeg", "-y", *frame_args, "-i", out, "-frames:v", "1",
         "-quality", "80", poster])
    if poster.stat().st_size > BUDGET["poster"]:
        run(["ffmpeg", "-y", *frame_args, "-i", out, "-frames:v", "1",
             "-quality", "65", poster])
    return str(out.relative_to(ROOT)).replace("\\", "/")


def do_scrub(src, name):
    if not which("ffmpeg"):
        pending.append((name, f"ffmpeg -i '{src}' -vf fps=12,scale={MAX_W}:-2 "
                              f"-quality 80 'site/assets/images/scrub/{src.stem}/frame-%04d.webp'"))
        return False
    slot_dir = OUT_IMAGES / "scrub" / src.stem
    kept = None
    for fps, q in ((12, 80), (12, 70), (10, 70)):   # ladder: quality, then fps
        if slot_dir.exists(): shutil.rmtree(slot_dir)
        slot_dir.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-i", src, "-vf", f"fps={fps},scale={MAX_W}:-2",
             "-quality", q, slot_dir / "frame-%04d.webp"])
        frames = sorted(slot_dir.glob("frame-*.webp"))
        total = sum(f.stat().st_size for f in frames)
        if total <= BUDGET["scrub"]:
            kept = (f"{fps}fps/q{q}", total, len(frames)); break
    frames = sorted(slot_dir.glob("frame-*.webp"))
    total = sum(f.stat().st_size for f in frames)
    if kept:
        report_kept(name, kept[0], kept[1], BUDGET["scrub"])
    else:
        flags.append(f"{name}: scrub {total / MB:.1f}MB exceeds "
                     f"{BUDGET['scrub'] / MB:.0f}MB [{PROFILE}] - cut the source")
    w = h = None
    try:
        outp = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                               "-show_entries", "stream=width,height", "-of",
                               "csv=p=0", str(frames[0])],
                              check=True, capture_output=True, text=True).stdout
        w, h = (int(x) for x in outp.strip().split(",")[:2])
    except Exception:
        w, h = MAX_W, 0
    fps_kept = int(kept[0].split("fps")[0]) if kept else 10
    manifest = {"slot": src.stem, "frames": len(frames), "fps": fps_kept,
                "width": w, "height": h, "pattern": "frame-%04d.webp"}
    (slot_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return str((slot_dir / "manifest.json").relative_to(ROOT)).replace("\\", "/")


def update_log(slot_name, final_path):
    if not MEDIA_LOG.exists(): return
    lines = MEDIA_LOG.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) > 9 and cells[1] == slot_name:
            cells[8], cells[9] = final_path, "in-use"
            lines[i] = "| " + " | ".join(cells[1:10]) + " |"
    MEDIA_LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- main -----------------------------------------------------------------
if not LIST.exists():
    print(f"no {LIST} - run Phase 4 (/build) first"); sys.exit(1)
text = LIST.read_text(encoding="utf-8")
slots = parse_list(text)
if not slots:
    print("SHOPPING_LIST.md has no slot blocks - check its format"); sys.exit(1)

print(f"budget profile: {PROFILE} "
      f"(client.md 'Hosting plan:' - business/cloud = cdn, else no-cdn)")

names = {s["name"] for s in slots}
# recursive scan: placement folders (slots/<Page - Section>/) are
# organizational sugar - files match by exact basename anywhere under
# slots/. Same filename in two places = conflict, never guessed.
found, conflicts = {}, []
for f in SLOTS.rglob("*"):
    if not f.is_file() or f.name in ("SHOPPING_LIST.md", ".gitkeep"):
        continue
    if f.name in found:
        conflicts.append(f.name)
    else:
        found[f.name] = f
unexpected = sorted(set(found) - names)

for s in slots:
    f = found.get(s["name"])
    if s["filled"] and not FORCE:
        if f is None and s["filled"]:
            flags.append(f"{s['name']}: ticked [x] but no file found - "
                         "tick without a file does nothing")
        continue
    if f is None:
        missing.append(s["name"]); continue
    if s["name"] in conflicts:
        flags.append(f"{s['name']}: same filename in multiple folders - "
                     "remove the duplicate, then re-run"); continue
    t = treatment_of(s)
    print(f"[{s['name']}] treatment={t}")
    if t == "scroll-scrub":
        res = do_scrub(f, s["name"])
    elif t in ("loop", "intro-loop"):
        res = do_video(f, s["name"])
    else:
        res = do_image(f, s["name"])
    if res:
        processed.append(s["name"])
        update_log(s["name"], res)
        text = re.sub(rf"^(## +{re.escape(s['name'])}\s+)\[ \]", r"\1[x]",
                      text, flags=re.M)

LIST.write_text(text, encoding="utf-8")

print("\n=== INGEST REPORT ===")
for n in processed: print(f"DONE     {n}")
for n, cmd in pending: print(f"PENDING  {n} - tool missing, run locally:\n         {cmd}")
for n in missing: print(f"UNFILLED {n} - no file, not ticked")
for n in unexpected: print(f"UNKNOWN  {n} - not a slot name; rename per SHOPPING_LIST or remove")
for w in flags: print(f"FLAG     {w}")
if missing:
    print("\nAPPROVE? The unfilled slots above are Higgsfield candidates."
          "\n         Claude: present them in-chat with estimated credits and"
          "\n         wait for explicit per-slot approval (media-log rule 1)"
          "\n         before any paid generation.")
print(f"{len(processed)} processed, {len(pending)} pending, "
      f"{len(missing)} missing, {len(unexpected)} unexpected [{PROFILE} profile]")
sys.exit(0 if not pending else 2)
