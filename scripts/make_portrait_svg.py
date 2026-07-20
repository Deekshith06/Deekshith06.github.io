"""Create the one-time portrait reveal SVG used by the static website."""
from __future__ import annotations

import base64
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "deekshith-ascii-clear.png"
OUTPUT = ROOT / "assets" / "deekshith-ascii-once.svg"


def png_size(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("clear portrait is not a valid PNG")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    data = SOURCE.read_bytes()
    width, height = png_size(data)
    if (width, height) != (666, 820):
        raise ValueError(f"unexpected portrait size: {width}x{height}")
    uri = "data:image/png;base64," + base64.b64encode(data).decode("ascii")
    steps = 62
    values = ";".join(f"{height * i / steps:.2f}" for i in range(steps + 1))
    times = ";".join(f"{i / steps:.5f}" for i in range(steps + 1))
    scan = ";".join(f"{height * i / steps - 3:.2f}" for i in range(steps + 1))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">Deekshith ASCII portrait</title><desc id="desc">A clear ASCII portrait of Deekshith revealed line by line once when the page opens.</desc><defs><clipPath id="portraitReveal"><rect x="0" y="0" width="{width}" height="0"><animate attributeName="height" values="{values}" keyTimes="{times}" calcMode="discrete" begin="0.35s" dur="4.4s" fill="freeze" repeatCount="1"/></rect></clipPath><linearGradient id="scanGlow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3ee888" stop-opacity="0"/><stop offset="0.5" stop-color="#3ee888" stop-opacity="0.85"/><stop offset="1" stop-color="#3ee888" stop-opacity="0"/></linearGradient></defs><image href="{uri}" x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet" clip-path="url(#portraitReveal)"/><rect x="0" y="-3" width="{width}" height="3" fill="url(#scanGlow)" opacity="0"><animate attributeName="y" values="{scan}" keyTimes="{times}" calcMode="discrete" begin="0.35s" dur="4.4s" fill="freeze" repeatCount="1"/><animate attributeName="opacity" values="0;0.75;0.75;0" keyTimes="0;0.03;0.96;1" begin="0.35s" dur="4.4s" fill="freeze" repeatCount="1"/></rect></svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
