import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

imgs = re.findall(r'<img[^>]+>', text)
print(f"Total <img> tags: {len(imgs)}")
for i, img in enumerate(imgs):
    # print first 100 chars of each img tag
    src_match = re.search(r'src="([^"]+)"', img)
    src_val = src_match.group(1) if src_match else "no src"
    print(f"Image {i+1}: src starts with {src_val[:40]}... (total src len: {len(src_val)})")
