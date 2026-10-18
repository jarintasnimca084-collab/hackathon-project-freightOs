import sys
sys.stdout.reconfigure(encoding='utf-8')

for path in ['freightos/index.html', 'index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {path} (len: {len(text)}) ===")
    idx = text.find('brand-logo-card')
    # skip css
    idx2 = text.find('brand-logo-card', idx + 100)
    print("HTML logo section:")
    print(text[idx2-50:idx2+400])
