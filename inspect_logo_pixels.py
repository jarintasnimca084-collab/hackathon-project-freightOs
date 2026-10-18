# Inspect pixels of freightos/logo.png
from PIL import Image

im = Image.open('freightos/logo.png')
print("Image format:", im.format, "size:", im.size, "mode:", im.mode)

# Sample some non-transparent pixels
pixels = list(im.getdata())
non_transparent = [p for p in pixels if len(p) < 4 or p[3] > 10]
print("Total pixels:", len(pixels))
print("Non-transparent pixels:", len(non_transparent))
if non_transparent:
    print("Sample pixel RGBA:", non_transparent[:5])
    # Average color
    r = sum(p[0] for p in non_transparent) // len(non_transparent)
    g = sum(p[1] for p in non_transparent) // len(non_transparent)
    b = sum(p[2] for p in non_transparent) // len(non_transparent)
    print(f"Average color: rgb({r}, {g}, {b})")
