"""Dependency-free integrity checks for the no-scroll terminal portfolio."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"
JS = ROOT / "assets" / "app.js"
PORTRAIT_SVG = ROOT / "assets" / "deekshith-ascii-once.svg"


class StrictHTMLParser(HTMLParser):
    def error(self, message: str) -> None:  # pragma: no cover
        raise ValueError(message)


def fail(message: str) -> None:
    raise SystemExit(f"site validation failed: {message}")


def main() -> None:
    required = [
        INDEX,
        ROOT / "404.html",
        CSS,
        JS,
        PORTRAIT_SVG,
        ROOT / "assets" / "deekshith-ascii-clear.png",
        ROOT / ".nojekyll",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    html = INDEX.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    svg = PORTRAIT_SVG.read_text(encoding="utf-8")
    StrictHTMLParser().feed(html)
    ET.fromstring(svg)

    expected_text = [
        "Deekshith Seelaboyina",
        "Lovely Professional University",
        "AI/ML Engineer · Full-Stack Developer",
        "I am an AI/ML Engineer and Full-Stack Developer.",
        "Using AI, I build fully working websites.",
        'data-mobile-panel="portrait"',
        'data-mobile-panel="profile"',
        "deekshith-ascii-once.svg",
    ]
    for text in expected_text:
        if text not in html:
            fail(f"expected content not found: {text}")

    for stale in ["IIIT Delhi", "Dock.us", "Turgon AI", "AccioJob", ".gif", ".webp"]:
        if stale in html:
            fail(f"stale or forbidden content found: {stale}")

    if "overflow: hidden" not in css or "100dvh" not in css:
        fail("the no-page-scroll viewport contract is missing")
    if "repeatCount=\"1\"" not in svg or "repeatCount=\"indefinite\"" in svg:
        fail("portrait reveal must run once and must not loop")
    if "data-type" not in js or "typeText" not in js:
        fail("one-time terminal typing behavior is missing")

    local_refs = re.findall(r'(?:src|href)="(\./[^"?#]+)', html)
    unresolved = []
    for ref in local_refs:
        path = ROOT / ref.removeprefix("./")
        if not path.exists():
            unresolved.append(ref)
    if unresolved:
        fail(f"unresolved local references: {', '.join(sorted(set(unresolved)))}")

    if (ROOT / "assets" / "deekshith-ascii-clear.png").stat().st_size < 100_000:
        fail("clear portrait asset is unexpectedly small")

    print("site validation: OK")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"site validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
