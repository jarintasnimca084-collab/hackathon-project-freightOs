import base64

def to_b64(path, mime):
    with open(path, 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

logo_b64 = to_b64("freightos/logo.png", "image/png")
hero_b64 = to_b64("freightos/hero.png", "image/png")
testi_b64 = to_b64("freightos/testimonial.jpg", "image/jpeg")

with open("freightos/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace src="logo.png", src="hero.png", src="testimonial.jpg"
html = html.replace('src="logo.png"', f'src="{logo_b64}"')
html = html.replace('src="hero.png"', f'src="{hero_b64}"')
html = html.replace('src="testimonial.jpg"', f'src="{testi_b64}"')

with open("freightos/index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully inlined all images as Base64 into freightos/index.html and root index.html!")
print("New file size:", len(html))
