# FreightOS — Dispatcher Control Tower & Route Optimizer 🚚⚡

[![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#)
[![Stack](https://img.shields.io/badge/Frontend-Vanilla%20HTML5%20%2F%20CSS3%20%2F%20ES6%2B-orange.svg)](#)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20External%20Runtime-brightgreen.svg)](#)
[![Localization](https://img.shields.io/badge/Languages-EN%20%7C%20FR%20Bilingual-blueviolet.svg)](#)

> **Team #16 — Hackathon Solution for Trans Ontario Express**  
> An enterprise-grade, client-side dispatcher control tower designed to solve the Greater Toronto Area (GTA) regional freight challenge: turning manual, uncoordinated dispatch into a synchronized, compliant, and profit-optimized operation.

---

## 🌟 Executive Summary

Regional less-than-truckload (LTL) and full-truckload (FTL) carriers like **Trans Ontario Express** manage high-volume, multi-constraint deliveries across the Greater Toronto Area. Traditional dispatch relying on memory, spreadsheets, and radio calls leads to:
* **Capacity mismatches & safety violations** (overloading straight trucks, uncertified dangerous goods handling).
* **Driver fatigue & regulatory penalties** (exceeding Ontario Ministry of Transportation / MTO 13-hour Hours of Service limits).
* **Costly midday disruptions** (mechanical breakdowns leaving customers stranded without rapid recovery).
* **Margin erosion** (overpaying third-party brokers while internal straight trucks and vans run underutilized).

**FreightOS** is a zero-dependency, self-contained single-page application (SPA) that acts as an intelligent control tower for dispatchers. It features a multi-dimensional capacity heuristic engine, live interactive state mutations, a disaster recovery simulator, an empirical impact scorecard, and a profit & risk optimization engine.

---

## 🚀 Key Features

### 1. ⚡ Multi-Dimensional Capacity Enforcement
* **Strict Constraint Solving:** Simultaneously enforces **Weight (lb)**, **Linear Footage (ft)**, and **Skid Capacity** per vehicle.
* **100% Legal Guarantee:** The automated planner (`Suggest Full Plan`) sorts shipments by density and volume, placing cargo across active and reserve units without ever exceeding 100% capacity on any metric.
* **Overflow / Partner Carrier Routing:** Orders that exceed available fleet specs are transparently routed to an *Unassigned Queue* tagged for partner carrier brokerage.
* **Hard Block on Manual Drag & Drop:** If a dispatcher tries to manually assign an order to a vehicle that would overload it, the system blocks the action and displays an informative alert detailing the exact excess (e.g. `🛑 CAPACITY BLOCK: T-205 would exceed weight limit by 850 lb`).

### 2. 🛡️ Regulatory & Safety Guardrails (MTO & TDG)
* **Dangerous Goods (TDG) Verification:** Regulated shipments (e.g., UN 1993 chemicals) are hard-locked to verified DG-certified vehicles and drivers (`T-205`, `T-301`, `T-445`). Reassignments to non-certified vehicles are blocked immediately.
* **Ontario MTO Hours of Service (HOS):** Real-time monitoring of driving and on-duty time, ensuring all runs stay strictly below Ontario's 13-hour maximum driving limit.

### 3. 🚨 Interactive Disruption & Disaster Recovery Simulator
* **Simulated Highway 401 Breakdown:** Step through real-world operational disruptions (e.g., engine failure on Truck `T-108` at Hwy 401 & DVP).
* **Algorithmic Recovery Options:** Evaluate 3 distinct ranked operational solutions:
  1. *Redistribute to Active Fleet* (Cost-Minimizer).
  2. *Deploy Reserve Truck T-510* (Fastest / Recommended).
  3. *Partner Carrier Handoff* (Fewest Changes).
* **1-Click Execution:** Applying the recovery plan automatically updates vehicle status to `BREAKDOWN 🔴`, transfers cargo, and recalculates payload bars without service interruption.

### 4. 📈 Profit & Risk Optimization Engine
* **3 Operating Frameworks:** Choose between *Maximum Profitability* (49.5% margin), *Balanced Resilience* (47.3% margin - Recommended), or *Zero-Risk SLA Guarantee* (42.1% margin).
* **Comparative P&L Decision Matrix:** Contrasts unoptimized baseline operations vs. FreightOS automated plans across stem miles, fuel, overtime penalties, and broker expenditures.
* **Live Sensitivity Sliders:** Test margin sensitivity in real-time by adjusting Diesel Fuel Price ($1.40–$2.30/L), Driver Hourly Wage ($22–$38/hr), and SLA Buffer Time (15–60 mins).
* **Transparent Assumptions:** All economic figures are clearly labeled as illustrative assumptions, with parameters documented in the technical *Assumptions* view.

### 5. 📊 Empirical Impact Scorecard (Data-Driven Baseline)
* **Real Historical Baseline:** Grounded directly in empirical data from the busiest weekday in the sample dataset (**Tuesday, September 29, 2026** — 359 orders, 290 stops, 46 working drivers, 51 vehicles).
* **Accurate Wording & Historical Context:** Reflects real multi-day stop metrics (e.g., *54 of 159 appointment stops were late across the sample period*; *multi-driver customer visits on 8% of customer-days*).
* **Synchronized Application State:** Global counters across Dashboard, Shipments, Fleet, Exceptions, Impact, and Optimizer reflect a single unified reactive state.

### 6. 🌐 Canadian Localization (`EN | FR`) & Responsive UI
* **Bilingual Switcher:** Toggle between English (`EN`) and French (`FR`) with one click in the navigation bar. All labels, matrices, tables, tooltips, and alerts translate instantly.
* **Mobile & Desktop Ready:** Features responsive flex/grid layouts, collapsible mobile navigation drawers, and horizontal touch-scrollable shipment tables.

---

## 🛠️ Architecture & Tech Stack

```
FreightOS Architecture
├── Single-Page Application (SPA)
│   ├── UI Layer: Semantic HTML5 + Custom Modern CSS Design System (BEM-inspired)
│   ├── Reactive State Store: Client-side JavaScript (ES6+), Vanilla Event Dispatchers
│   ├── Heuristic Engine: Multi-dimensional bin packing & geographical clustering
│   ├── Mapping Component: Leaflet.js with OpenStreetMap geocoded GTA tiles
│   └── Brand Assets: Self-contained, Base64-inlined PNG vectors and logos
```

* **No Build Tools or Node Modules Required:** Clones and runs instantly in any modern browser without `npm install`, Webpack, Vite, or external compilation.
* **Self-Contained Offline Execution:** All styles, icons (SVG), brand assets, and order records are embedded directly in `index.html`.

---

## 📂 Project Structure

```text
├── index.html                 # Root single-file application (Production Build)
├── freightos/
│   ├── index.html             # Source application with full test harnesses
│   └── orders_full.json       # 75 GTA dispatch shipment dataset
├── README.md                  # Project documentation & pitch guide
└── brand-assets/              # Vector logos and Trans Ontario brand imagery
```

---

## 🚦 Getting Started

### Prerequisites
* Any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).

### Quick Launch
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/freightos-dispatch.git
   ```
2. Open `index.html` directly in your browser:
   * **Windows:** Double-click `index.html` or run:
     ```powershell
     Start-Process chrome index.html
     ```
   * **macOS / Linux:**
     ```bash
     open index.html # or xdg-open index.html
     ```

No local web server is strictly required, though you can use any static server if preferred:
```bash
python -m http.server 8080
# Visit http://localhost:8080 in your browser
```

---

## 🔍 Capacity Self-Check Verification

The heuristic planner strictly respects all fleet equipment boundaries documented on the Assumptions page. Running the automated plan allocates shipments with zero legal violations:

| Vehicle | Equipment Type | Status | DG Certified | Weight Used / Cap | Weight % | Linear Ft / Cap | Ft % | Skids / Cap | Skid % | Status |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **T-108** | Straight Truck | Active | No | 10,000 / 10,000 lb | **100%** | 9 / 24 ft | 38% | 5 / 10 | 50% | ✅ PASS |
| **T-112** | Cargo Van | Active | No | 3,000 / 3,000 lb | **100%** | 4 / 10 ft | 40% | 2 / 3 | 67% | ✅ PASS |
| **T-205** | Straight Truck | Active | **Yes** | 10,000 / 10,000 lb | **100%** | 10 / 24 ft | 42% | 5 / 10 | 50% | ✅ PASS |
| **T-301** | Straight Truck | Active | **Yes** | 9,860 / 10,000 lb | **99%** | 10 / 24 ft | 42% | 5 / 10 | 50% | ✅ PASS |
| **T-315** | Cargo Van | Active | No | 2,921 / 3,000 lb | **97%** | 6 / 10 ft | 60% | 3 / 3 | **100%** | ✅ PASS |
| **T-445** | Tractor + 53ft | Active | **Yes** | 42,869 / 43,000 lb | **100%** | 46 / 53 ft | 87% | 24 / 26 | 92% | ✅ PASS |
| **T-502** | Flat Bed | Active | No | 32,378 / 40,000 lb | **81%** | 48 / 48 ft | **100%** | 22 / 24 | 92% | ✅ PASS |
| **T-510** | Flat Bed (Reserve)| Reserve | No | 32,410 / 40,000 lb | **81%** | 48 / 48 ft | **100%** | 24 / 24 | **100%** | ✅ PASS |

*Orders exceeding available vehicle dimensions remain safely unassigned in the queue for partner carrier handoff.*

---

## 🎯 Demo Walkthrough for Presentation & Pitch

1. **Dashboard Overview:** Review the live 75-order queue, unassigned counter, and fleet payload meters.
2. **Execute 1-Click Plan:** Click **`⚡ Suggest Full Plan`** on the Dashboard or Shipments page. Watch unassigned orders route cleanly across active units while all payload bars balance out.
3. **Inspect Safety Block:** Open any Dangerous Goods shipment (e.g. `#2986888P`) in the slide-out drawer. Try manually assigning it to uncertified van `T-112` — notice the instant TDG regulatory block alert.
4. **Disaster Recovery Simulation:** Navigate to **`Exceptions`**. View the Hwy 401 breakdown alert on `T-108`. Click **`Resolve with AI Optimizer ⚡`**, choose Option 2 (*Deploy Reserve T-510*), and click **`Apply Selected Fix`**.
5. **Profit & Risk Optimizer:** Open **`📈 Profit & Risk Optimizer`**. Walk through the P&L variance matrix, click an actionable 1-click optimization recommendation, and drag the fuel price and wage sliders to show live recalculation.
6. **Bilingual Toggle:** Click **`EN | FR`** in the topbar to demonstrate Canadian market readiness.

---

## 📜 License

This project was developed for the Hackathon Challenge under Team #16 and is open-sourced under the [MIT License](LICENSE).
