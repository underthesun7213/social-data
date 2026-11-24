# Crop and tone the Unsplash photos for the deck. Usage: python -I prep_photos.py RAW_DIR OUT_DIR
import sys
from PIL import Image, ImageOps, ImageEnhance
raw, out = sys.argv[1], sys.argv[2]
HALF = 6.433 / 7.5          # right-half photo on section slides
FULL = 13.333 / 7.5
# name, source id, aspect, grayscale, focus x (0-1), focus y (0-1)
JOBS = [
    ("cover", "AISimklDWqw", FULL, False, 0.5, 0.5),
    ("part1", "-YFtRc2wRYE", HALF, True, 0.5, float(sys.argv[3]) if len(sys.argv) > 3 else 0.5),
    ("part2", "MHN96iFvKIU", HALF, True, 0.5, 0.5),
    ("part3", "Yy4sN6QzboU", HALF, True, 0.5, 0.5),
    ("part4", "ZmgJiztRHXE", HALF, True, 0.5, 0.5),
    ("closing", "wWiLeqND1Ag", FULL, True, 0.5, 0.5),
]
for name, pid, asp, gray, fx, fy in JOBS:
    im = Image.open(f"{raw}/p_{pid}.jpg").convert("RGB")
    W, H = im.size
    if W / H > asp:
        w, h = int(H * asp), H
    else:
        w, h = W, int(W / asp)
    x0 = min(max(int(fx * W - w / 2), 0), W - w)
    y0 = min(max(int(fy * H - h / 2), 0), H - h)
    im = im.crop((x0, y0, x0 + w, y0 + h))
    if max(im.size) > 2000:
        im.thumbnail((2000, 2000), Image.LANCZOS)
    if gray:
        im = ImageOps.grayscale(im).convert("RGB")
        im = ImageEnhance.Contrast(im).enhance(1.08)
    im.save(f"{out}/{name}.jpg", quality=84, optimize=True, progressive=True)
    print(name, im.size)
