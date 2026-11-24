"""Trim uniform white/near-white margins from evidence screenshots.

Only removes empty border space; never touches content. Overwrites in place
only when the trim removes at least 5% of a dimension.
"""
from pathlib import Path

from PIL import Image, ImageChops

BASE = Path(__file__).resolve().parent.parent / "evidence" / "screenshots"


def trim(path: Path):
    img = Image.open(path).convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    # treat near-white as white
    mask = diff.convert("L").point(lambda p: 255 if p > 12 else 0)
    bbox = mask.getbbox()
    if not bbox:
        print(f"skip (blank?): {path.name}")
        return
    w, h = img.size
    nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if nw < w * 0.95 or nh < h * 0.95:
        img.crop(bbox).save(path)
        print(f"trimmed {path.name}: {w}x{h} -> {nw}x{nh}")
    else:
        print(f"kept {path.name}: no significant margin")


for png in sorted(BASE.rglob("*.png")):
    trim(png)
