"""Dependency-free integrity checks for the static one-screen portfolio."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"
JS = ROOT / "assets" / "app.js"


class StrictHTMLParser(HTMLParser):
    def error(self, message: str) -> None:  # pragma: no cover - retained for older Python
        raise ValueError(message)


def fail(message: str) -> None:
    raise SystemExit(f"site validation failed: {message}")


def main() -> None:
    required = [
        INDEX,
        ROOT / "404.html",
        CSS,
        JS,
        ROOT / "assets" / "deekshith-ascii.webp",
        ROOT / "assets" / "deekshith-ascii.png",
        ROOT / "assets" / "deekshith-ascii.gif",
        ROOT / ".nojekyll",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")

    html = INDEX.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")
    StrictHTMLParser().feed(html)

    expected_text = [
        "Deekshith Seelaboyina",
        "Lovely Professional University",
        "B.Tech CSE",
        "Expected graduation · 2027",
        'role="tablist"',
        'data-panel="projects"',
        'data-panel="skills"',
        'data-panel="education"',
    ]
    for text in expected_text:
        if text not in html:
            fail(f"expected content not found: {text}")

    stale_text = ["IIIT Delhi", "Dock.us", "Turgon AI", "AccioJob"]
    for text in stale_text:
        if text in html:
            fail(f"stale identity content found: {text}")

    if "overflow: hidden" not in css or "100dvh" not in css:
        fail("the no-page-scroll viewport contract is missing")
    if "data-tab" not in js or "aria-selected" not in js:
        fail("accessible tab behavior is missing")

    local_refs = re.findall(r'(?:src|href)="(\./[^"?#]+)', html)
    unresolved = []
    for ref in local_refs:
        path = ROOT / ref.removeprefix("./")
        if not path.exists():
            unresolved.append(ref)
    if unresolved:
        fail(f"unresolved local references: {', '.join(sorted(set(unresolved)))}")

    print("site validation: OK")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f"site validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
