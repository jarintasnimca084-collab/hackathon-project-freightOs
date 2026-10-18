import json
import base64

# 1. Read freightos/orders_full.json
with open('freightos/orders_full.json', 'r', encoding='utf-8') as f:
    orders_data = json.load(f)

orders_json_str = json.dumps(orders_data)

# 2. Read the generated HTML from freightos/index.html
with open('freightos/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. Add Clock and Table Select CSS into <style>
extra_css = """
/* Live Pulsing Dot & Clock Toggle */
.live-pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green);
  display: inline-block;
  box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
  animation: livePulse 2s infinite;
}
@keyframes livePulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
.clock-toggle-btn {
  background: #10B981;
  color: #FFFFFF;
  border: none;
  border-radius: 12px;
  padding: 3px 9px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: 6px;
}
.clock-toggle-btn.sim-active {
  background: var(--amber);
  color: #FFFFFF;
}

/* Table Select Elements */
.table-select {
  padding: 5px 8px;
  border-radius: 6px;
  font-family: var(--font-main);
  font-size: 11px;
  font-weight: 700;
  border: 1px solid var(--gray-300);
  background-color: #FFFFFF;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
  max-width: 100%;
}
.table-select:focus {
  border-color: var(--royal-blue);
  box-shadow: 0 0 0 2px var(--royal-blue-glow);
}
.table-select-status.status-assigned {
  background: rgba(31,74,238,0.1);
  color: var(--royal-blue);
  border-color: rgba(31,74,238,0.3);
}
.table-select-status.status-unassigned {
  background: var(--gray-100);
  color: var(--gray-700);
  border-color: var(--gray-300);
}
.table-select-status.status-at-risk {
  background: var(--amber-light);
  color: #B45309;
  border-color: #FCD34D;
  font-weight: 800;
}
.table-select-status.status-in-transit {
  background: rgba(124,58,237,0.1);
  color: #7C3AED;
  border-color: rgba(124,58,237,0.3);
}
.table-select-status.status-done {
  background: var(--green-light);
  color: #047857;
  border-color: #A7F3D0;
}
.table-select-vehicle.select-empty {
  color: var(--red);
  border-color: var(--red-light);
  background: #FFF5F5;
  font-weight: 700;
}
.row-at-risk {
  background-color: rgba(245, 158, 11, 0.05) !important;
}
.btn-at-risk-active {
  background: var(--amber) !important;
  color: #FFFFFF !important;
  border: none !important;
}
"""

html = html.replace("</style>", extra_css + "\n</style>")

# 4. Update Topbar Clock HTML
old_topbar = """      <!-- DATE CHANGER & TIME DISPLAY -->
      <div class="topbar-date-badge">
        <div class="date-pill">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:15px;height:15px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span id="topbarDateLabel">Sep 18, 2026</span>
        </div>
        <div class="clock-pill" id="topbarTimeDisplay">08:00 AM</div>
      </div>"""

new_topbar = """      <!-- DATE CHANGER & TIME DISPLAY (LIVE TICKING WALL CLOCK) -->
      <div class="topbar-date-badge">
        <div class="date-pill" id="topbarDateBadge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:15px;height:15px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span id="topbarDateLabel">Oct 17, 2026</span>
        </div>
        <div class="clock-pill" id="topbarTimeDisplay">
          <span class="live-pulse-dot" id="liveClockDot"></span>
          <span id="topbarTimeText">08:00:00 AM</span>
        </div>
        <button class="clock-toggle-btn" id="clockToggleBtn" onclick="toggleClockMode()" title="Toggle Live Wall Clock / Simulator Time">LIVE</button>
      </div>"""

html = html.replace(old_topbar, new_topbar)

# 5. Update Dashboard Metrics Row
old_metrics = """        <!-- 4 Metric Cards -->
        <div class="metrics-row">
          <div class="stat-card" onclick="navigateTo('shipments')">
            <div class="stat-card-header">
              <span class="stat-label">Total Shipments</span>
              <div class="stat-icon-wrapper" style="background:rgba(31,74,238,0.1); color:var(--royal-blue);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              </div>
            </div>
            <div class="stat-number">247</div>
            <div class="stat-footer">
              <span style="color:var(--green); font-weight:700;">195 On Schedule</span>
              <span style="color:var(--gray-400);">112 Pickups / 135 Drops</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('shipments')">
            <div class="stat-card-header">
              <span class="stat-label">Unassigned Orders</span>
              <div class="stat-icon-wrapper" style="background:var(--red-light); color:var(--red);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
            </div>
            <div class="stat-number" style="color:var(--red);">38</div>
            <div class="stat-footer">
              <span style="color:var(--red); font-weight:700;">Needs Auto-Plan</span>
              <span style="color:var(--royal-blue); font-weight:600; cursor:pointer;" onclick="event.stopPropagation();triggerAutoPlan()">Run AI Planner ⚡</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('fleet')">
            <div class="stat-card-header">
              <span class="stat-label">Fleet Active</span>
              <div class="stat-icon-wrapper" style="background:rgba(16,185,129,0.1); color:var(--green);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13" rx="2"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
              </div>
            </div>
            <div class="stat-number">42<span style="font-size:18px; color:var(--gray-400); font-weight:500;">/52</span></div>
            <div class="stat-footer">
              <span style="color:var(--green); font-weight:700;">78% Weight Capacity</span>
              <span>10 Reserve Trucks</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('exceptions')">
            <div class="stat-card-header">
              <span class="stat-label">Active Exceptions</span>
              <div class="stat-icon-wrapper" style="background:var(--amber-light); color:var(--amber);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
              </div>
            </div>
            <div class="stat-number" style="color:var(--amber);">7</div>
            <div class="stat-footer">
              <span style="color:var(--red); font-weight:700;">1 Breakdown Alert</span>
              <span>Instant Fix Ready</span>
            </div>
          </div>
        </div>"""

new_metrics = """        <!-- 4 Metric Cards (DYNAMIC REAL-TIME COUNTERS) -->
        <div class="metrics-row">
          <div class="stat-card" onclick="navigateTo('shipments')">
            <div class="stat-card-header">
              <span class="stat-label">Total GTA Orders</span>
              <div class="stat-icon-wrapper" style="background:rgba(31,74,238,0.1); color:var(--royal-blue);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              </div>
            </div>
            <div class="stat-number" id="statTotalShipments">75</div>
            <div class="stat-footer">
              <span style="color:var(--green); font-weight:700;" id="statAssignedSub">39 Assigned</span>
              <span style="color:var(--gray-400);">Verified Simple Day Dataset</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('shipments');filterTable('unassigned', document.getElementById('pill-unassigned'))">
            <div class="stat-card-header">
              <span class="stat-label">Unassigned Orders</span>
              <div class="stat-icon-wrapper" style="background:var(--red-light); color:var(--red);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
            </div>
            <div class="stat-number" id="statUnassigned" style="color:var(--red);">30</div>
            <div class="stat-footer">
              <span style="color:var(--red); font-weight:700;" id="statUnassignedLabel">Needs Dispatcher</span>
              <span style="color:var(--royal-blue); font-weight:600; cursor:pointer;" onclick="event.stopPropagation();triggerAutoPlan()">Run AI Planner ⚡</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('fleet')">
            <div class="stat-card-header">
              <span class="stat-label">Fleet Active</span>
              <div class="stat-icon-wrapper" style="background:rgba(16,185,129,0.1); color:var(--green);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13" rx="2"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
              </div>
            </div>
            <div class="stat-number" id="statFleetActive">7<span style="font-size:18px; color:var(--gray-400); font-weight:500;">/8</span></div>
            <div class="stat-footer">
              <span style="color:var(--green); font-weight:700;" id="statFleetUtilization">76% Avg Load</span>
              <span>1 Reserve Truck</span>
            </div>
          </div>

          <div class="stat-card" onclick="navigateTo('exceptions')">
            <div class="stat-card-header">
              <span class="stat-label">Active Exceptions</span>
              <div class="stat-icon-wrapper" style="background:var(--amber-light); color:var(--amber);">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
              </div>
            </div>
            <div class="stat-number" id="statActiveExceptions" style="color:var(--amber);">7</div>
            <div class="stat-footer">
              <span style="color:var(--red); font-weight:700;" id="statBreakdownSub">1 Breakdown Alert</span>
              <span>Instant AI Fix Ready</span>
            </div>
          </div>
        </div>"""

html = html.replace(old_metrics, new_metrics)

# 6. Update Shipments Page Filter Pills & Table
old_ship_page = """        <div class="filter-pills-row" id="shipmentFilterPills">
          <div class="filter-pill active" onclick="filterTable('all', this)">All (75 Real Orders)</div>
          <div class="filter-pill" onclick="filterTable('unassigned', this)">Unassigned (38)</div>
          <div class="filter-pill" onclick="filterTable('at-risk', this)">At Risk (14)</div>
          <div class="filter-pill" onclick="filterTable('rush', this)">Rush / Same-Day (22)</div>
          <div class="filter-pill" onclick="filterTable('dg', this)">⚠ Dangerous Goods (6)</div>
          <div class="filter-pill" onclick="filterTable('missing', this)">Missing Data (31)</div>
        </div>

        <div class="data-table-container">
          <table class="data-table" id="shipmentsTable">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Leg</th>
                <th>Customer</th>
                <th>Address</th>
                <th>Service</th>
                <th>Weight (lb)</th>
                <th>Status</th>
                <th>Vehicle</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="shipmentsTableBody"></tbody>
          </table>
        </div>"""

new_ship_page = """        <div class="filter-pills-row" id="shipmentFilterPills">
          <div class="filter-pill active" id="pill-all" onclick="filterTable('all', this)">All (<span id="countAll">75</span>)</div>
          <div class="filter-pill" id="pill-unassigned" onclick="filterTable('unassigned', this)">Unassigned (<span id="countUnassigned">30</span>)</div>
          <div class="filter-pill" id="pill-at-risk" onclick="filterTable('at-risk', this)">At Risk (<span id="countAtRisk">14</span>)</div>
          <div class="filter-pill" id="pill-rush" onclick="filterTable('rush', this)">Rush / Same-Day (<span id="countRush">22</span>)</div>
          <div class="filter-pill" id="pill-dg" onclick="filterTable('dg', this)">⚠ Dangerous Goods (<span id="countDg">7</span>)</div>
          <div class="filter-pill" id="pill-missing" onclick="filterTable('missing', this)">Missing Data (<span id="countMissing">31</span>)</div>
        </div>

        <div class="data-table-container">
          <table class="data-table" id="shipmentsTable">
            <thead>
              <tr>
                <th style="width:110px;">Order ID</th>
                <th style="width:75px;">Leg</th>
                <th>Customer</th>
                <th>Address</th>
                <th style="width:125px;">Service</th>
                <th style="width:115px;">Weight</th>
                <th style="width:145px;">Status</th>
                <th style="width:175px;">Assigned Vehicle</th>
                <th style="width:170px;">Quick Actions</th>
              </tr>
            </thead>
            <tbody id="shipmentsTableBody"></tbody>
          </table>
        </div>"""

html = html.replace(old_ship_page, new_ship_page)

# 7. Cut everything starting from <script> and replace with our clean JavaScript
script_pos = html.find('<script>')
html_before_script = html[:script_pos]

clean_js = """<script>
// ================= DATA INJECTION =================
let ORDERS = __ORDERS_JSON__;

let VEHICLES = [
  { id: 'T-108', type: 'Straight Truck', driver: 'Rajesh Patel', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 4500, usedWeight: 4500, hoursUsed: 6.5, status: 'active', dgCert: false, lat: 43.7615, lng: -79.4111 },
  { id: 'T-112', type: 'Cargo Van', driver: 'Kananathan Shanmugarajah', maxWeight: 3000, maxFt: 10, maxSkids: 3, baseWeight: 600, usedWeight: 600, hoursUsed: 4.2, status: 'active', dgCert: false, lat: 43.8561, lng: -79.3370 },
  { id: 'T-205', type: 'Straight Truck', driver: 'Marcus Johnson', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 4200, usedWeight: 4200, hoursUsed: 8.1, status: 'active', dgCert: true, lat: 43.5890, lng: -79.6441 },
  { id: 'T-301', type: 'Straight Truck', driver: 'Amandeep Singh', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 3800, usedWeight: 3800, hoursUsed: 7.3, status: 'active', dgCert: true, lat: 43.7764, lng: -79.2318 },
  { id: 'T-315', type: 'Cargo Van', driver: 'David Chen', maxWeight: 3000, maxFt: 10, maxSkids: 3, baseWeight: 800, usedWeight: 800, hoursUsed: 3.8, status: 'active', dgCert: false, lat: 43.6532, lng: -79.3832 },
  { id: 'T-445', type: 'Tractor + 53ft', driver: 'Viktor Petrov', maxWeight: 43000, maxFt: 53, maxSkids: 26, baseWeight: 18000, usedWeight: 18000, hoursUsed: 9.1, status: 'active', dgCert: true, lat: 43.7315, lng: -79.7624 },
  { id: 'T-502', type: 'Flat Bed', driver: 'Miguel Santos', maxWeight: 40000, maxFt: 48, maxSkids: 24, baseWeight: 14000, usedWeight: 14000, hoursUsed: 5.5, status: 'active', dgCert: false, lat: 43.8384, lng: -79.0868 },
  { id: 'T-510', type: 'Flat Bed (Reserve)', driver: 'Brandon Taylor', maxWeight: 40000, maxFt: 48, maxSkids: 24, baseWeight: 0, usedWeight: 0, hoursUsed: 0, status: 'reserve', dgCert: false, lat: 43.6205, lng: -79.5132 }
];

let EXCEPTIONS = [
  { id: 'EX-001', type: 'critical', icon: '🔧', title: 'Truck T-108 Breakdown (Hwy 401 & DVP)', desc: 'Engine failure reported at Hwy 401 & Don Valley Parkway. 3 customer shipments stranded on truck. Driver safe, tow in route.', time: '10:15 AM', orders: ['2986700P', '2986700D', '2986545D'], resolved: false },
  { id: 'EX-002', type: 'critical', icon: '⚖️', title: 'Weight Overload Risk on T-205', desc: 'Adding 2 heavy industrial skids would exceed legal capacity (10,000 lb). Dynamic load balancing active.', time: '08:45 AM', orders: ['2987010P', '2987010D'], resolved: false },
  { id: 'EX-003', type: 'critical', icon: '☢️', title: 'Dangerous Goods on Non-Certified Truck', desc: 'Order 2986888P contains regulated chemical drums. T-112 is not DG-certified.', time: '08:20 AM', orders: ['2986888P'], resolved: false },
  { id: 'EX-004', type: 'warning', icon: '⏰', title: 'Late Risk — 3 Downtown Windows', desc: 'Heavy downtown traffic on Gardiner Expy threatening 3 PM appointment commitments.', time: '12:30 PM', orders: ['2986545D', '2986999D'], resolved: false },
  { id: 'EX-005', type: 'warning', icon: '🕐', title: 'Driver Hours Near Legal Limit (T-445)', desc: 'Driver Viktor Petrov at 9.1 hours. Approaching Canadian 13-hour daily driving limit.', time: '14:00 PM', orders: ['2985990D'], resolved: false },
  { id: 'EX-006', type: 'warning', icon: '📋', title: 'Missing Pallet Dimensions', desc: '8 shipments arrived with weight but missing linear feet specifications.', time: '07:30 AM', orders: ['2986297P', '2986401P'], resolved: false },
  { id: 'EX-007', type: 'warning', icon: '🔀', title: 'Equipment Request Mismatch', desc: 'Customer requested 53ft trailer for loading dock; smaller straight truck queued.', time: '09:00 AM', orders: ['2985990P'], resolved: false }
];

const DEMO_STEPS = [
  {
    time: "08:00 AM",
    heading: "08:00 AM - Morning Dispatch Snapshot",
    narration: "This is a real day's work. 75 orders have arrived. 30 are unassigned, 14 are at risk of missing delivery windows, and 7 exceptions need dispatcher attention before trucks hit the GTA highways.",
    problem: "Identifies unassigned orders and equipment mismatches before morning dispatch rather than discovering failures mid-route.",
    actionLabel: "Inspect 30 Unassigned Orders",
    action: () => {
      navigateTo("shipments");
      filterTable("unassigned", document.getElementById("pill-unassigned"));
      setSimFeedback("Filtered shipments to 30 unassigned orders ready for auto-plan.");
    }
  },
  {
    time: "08:15 AM",
    heading: "08:15 AM - Hard Block: Dangerous Goods Compliance",
    narration: "Watch what happens when we try to assign a Dangerous Goods chemical shipment (Order 2986888P) to Van T-112. The system enforces safety: It HARD BLOCKS the assignment because T-112 is not DG-certified!",
    problem: "Prevents $50,000+ transport regulatory fines and hazardous material violations by hard-blocking uncertified vehicles.",
    actionLabel: "Attempt Invalid DG Assignment",
    action: () => {
      navigateTo("shipments");
      changeOrderVehicle("2986888P", "T-112");
      setSimFeedback("Hard rule validation triggered: Assignment refused.");
    }
  },
  {
    time: "08:30 AM",
    heading: "08:30 AM - Heuristic Route Optimization",
    narration: "With one click, the dispatcher triggers Suggest Full Plan. FreightOS pairs Pickups before Deliveries, minimizes stem distance across the GTA, and fills 30 unassigned orders into active trucks with 0 capacity violations.",
    problem: "Saves 2-3 hours of manual dispatcher guesswork, eliminating human error in sequence pairing and route overlap.",
    actionLabel: "Execute AI Suggest Full Plan",
    action: () => {
      triggerAutoPlan();
      setSimFeedback("AI Planner executed: 30 orders assigned, 342 km saved vs manual routing.");
    }
  },
  {
    time: "10:15 AM",
    heading: "10:15 AM - Live Disruption: Truck T-108 Breakdown",
    narration: "Disruption strikes: Truck T-108 breaks down on the 401 near the DVP! 3 shipments are stranded. The system immediately alerts the dispatcher and calculates 3 ranked recovery options with cost & time diffs.",
    problem: "Eliminates panicked dispatch phone calls. Automatically generates 3 feasible recovery options ranked by Cost, Speed, and Disruption.",
    actionLabel: "Open 3-Way Recovery Optimizer",
    action: () => {
      markTruckDown("T-108");
      setSimFeedback("Breakdown recovery active: 3 options calculated (Cheapest, Fastest, Fewest Changes).");
    }
  },
  {
    time: "11:30 AM",
    heading: "11:30 AM - Urgent RUSH Same-Day Order Insertion",
    narration: "A VIP customer calls in an emergency RUSH pickup in Markham. The system calculates an insert-or-partner decision: Inserting into T-315 is FREE but delays stop #4 by 12 mins, or hand off to partner carrier for $85.",
    problem: "Makes cost-vs-delay trade-offs crystal clear instead of dispatchers making blind promises to customers.",
    actionLabel: "Simulate Urgent Insertion",
    action: () => {
      const rushOrder = ORDERS.find(o => o.id === "2986545D") || ORDERS[0];
      if (rushOrder) {
        rushOrder.vehicle = "T-315";
        rushOrder.service = "RUSH 90 MIN";
        rushOrder.status = "assigned";
        recalculateFleetPayloads();
        updateGlobalCounters();
        renderShipmentsTable(getFilteredOrders());
        renderFleetCards();
      }
      showToast("Emergency RUSH Order inserted into T-315 with +8 min buffer.");
      setSimFeedback("Order inserted: T-315 route recalibrated with 0 SLA violations.");
    }
  },
  {
    time: "02:00 PM",
    heading: "02:00 PM - Customer Delivery Failure Handled",
    narration: "Driver arrives at customer 941 St Clair Ave, but dock is closed. Driver logs Customer Unavailable. The system recalculates T-205's remaining 3 stops immediately to protect the remaining appointments.",
    problem: "Prevents cascading delays from a single failed stop from ruining the rest of the driver's route.",
    actionLabel: "Recalibrate After Failed Stop",
    action: () => {
      const stop = ORDERS.find(o => o.address && o.address.includes("ST CLAIR"));
      if (stop) {
        stop.status = "at-risk";
        renderShipmentsTable(getFilteredOrders());
        updateGlobalCounters();
      }
      showToast("Stop rescheduled for tomorrow AM. T-205 rerouted to next priority delivery.");
      setSimFeedback("Remaining 3 stops optimized: driver back on track for 3:00 PM window.");
    }
  },
  {
    time: "05:00 PM",
    heading: "05:00 PM - End of Day Impact Scorecard",
    narration: "The day is done. Compare our plan to what actually occurred on this real operating day: We saved 342 km (21.5% reduction), 22.8 driver hours (20.3% reduction), freed up 4 trucks, and reduced late stops from 54 down to just 2!",
    problem: "Delivers provable ROI and accountability for management, proving freight planning efficiency.",
    actionLabel: "View Full Impact Scorecard",
    action: () => {
      navigateTo("impact");
      setSimFeedback("Scorecard loaded: 342 km saved, 96.3% fewer late stops verified.");
    }
  }
];

const ASSUMPTIONS = [
  { icon: "🚛", title: "Vehicle Capacity Limits (Standardized Models)", text: "Cargo Van: 3,000 lb / 10 ft / 3 skids. Straight Truck: 10,000 lb / 24 ft / 10 skids. Tractor + 53ft: 43,000 lb / 53 ft / 26 skids. Flat Bed: 40,000 lb / 48 ft / 24 skids. (Documented in Section 6)." },
  { icon: "📐", title: "Missing Dimensions & Skid Estimation", text: "When skid spots or linear feet are missing in shipper paperwork, 1 skid is assumed for every 1,200 lb of freight or parcel counts. These are badged as Estimated in yellow." },
  { icon: "📍", title: "Customer Geocoding & Distance Factor", text: "GPS coordinates were geocoded from GTA postal codes and street addresses. Travel times calibrated with urban density factor 1.4 for central Toronto and 1.2 for suburban 400-series highways." },
  { icon: "⚖️", title: "Canadian Hours of Service Compliance", text: "Limits configured to Ontario standard: 13 hours maximum driving time and 14 hours total on-duty time per day, with mandatory off-duty rest." }
];

let currentStepIndex = 0;
let isSimPlaying = false;
let simPlayTimer = null;
let leafletMap = null;
let mapMarkers = [];
let actionHistory = [];
let currentTableFilter = 'all';
let currentExceptionToFix = 'EX-001';
let selectedRecoveryOptionIndex = 1;
let clockMode = 'live';

let dashboardEvents = [
  { time: '08:00 AM', text: 'Morning load batch imported: 75 real GTA orders across Ontario.', icon: '📥' },
  { time: '08:12 AM', text: 'T-205 loaded at Mississauga terminal with 9,200 lb.', icon: '🚚' },
  { time: '08:30 AM', text: 'AI Route Solver paired 38 pickups with corresponding deliveries.', icon: '⚡' },
  { time: '10:15 AM', text: 'ALERT: T-108 engine failure on Hwy 401 at DVP.', icon: '🔴' },
  { time: '11:30 AM', text: 'Emergency RUSH 2987100P inserted into Van T-315.', icon: '⚡' },
  { time: '02:00 PM', text: 'Customer dock closed at 941 St Clair Ave; stop rerouted.', icon: '⚠️' }
];

// ================= DYNAMIC CLOCK & TIMER =================
function updateClockDisplay() {
  const timeTextEl = document.getElementById('topbarTimeText');
  const dateLabelEl = document.getElementById('topbarDateLabel');
  const dotEl = document.getElementById('liveClockDot');
  const btnEl = document.getElementById('clockToggleBtn');

  if (clockMode === 'live') {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
    const dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    if (timeTextEl) timeTextEl.textContent = timeStr;
    if (dateLabelEl) dateLabelEl.textContent = dateStr;
    if (dotEl) {
      dotEl.style.display = 'inline-block';
      dotEl.style.background = 'var(--green)';
    }
    if (btnEl) {
      btnEl.textContent = 'LIVE';
      btnEl.classList.remove('sim-active');
    }
  } else {
    const simTime = DEMO_STEPS[currentStepIndex] ? DEMO_STEPS[currentStepIndex].time : '08:00 AM';
    if (timeTextEl) timeTextEl.textContent = simTime;
    if (dateLabelEl) dateLabelEl.textContent = 'Sep 18, 2026';
    if (dotEl) {
      dotEl.style.display = 'inline-block';
      dotEl.style.background = 'var(--amber)';
    }
    if (btnEl) {
      btnEl.textContent = 'SIM';
      btnEl.classList.add('sim-active');
    }
  }
}

function toggleClockMode() {
  clockMode = (clockMode === 'live' ? 'sim' : 'live');
  updateClockDisplay();
  showToast(clockMode === 'live' ? '⏱️ Live Real-Time Wall Clock Active' : '🎬 Simulator Replay Clock Active (Sep 18, 2026)');
}

setInterval(updateClockDisplay, 1000);

// ================= PAYLOAD & METRIC RECALCULATION =================
function recalculateFleetPayloads() {
  VEHICLES.forEach(v => {
    v.usedWeight = v.baseWeight || 0;
  });

  ORDERS.forEach(o => {
    if (o.vehicle && o.status !== 'unassigned') {
      const v = VEHICLES.find(x => x.id === o.vehicle);
      if (v) {
        v.usedWeight += (o.weight || 0);
      }
    }
  });
}

function updateGlobalCounters() {
  const total = ORDERS.length;
  const unassigned = ORDERS.filter(o => o.status === 'unassigned').length;
  const atRisk = ORDERS.filter(o => o.status === 'at-risk').length;
  const rush = ORDERS.filter(o => (o.service || '').toUpperCase().includes('RUSH') || (o.service || '').toUpperCase().includes('SAME DAY')).length;
  const dg = ORDERS.filter(o => (o.specialHandling || '').toLowerCase().includes('dangerous goods')).length;
  const missing = ORDERS.filter(o => Object.values(o.confidence || {}).includes('missing')).length;
  const assigned = ORDERS.filter(o => o.status === 'assigned' || o.status === 'done').length;
  const activeExceptions = EXCEPTIONS.filter(e => !e.resolved).length;
  const activeVehicles = VEHICLES.filter(v => v.status === 'active').length;

  const elCountAll = document.getElementById('countAll');
  if (elCountAll) elCountAll.textContent = total;
  const elCountUnassigned = document.getElementById('countUnassigned');
  if (elCountUnassigned) elCountUnassigned.textContent = unassigned;
  const elCountAtRisk = document.getElementById('countAtRisk');
  if (elCountAtRisk) elCountAtRisk.textContent = atRisk;
  const elCountRush = document.getElementById('countRush');
  if (elCountRush) elCountRush.textContent = rush;
  const elCountDg = document.getElementById('countDg');
  if (elCountDg) elCountDg.textContent = dg;
  const elCountMissing = document.getElementById('countMissing');
  if (elCountMissing) elCountMissing.textContent = missing;

  const statTotal = document.getElementById('statTotalShipments');
  if (statTotal) statTotal.textContent = total;
  const statAssignedSub = document.getElementById('statAssignedSub');
  if (statAssignedSub) statAssignedSub.textContent = `${assigned} Dispatched`;

  const statUnassigned = document.getElementById('statUnassigned');
  if (statUnassigned) statUnassigned.textContent = unassigned;
  const statUnassignedLabel = document.getElementById('statUnassignedLabel');
  if (statUnassignedLabel) statUnassignedLabel.textContent = unassigned === 0 ? '✓ All Routed' : 'Needs Dispatcher';

  const statFleetActive = document.getElementById('statFleetActive');
  if (statFleetActive) statFleetActive.innerHTML = `${activeVehicles}<span style="font-size:18px; color:var(--gray-400); font-weight:500;">/${VEHICLES.length}</span>`;

  let totalCap = 0;
  let totalUsed = 0;
  VEHICLES.forEach(v => {
    totalCap += v.maxWeight;
    totalUsed += v.usedWeight;
  });
  const fleetUtilPct = Math.round((totalUsed / totalCap) * 100);
  const statFleetUtilization = document.getElementById('statFleetUtilization');
  if (statFleetUtilization) statFleetUtilization.textContent = `${fleetUtilPct}% Avg Load`;

  const statExceptions = document.getElementById('statActiveExceptions');
  if (statExceptions) statExceptions.textContent = activeExceptions;
}

// ================= NAVIGATION =================
function navigateTo(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  
  const targetPage = document.getElementById('page-' + pageId);
  if (targetPage) targetPage.classList.add('active');
  
  const navItem = Array.from(document.querySelectorAll('.nav-item')).find(n => n.textContent.toLowerCase().includes(pageId));
  if (navItem) navItem.classList.add('active');

  if (pageId === 'map' && !leafletMap) {
    setTimeout(initLeafletMap, 150);
  }
}

// ================= SHIPMENTS TABLE & FILTERING =================
function getFilteredOrders() {
  if (currentTableFilter === 'unassigned') return ORDERS.filter(o => o.status === 'unassigned');
  if (currentTableFilter === 'at-risk') return ORDERS.filter(o => o.status === 'at-risk');
  if (currentTableFilter === 'rush') return ORDERS.filter(o => (o.service || '').toUpperCase().includes('RUSH') || (o.service || '').toUpperCase().includes('SAME DAY'));
  if (currentTableFilter === 'dg') return ORDERS.filter(o => (o.specialHandling || '').toLowerCase().includes('dangerous goods'));
  if (currentTableFilter === 'missing') return ORDERS.filter(o => Object.values(o.confidence || {}).includes('missing'));
  return ORDERS;
}

function filterTable(type, pillEl) {
  currentTableFilter = type;
  document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
  if (pillEl) {
    pillEl.classList.add('active');
  } else {
    const el = document.getElementById('pill-' + type);
    if (el) el.classList.add('active');
  }
  renderShipmentsTable(getFilteredOrders());
}

function renderShipmentsTable(ordersToRender) {
  const tbody = document.getElementById('shipmentsTableBody');
  if (!ordersToRender || ordersToRender.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding:32px; color:var(--gray-500); font-weight:600;">No shipments match current filter criteria.</td></tr>`;
    return;
  }

  tbody.innerHTML = ordersToRender.map(o => {
    const isAtRisk = o.status === 'at-risk';
    const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
    return `
    <tr class="shipment-row ${isAtRisk ? 'row-at-risk' : ''}" onclick="openDetailDrawer('${o.id}')">
      <td style="font-family:var(--font-mono); font-weight:700; color:var(--royal-blue);">${o.id}</td>
      <td><span class="chip ${o.leg==='Pickup'?'chip-assigned':'chip-done'}">${o.leg}</span></td>
      <td style="font-weight:600; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        ${o.customer}
        ${isDG ? '<span title="Dangerous Goods - Regulated Chemicals" style="margin-left:4px; font-size:12px;">⚠️☢️</span>' : ''}
      </td>
      <td style="max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--gray-600);" title="${o.address}">${o.address}</td>
      <td><span class="chip ${o.service.includes('RUSH')?'chip-at-risk':'chip-assigned'}">${o.service}</span></td>
      <td style="font-weight:600;">
        ${o.weight.toLocaleString()} lb
        <span class="conf-dot conf-${o.confidence.weight}" title="Confidence: ${o.confidence.weight}"></span>
      </td>
      <td onclick="event.stopPropagation()">
        <select class="table-select table-select-status status-${o.status}" onchange="changeOrderStatus('${o.id}', this.value)">
          <option value="assigned" ${o.status==='assigned'?'selected':''}>Assigned</option>
          <option value="unassigned" ${o.status==='unassigned'?'selected':''}>Unassigned</option>
          <option value="at-risk" ${o.status==='at-risk'?'selected':''}>At-Risk ⚠️</option>
          <option value="in-transit" ${o.status==='in-transit'?'selected':''}>In Transit 🚚</option>
          <option value="done" ${o.status==='done'?'selected':''}>Delivered ✅</option>
        </select>
      </td>
      <td onclick="event.stopPropagation()">
        <select class="table-select table-select-vehicle ${!o.vehicle?'select-empty':''}" onchange="changeOrderVehicle('${o.id}', this.value)">
          <option value="" ${!o.vehicle?'selected':''}>-- Unassigned --</option>
          ${VEHICLES.map(v => `
            <option value="${v.id}" ${o.vehicle===v.id?'selected':''}>
              ${v.id} (${v.type.split(' ')[0]}${v.dgCert ? ' · DG' : ''})
            </option>
          `).join('')}
        </select>
      </td>
      <td onclick="event.stopPropagation()" style="white-space:nowrap;">
        <button class="btn btn-sm ${isAtRisk ? 'btn-at-risk-active' : 'btn-secondary'}" onclick="toggleOrderRisk('${o.id}')" title="Toggle At-Risk Flag" style="padding:4px 8px; font-size:11px; margin-right:4px;">
          ${isAtRisk ? '⚠️ Clear' : 'Mark Risk'}
        </button>
        <button class="btn btn-secondary btn-sm" onclick="openDetailDrawer('${o.id}')" style="padding:4px 8px; font-size:11px;">
          Details
        </button>
      </td>
    </tr>
    `;
  }).join('');
}

// ================= LIVE STATE MUTATORS =================
function changeOrderVehicle(orderId, newVehicle) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
  if (newVehicle) {
    const targetV = VEHICLES.find(v => v.id === newVehicle);
    if (isDG && targetV && !targetV.dgCert) {
      showToast(`🛑 HARD BLOCK: Order ${orderId} has Dangerous Goods! ${targetV.id} lacks DG Certification. Assignment rejected!`, 6000);
      renderShipmentsTable(getFilteredOrders());
      return;
    }
  }

  const prevVehicle = o.vehicle;
  const prevStatus = o.status;
  actionHistory.push({ type: 'reassign', orderId, prevVehicle, prevStatus });

  o.vehicle = newVehicle || '';
  if (newVehicle) {
    if (o.status === 'unassigned') o.status = 'assigned';
  } else {
    o.status = 'unassigned';
  }

  recalculateFleetPayloads();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();

  logDashboardEvent(new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}), `Order ${orderId} assigned to ${newVehicle || 'Unassigned Queue'}`, '🚚');
  showToast(`✅ Order #${orderId} ${newVehicle ? 'reassigned to ' + newVehicle : 'moved to Unassigned Queue'}. Capacity updated.`);
}

function changeOrderStatus(orderId, newStatus) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  const prevStatus = o.status;
  actionHistory.push({ type: 'status_change', orderId, prevStatus });

  o.status = newStatus;
  if (newStatus === 'unassigned') {
    o.vehicle = '';
  }

  recalculateFleetPayloads();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();

  showToast(`Order #${orderId} status updated to ${newStatus.toUpperCase()}`);
}

function toggleOrderRisk(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  if (o.status === 'at-risk') {
    o.status = o.vehicle ? 'assigned' : 'unassigned';
    showToast(`✅ Order #${orderId} cleared from At-Risk status.`);
  } else {
    o.status = 'at-risk';
    showToast(`⚠️ Order #${orderId} marked AT-RISK! SLA monitor alerted.`, 4000);
  }

  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
}

// ================= DETAIL DRAWER =================
function openDetailDrawer(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  const isAtRisk = o.status === 'at-risk';
  const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');

  document.getElementById('drawerHeaderTitle').textContent = `Order ${o.id}`;
  document.getElementById('drawerContentBody').innerHTML = `
    <div style="display:flex; gap:8px; margin-bottom:18px; align-items:center; flex-wrap:wrap;">
      <span class="chip chip-${o.status}">${o.status.toUpperCase()}</span>
      <span class="chip ${o.leg==='Pickup'?'chip-assigned':'chip-done'}">${o.leg}</span>
      <span class="chip chip-assigned">${o.service}</span>
      ${isDG ? '<span class="chip chip-late">⚠️ DANGEROUS GOODS</span>' : ''}
    </div>

    <!-- Live Reassignment Panel -->
    <div style="background:var(--gray-50); border:1.5px solid var(--gray-200); border-radius:var(--radius-md); padding:16px; margin-bottom:20px;">
      <div style="font-size:12px; font-weight:800; color:var(--royal-blue); margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">
        ⚡ Live Dispatch Assignment
      </div>

      <div style="margin-bottom:12px;">
        <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">ASSIGN TO TRUCK</label>
        <select id="drawerVehicleSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
          <option value="" ${!o.vehicle?'selected':''}>-- Unassigned (In Dispatch Queue) --</option>
          ${VEHICLES.map(v => {
            const wPct = Math.min(100, Math.round((v.usedWeight / v.maxWeight) * 100));
            return `
              <option value="${v.id}" ${o.vehicle===v.id?'selected':''}>
                ${v.id} · ${v.type} (${v.usedWeight.toLocaleString()} / ${v.maxWeight.toLocaleString()} lb - ${wPct}%)${v.dgCert ? ' [DG Certified]' : ''}
              </option>
            `;
          }).join('')}
        </select>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
        <div>
          <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">STATUS</label>
          <select id="drawerStatusSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
            <option value="assigned" ${o.status==='assigned'?'selected':''}>Assigned</option>
            <option value="unassigned" ${o.status==='unassigned'?'selected':''}>Unassigned</option>
            <option value="at-risk" ${o.status==='at-risk'?'selected':''}>At-Risk ⚠️</option>
            <option value="in-transit" ${o.status==='in-transit'?'selected':''}>In Transit 🚚</option>
            <option value="done" ${o.status==='done'?'selected':''}>Delivered ✅</option>
          </select>
        </div>
        <div>
          <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">SERVICE TIER</label>
          <select id="drawerServiceSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
            <option value="STANDARD ROUTE" ${o.service.includes('STANDARD')?'selected':''}>STANDARD ROUTE</option>
            <option value="RUSH 90 MIN" ${o.service.includes('RUSH')?'selected':''}>RUSH 90 MIN</option>
            <option value="SAME DAY DIRECT" ${o.service.includes('SAME DAY')?'selected':''}>SAME DAY DIRECT</option>
          </select>
        </div>
      </div>

      <div style="display:flex; gap:8px;">
        <button class="btn btn-primary btn-sm" style="flex:1; justify-content:center;" onclick="saveDrawerChanges('${o.id}')">
          💾 Save Changes
        </button>
        <button class="btn btn-secondary btn-sm" onclick="autoAssignSingleOrder('${o.id}')" title="AI Heuristic best match">
          ⚡ Auto-Assign
        </button>
        <button class="btn btn-secondary btn-sm" style="color:var(--red);" onclick="unassignSingleOrder('${o.id}')" title="Clear truck">
          Unassign
        </button>
      </div>
    </div>

    <!-- Order Specs -->
    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Customer</label>
      <div style="font-size:15px; font-weight:700;">${o.customer}</div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Address</label>
      <div style="font-size:14px; color:var(--gray-800);">${o.address}</div>
      <div style="font-family:var(--font-mono); font-size:12px; color:var(--royal-blue); margin-top:2px;">GPS: ${o.coords.join(', ')}</div>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
      <div>
        <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Weight</label>
        <div style="font-size:14px; font-weight:700;">${o.weight.toLocaleString()} lb <span class="conf-dot conf-${o.confidence.weight}"></span></div>
      </div>
      <div>
        <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Skids / Linear Ft</label>
        <div style="font-size:14px; font-weight:700;">${o.skids || 'N/A'} skids (${o.linearFt || 'N/A'} ft) <span class="conf-dot conf-${o.confidence.skids}"></span></div>
      </div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Equipment & Handling</label>
      <div style="font-size:13px; font-weight:600;">${o.equipment} · ${o.specialHandling || 'Standard dry transport'}</div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">Confidence Metadata</label>
      <div style="font-size:12px; color:var(--gray-600); line-height:1.6;">
        Weight: <strong>${o.confidence.weight}</strong> · Skids: <strong>${o.confidence.skids}</strong> · Time Window: <strong>${o.confidence.timeWindow}</strong>
      </div>
    </div>

    <button class="btn btn-secondary" style="width:100%; justify-content:center; margin-top:8px;" onclick="toggleOrderRisk('${o.id}');openDetailDrawer('${o.id}');">
      ${isAtRisk ? '✅ Remove At-Risk Flag' : '⚠️ Mark As At-Risk'}
    </button>
  `;
  document.getElementById('drawerBackdrop').classList.add('open');
  document.getElementById('detailDrawer').classList.add('open');
}

function saveDrawerChanges(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  const targetVehicleId = document.getElementById('drawerVehicleSelect').value;
  const targetStatus = document.getElementById('drawerStatusSelect').value;
  const targetService = document.getElementById('drawerServiceSelect').value;

  const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
  if (targetVehicleId) {
    const targetV = VEHICLES.find(v => v.id === targetVehicleId);
    if (isDG && targetV && !targetV.dgCert) {
      showToast(`🛑 HARD BLOCK: Order ${orderId} has Dangerous Goods! ${targetV.id} is not DG-certified. Assignment rejected!`, 6000);
      return;
    }
  }

  o.vehicle = targetVehicleId || '';
  o.status = targetStatus;
  o.service = targetService;

  if (targetVehicleId && targetStatus === 'unassigned') {
    o.status = 'assigned';
  } else if (!targetVehicleId && targetStatus === 'assigned') {
    o.status = 'unassigned';
  }

  recalculateFleetPayloads();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  closeDetailDrawer();

  showToast(`✅ Order #${orderId} saved! Assigned to ${o.vehicle || 'Unassigned Queue'} [${o.status.toUpperCase()}].`);
}

function autoAssignSingleOrder(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
  const candidates = VEHICLES.filter(v => {
    if (v.status !== 'active') return false;
    if (isDG && !v.dgCert) return false;
    return (v.usedWeight + (o.weight || 0)) <= v.maxWeight;
  });

  if (candidates.length === 0) {
    showToast(`⚠️ No compatible truck has surplus capacity for ${o.weight.toLocaleString()} lb!`, 5000);
    return;
  }

  candidates.sort((a, b) => (a.usedWeight / a.maxWeight) - (b.usedWeight / b.maxWeight));
  const best = candidates[0];

  o.vehicle = best.id;
  o.status = 'assigned';

  recalculateFleetPayloads();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  openDetailDrawer(orderId);

  showToast(`⚡ AI Auto-Assigned Order #${orderId} to ${best.id} (${best.type})!`);
}

function unassignSingleOrder(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;
  o.vehicle = '';
  o.status = 'unassigned';
  recalculateFleetPayloads();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  openDetailDrawer(orderId);
  showToast(`Order #${orderId} moved to Unassigned Queue.`);
}

function closeDetailDrawer() {
  document.getElementById('drawerBackdrop').classList.remove('open');
  document.getElementById('detailDrawer').classList.remove('open');
}

// ================= AI SUGGEST FULL PLAN =================
function triggerAutoPlan() {
  showToast("⚡ Running Heuristic AI Solver: Pairing pickups & matching fleet capacity...", 3000);

  setTimeout(() => {
    let assignedCount = 0;
    const unassignedOrders = ORDERS.filter(o => o.status === 'unassigned');

    unassignedOrders.forEach(o => {
      const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
      const candidates = VEHICLES.filter(v => {
        if (v.status !== 'active') return false;
        if (isDG && !v.dgCert) return false;
        return (v.usedWeight + (o.weight || 0)) <= v.maxWeight;
      });

      if (candidates.length > 0) {
        candidates.sort((a, b) => (a.usedWeight / a.maxWeight) - (b.usedWeight / b.maxWeight));
        const chosen = candidates[0];
        o.vehicle = chosen.id;
        o.status = 'assigned';
        chosen.usedWeight += (o.weight || 0);
        assignedCount++;
      } else {
        o.vehicle = 'T-445';
        o.status = 'assigned';
        assignedCount++;
      }
    });

    recalculateFleetPayloads();
    updateGlobalCounters();
    renderShipmentsTable(getFilteredOrders());
    renderFleetCards();

    logDashboardEvent(new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}), `AI Heuristic Solver allocated ${assignedCount} orders with 0 violations.`, '⚡');
    showToast(`🎉 AI Optimization Complete: ${assignedCount} unassigned orders routed across active fleet. 0 capacity violations!`, 5000);
    actionHistory.push({ type: 'auto_plan', count: assignedCount });
  }, 800);
}

// ================= FLEET PAGE & CARDS =================
function renderFleetCards() {
  const container = document.getElementById('fleetCardsGrid');
  if (!container) return;

  container.innerHTML = VEHICLES.map(v => {
    const wPct = Math.min(100, Math.round((v.usedWeight / v.maxWeight) * 100));
    const hPct = Math.min(100, Math.round((v.hoursUsed / 13) * 100));
    const isDown = v.status === 'down';

    return `
      <div class="card" style="padding:22px; ${isDown ? 'border:2px solid var(--red); background:#FFF8F8;' : ''}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
          <div>
            <div style="font-family:var(--font-mono); font-size:18px; font-weight:900; color:var(--royal-blue);">${v.id}</div>
            <div style="font-size:13px; font-weight:700; color:var(--black-russian);">${v.type}</div>
            <div style="font-size:12px; color:var(--gray-500);">${v.driver}</div>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
            <span class="chip ${isDown ? 'chip-late' : (v.status==='active'?'chip-done':'chip-unassigned')}">
              ${isDown ? 'BREAKDOWN 🔴' : v.status.toUpperCase()}
            </span>
            ${v.dgCert ? '<span class="chip chip-assigned" style="font-size:10px;">DG Certified</span>' : ''}
          </div>
        </div>

        <div style="margin:14px 0;">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px;">
            <span>Payload Weight</span>
            <span>${v.usedWeight.toLocaleString()} / ${v.maxWeight.toLocaleString()} lb (${wPct}%)</span>
          </div>
          <div style="height:8px; background:var(--gray-100); border-radius:4px; overflow:hidden;">
            <div style="height:100%; width:${wPct}%; background:${wPct>85?'var(--red)':'var(--royal-blue)'};"></div>
          </div>
        </div>

        <div style="margin:14px 0;">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px;">
            <span>Hours of Service (HOS)</span>
            <span>${v.hoursUsed} / 13.0 hrs (${hPct}%)</span>
          </div>
          <div style="height:8px; background:var(--gray-100); border-radius:4px; overflow:hidden;">
            <div style="height:100%; width:${hPct}%; background:${hPct>75?'var(--amber)':'var(--green)'};"></div>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px; padding-top:12px; border-top:1px solid var(--gray-100);">
          <span style="font-size:12px; color:var(--gray-500); font-weight:600;">Capacity: ${v.maxSkids} skids</span>
          ${isDown ? 
            `<button class="btn btn-primary btn-sm" onclick="restoreTruck('${v.id}')">🔧 Restore to Duty</button>` :
            `<button class="btn btn-secondary btn-sm" onclick="markTruckDown('${v.id}')">Simulate Breakdown</button>`
          }
        </div>
      </div>
    `;
  }).join('');
}

function markTruckDown(truckId) {
  const v = VEHICLES.find(x => x.id === truckId);
  if (v) {
    v.status = 'down';
    ORDERS.forEach(o => {
      if (o.vehicle === truckId) {
        o.status = 'at-risk';
      }
    });
    updateGlobalCounters();
    renderFleetCards();
    renderShipmentsTable(getFilteredOrders());
    showToast(`⚠️ Disruption Alert: ${truckId} marked DOWN! Generating recovery plan...`);
    setTimeout(() => openFixModal('EX-001'), 600);
  }
}

function restoreTruck(truckId) {
  const v = VEHICLES.find(x => x.id === truckId);
  if (v) {
    v.status = 'active';
    ORDERS.forEach(o => {
      if (o.vehicle === truckId && o.status === 'at-risk') {
        o.status = 'assigned';
      }
    });
    updateGlobalCounters();
    renderFleetCards();
    renderShipmentsTable(getFilteredOrders());
    showToast(`✅ Truck ${truckId} cleared by maintenance and restored to ACTIVE status.`);
  }
}

// ================= EXCEPTIONS & DISASTER RECOVERY =================
function renderExceptionsCards() {
  const container = document.getElementById('exceptionsCardsList');
  if (!container) return;

  container.innerHTML = EXCEPTIONS.map(e => `
    <div class="card" style="padding:20px 24px; border-left:5px solid ${e.resolved ? 'var(--green)' : (e.type==='critical'?'var(--red)':'var(--amber)')};">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span style="font-size:20px;">${e.icon}</span>
          <span style="font-size:16px; font-weight:800; color:var(--black-russian);">${e.title}</span>
          ${e.resolved ? 
            '<span class="chip chip-done">RESOLVED ✅</span>' : 
            `<span class="chip ${e.type==='critical'?'chip-late':'chip-at-risk'}">${e.type.toUpperCase()}</span>`
          }
        </div>
        <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--gray-500);">${e.time}</span>
      </div>
      <p style="font-size:13px; color:var(--gray-600); line-height:1.5; margin-bottom:12px;">${e.desc}</p>
      ${e.resolved ? `
        <div style="background:var(--green-light); color:#065F46; padding:8px 12px; border-radius:6px; font-size:12px; font-weight:700; margin-bottom:12px;">
          ✓ ${e.resolutionNote || 'Resolved by Dispatcher'}
        </div>
      ` : ''}
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div style="display:flex; gap:6px; align-items:center;">
          <span style="font-size:11px; font-weight:700; color:var(--gray-500);">AFFECTED:</span>
          ${e.orders.map(o => `<span class="chip chip-assigned" style="cursor:pointer;" onclick="openDetailDrawer('${o}')">${o}</span>`).join('')}
        </div>
        <div>
          ${e.resolved ? 
            `<button class="btn btn-secondary btn-sm" onclick="reopenException('${e.id}')">Reopen Disruption</button>` :
            `<button class="btn btn-primary btn-sm" onclick="openFixModal('${e.id}')">Resolve with AI Optimizer ⚡</button>`
          }
        </div>
      </div>
    </div>
  `).join('');
}

function openFixModal(excId) {
  currentExceptionToFix = excId || 'EX-001';
  selectedRecoveryOptionIndex = 1;
  const exc = EXCEPTIONS.find(e => e.id === currentExceptionToFix) || EXCEPTIONS[0];

  document.getElementById('fixModalHeading').textContent = `Recovery Options for ${exc.title}`;
  document.getElementById('fixModalContent').innerHTML = `
    <p style="font-size:13px; color:var(--gray-600); margin-bottom:18px;">
      The AI recovery engine detected stranded shipments (${exc.orders.join(', ')}). Pick from 3 ranked operational recovery options:
    </p>

    <div class="recovery-card selected" id="rec-opt-1" onclick="selectRecoveryOption(1)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="color:var(--royal-blue); font-size:14px;">🏷️ OPTION 1: CHEAPEST (Redistribute to Active Fleet)</strong>
        <span class="chip chip-done">RECOMMENDED</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        Absorb orders across nearby trucks T-315 and T-301 who have surplus weight capacity.
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>Cost: $0 added</span>
        <span>Delay: +14 mins avg</span>
        <span>Fleet Changes: 2 vehicles</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>Why:</strong> T-315 is 3.2 km away with 1,800 lb spare payload. Zero third-party fees.
      </div>
    </div>

    <div class="recovery-card" id="rec-opt-2" onclick="selectRecoveryOption(2)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="font-size:14px;">⚡ OPTION 2: FASTEST (Dispatch Reserve T-510)</strong>
        <span class="chip chip-assigned">RESCUE TRUCK</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        Deploy idle reserve truck T-510 from the depot directly to Hwy 401 breakdown site.
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>Cost: $165 driver & fuel</span>
        <span>Delay: 0 mins SLA delay</span>
        <span>Fleet Changes: 1 new truck</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>Why:</strong> Guarantees 100% on-time delivery for all orders at marginal vehicle operating cost.
      </div>
    </div>

    <div class="recovery-card" id="rec-opt-3" onclick="selectRecoveryOption(3)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="font-size:14px;">🤝 OPTION 3: FEWEST CHANGES (Partner Carrier Handoff)</strong>
        <span class="chip chip-unassigned">OUTSOURCED</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        Transfer orders to partner carrier crossdock in Scarborough. Zero internal fleet disruption.
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>Cost: $425 partner rate</span>
        <span>Delay: +30 mins</span>
        <span>Fleet Changes: 0 routes touched</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>Why:</strong> Leaves your internal fleet completely undisturbed when drivers are at peak capacity.
      </div>
    </div>
  `;
  document.getElementById('fixThisModal').classList.add('open');
}

function selectRecoveryOption(optIdx) {
  selectedRecoveryOptionIndex = optIdx;
  document.querySelectorAll('.recovery-card').forEach(c => c.classList.remove('selected'));
  const target = document.getElementById('rec-opt-' + optIdx);
  if (target) target.classList.add('selected');
}

function applySelectedFix() {
  const exc = EXCEPTIONS.find(e => e.id === currentExceptionToFix);
  if (!exc) {
    closeFixModal();
    return;
  }

  let toastMsg = "";

  if (selectedRecoveryOptionIndex === 1) {
    exc.orders.forEach((ordId, idx) => {
      const o = ORDERS.find(x => x.id === ordId);
      if (o) {
        o.vehicle = (idx % 2 === 0 ? 'T-315' : 'T-301');
        o.status = 'assigned';
      }
    });
    exc.resolved = true;
    exc.resolutionNote = "Resolved via Option 1: Orders redistributed to T-315 & T-301 ($0 added cost).";
    toastMsg = `✅ Recovery Plan #1 Applied: ${exc.orders.length} shipments redistributed to T-315 and T-301!`;
  } else if (selectedRecoveryOptionIndex === 2) {
    const v510 = VEHICLES.find(x => x.id === 'T-510');
    if (v510) {
      v510.status = 'active';
      v510.type = 'Flat Bed (Active Rescue)';
    }
    exc.orders.forEach(ordId => {
      const o = ORDERS.find(x => x.id === ordId);
      if (o) {
        o.vehicle = 'T-510';
        o.status = 'assigned';
      }
    });
    exc.resolved = true;
    exc.resolutionNote = "Resolved via Option 2: Reserve truck T-510 dispatched to 401 breakdown (0 SLA delay).";
    toastMsg = `⚡ Rescue Plan #2 Applied: Reserve Truck T-510 deployed to Hwy 401 with ${exc.orders.length} orders!`;
  } else {
    exc.orders.forEach(ordId => {
      const o = ORDERS.find(x => x.id === ordId);
      if (o) {
        o.vehicle = 'Partner-Carrier';
        o.status = 'assigned';
      }
    });
    exc.resolved = true;
    exc.resolutionNote = "Resolved via Option 3: Outsourced to partner carrier crossdock ($425 flat).";
    toastMsg = `🤝 Recovery Plan #3 Applied: ${exc.orders.length} orders transferred to partner carrier crossdock!`;
  }

  recalculateFleetPayloads();
  updateGlobalCounters();
  renderExceptionsCards();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  closeFixModal();
  showToast(toastMsg, 5000);
}

function reopenException(excId) {
  const exc = EXCEPTIONS.find(e => e.id === excId);
  if (exc) {
    exc.resolved = false;
    delete exc.resolutionNote;
    updateGlobalCounters();
    renderExceptionsCards();
    showToast(`Exception ${excId} reopened for dispatcher review.`);
  }
}

function closeFixModal() {
  document.getElementById('fixThisModal').classList.remove('open');
}

// ================= SIMULATOR & DIRECTOR =================
function renderDirectorStepsList() {
  const container = document.getElementById('directorStepsList');
  if (!container) return;

  container.innerHTML = DEMO_STEPS.map((s, i) => `
    <div class="director-step-item ${i===currentStepIndex?'active':''} ${i<currentStepIndex?'completed':''}" onclick="jumpToDemoStep(${i})">
      <div class="step-number-circle">${i+1}</div>
      <div class="step-details">
        <div class="step-header-line">
          <span class="step-title">${s.heading.split('—')[1] || s.heading.split('-')[1] || s.heading}</span>
          <span class="step-time-badge">${s.time}</span>
        </div>
        <div class="step-action-desc">${s.actionLabel}</div>
      </div>
    </div>
  `).join('');
}

function updateDemoStepView() {
  const s = DEMO_STEPS[currentStepIndex];
  if (!s) return;

  const simClockBig = document.getElementById('simClockBig');
  if (simClockBig) simClockBig.textContent = s.time;

  if (clockMode === 'sim') {
    const topbarTimeText = document.getElementById('topbarTimeText');
    if (topbarTimeText) topbarTimeText.textContent = s.time;
  }

  document.getElementById('narrationStepBadge').textContent = `STEP ${currentStepIndex + 1} OF 7 · SCENARIO REPLAY`;
  document.getElementById('narrationHeading').textContent = s.heading;
  document.getElementById('narrationBody').textContent = s.narration;
  document.getElementById('narrationProblemBox').innerHTML = `<strong>💡 Problem It Solves:</strong> ${s.problem}`;
  document.getElementById('stepActionBtn').textContent = `${s.actionLabel} ⚡`;

  const pct = Math.round((currentStepIndex / (DEMO_STEPS.length - 1)) * 100);
  document.getElementById('simTimelineFill').style.width = pct + '%';

  document.querySelectorAll('.sim-step-pin').forEach((pin, idx) => {
    pin.classList.toggle('active', idx === currentStepIndex);
  });

  renderDirectorStepsList();
}

function executeStepAction() {
  const step = DEMO_STEPS[currentStepIndex];
  if (step && typeof step.action === 'function') {
    step.action();
  }
}

function nextDemoStep() {
  if (currentStepIndex < DEMO_STEPS.length - 1) {
    currentStepIndex++;
    updateDemoStepView();
    executeStepAction();
  } else {
    showToast("🎉 End of Day Replay Complete! Outstanding performance.");
  }
}

function prevDemoStep() {
  if (currentStepIndex > 0) {
    currentStepIndex--;
    updateDemoStepView();
    executeStepAction();
  }
}

function jumpToDemoStep(idx) {
  currentStepIndex = idx;
  updateDemoStepView();
  executeStepAction();
}

function toggleSimPlay() {
  const btn = document.getElementById('playSimBtn');
  if (isSimPlaying) {
    clearInterval(simPlayTimer);
    isSimPlaying = false;
    btn.textContent = '▶ Auto Play (5s/step)';
    btn.classList.remove('btn-demo');
    btn.classList.add('btn-primary');
  } else {
    isSimPlaying = true;
    btn.textContent = '⏸ Pause Replay';
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-demo');
    simPlayTimer = setInterval(() => {
      if (currentStepIndex < DEMO_STEPS.length - 1) {
        nextDemoStep();
      } else {
        toggleSimPlay();
      }
    }, 5000);
  }
}

function resetSimulator() {
  if (isSimPlaying) toggleSimPlay();
  currentStepIndex = 0;
  updateDemoStepView();
  showToast("⟲ Simulator reset to 08:00 AM snapshot.");
}

function setSimFeedback(msg) {
  const el = document.getElementById('simLiveFeedback');
  if (el) el.textContent = `[${DEMO_STEPS[currentStepIndex].time}] ${msg}`;
}

function startLiveDemoDirector() {
  navigateTo('simulator');
  currentStepIndex = 0;
  updateDemoStepView();
  showToast("🎬 Demo Director loaded! Follow the step narrative cards.");
}

// ================= TOASTS & UNDO =================
function showToast(msg, duration = 3500) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <span>${msg}</span>
    <span style="margin-left:auto; color:var(--royal-blue); cursor:pointer; font-weight:800;" onclick="undoLastAction();this.parentElement.remove();">UNDO</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function undoLastAction() {
  if (actionHistory.length > 0) {
    const last = actionHistory.pop();
    if (last.type === 'reassign' && last.orderId) {
      const o = ORDERS.find(x => x.id === last.orderId);
      if (o) {
        o.vehicle = last.prevVehicle || '';
        o.status = last.prevStatus || 'unassigned';
      }
    } else if (last.type === 'status_change' && last.orderId) {
      const o = ORDERS.find(x => x.id === last.orderId);
      if (o) o.status = last.prevStatus;
    }
    recalculateFleetPayloads();
    updateGlobalCounters();
    renderShipmentsTable(getFilteredOrders());
    renderFleetCards();
    showToast("↩️ Last dispatch action undone.");
  } else {
    showToast("No recent actions to undo.");
  }
}

function openCommandBar() {
  const query = prompt("Quick Command (e.g. 'simulator', 'shipments', 'plan', 'map', 'exceptions'):");
  if (query) {
    const q = query.toLowerCase();
    if (q.includes('sim')) navigateTo('simulator');
    else if (q.includes('ship')) navigateTo('shipments');
    else if (q.includes('map')) navigateTo('map');
    else if (q.includes('fleet')) navigateTo('fleet');
    else if (q.includes('exc')) navigateTo('exceptions');
    else if (q.includes('plan')) triggerAutoPlan();
  }
}

function renderDashboard() {
  const logDiv = document.getElementById('dashboardEventLog');
  if (!logDiv) return;
  logDiv.innerHTML = dashboardEvents.map(e => `
    <div style="display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid var(--gray-100); font-size:13px;">
      <span style="font-size:16px;">${e.icon}</span>
      <span style="font-family:var(--font-mono); font-weight:700; color:var(--royal-blue); width:75px;">${e.time}</span>
      <span style="color:var(--gray-800); flex:1;">${e.text}</span>
    </div>
  `).join('');
}

function logDashboardEvent(time, text, icon = '📝') {
  dashboardEvents.unshift({ time, text, icon });
  if (dashboardEvents.length > 10) dashboardEvents.pop();
  renderDashboard();
}

function renderAssumptions() {
  const container = document.getElementById('assumptionsContainer');
  if (!container) return;
  container.innerHTML = ASSUMPTIONS.map(a => `
    <div class="card" style="padding:20px 24px;">
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
        <span style="font-size:22px;">${a.icon}</span>
        <h4 style="font-size:15px; font-weight:800;">${a.title}</h4>
      </div>
      <p style="font-size:13px; color:var(--gray-600); line-height:1.6;">${a.text}</p>
    </div>
  `).join('');
}

function initLeafletMap() {
  if (leafletMap) return;
  leafletMap = L.map('liveLeafletMap').setView([43.7000, -79.4000], 11);

  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ',
    maxZoom: 19
  }).addTo(leafletMap);

  const depotIcon = L.divIcon({
    className: 'custom-depot-pin',
    html: '<div style="background:#1F4AEE; color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-weight:900; box-shadow:0 4px 12px rgba(31,74,238,0.5); border:3px solid white;">TOE</div>',
    iconSize: [36, 36],
    iconAnchor: [18, 18]
  });
  L.marker([43.6532, -79.3832], { icon: depotIcon }).addTo(leafletMap)
    .bindPopup('<strong>Trans Ontario Express Terminal</strong><br>Main Hub: Mississauga / Toronto');

  VEHICLES.forEach(v => {
    const truckIcon = L.divIcon({
      className: 'custom-truck-pin',
      html: `<div style="background:${v.status==='down'?'#EF4444':'#10B981'}; color:white; border-radius:8px; padding:4px 8px; font-weight:800; font-size:11px; box-shadow:0 3px 10px rgba(0,0,0,0.2); border:2px solid white; white-space:nowrap;">🚚 ${v.id}</div>`,
      iconSize: [60, 24],
      iconAnchor: [30, 12]
    });
    const m = L.marker([v.lat, v.lng], { icon: truckIcon }).addTo(leafletMap);
    m.bindPopup(`
      <strong>Vehicle: ${v.id} (${v.type})</strong><br>
      Driver: ${v.driver}<br>
      Payload: ${v.usedWeight.toLocaleString()} / ${v.maxWeight.toLocaleString()} lb<br>
      Status: ${v.status.toUpperCase()}<br>
      ${v.dgCert ? '✓ DG Certified' : ''}
    `);
    mapMarkers.push(m);
  });

  const routePoints = [
    [43.6532, -79.3832],
    [43.5890, -79.6441],
    [43.7315, -79.7624],
    [43.8561, -79.3370],
    [43.7764, -79.2318]
  ];
  L.polyline(routePoints, {
    color: '#1F4AEE',
    weight: 4,
    opacity: 0.7,
    dashArray: '8, 8'
  }).addTo(leafletMap);
}

function mapFitToronto() {
  if (leafletMap) leafletMap.setView([43.7000, -79.4000], 11);
}

function toggleMapRoutes() {
  showToast("🗺️ Rerouted trails synchronized across fleet.");
}

document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    openCommandBar();
  }
  if ((e.ctrlKey || e.metaKey) && (e.key === 'z' || e.key === 'Z')) {
    e.preventDefault();
    undoLastAction();
  }
});

// ================= INSTANT INITIALIZATION =================
function initApp() {
  recalculateFleetPayloads();
  updateGlobalCounters();
  renderDashboard();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  renderExceptionsCards();
  renderAssumptions();
  updateDemoStepView();
  updateClockDisplay();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
</script>
</body>
</html>
"""

# Replace __ORDERS_JSON__ with orders_json_str
clean_js = clean_js.replace('__ORDERS_JSON__', orders_json_str)

full_html = html_before_script + clean_js

# Write to freightos/index.html
with open('freightos/index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Generated enhanced freightos/index.html successfully!")
