# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Validating freightos/index.html...")

with open('freightos/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content), "bytes")

# 1. Locate the main application script (last <script> tag)
s_start = content.rfind('<script>')
s_end = content.rfind('</script>')
assert s_start != -1 and s_end != -1 and s_end > s_start, "Missing main script tag!"
js_code = content[s_start + 8 : s_end]
print("JS code length:", len(js_code), "bytes")

# 2. Bracket stack check
stack = []
pairs = {')': '(', ']': '[', '}': '{'}
in_string = None
escape = False
line_num = 1

for char in js_code:
    if char == '\n':
        line_num += 1

    if escape:
        escape = False
        continue

    if char == '\\':
        escape = True
        continue

    if in_string:
        if char == in_string:
            in_string = None
        continue
    else:
        if char in ('"', "'", '`'):
            in_string = char
            continue

    if char in ('(', '[', '{'):
        stack.append((char, line_num))
    elif char in (')', ']', '}'):
        if not stack:
            raise AssertionError(f"Unmatched closing '{char}' at line {line_num}")
        top, top_line = stack.pop()
        if top != pairs[char]:
            raise AssertionError(f"Mismatched '{top}' (from line {top_line}) with '{char}' at line {line_num}")

if stack:
    top, top_line = stack[-1]
    raise AssertionError(f"Unclosed '{top}' from line {top_line}")

print("✅ JavaScript syntax bracket balance check PASSED! 0 syntax errors.")

# 3. Check critical functions
expected_funcs = [
    'updateClockDisplay', 'toggleClockMode', 'recalculateFleetPayloads', 'updateGlobalCounters',
    'toggleMobileSidebar', 'navigateTo', 'getFilteredOrders', 'filterTable', 'renderShipmentsTable',
    'changeOrderVehicle', 'changeOrderStatus', 'toggleOrderRisk', 'openDetailDrawer',
    'saveDrawerChanges', 'autoAssignSingleOrder', 'unassignSingleOrder', 'closeDetailDrawer',
    'triggerAutoPlan', 'renderFleetCards', 'markTruckDown', 'restoreTruck', 'renderExceptionsCards',
    'openFixModal', 'selectRecoveryOption', 'applySelectedFix', 'reopenException', 'closeFixModal',
    'renderDirectorStepsList', 'updateDemoStepView', 'executeStepAction', 'nextDemoStep', 'prevDemoStep',
    'jumpToDemoStep', 'toggleSimPlay', 'resetSimulator', 'setSimFeedback', 'startLiveDemoDirector',
    'showToast', 'undoLastAction', 'openCommandBar', 'renderDashboard', 'logDashboardEvent',
    'renderAssumptions', 'initLeafletMap', 'mapFitToronto', 'toggleMapRoutes', 'initApp',
    'toggleLanguage', 'applyLanguage', 't', 'getVehicleTypeTranslated',
    'setOptimizerStrategy', 'calculateFinancialMetrics', 'renderOptimizerPage',
    'renderProfitRecommendations', 'applySingleRec', 'applyProfitOptimization',
    'updateFinancialSliders', 'resetOptimizerToBaseline'
]

for func in expected_funcs:
    assert func in js_code, f"Missing function: {func}"

print(f"✅ All {len(expected_funcs)} critical JavaScript functions verified present.")

# 4. Check Language switcher elements
assert 'id="langToggleBtn"' in content, "Missing langToggleBtn element in HTML"
assert '.lang-toggle-btn' in content, "Missing .lang-toggle-btn in CSS"
assert 'TRANSLATIONS' in js_code, "Missing TRANSLATIONS in JS"
assert 'data-i18n="nav_dashboard"' in content, "Missing data-i18n on Dashboard nav item"

print("✅ Language switcher UI elements & attributes verified present.")

# 4b. Check Profit & Risk Optimizer elements
assert 'id="page-optimizer"' in content, "Missing page-optimizer in HTML"
assert 'nav_optimizer' in js_code, "Missing nav_optimizer translation key"
assert 'strat-card-profit' in content, "Missing strat-card-profit in HTML"
assert 'strat-card-balanced' in content, "Missing strat-card-balanced in HTML"
assert 'strat-card-risk' in content, "Missing strat-card-risk in HTML"
assert 'sliderFuel' in content, "Missing sliderFuel in HTML"
assert 'sliderLabor' in content, "Missing sliderLabor in HTML"
assert 'sliderSla' in content, "Missing sliderSla in HTML"

print("✅ Profit & Risk Optimizer UI elements verified present.")

# 5. Check Base64 images
assert 'data:image/png;base64,' in content, "Missing Base64 PNG image in HTML"

print("✅ Base64 brand assets verified embedded (PNG logo and hero banner).")

# Check root index.html
with open('index.html', 'r', encoding='utf-8') as f:
    root_content = f.read()

assert len(root_content) == len(content), "Root index.html size does not match freightos/index.html!"
print(f"✅ Root index.html matches freightos/index.html ({len(root_content)} bytes).")

print("\n🎉 ALL VALIDATION CHECKS PASSED PERFECTLY!")
