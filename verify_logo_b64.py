import base64

with open('freightos/logo.png', 'rb') as f:
    raw_logo = f.read()

real_b64 = base64.b64encode(raw_logo).decode()
print("Real logo.png size:", len(raw_logo), "bytes")
print("Real logo b64 start:", real_b64[:60])
print("Real logo b64 len:", len(real_b64))

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('alt="Trans Ontario Express"')
src_start = text.rfind('src="', 0, idx)
src_val = text[src_start+5:idx].strip().strip('"')
print("index.html src starts with:", src_val[:60])
print("index.html src len:", len(src_val))

# Also check brand-assets/
import os
if os.path.exists('brand-assets'):
    print("brand-assets files:", os.listdir('brand-assets'))
