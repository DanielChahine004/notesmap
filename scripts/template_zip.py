"""Builds notesmap-notes.zip, the downloadable template folder, from
src/notesmap/templates: notes/main.tex, notes/notesmap.sty, notes/img/*.png.

    python scripts/template_zip.py           # rewrite it
    python scripts/template_zip.py --check   # exit 1 if it is out of date

The same zip opens as an Overleaf project (README's Start in Overleaf link).
"""
import io
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "src" / "notesmap" / "templates"
OUT = ROOT / "notesmap-notes.zip"
FILES = ["main.tex", "notesmap.sty", "img/example.png", "img/paper.png"]


def build() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            info = zipfile.ZipInfo("notes/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            data = (TEMPLATES / name).read_bytes()
            if not name.endswith(".png"):   # the same zip whatever the checkout's line endings
                data = data.replace(bytes([13, 10]), bytes([10]))
            z.writestr(info, data)
    return buf.getvalue()


if __name__ == "__main__":
    data = build()
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_bytes() != data:
            sys.exit(f"{OUT.name} is out of date: run python scripts/template_zip.py")
    else:
        OUT.write_bytes(data)
        print(f"wrote {OUT.name} ({len(data)} bytes)")
