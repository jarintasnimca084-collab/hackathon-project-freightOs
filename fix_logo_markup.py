import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('freightos/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the duplicate brand-logo-card
old_brand_pattern = """    <div class="sidebar-brand">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
        <div class="brand-logo-card" style="flex:1;">
      <div class="brand-logo-card">"""

new_brand_pattern = """    <div class="sidebar-brand">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; margin-bottom:12px;">
        <div class="brand-logo-card" style="flex:1;">"""

if old_brand_pattern in html:
    html = html.replace(old_brand_pattern, new_brand_pattern, 1)
    print("Fixed duplicate brand-logo-card opening div!")
else:
    print("Warning: old_brand_pattern not matched directly, checking variations...")
    # Find sidebar-brand
    s_idx = html.find('<div class="sidebar-brand">')
    print(html[s_idx:s_idx+300])

with open('freightos/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved logo fix to both files.")
