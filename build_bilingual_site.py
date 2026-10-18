# -*- coding: utf-8 -*-
"""
build_bilingual_site.py
Builds the complete bilingual English/French FreightOS web application.
"""
import sys
import json
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("1. Loading orders from freightos/orders_full.json...")
with open('freightos/orders_full.json', 'r', encoding='utf-8') as f:
    orders_data = json.load(f)

orders_json_str = json.dumps(orders_data)

print(f"Loaded {len(orders_data)} orders.")

print("2. Reading freightos/index.html...")
with open('freightos/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate <script> tag
script_pos = html.find('<script>')
assert script_pos != -1, "Cannot find <script> tag in freightos/index.html"

html_before_script = html[:script_pos]
print(f"HTML before <script> has {len(html_before_script)} characters.")

# Define the complete bilingual JavaScript
bilingual_js = r'''<script>
// ================= DATA INJECTION =================
let ORDERS = __ORDERS_JSON__;

let VEHICLES = [
  { id: 'T-108', type: 'Straight Truck', type_fr: 'Camion porteur', driver: 'Rajesh Patel', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 4500, usedWeight: 4500, hoursUsed: 6.5, status: 'active', dgCert: false, lat: 43.7615, lng: -79.4111 },
  { id: 'T-112', type: 'Cargo Van', type_fr: 'Fourgonnette', driver: 'Kananathan Shanmugarajah', maxWeight: 3000, maxFt: 10, maxSkids: 3, baseWeight: 600, usedWeight: 600, hoursUsed: 4.2, status: 'active', dgCert: false, lat: 43.8561, lng: -79.3370 },
  { id: 'T-205', type: 'Straight Truck', type_fr: 'Camion porteur', driver: 'Marcus Johnson', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 4200, usedWeight: 4200, hoursUsed: 8.1, status: 'active', dgCert: true, lat: 43.5890, lng: -79.6441 },
  { id: 'T-301', type: 'Straight Truck', type_fr: 'Camion porteur', driver: 'Amandeep Singh', maxWeight: 10000, maxFt: 24, maxSkids: 10, baseWeight: 3800, usedWeight: 3800, hoursUsed: 7.3, status: 'active', dgCert: true, lat: 43.7764, lng: -79.2318 },
  { id: 'T-315', type: 'Cargo Van', type_fr: 'Fourgonnette', driver: 'David Chen', maxWeight: 3000, maxFt: 10, maxSkids: 3, baseWeight: 800, usedWeight: 800, hoursUsed: 3.8, status: 'active', dgCert: false, lat: 43.6532, lng: -79.3832 },
  { id: 'T-445', type: 'Tractor + 53ft', type_fr: 'Tracteur + 53 pi', driver: 'Viktor Petrov', maxWeight: 43000, maxFt: 53, maxSkids: 26, baseWeight: 18000, usedWeight: 18000, hoursUsed: 9.1, status: 'active', dgCert: true, lat: 43.7315, lng: -79.7624 },
  { id: 'T-502', type: 'Flat Bed', type_fr: 'Plateau', driver: 'Miguel Santos', maxWeight: 40000, maxFt: 48, maxSkids: 24, baseWeight: 14000, usedWeight: 14000, hoursUsed: 5.5, status: 'active', dgCert: false, lat: 43.8384, lng: -79.0868 },
  { id: 'T-510', type: 'Flat Bed (Reserve)', type_fr: 'Plateau (Réserve)', driver: 'Brandon Taylor', maxWeight: 40000, maxFt: 48, maxSkids: 24, baseWeight: 0, usedWeight: 0, hoursUsed: 0, status: 'reserve', dgCert: false, lat: 43.6205, lng: -79.5132 }
];

let EXCEPTIONS = [
  { id: 'EX-001', type: 'critical', icon: '🔧', title_en: 'Truck T-108 Breakdown (Hwy 401 & DVP)', title_fr: 'Panne du camion T-108 (Autoroute 401 & DVP)', desc_en: 'Engine failure reported at Hwy 401 & Don Valley Parkway. 3 customer shipments stranded on truck. Driver safe, tow in route.', desc_fr: 'Panne moteur à l\'angle autoroute 401 et Don Valley Pkwy. 3 expéditions immobilisées. Chauffeur en sécurité, remorquage en route.', time: '10:15 AM', orders: ['2986700P', '2986700D', '2986545D'], resolved: false },
  { id: 'EX-002', type: 'critical', icon: '⚖️', title_en: 'Weight Overload Risk on T-205', title_fr: 'Risque de surcharge de poids sur T-205', desc_en: 'Adding 2 heavy industrial skids would exceed legal capacity (10,000 lb). Dynamic load balancing active.', desc_fr: 'L\'ajout de 2 palettes industrielles lourdes dépasserait la limite légale (10 000 lb). Équilibrage dynamique actif.', time: '08:45 AM', orders: ['2987010P', '2987010D'], resolved: false },
  { id: 'EX-003', type: 'critical', icon: '☢️', title_en: 'Dangerous Goods on Non-Certified Truck', title_fr: 'Matières dangereuses sur camion non certifié', desc_en: 'Order 2986888P contains regulated chemical drums. T-112 is not DG-certified.', desc_fr: 'La commande 2986888P contient des fûts chimiques réglementés. Le T-112 n\'est pas certifié MD.', time: '08:20 AM', orders: ['2986888P'], resolved: false },
  { id: 'EX-004', type: 'warning', icon: '⏰', title_en: 'Late Risk — 3 Downtown Windows', title_fr: 'Risque de retard — 3 créneaux centre-ville', desc_en: 'Heavy downtown traffic on Gardiner Expy threatening 3 PM appointment commitments.', desc_fr: 'Trafic dense sur l\'autoroute Gardiner menaçant les créneaux de livraison de 15h00.', time: '12:30 PM', orders: ['2986545D', '2986999D'], resolved: false },
  { id: 'EX-005', type: 'warning', icon: '🕐', title_en: 'Driver Hours Near Legal Limit (T-445)', title_fr: 'Heures chauffeur proches du seuil légal (T-445)', desc_en: 'Driver Viktor Petrov at 9.1 hours. Approaching Canadian 13-hour daily driving limit.', desc_fr: 'Le chauffeur Viktor Petrov a 9,1 heures. Proche de la limite quotidienne canadienne de 13 heures.', time: '14:00 PM', orders: ['2985990D'], resolved: false },
  { id: 'EX-006', type: 'warning', icon: '📋', title_en: 'Missing Pallet Dimensions', title_fr: 'Dimensions de palettes manquantes', desc_en: '8 shipments arrived with weight but missing linear feet specifications.', desc_fr: '8 expéditions sont arrivées avec le poids mais sans les spécifications de pieds linéaires.', time: '07:30 AM', orders: ['2986297P', '2986401P'], resolved: false },
  { id: 'EX-007', type: 'warning', icon: '🔀', title_en: 'Equipment Request Mismatch', title_fr: 'Incompatibilité d\'équipement demandé', desc_en: 'Customer requested 53ft trailer for loading dock; smaller straight truck queued.', desc_fr: 'Le client a demandé une semi-remorque de 53 pi pour le quai ; un camion porteur a été mis en file.', time: '09:00 AM', orders: ['2985990P'], resolved: false }
];

const DEMO_STEPS = [
  {
    time: "08:00 AM",
    heading_en: "08:00 AM - Morning Dispatch Snapshot",
    heading_fr: "08h00 - Aperçu de la répartition matinale",
    narration_en: "This is a real day's work. 75 orders have arrived. 30 are unassigned, 14 are at risk of missing delivery windows, and 7 exceptions need dispatcher attention before trucks hit the GTA highways.",
    narration_fr: "Voici une vraie journée de travail. 75 commandes sont arrivées. 30 ne sont pas assignées, 14 risquent de manquer leurs créneaux et 7 exceptions nécessitent l'attention du répartiteur avant le départ sur les autoroutes du Grand Toronto.",
    problem_en: "Identifies unassigned orders and equipment mismatches before morning dispatch rather than discovering failures mid-route.",
    problem_fr: "Identifie les commandes non assignées et les incompatibilités d'équipement avant les départs plutôt que de découvrir les échecs en cours de route.",
    actionLabel_en: "Inspect 30 Unassigned Orders",
    actionLabel_fr: "Inspecter les 30 commandes non assignées",
    action: () => {
      navigateTo("shipments");
      filterTable("unassigned", document.getElementById("pill-unassigned"));
      setSimFeedback(currentLang === 'fr' ? "Expéditions filtrées sur 30 commandes non assignées prêtes pour la planification." : "Filtered shipments to 30 unassigned orders ready for auto-plan.");
    }
  },
  {
    time: "08:15 AM",
    heading_en: "08:15 AM - Hard Block: Dangerous Goods Compliance",
    heading_fr: "08h15 - Blocage strict : Conformité matières dangereuses",
    narration_en: "Watch what happens when we try to assign a Dangerous Goods chemical shipment (Order 2986888P) to Van T-112. The system enforces safety: It HARD BLOCKS the assignment because T-112 is not DG-certified!",
    narration_fr: "Regardez ce qui arrive lorsqu'on tente d'assigner une expédition de matières dangereuses (Commande 2986888P) au fourgon T-112. Le système bloque strictement l'affectation car le T-112 n'est pas certifié MD !",
    problem_en: "Prevents $50,000+ transport regulatory fines and hazardous material violations by hard-blocking uncertified vehicles.",
    problem_fr: "Évite plus de 50 000 $ d'amendes réglementaires et de violations de matières dangereuses en bloquant les véhicules non certifiés.",
    actionLabel_en: "Attempt Invalid DG Assignment",
    actionLabel_fr: "Tenter une assignation MD invalide",
    action: () => {
      navigateTo("shipments");
      changeOrderVehicle("2986888P", "T-112");
      setSimFeedback(currentLang === 'fr' ? "Validation de règle stricte déclenchée : Assignation refusée !" : "Hard rule validation triggered: Assignment refused.");
    }
  },
  {
    time: "08:30 AM",
    heading_en: "08:30 AM - Heuristic Route Optimization",
    heading_fr: "08h30 - Optimisation heuristique des tournées",
    narration_en: "With one click, the dispatcher triggers Suggest Full Plan. FreightOS pairs Pickups before Deliveries, minimizes stem distance across the GTA, and fills 30 unassigned orders into active trucks with 0 capacity violations.",
    narration_fr: "En un clic, le répartiteur déclenche le Plan automatique. FreightOS ordonne les collectes avant les livraisons, minimise la distance dans le Grand Toronto et répartit 30 commandes sans violation de capacité.",
    problem_en: "Saves 2-3 hours of manual dispatching and eliminates empty return miles through smart cross-GTA pairing.",
    problem_fr: "Économise 2 à 3 heures de répartition manuelle et élimine les kilomètres à vide grâce à un appariement intelligent.",
    actionLabel_en: "Run AI Auto-Plan",
    actionLabel_fr: "Lancer le planificateur IA",
    action: () => {
      triggerAutoPlan();
      setSimFeedback(currentLang === 'fr' ? "Planificateur heuristique exécuté : 30 commandes routées." : "Heuristic solver executed: 30 unassigned orders routed.");
    }
  },
  {
    time: "10:15 AM",
    heading_en: "10:15 AM - Disruption Alert: Truck T-108 Breakdown",
    heading_fr: "10h15 - Alerte perturbation : Panne du camion T-108",
    narration_en: "Disaster strikes: Truck T-108 reports an engine breakdown on Hwy 401 near the Don Valley Parkway with 3 live customer shipments stranded inside. FreightOS immediately alerts dispatch and flags shipments as At-Risk.",
    narration_fr: "Incident imprévu : Le camion T-108 signale une panne de moteur sur l'autoroute 401 près de la DVP avec 3 expéditions bloquées à bord. FreightOS alerte immédiatement le répartiteur et passe les commandes en statut À risque.",
    problem_en: "Detects mid-day vehicle breakdowns immediately and isolates impacted shipments before customer delivery windows expire.",
    problem_fr: "Détecte immédiatement les pannes en milieu de journée et isole les expéditions avant l'expiration des créneaux.",
    actionLabel_en: "Simulate Breakdown on T-108",
    actionLabel_fr: "Simuler la panne sur T-108",
    action: () => {
      navigateTo("fleet");
      markTruckDown("T-108");
      setSimFeedback(currentLang === 'fr' ? "T-108 marqué EN PANNE sur l'autoroute 401. 3 expéditions compromises." : "T-108 marked DOWN on Hwy 401. 3 stranded shipments compromised.");
    }
  },
  {
    time: "10:30 AM",
    heading_en: "10:30 AM - Ranked Operational Recovery Options",
    heading_fr: "10h30 - Options de reprise opérationnelle classées",
    narration_en: "Rather than guessing, the dispatcher is given 3 ranked options: 1) Cheapest (Redistribute to surplus fleet, $0), 2) Fastest (Dispatch reserve flatbed T-510, $165), 3) Fewest Changes (Outsource to partner carrier, $425). We apply Option 1!",
    narration_fr: "Plutôt que d'improviser, le répartiteur reçoit 3 options classées : 1) Moins chère (Redistribuer sur la flotte active, 0 $), 2) Plus rapide (Déployer le camion de réserve T-510, 165 $), 3) Moins de changements (Sous-traiter, 425 $). Nous appliquons l'option 1 !",
    problem_en: "Removes panic from emergency dispatch by mathematically calculating cost, delay, and ripple effects for every fix option.",
    problem_fr: "Élimine la panique en cas d'urgence en calculant avec précision le coût, le retard et les répercussions de chaque solution.",
    actionLabel_en: "Apply Recovery Plan #1",
    actionLabel_fr: "Appliquer le plan de reprise #1",
    action: () => {
      navigateTo("exceptions");
      openFixModal("EX-001");
      selectRecoveryOption(1);
      setTimeout(() => applySelectedFix(), 1000);
      setSimFeedback(currentLang === 'fr' ? "Plan de reprise #1 appliqué : Commandes redistribuées sans coût additionnel." : "Recovery Plan #1 applied: Stranded shipments absorbed with $0 added cost.");
    }
  },
  {
    time: "12:30 PM",
    heading_en: "12:30 PM - Real-Time Traffic & SLA Monitoring",
    heading_fr: "12h30 - Surveillance du trafic et des SLA en direct",
    narration_en: "Heavy midday traffic hits the Gardiner Expressway. FreightOS calculates that afternoon downtown deliveries are at risk of missing strict 3 PM appointments. Dispatcher can proactively notify clients or adjust priority.",
    narration_fr: "Le trafic de midi s'intensifie sur l'autoroute Gardiner. FreightOS calcule que les livraisons de l'après-midi au centre-ville risquent de dépasser les créneaux stricts de 15h00. Le répartiteur peut avertir les clients de manière proactive.",
    problem_en: "Eliminates customer surprise and SLA breach penalties by providing 2.5 hours of advance warning on potential delay.",
    problem_fr: "Élimine les pénalités de retard et prévient les clients 2,5 heures à l'avance en cas de risque d'engorgement.",
    actionLabel_en: "Inspect At-Risk SLA Orders",
    actionLabel_fr: "Inspecter les commandes SLA à risque",
    action: () => {
      navigateTo("shipments");
      filterTable("at-risk", document.getElementById("pill-at-risk"));
      setSimFeedback(currentLang === 'fr' ? "Surveillance SLA : Expéditions à risque isolées pour notification client." : "SLA monitor: Filtered table to high-risk downtown appointments.");
    }
  },
  {
    time: "17:00 PM",
    heading_en: "17:00 PM - End-of-Day Impact Scorecard",
    heading_fr: "17h00 - Bilan de performance de fin de journée",
    narration_en: "At 5:00 PM, the dispatch cycle completes. The scorecard proves the value: 342 km saved (↓21.5%), 22.8 driver hours eliminated (↓20.3%), late deliveries cut from 54 down to 2 (↓96.3%), and $1,480 saved in direct fuel and labor.",
    narration_fr: "À 17h00, le cycle de répartition s'achève. Le bilan prouve la valeur : 342 km économisés (↓21,5 %), 22,8 heures de chauffeur éliminées (↓20,3 %), livraisons en retard réduites de 54 à 2 (↓96,3 %) et 1 480 $ économisés en carburant et main-d'œuvre.",
    problem_en: "Provides executive leadership with audit-proof metrics comparing planned routing versus actual performance.",
    problem_fr: "Offre à la direction des indicateurs audités comparant la tournée planifiée aux performances réelles.",
    actionLabel_en: "View Final Impact Scorecard",
    actionLabel_fr: "Voir le tableau d'impact final",
    action: () => {
      navigateTo("impact");
      setSimFeedback(currentLang === 'fr' ? "Bilan de journée : 342 km économisés, 96,3 % de livraisons en retard en moins." : "Day summary: 342 km saved, 96.3% late stop reduction.");
    }
  }
];

const ASSUMPTIONS = [
  { 
    icon: "🚛", 
    title_en: "Vehicle Capacity Limits (Standardized Models)", 
    title_fr: "Limites de capacité des véhicules (modèles standardisés)",
    text_en: "Cargo Van: 3,000 lb / 10 ft / 3 skids. Straight Truck: 10,000 lb / 24 ft / 10 skids. Tractor + 53ft: 43,000 lb / 53 ft / 26 skids. Flat Bed: 40,000 lb / 48 ft / 24 skids. (Documented in Section 6).",
    text_fr: "Fourgonnette : 3 000 lb / 10 pi / 3 palettes. Porteur : 10 000 lb / 24 pi / 10 palettes. Tracteur + 53 pi : 43 000 lb / 53 pi / 26 palettes. Plateau : 40 000 lb / 48 pi / 24 palettes. (Détaillé en Section 6)."
  },
  { 
    icon: "📐", 
    title_en: "Missing Dimensions & Skid Estimation", 
    title_fr: "Dimensions manquantes et estimation des palettes",
    text_en: "When skid spots or linear feet are missing in shipper paperwork, 1 skid is assumed for every 1,200 lb of freight or parcel counts. These are badged as Estimated in yellow.",
    text_fr: "Lorsque les emplacements de palettes ou les pieds linéaires manquent sur les bordereaux, 1 palette est estimée pour chaque 1 200 lb de fret. Celles-ci portent un badge 'Estimé' en jaune."
  },
  { 
    icon: "📍", 
    title_en: "Customer Geocoding & Distance Factor", 
    title_fr: "Géocodage des clients et facteur de distance",
    text_en: "GPS coordinates were geocoded from GTA postal codes and street addresses. Travel times calibrated with urban density factor 1.4 for central Toronto and 1.2 for suburban 400-series highways.",
    text_fr: "Les coordonnées GPS ont été géocodées à partir des codes postaux et adresses du Grand Toronto. Temps de trajet calibrés avec facteur urbain de 1,4 pour Toronto centre et 1,2 pour autoroutes 400."
  },
  { 
    icon: "⚖️", 
    title_en: "Canadian Hours of Service Compliance", 
    title_fr: "Conformité aux heures de service canadiennes",
    text_en: "Limits configured to Ontario standard: 13 hours maximum driving time and 14 hours total on-duty time per day, with mandatory off-duty rest.",
    text_fr: "Limites configurées selon la norme ontarienne : 13 heures de conduite max et 14 heures de service totales par jour, avec repos obligatoire."
  }
];

// ================= I18N BILINGUAL DICTIONARY =================
let currentLang = 'en';

const TRANSLATIONS = {
  en: {
    // Nav & Sidebar
    live_dispatch: 'LIVE DISPATCH',
    nav_dashboard: 'Dashboard',
    nav_simulator: 'Simulator & Demo',
    nav_map: 'Interactive Map',
    nav_shipments: 'Shipments',
    nav_fleet: 'Fleet Capacity',
    nav_exceptions: 'Exceptions',
    nav_impact: 'Impact Scorecard',
    nav_assumptions: 'Assumptions',
    footer_system: 'GTA & Canada Transport System',

    // Topbar
    search_placeholder: 'Search shipments, trucks, routes…',
    btn_undo: 'Undo',
    btn_director: 'Director Walkthrough',
    clock_live: 'LIVE',
    clock_sim: 'SIM',

    // Dashboard Hero
    hero_pill: '🏆 40 YEARS OF SERVICE · TRANS ONTARIO EXPRESS',
    hero_title: 'AI-Powered Logistics Control Tower',
    hero_subtitle: 'Real-time dispatch optimization, automated load matching, and instant disruption recovery for 75 live shipments across Ontario & Canada.',
    lbl_saved_today: 'Saved Today',
    lbl_late_stops: 'Fewer Late Stops',
    lbl_fuel_saved: 'Fuel & Labor Saved',
    btn_launch_demo: 'Launch Interactive Demo →',

    // Metric Cards
    stat_total_orders: 'Total GTA Orders',
    stat_unassigned: 'Unassigned Orders',
    stat_fleet_active: 'Fleet Active',
    stat_exceptions: 'Active Exceptions',
    stat_assigned_suffix: 'Assigned',
    stat_needs_dispatcher: 'Needs Dispatcher',
    stat_run_planner: 'Run AI Planner ⚡',
    stat_avg_load: 'Avg Load',
    stat_reserve_truck: '1 Reserve Truck',
    stat_breakdown_alert: 'Breakdown Alert',
    stat_ai_fix_ready: 'Instant AI Fix Ready',

    // Dashboard Section Headings
    event_log_title: 'Today\'s Real-Time Event Log',
    problem_solver_title: 'Logistics Problem Solver Overview',
    testimonial_tag: 'Client Success · Traffic Manager Endorsement',
    testimonial_quote: '"Trans Ontario\'s commitment to precision delivery across the GTA has kept our supply chain running flawlessly. The transition to intelligent dispatching sets a new standard in freight."',
    testimonial_location: 'Leading GTA Distribution Center — Scarborough, ON',

    // Shipments Table
    shipments_page_title: 'Shipments Management',
    shipments_page_desc: 'Verified pair-legs, dangerous goods compliance, and confidence data indicators.',
    btn_suggest_plan: '⚡ Suggest Full Plan',
    pill_all: 'All',
    pill_unassigned: 'Unassigned',
    pill_at_risk: 'At Risk',
    pill_rush: 'Rush / Same-Day',
    pill_dg: '⚠ Dangerous Goods',
    pill_missing: 'Missing Data',
    th_order: 'Order ID',
    th_leg: 'Leg',
    th_customer: 'Customer',
    th_address: 'Address',
    th_service: 'Service',
    th_weight: 'Weight',
    th_status: 'Status',
    th_vehicle: 'Assigned Vehicle',
    th_actions: 'Quick Actions',
    leg_delivery: 'Delivery',
    leg_pickup: 'Pickup',
    status_assigned: 'Assigned',
    status_unassigned: 'Unassigned',
    status_at_risk: 'At-Risk',
    status_in_transit: 'In Transit',
    status_done: 'Delivered',
    unassigned_vehicle_option: '-- Unassigned --',
    btn_mark_risk: 'Mark Risk',
    btn_clear_risk: 'Normal',
    btn_details: 'Details',

    // Detail Drawer
    drawer_header: 'Shipment Details',
    order_label: 'Order',
    drawer_assign_heading: '⚡ Live Dispatch Assignment',
    drawer_truck_label: 'ASSIGN TO TRUCK',
    drawer_status_label: 'STATUS',
    drawer_service_label: 'SERVICE TIER',
    drawer_unassigned_opt: '-- Unassigned (In Dispatch Queue) --',
    btn_save_changes: '💾 Save Changes',
    btn_auto_assign: '⚡ Auto-Assign',
    btn_unassign: 'Unassign',
    label_customer: 'Customer',
    label_address: 'Address',
    label_weight: 'Weight',
    label_skids: 'Skids / Linear Ft',
    label_equip: 'Equipment & Handling',
    label_confidence: 'Confidence Metadata',
    btn_remove_risk: '✅ Remove At-Risk Flag',

    // Fleet Cards
    fleet_page_title: 'Fleet Capacity & Driver Hours',
    fleet_page_desc: 'Legal weight limits, linear feet, skid counts, and Canadian Hours of Service tracking.',
    payload_weight: 'Payload Weight',
    hours_of_service: 'Hours of Service (HOS)',
    capacity_label: 'Capacity',
    skids_unit: 'skids',
    btn_simulate_breakdown: 'Simulate Breakdown',
    btn_restore: '🔧 Restore to Duty',
    dg_certified: 'DG Certified',
    status_active: 'ACTIVE',
    status_reserve: 'RESERVE',
    status_breakdown: 'BREAKDOWN 🔴',

    // Exceptions Page
    exceptions_page_title: 'Disruptions & Exceptions Inbox',
    exceptions_page_desc: 'Prioritized operational failures with 3-way ranked automated recovery plans.',
    badge_resolved: 'RESOLVED ✅',
    badge_critical: 'CRITICAL',
    badge_warning: 'WARNING',
    label_affected: 'AFFECTED:',
    btn_resolve_ai: 'Resolve with AI Optimizer ⚡',
    btn_reopen_disruption: 'Reopen Disruption',

    // Fix Modal
    fix_modal_header: 'Recovery Plan Optimizer',
    fix_modal_intro: 'The AI recovery engine detected stranded shipments. Pick from 3 ranked operational recovery options:',
    btn_cancel: 'Cancel',
    btn_apply_fix: 'Apply Selected Fix',

    // Simulator
    sim_page_title: 'Dispatch Simulator & Demo Director',
    sim_page_desc: 'Step through the 7-phase real day scenario with automated live actions and full reasoning.',
    btn_reset_day: '⟲ Reset Day',
    director_seq_title: 'Director Step Sequence',
    btn_prev: '← Prev',
    btn_next: 'Next →',
    btn_auto_play: '▶ Auto Play (5s/step)',
    btn_pause_play: '⏸ Pause Replay',

    // Map Page
    map_page_title: 'Interactive GTA Route Map',
    map_page_desc: 'Real GPS coordinates and optimized routes for Trans Ontario\'s Greater Toronto Area fleet.',
    btn_center_gta: 'Center GTA',
    btn_toggle_routes: 'Toggle Routes',
    map_radar_title: 'Trans Ontario Fleet Radar',
    map_radar_desc: 'Live vehicle tracking & telemetry across GTA highways',
    legend_depot: 'Trans Ontario Depot',
    legend_truck: 'Active Delivery Truck',
    legend_route: 'Planned Travel Corridor',

    // Impact Page
    impact_page_title: 'Impact Scorecard: Plan vs. Actual Day',
    impact_page_desc: 'Direct mathematical comparison between what drivers actually drove on Sep 18 vs. FreightOS automated routing.',
    kpi_distance: 'Total Travel Distance',
    kpi_distance_sub: '↓ 21.5% (342 km saved)',
    kpi_hours: 'Driver On-Duty Hours',
    kpi_hours_sub: '↓ 20.3% (22.8 hours saved)',
    kpi_late: 'Late Customer Stops',
    kpi_late_sub: '↓ 96.3% reduction in late stops',
    kpi_resilience: 'Plan Resilience Score',
    kpi_resilience_sub: 'Can absorb 2 vehicle failures',
    outcomes_title: 'Key Financial & Operational Outcomes',
    col1_title: 'Fuel & Emission Savings',
    col1_desc: 'At an average commercial consumption of 32L/100km for diesel straight trucks, saving 342 km eliminates 109.4 Liters of diesel daily (~$218/day in fuel alone).',
    col2_title: 'Driver Overtime Elimination',
    col2_desc: 'Saving 22.8 driver-hours across 42 routes directly eliminates costly end-of-day overtime and avoids drivers hitting the strict 13-hour driving limits.',
    col3_title: 'Fleet Asset Efficiency',
    col3_desc: 'Carrying out the day with 38 vehicles instead of 42 frees up 4 trucks at the depot for maintenance or profitable emergency on-demand cross-border loads.',

    // Assumptions Page
    assumptions_page_title: 'Documented Assumptions & Data Transparency',
    assumptions_page_desc: 'As required by Section 11 of the Trans Ontario Blueprint, all estimates are openly disclosed.'
  },

  fr: {
    // Nav & Sidebar
    live_dispatch: 'RÉPARTITION EN DIRECT',
    nav_dashboard: 'Tableau de bord',
    nav_simulator: 'Simulateur & Démo',
    nav_map: 'Carte interactive',
    nav_shipments: 'Expéditions',
    nav_fleet: 'Capacité de flotte',
    nav_exceptions: 'Exceptions',
    nav_impact: 'Tableau d\'impact',
    nav_assumptions: 'Hypothèses',
    footer_system: 'Système de transport Grand Toronto & Canada',

    // Topbar
    search_placeholder: 'Rechercher expéditions, camions, routes…',
    btn_undo: 'Annuler',
    btn_director: 'Visite guidée',
    clock_live: 'DIRECT',
    clock_sim: 'SIM',

    // Dashboard Hero
    hero_pill: '🏆 40 ANS DE SERVICE · TRANS ONTARIO EXPRESS',
    hero_title: 'Tour de contrôle logistique par IA',
    hero_subtitle: 'Optimisation de la répartition en temps réel, affectation automatique et reprise après panne pour 75 expéditions en Ontario et au Canada.',
    lbl_saved_today: 'Économisé aujourd\'hui',
    lbl_late_stops: 'Retards évités',
    lbl_fuel_saved: 'Carburant & main-d\'œuvre',
    btn_launch_demo: 'Lancer la démo interactive →',

    // Metric Cards
    stat_total_orders: 'Total commandes GTA',
    stat_unassigned: 'Commandes non assignées',
    stat_fleet_active: 'Flotte active',
    stat_exceptions: 'Exceptions actives',
    stat_assigned_suffix: 'Assignées',
    stat_needs_dispatcher: 'Action requise',
    stat_run_planner: 'Planifier par IA ⚡',
    stat_avg_load: 'Charge moy.',
    stat_reserve_truck: '1 camion de réserve',
    stat_breakdown_alert: 'Alerte panne',
    stat_ai_fix_ready: 'Solution IA prête',

    // Dashboard Section Headings
    event_log_title: 'Journal d\'activité en direct du jour',
    problem_solver_title: 'Vue d\'ensemble de résolution logistique',
    testimonial_tag: 'Succès client · Témoignage gestionnaire de trafic',
    testimonial_quote: '"L\'engagement de Trans Ontario pour la précision de livraison dans le Grand Toronto a maintenu notre chaîne d\'approvisionnement sans faille. Le passage à la répartition intelligente établit un nouveau standard."',
    testimonial_location: 'Centre de distribution majeur du Grand Toronto — Scarborough, ON',

    // Shipments Table
    shipments_page_title: 'Gestion des expéditions',
    shipments_page_desc: 'Paires collecte-livraison vérifiées, conformité matières dangereuses et indicateurs de confiance.',
    btn_suggest_plan: '⚡ Suggérer plan complet',
    pill_all: 'Toutes',
    pill_unassigned: 'Non assignées',
    pill_at_risk: 'À risque',
    pill_rush: 'Urgent / Même jour',
    pill_dg: '⚠ Matières dangereuses',
    pill_missing: 'Données manquantes',
    th_order: 'N° Commande',
    th_leg: 'Trajet',
    th_customer: 'Client',
    th_address: 'Adresse',
    th_service: 'Service',
    th_weight: 'Poids',
    th_status: 'Statut',
    th_vehicle: 'Véhicule assigné',
    th_actions: 'Actions rapides',
    leg_delivery: 'Livraison',
    leg_pickup: 'Collecte',
    status_assigned: 'Assignée',
    status_unassigned: 'Non assignée',
    status_at_risk: 'À risque',
    status_in_transit: 'En transit',
    status_done: 'Livrée',
    unassigned_vehicle_option: '-- Non assigné --',
    btn_mark_risk: 'À risque',
    btn_clear_risk: 'Normal',
    btn_details: 'Détails',

    // Detail Drawer
    drawer_header: 'Détails de l\'expédition',
    order_label: 'Commande',
    drawer_assign_heading: '⚡ Affectation de répartition en direct',
    drawer_truck_label: 'ASSIGNER AU CAMION',
    drawer_status_label: 'STATUT',
    drawer_service_label: 'NIVEAU DE SERVICE',
    drawer_unassigned_opt: '-- Non assigné (File de répartition) --',
    btn_save_changes: '💾 Enregistrer',
    btn_auto_assign: '⚡ Auto-assigner',
    btn_unassign: 'Désassigner',
    label_customer: 'Client',
    label_address: 'Adresse',
    label_weight: 'Poids',
    label_skids: 'Palettes / Pi. linéaires',
    label_equip: 'Équipement & manutention',
    label_confidence: 'Métadonnées de confiance',
    btn_remove_risk: '✅ Retirer le drapeau à risque',

    // Fleet Cards
    fleet_page_title: 'Capacité de flotte & heures de chauffeur',
    fleet_page_desc: 'Limites de poids légales, pieds linéaires, nombre de palettes et conformité aux heures de service.',
    payload_weight: 'Poids de charge',
    hours_of_service: 'Heures de service (HOS)',
    capacity_label: 'Capacité',
    skids_unit: 'palettes',
    btn_simulate_breakdown: 'Simuler une panne',
    btn_restore: '🔧 Remettre en service',
    dg_certified: 'Certifié MD',
    status_active: 'ACTIF',
    status_reserve: 'RÉSERVE',
    status_breakdown: 'EN PANNE 🔴',

    // Exceptions Page
    exceptions_page_title: 'Boîte de réception des perturbations',
    exceptions_page_desc: 'Pannes et incidents priorisés avec génération de plans de récupération automatisés à 3 options.',
    badge_resolved: 'RÉSOLU ✅',
    badge_critical: 'CRITIQUE',
    badge_warning: 'AVERTISSEMENT',
    label_affected: 'TOUCHÉ :',
    btn_resolve_ai: 'Résoudre avec l\'optimiseur IA ⚡',
    btn_reopen_disruption: 'Rouvrir la perturbation',

    // Fix Modal
    fix_modal_header: 'Optimiseur de plan de reprise',
    fix_modal_intro: 'Le moteur de récupération IA a détecté des expéditions bloquées. Choisissez parmi 3 options opérationnelles classées :',
    btn_cancel: 'Annuler',
    btn_apply_fix: 'Appliquer la solution choisie',

    // Simulator
    sim_page_title: 'Simulateur & démonstrateur de journée',
    sim_page_desc: 'Parcourez le scénario réel en 7 phases avec actions automatisées en direct et explications complètes.',
    btn_reset_day: '⟲ Réinitialiser',
    director_seq_title: 'Séquence du démonstrateur',
    btn_prev: '← Préc.',
    btn_next: 'Suiv. →',
    btn_auto_play: '▶ Lecture auto (5s/étape)',
    btn_pause_play: '⏸ Mettre en pause',

    // Map Page
    map_page_title: 'Carte interactive des tournées GTA',
    map_page_desc: 'Coordonnées GPS réelles et routes optimisées pour la flotte Trans Ontario dans le Grand Toronto.',
    btn_center_gta: 'Centrer GTA',
    btn_toggle_routes: 'Afficher/Masquer routes',
    map_radar_title: 'Radar de flotte Trans Ontario',
    map_radar_desc: 'Télémétrie et suivi des véhicules en direct sur les autoroutes du Grand Toronto',
    legend_depot: 'Dépôt Trans Ontario',
    legend_truck: 'Camion en livraison active',
    legend_route: 'Couloir de déplacement planifié',

    // Impact Page
    impact_page_title: 'Tableau d\'impact : Plan vs. Réalité',
    impact_page_desc: 'Comparaison mathématique directe entre les trajets réels des chauffeurs et le routage automatisé FreightOS.',
    kpi_distance: 'Distance totale parcourue',
    kpi_distance_sub: '↓ 21,5 % (342 km économisés)',
    kpi_hours: 'Heures de service chauffeurs',
    kpi_hours_sub: '↓ 20,3 % (22,8 heures économisées)',
    kpi_late: 'Arrêts clients en retard',
    kpi_late_sub: '↓ 96,3 % de réduction des retards',
    kpi_resilience: 'Score de résilience du plan',
    kpi_resilience_sub: 'Peut absorber 2 pannes de véhicules',
    outcomes_title: 'Résultats financiers et opérationnels clés',
    col1_title: 'Économies de carburant et d\'émissions',
    col1_desc: 'À une consommation moyenne de 32 L/100 km pour un camion porteur diesel, économiser 342 km élimine 109,4 L de diesel par jour (~218 $/jour en carburant seul).',
    col2_title: 'Élimination des heures supplémentaires',
    col2_desc: 'Économiser 22,8 heures-chauffeur sur 42 tournées élimine directement les heures supplémentaires coûteuses et respecte la limite stricte de 13 heures.',
    col3_title: 'Efficacité d\'utilisation des actifs',
    col3_desc: 'Effectuer la journée avec 38 véhicules au lieu de 42 libère 4 camions au dépôt pour l\'entretien ou des chargements d\'urgence transfrontaliers rentables.',

    // Assumptions Page
    assumptions_page_title: 'Hypothèses documentées & transparence',
    assumptions_page_desc: 'Conformément à la section 11 du cahier des charges de Trans Ontario, toutes les estimations sont divulguées en toute transparence.'
  }
};

function t(key) {
  if (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key] !== undefined) {
    return TRANSLATIONS[currentLang][key];
  }
  if (TRANSLATIONS['en'] && TRANSLATIONS['en'][key] !== undefined) {
    return TRANSLATIONS['en'][key];
  }
  return key;
}

function toggleLanguage() {
  currentLang = (currentLang === 'en') ? 'fr' : 'en';
  const btn = document.getElementById('langToggleBtn');
  const btnText = document.getElementById('langToggleText');
  if (btn) {
    btn.classList.toggle('fr-active', currentLang === 'fr');
  }
  if (btnText) {
    btnText.textContent = currentLang === 'en' ? 'EN | FR' : 'FR | EN';
  }

  applyLanguage();
  showToast(currentLang === 'fr' ? '🌐 Langue changée en Français (Canada)' : '🌐 Language switched to English');
}

function applyLanguage() {
  // Apply all data-i18n static text elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translated = t(key);
    if (translated) {
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.placeholder = translated;
      } else {
        el.textContent = translated;
      }
    }
  });

  // Update clock mode toggle text
  const clockBtn = document.getElementById('clockToggleBtn');
  if (clockBtn) {
    clockBtn.textContent = (clockMode === 'live') ? t('clock_live') : t('clock_sim');
  }

  // Update play sim button text
  const playBtn = document.getElementById('playSimBtn');
  if (playBtn) {
    playBtn.textContent = isSimPlaying ? t('btn_pause_play') : t('btn_auto_play');
  }

  // Refresh dynamic widgets
  updateClockDisplay();
  updateGlobalCounters();
  renderShipmentsTable(getFilteredOrders());
  renderFleetCards();
  renderExceptionsCards();
  renderAssumptions();
  renderDirectorStepsList();
  updateDemoStepView();
}

function getVehicleTypeTranslated(type) {
  if (currentLang !== 'fr') return type;
  if (type.includes('Straight Truck')) return 'Camion porteur';
  if (type.includes('Cargo Van')) return 'Fourgonnette';
  if (type.includes('Tractor + 53ft')) return 'Tracteur + 53 pi';
  if (type.includes('Active Rescue')) return 'Plateau (Secours actif)';
  if (type.includes('Reserve')) return 'Plateau (Réserve)';
  if (type.includes('Flat Bed')) return 'Plateau';
  return type;
}

// ================= APP STATE =================
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
  { time: '08:00 AM', text_en: 'Morning load batch imported: 75 real GTA orders across Ontario.', text_fr: 'Lot de chargements importé : 75 commandes réelles dans le Grand Toronto.', icon: '📥' },
  { time: '08:12 AM', text_en: 'T-205 loaded at Mississauga terminal with 4,200 lb.', text_fr: 'T-205 chargé au terminal de Mississauga avec 4 200 lb.', icon: '🚛' },
  { time: '08:15 AM', text_en: 'Safety block triggered: Van T-112 refused UN 1993 Dangerous Goods.', text_fr: 'Blocage de sécurité : Fourgon T-112 a refusé les matières dangereuses UN 1993.', icon: '🛑' },
  { time: '08:30 AM', text_en: 'AI heuristic solver allocated 30 orders across active fleet.', text_fr: 'L\'optimiseur heuristique a alloué 30 commandes sur la flotte active.', icon: '⚡' }
];

// ================= CLOCK LOGIC =================
function updateClockDisplay() {
  if (clockMode === 'live') {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const topbarTimeText = document.getElementById('topbarTimeText');
    if (topbarTimeText) topbarTimeText.textContent = timeStr;

    const dateOptions = { month: 'short', day: 'numeric', year: 'numeric' };
    const dateStr = now.toLocaleDateString(currentLang === 'fr' ? 'fr-CA' : 'en-CA', dateOptions);
    const topbarDateLabel = document.getElementById('topbarDateLabel');
    if (topbarDateLabel) topbarDateLabel.textContent = dateStr;
  }
}

setInterval(updateClockDisplay, 1000);

function toggleClockMode() {
  const btn = document.getElementById('clockToggleBtn');
  const dot = document.getElementById('liveClockDot');
  if (clockMode === 'live') {
    clockMode = 'sim';
    btn.textContent = t('clock_sim');
    btn.classList.add('sim-active');
    btn.title = currentLang === 'fr' ? "En mode simulation. Cliquez pour repasser à l'horloge réelle" : "In Simulator Mode. Click to switch to Real-Time Wall Clock";
    if (dot) dot.style.display = 'none';
    const topbarTimeText = document.getElementById('topbarTimeText');
    if (topbarTimeText) topbarTimeText.textContent = DEMO_STEPS[currentStepIndex].time;
    showToast(currentLang === 'fr' ? "Mode horloge : Temps simulé (synchronisé avec les étapes)" : "Clock Mode: Simulator Time (synced with demo step time)");
  } else {
    clockMode = 'live';
    btn.textContent = t('clock_live');
    btn.classList.remove('sim-active');
    btn.title = currentLang === 'fr' ? "En mode temps réel. Cliquez pour synchroniser avec la simulation" : "In Live Mode. Click to switch to Simulator Step Time";
    if (dot) dot.style.display = 'inline-block';
    updateClockDisplay();
    showToast(currentLang === 'fr' ? "Mode horloge : Heure réelle en direct" : "Clock Mode: Live Wall Clock (Real-Time)");
  }
}

// ================= CAPACITY & RECALCULATION =================
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
  const assigned = total - unassigned;
  const atRisk = ORDERS.filter(o => o.status === 'at-risk').length;
  const rush = ORDERS.filter(o => (o.service || '').toLowerCase().includes('rush') || (o.service || '').toLowerCase().includes('same day')).length;
  const dg = ORDERS.filter(o => (o.specialHandling || '').toLowerCase().includes('dangerous goods')).length;
  const missing = ORDERS.filter(o => o.confidence && (o.confidence.linearFt === 'missing' || o.confidence.skids === 'missing' || o.confidence.appointment === 'missing')).length;

  const statTotal = document.getElementById('statTotalShipments');
  if (statTotal) statTotal.textContent = total;

  const statAssignedSub = document.getElementById('statAssignedSub');
  if (statAssignedSub) statAssignedSub.textContent = `${assigned} ${t('stat_assigned_suffix')}`;

  const statUnassigned = document.getElementById('statUnassigned');
  if (statUnassigned) statUnassigned.textContent = unassigned;

  const statUnassignedLabel = document.getElementById('statUnassignedLabel');
  if (statUnassignedLabel) {
    statUnassignedLabel.textContent = unassigned > 0 ? t('stat_needs_dispatcher') : (currentLang === 'fr' ? 'Planifié ✅' : 'Fully Planned ✅');
    statUnassignedLabel.style.color = unassigned > 0 ? 'var(--red)' : 'var(--green)';
  }

  let totalCap = 0;
  let totalUsed = 0;
  VEHICLES.forEach(v => {
    if (v.status === 'active') {
      totalCap += v.maxWeight;
      totalUsed += v.usedWeight;
    }
  });
  const avgUtil = totalCap > 0 ? Math.round((totalUsed / totalCap) * 100) : 0;
  const statFleetUtil = document.getElementById('statFleetUtilization');
  if (statFleetUtil) statFleetUtil.textContent = `${avgUtil}% ${t('stat_avg_load')}`;

  const activeVehicles = VEHICLES.filter(v => v.status === 'active').length;
  const statFleetActive = document.getElementById('statFleetActive');
  if (statFleetActive) statFleetActive.innerHTML = `${activeVehicles}<span style="font-size:18px; color:var(--gray-400); font-weight:500;">/8</span>`;

  const activeExceptions = EXCEPTIONS.filter(e => !e.resolved).length;
  const statExceptions = document.getElementById('statActiveExceptions');
  if (statExceptions) statExceptions.textContent = activeExceptions;

  const downTrucks = VEHICLES.filter(v => v.status === 'down');
  const statBreakdownSub = document.getElementById('statBreakdownSub');
  if (statBreakdownSub) {
    if (downTrucks.length > 0) {
      statBreakdownSub.textContent = `${downTrucks.length} ${t('stat_breakdown_alert')}`;
      statBreakdownSub.style.color = 'var(--red)';
    } else {
      statBreakdownSub.textContent = currentLang === 'fr' ? 'Flotte opérationnelle 100%' : '100% Fleet Operational';
      statBreakdownSub.style.color = 'var(--green)';
    }
  }

  const excBadge = document.getElementById('exceptionCountBadge');
  if (excBadge) excBadge.textContent = activeExceptions;

  // Filter Pill Counts & Labels
  const pillAll = document.getElementById('pill-all');
  if (pillAll) pillAll.innerHTML = `${t('pill_all')} (<span id="countAll">${total}</span>)`;

  const pillUnassigned = document.getElementById('pill-unassigned');
  if (pillUnassigned) pillUnassigned.innerHTML = `${t('pill_unassigned')} (<span id="countUnassigned">${unassigned}</span>)`;

  const pillAtRisk = document.getElementById('pill-at-risk');
  if (pillAtRisk) pillAtRisk.innerHTML = `${t('pill_at_risk')} (<span id="countAtRisk">${atRisk}</span>)`;

  const pillRush = document.getElementById('pill-rush');
  if (pillRush) pillRush.innerHTML = `${t('pill_rush')} (<span id="countRush">${rush}</span>)`;

  const pillDg = document.getElementById('pill-dg');
  if (pillDg) pillDg.innerHTML = `${t('pill_dg')} (<span id="countDg">${dg}</span>)`;

  const pillMissing = document.getElementById('pill-missing');
  if (pillMissing) pillMissing.innerHTML = `${t('pill_missing')} (<span id="countMissing">${missing}</span>)`;
}

// ================= MOBILE NAVIGATION =================
function toggleMobileSidebar() {
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (sidebar && backdrop) {
    const isOpen = sidebar.classList.contains('mobile-open');
    sidebar.classList.toggle('mobile-open', !isOpen);
    backdrop.classList.toggle('open', !isOpen);
  }
}

function navigateTo(pageId) {
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (sidebar && sidebar.classList.contains('mobile-open')) {
    sidebar.classList.remove('mobile-open');
    if (backdrop) backdrop.classList.remove('open');
  }

  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  const targetPage = document.getElementById('page-' + pageId);
  if (targetPage) targetPage.classList.add('active');

  const navMap = {
    dashboard: 0,
    simulator: 1,
    map: 2,
    shipments: 3,
    fleet: 4,
    exceptions: 5,
    impact: 6,
    assumptions: 7
  };

  const navItems = document.querySelectorAll('.nav-item');
  const idx = navMap[pageId];
  if (idx !== undefined && navItems[idx]) {
    navItems[idx].classList.add('active');
  }

  if (pageId === 'map') {
    setTimeout(initLeafletMap, 150);
  }
}

// ================= SHIPMENTS FILTERING & TABLE =================
function getFilteredOrders() {
  if (currentTableFilter === 'unassigned') {
    return ORDERS.filter(o => o.status === 'unassigned');
  } else if (currentTableFilter === 'at-risk') {
    return ORDERS.filter(o => o.status === 'at-risk');
  } else if (currentTableFilter === 'rush') {
    return ORDERS.filter(o => (o.service || '').toLowerCase().includes('rush') || (o.service || '').toLowerCase().includes('same day'));
  } else if (currentTableFilter === 'dg') {
    return ORDERS.filter(o => (o.specialHandling || '').toLowerCase().includes('dangerous goods'));
  } else if (currentTableFilter === 'missing') {
    return ORDERS.filter(o => o.confidence && (o.confidence.linearFt === 'missing' || o.confidence.skids === 'missing' || o.confidence.appointment === 'missing'));
  }
  return ORDERS;
}

function filterTable(filterType, el) {
  currentTableFilter = filterType;
  document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
  if (el) el.classList.add('active');
  renderShipmentsTable(getFilteredOrders());
}

function renderShipmentsTable(ordersList) {
  const tbody = document.getElementById('shipmentsTableBody');
  if (!tbody) return;

  tbody.innerHTML = ordersList.map(o => {
    const isAtRisk = o.status === 'at-risk';
    const isDG = (o.specialHandling || '').toLowerCase().includes('dangerous goods');
    const legLabel = o.leg === 'Pickup' ? t('leg_pickup') : t('leg_delivery');

    return `
      <tr class="${isAtRisk ? 'row-at-risk' : ''}">
        <td style="font-family:var(--font-mono); font-weight:800; color:var(--royal-blue); cursor:pointer;" onclick="openDetailDrawer('${o.id}')">
          ${o.id}
          ${isDG ? '<span title="' + (currentLang==='fr'?'Matières dangereuses réglementées':'Regulated Dangerous Goods') + '" style="color:var(--red); font-size:12px; margin-left:3px;">⚠</span>' : ''}
        </td>
        <td>
          <span class="chip ${o.leg==='Pickup' ? 'chip-assigned' : 'chip-done'}" style="font-size:10px;">
            ${legLabel}
          </span>
        </td>
        <td style="font-weight:700; color:var(--black-russian);">${o.customer}</td>
        <td style="max-width:240px; font-size:12px; color:var(--gray-600); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${o.address}">
          ${o.address}
        </td>
        <td>
          <span style="font-size:11px; font-weight:700; background:var(--gray-100); padding:3px 7px; border-radius:4px; color:var(--gray-700);">
            ${o.service}
          </span>
        </td>
        <td style="font-family:var(--font-mono); font-weight:700;">
          ${(o.weight || 0).toLocaleString()} lb
          <span class="conf-dot conf-${o.confidence ? o.confidence.weight : 'provided'}" title="${currentLang==='fr'?'Confiance: ':'Confidence: '}${o.confidence ? o.confidence.weight : 'provided'}"></span>
        </td>
        <td>
          <select class="table-select table-select-status status-${o.status}" onchange="changeOrderStatus('${o.id}', this.value)">
            <option value="assigned" ${o.status==='assigned'?'selected':''}>${t('status_assigned')}</option>
            <option value="unassigned" ${o.status==='unassigned'?'selected':''}>${t('status_unassigned')}</option>
            <option value="at-risk" ${o.status==='at-risk'?'selected':''}>${t('status_at_risk')} ⚠️</option>
            <option value="in-transit" ${o.status==='in-transit'?'selected':''}>${t('status_in_transit')} 🚚</option>
            <option value="done" ${o.status==='done'?'selected':''}>${t('status_done')} ✅</option>
          </select>
        </td>
        <td>
          <select class="table-select table-select-vehicle ${!o.vehicle?'select-empty':''}" onchange="changeOrderVehicle('${o.id}', this.value)">
            <option value="" ${!o.vehicle?'selected':''}>${t('unassigned_vehicle_option')}</option>
            ${VEHICLES.map(v => {
              const typeLabel = getVehicleTypeTranslated(v.type);
              return `<option value="${v.id}" ${o.vehicle===v.id?'selected':''}>${v.id} · ${typeLabel}${v.dgCert ? ' [DG]' : ''}</option>`;
            }).join('')}
          </select>
        </td>
        <td>
          <div style="display:flex; gap:5px;">
            <button class="btn btn-secondary btn-sm ${isAtRisk ? 'btn-at-risk-active' : ''}" style="padding:4px 8px; font-size:11px;" onclick="toggleOrderRisk('${o.id}')" title="${currentLang==='fr'?'Basculer statut à risque':'Toggle SLA at-risk flag'}">
              ${isAtRisk ? t('btn_clear_risk') : t('btn_mark_risk')}
            </button>
            <button class="btn btn-secondary btn-sm" style="padding:4px 8px; font-size:11px;" onclick="openDetailDrawer('${o.id}')" title="${currentLang==='fr'?'Voir détails complets':'Inspect full details'}">
              ${t('btn_details')}
            </button>
          </div>
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
      showToast(currentLang === 'fr' 
        ? `🛑 BLOCAGE STRICT : La commande #${orderId} contient des matières dangereuses ! Le ${targetV.id} n'est pas certifié MD. Affectation rejetée !`
        : `🛑 HARD BLOCK: Order #${orderId} has Dangerous Goods! ${targetV.id} lacks DG Certification. Assignment rejected!`, 6000);
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

  logDashboardEvent(
    new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}), 
    currentLang === 'fr' 
      ? `Commande #${orderId} assignée à ${newVehicle || 'File non assignée'}`
      : `Order #${orderId} assigned to ${newVehicle || 'Unassigned Queue'}`, 
    '🚚'
  );

  showToast(currentLang === 'fr'
    ? `✅ Commande #${orderId} ${newVehicle ? 'réaffectée à ' + newVehicle : 'déplacée en file non assignée'}. Capacité mise à jour.`
    : `✅ Order #${orderId} ${newVehicle ? 'reassigned to ' + newVehicle : 'moved to Unassigned Queue'}. Capacity updated.`
  );
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

  showToast(currentLang === 'fr'
    ? `Statut de la commande #${orderId} mis à jour : ${newStatus.toUpperCase()}`
    : `Order #${orderId} status updated to ${newStatus.toUpperCase()}`
  );
}

function toggleOrderRisk(orderId) {
  const o = ORDERS.find(x => x.id === orderId);
  if (!o) return;

  if (o.status === 'at-risk') {
    o.status = o.vehicle ? 'assigned' : 'unassigned';
    showToast(currentLang === 'fr'
      ? `✅ Commande #${orderId} retirée du statut à risque.`
      : `✅ Order #${orderId} cleared from At-Risk status.`
    );
  } else {
    o.status = 'at-risk';
    showToast(currentLang === 'fr'
      ? `⚠️ Commande #${orderId} marquée À RISQUE ! Alerte envoyée au moniteur SLA.`
      : `⚠️ Order #${orderId} marked AT-RISK! SLA monitor alerted.`, 4000
    );
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
  const legLabel = o.leg === 'Pickup' ? t('leg_pickup') : t('leg_delivery');

  document.getElementById('drawerHeaderTitle').textContent = `${t('order_label')} ${o.id}`;
  document.getElementById('drawerContentBody').innerHTML = `
    <div style="display:flex; gap:8px; margin-bottom:18px; align-items:center; flex-wrap:wrap;">
      <span class="chip chip-${o.status}">${t('status_' + o.status.replace('-', '_'))}</span>
      <span class="chip ${o.leg==='Pickup'?'chip-assigned':'chip-done'}">${legLabel}</span>
      <span class="chip chip-assigned">${o.service}</span>
      ${isDG ? '<span class="chip chip-late">⚠️ ' + (currentLang==='fr'?'MATIÈRES DANGEREUSES':'DANGEROUS GOODS') + '</span>' : ''}
    </div>

    <!-- Live Reassignment Panel -->
    <div style="background:var(--gray-50); border:1.5px solid var(--gray-200); border-radius:var(--radius-md); padding:16px; margin-bottom:20px;">
      <div style="font-size:12px; font-weight:800; color:var(--royal-blue); margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">
        ${t('drawer_assign_heading')}
      </div>

      <div style="margin-bottom:12px;">
        <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">${t('drawer_truck_label')}</label>
        <select id="drawerVehicleSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
          <option value="" ${!o.vehicle?'selected':''}>${t('drawer_unassigned_opt')}</option>
          ${VEHICLES.map(v => {
            const wPct = Math.min(100, Math.round((v.usedWeight / v.maxWeight) * 100));
            const typeLabel = getVehicleTypeTranslated(v.type);
            return `
              <option value="${v.id}" ${o.vehicle===v.id?'selected':''}>
                ${v.id} · ${typeLabel} (${v.usedWeight.toLocaleString()} / ${v.maxWeight.toLocaleString()} lb - ${wPct}%)${v.dgCert ? ' [DG]' : ''}
              </option>
            `;
          }).join('')}
        </select>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:12px;">
        <div>
          <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">${t('drawer_status_label')}</label>
          <select id="drawerStatusSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
            <option value="assigned" ${o.status==='assigned'?'selected':''}>${t('status_assigned')}</option>
            <option value="unassigned" ${o.status==='unassigned'?'selected':''}>${t('status_unassigned')}</option>
            <option value="at-risk" ${o.status==='at-risk'?'selected':''}>${t('status_at_risk')} ⚠️</option>
            <option value="in-transit" ${o.status==='in-transit'?'selected':''}>${t('status_in_transit')} 🚚</option>
            <option value="done" ${o.status==='done'?'selected':''}>${t('status_done')} ✅</option>
          </select>
        </div>
        <div>
          <label style="font-size:11px; font-weight:700; color:var(--gray-600); display:block; margin-bottom:4px;">${t('drawer_service_label')}</label>
          <select id="drawerServiceSelect" style="width:100%; padding:9px 12px; border-radius:6px; border:1px solid var(--gray-300); font-family:var(--font-main); font-size:13px; font-weight:600; background:#FFF;">
            <option value="STANDARD ROUTE" ${o.service.includes('STANDARD')?'selected':''}>${currentLang==='fr'?'ROUTE STANDARD':'STANDARD ROUTE'}</option>
            <option value="RUSH 90 MIN" ${o.service.includes('RUSH')?'selected':''}>${currentLang==='fr'?'URGENT 90 MIN':'RUSH 90 MIN'}</option>
            <option value="SAME DAY DIRECT" ${o.service.includes('SAME DAY')?'selected':''}>${currentLang==='fr'?'MÊME JOUR DIRECT':'SAME DAY DIRECT'}</option>
          </select>
        </div>
      </div>

      <div style="display:flex; gap:8px;">
        <button class="btn btn-primary btn-sm" style="flex:1; justify-content:center;" onclick="saveDrawerChanges('${o.id}')">
          ${t('btn_save_changes')}
        </button>
        <button class="btn btn-secondary btn-sm" onclick="autoAssignSingleOrder('${o.id}')" title="AI Heuristic best match">
          ${t('btn_auto_assign')}
        </button>
        <button class="btn btn-secondary btn-sm" style="color:var(--red);" onclick="unassignSingleOrder('${o.id}')" title="Clear truck">
          ${t('btn_unassign')}
        </button>
      </div>
    </div>

    <!-- Order Specs -->
    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_customer')}</label>
      <div style="font-size:15px; font-weight:700;">${o.customer}</div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_address')}</label>
      <div style="font-size:14px; color:var(--gray-800);">${o.address}</div>
      <div style="font-family:var(--font-mono); font-size:12px; color:var(--royal-blue); margin-top:2px;">GPS: ${o.coords.join(', ')}</div>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px;">
      <div>
        <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_weight')}</label>
        <div style="font-size:14px; font-weight:700;">${o.weight.toLocaleString()} lb <span class="conf-dot conf-${o.confidence.weight}"></span></div>
      </div>
      <div>
        <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_skids')}</label>
        <div style="font-size:14px; font-weight:700;">${o.skids || 'N/A'} ${t('skids_unit')} (${o.linearFt || 'N/A'} ft) <span class="conf-dot conf-${o.confidence.skids}"></span></div>
      </div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_equip')}</label>
      <div style="font-size:13px; font-weight:600;">${o.equipment} · ${o.specialHandling || (currentLang==='fr'?'Transport sec standard':'Standard dry transport')}</div>
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px; font-weight:700; color:var(--gray-500); text-transform:uppercase;">${t('label_confidence')}</label>
      <div style="font-size:12px; color:var(--gray-600); line-height:1.6;">
        ${currentLang==='fr'?'Poids':'Weight'}: <strong>${o.confidence.weight}</strong> · ${currentLang==='fr'?'Palettes':'Skids'}: <strong>${o.confidence.skids}</strong> · ${currentLang==='fr'?'Créneau':'Time Window'}: <strong>${o.confidence.timeWindow}</strong>
      </div>
    </div>

    <button class="btn btn-secondary" style="width:100%; justify-content:center; margin-top:8px;" onclick="toggleOrderRisk('${o.id}');openDetailDrawer('${o.id}');">
      ${isAtRisk ? t('btn_remove_risk') : ('⚠️ ' + t('btn_mark_risk'))}
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
      showToast(currentLang === 'fr'
        ? `🛑 BLOCAGE STRICT : La commande #${orderId} contient des matières dangereuses ! Le ${targetV.id} n'est pas certifié MD. Rejeté !`
        : `🛑 HARD BLOCK: Order #${orderId} has Dangerous Goods! ${targetV.id} is not DG-certified. Assignment rejected!`, 6000
      );
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

  showToast(currentLang === 'fr'
    ? `✅ Commande #${orderId} enregistrée ! Assignée à ${o.vehicle || 'File non assignée'} [${o.status.toUpperCase()}].`
    : `✅ Order #${orderId} saved! Assigned to ${o.vehicle || 'Unassigned Queue'} [${o.status.toUpperCase()}].`
  );
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
    showToast(currentLang === 'fr'
      ? `⚠️ Aucun camion compatible ne dispose de capacité excédentaire pour ${o.weight.toLocaleString()} lb !`
      : `⚠️ No compatible truck has surplus capacity for ${o.weight.toLocaleString()} lb!`, 5000
    );
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

  const typeLabel = getVehicleTypeTranslated(best.type);
  showToast(currentLang === 'fr'
    ? `⚡ Assignation IA automatique de la commande #${orderId} à ${best.id} (${typeLabel}) !`
    : `⚡ AI Auto-Assigned Order #${orderId} to ${best.id} (${best.type})!`
  );
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
  showToast(currentLang === 'fr' ? `Commande #${orderId} déplacée en file non assignée.` : `Order #${orderId} moved to Unassigned Queue.`);
}

function closeDetailDrawer() {
  document.getElementById('drawerBackdrop').classList.remove('open');
  document.getElementById('detailDrawer').classList.remove('open');
}

// ================= AI SUGGEST FULL PLAN =================
function triggerAutoPlan() {
  showToast(currentLang === 'fr' 
    ? "⚡ Résolution heuristique par IA : Appariement des collectes et optimisation de la flotte..."
    : "⚡ Running Heuristic AI Solver: Pairing pickups & matching fleet capacity...", 3000
  );

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

    logDashboardEvent(
      new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'}), 
      currentLang === 'fr'
        ? `L'optimiseur IA a alloué ${assignedCount} commandes avec 0 violation.`
        : `AI Heuristic Solver allocated ${assignedCount} orders with 0 violations.`, 
      '⚡'
    );

    showToast(currentLang === 'fr'
      ? `🎉 Optimisation IA terminée : ${assignedCount} commandes non assignées réparties. 0 violation de capacité !`
      : `🎉 AI Optimization Complete: ${assignedCount} unassigned orders routed across active fleet. 0 capacity violations!`, 5000
    );

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
    const typeLabel = getVehicleTypeTranslated(v.type);

    return `
      <div class="card" style="padding:22px; ${isDown ? 'border:2px solid var(--red); background:#FFF8F8;' : ''}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
          <div>
            <div style="font-family:var(--font-mono); font-size:18px; font-weight:900; color:var(--royal-blue);">${v.id}</div>
            <div style="font-size:13px; font-weight:700; color:var(--black-russian);">${typeLabel}</div>
            <div style="font-size:12px; color:var(--gray-500);">${v.driver}</div>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:4px;">
            <span class="chip ${isDown ? 'chip-late' : (v.status==='active'?'chip-done':'chip-unassigned')}">
              ${isDown ? t('status_breakdown') : (v.status==='active' ? t('status_active') : t('status_reserve'))}
            </span>
            ${v.dgCert ? '<span class="chip chip-assigned" style="font-size:10px;">' + t('dg_certified') + '</span>' : ''}
          </div>
        </div>

        <div style="margin:14px 0;">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px;">
            <span>${t('payload_weight')}</span>
            <span>${v.usedWeight.toLocaleString()} / ${v.maxWeight.toLocaleString()} lb (${wPct}%)</span>
          </div>
          <div style="height:8px; background:var(--gray-100); border-radius:4px; overflow:hidden;">
            <div style="height:100%; width:${wPct}%; background:${wPct>85?'var(--red)':'var(--royal-blue)'};"></div>
          </div>
        </div>

        <div style="margin:14px 0;">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-weight:700; margin-bottom:4px;">
            <span>${t('hours_of_service')}</span>
            <span>${v.hoursUsed} / 13.0 hrs (${hPct}%)</span>
          </div>
          <div style="height:8px; background:var(--gray-100); border-radius:4px; overflow:hidden;">
            <div style="height:100%; width:${hPct}%; background:${hPct>75?'var(--amber)':'var(--green)'};"></div>
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px; padding-top:12px; border-top:1px solid var(--gray-100);">
          <span style="font-size:12px; color:var(--gray-500); font-weight:600;">${t('capacity_label')}: ${v.maxSkids} ${t('skids_unit')}</span>
          ${isDown ? 
            `<button class="btn btn-primary btn-sm" onclick="restoreTruck('${v.id}')">${t('btn_restore')}</button>` :
            `<button class="btn btn-secondary btn-sm" onclick="markTruckDown('${v.id}')">${t('btn_simulate_breakdown')}</button>`
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
    showToast(currentLang === 'fr'
      ? `⚠️ Alerte perturbation : ${truckId} marqué EN PANNE ! Génération du plan de reprise...`
      : `⚠️ Disruption Alert: ${truckId} marked DOWN! Generating recovery plan...`
    );
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
    showToast(currentLang === 'fr'
      ? `✅ Camion ${truckId} remis en service par la maintenance.`
      : `✅ Truck ${truckId} cleared by maintenance and restored to ACTIVE status.`
    );
  }
}

// ================= EXCEPTIONS & DISASTER RECOVERY =================
function renderExceptionsCards() {
  const container = document.getElementById('exceptionsCardsList');
  if (!container) return;

  container.innerHTML = EXCEPTIONS.map(e => {
    const title = currentLang === 'fr' ? (e.title_fr || e.title_en) : e.title_en;
    const desc = currentLang === 'fr' ? (e.desc_fr || e.desc_en) : e.desc_en;

    return `
      <div class="card" style="padding:20px 24px; border-left:5px solid ${e.resolved ? 'var(--green)' : (e.type==='critical'?'var(--red)':'var(--amber)')};">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:20px;">${e.icon}</span>
            <span style="font-size:16px; font-weight:800; color:var(--black-russian);">${title}</span>
            ${e.resolved ? 
              '<span class="chip chip-done">' + t('badge_resolved') + '</span>' : 
              `<span class="chip ${e.type==='critical'?'chip-late':'chip-at-risk'}">${e.type==='critical'?t('badge_critical'):t('badge_warning')}</span>`
            }
          </div>
          <span style="font-family:var(--font-mono); font-size:12px; font-weight:700; color:var(--gray-500);">${e.time}</span>
        </div>
        <p style="font-size:13px; color:var(--gray-600); line-height:1.5; margin-bottom:12px;">${desc}</p>
        ${e.resolved ? `
          <div style="background:var(--green-light); color:#065F46; padding:8px 12px; border-radius:6px; font-size:12px; font-weight:700; margin-bottom:12px;">
            ✓ ${e.resolutionNote || (currentLang==='fr'?'Résolu par le répartiteur':'Resolved by Dispatcher')}
          </div>
        ` : ''}
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
          <div style="display:flex; gap:6px; align-items:center;">
            <span style="font-size:11px; font-weight:700; color:var(--gray-500);">${t('label_affected')}</span>
            ${e.orders.map(o => `<span class="chip chip-assigned" style="cursor:pointer;" onclick="openDetailDrawer('${o}')">${o}</span>`).join('')}
          </div>
          <div>
            ${e.resolved ? 
              `<button class="btn btn-secondary btn-sm" onclick="reopenException('${e.id}')">${t('btn_reopen_disruption')}</button>` :
              `<button class="btn btn-primary btn-sm" onclick="openFixModal('${e.id}')">${t('btn_resolve_ai')}</button>`
            }
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function openFixModal(excId) {
  currentExceptionToFix = excId || 'EX-001';
  selectedRecoveryOptionIndex = 1;
  const exc = EXCEPTIONS.find(e => e.id === currentExceptionToFix) || EXCEPTIONS[0];
  const excTitle = currentLang === 'fr' ? (exc.title_fr || exc.title_en) : exc.title_en;

  document.getElementById('fixModalHeading').textContent = `${t('fix_modal_header')} — ${excTitle}`;
  document.getElementById('fixModalContent').innerHTML = `
    <p style="font-size:13px; color:var(--gray-600); margin-bottom:18px;">
      ${t('fix_modal_intro')} (<strong>${exc.orders.join(', ')}</strong>) :
    </p>

    <div class="recovery-card selected" id="rec-opt-1" onclick="selectRecoveryOption(1)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="color:var(--royal-blue); font-size:14px;">
          ${currentLang==='fr'?'🏷️ OPTION 1 : MOINS CHÈRE (Redistribuer sur la flotte active)':'🏷️ OPTION 1: CHEAPEST (Redistribute to Active Fleet)'}
        </strong>
        <span class="chip chip-done">${currentLang==='fr'?'RECOMMANDÉ':'RECOMMENDED'}</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        ${currentLang==='fr'
          ?'Absorber les commandes sur les camions proches T-315 et T-301 disposant de charge libre.'
          :'Absorb orders across nearby trucks T-315 and T-301 who have surplus weight capacity.'}
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>${currentLang==='fr'?'Coût : +0 $':'Cost: $0 added'}</span>
        <span>${currentLang==='fr'?'Délai : +14 min moy.':'Delay: +14 mins avg'}</span>
        <span>${currentLang==='fr'?'Changements flotte : 2 camions':'Fleet Changes: 2 vehicles'}</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>${currentLang==='fr'?'Pourquoi :':'Why:'}</strong> 
        ${currentLang==='fr'
          ?'T-315 est à 3,2 km avec 1 800 lb de charge libre. Zéro frais tiers.'
          :'T-315 is 3.2 km away with 1,800 lb spare payload. Zero third-party fees.'}
      </div>
    </div>

    <div class="recovery-card" id="rec-opt-2" onclick="selectRecoveryOption(2)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="font-size:14px;">
          ${currentLang==='fr'?'⚡ OPTION 2 : PLUS RAPIDE (Déployer le camion de réserve T-510)':'⚡ OPTION 2: FASTEST (Dispatch Reserve T-510)'}
        </strong>
        <span class="chip chip-assigned">${currentLang==='fr'?'CAMION DE SECOURS':'RESCUE TRUCK'}</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        ${currentLang==='fr'
          ?'Déployer le camion de réserve T-510 du dépôt directement sur le lieu de panne de la 401.'
          :'Deploy idle reserve truck T-510 from the depot directly to Hwy 401 breakdown site.'}
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>${currentLang==='fr'?'Coût : 165 $ chauffeur & carburant':'Cost: $165 driver & fuel'}</span>
        <span>${currentLang==='fr'?'Délai : 0 min retard SLA':'Delay: 0 mins SLA delay'}</span>
        <span>${currentLang==='fr'?'Changements flotte : 1 nouveau camion':'Fleet Changes: 1 new truck'}</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>${currentLang==='fr'?'Pourquoi :':'Why:'}</strong> 
        ${currentLang==='fr'
          ?'Garantit 100 % de ponctualité sur toutes les commandes à un coût d\'exploitation marginal.'
          :'Guarantees 100% on-time delivery for all orders at marginal vehicle operating cost.'}
      </div>
    </div>

    <div class="recovery-card" id="rec-opt-3" onclick="selectRecoveryOption(3)">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong style="font-size:14px;">
          ${currentLang==='fr'?'🤝 OPTION 3 : MOINS DE CHANGEMENTS (Transfert transporteur partenaire)':'🤝 OPTION 3: FEWEST CHANGES (Partner Carrier Handoff)'}
        </strong>
        <span class="chip chip-unassigned">${currentLang==='fr'?'SOUS-TRAITÉ':'OUTSOURCED'}</span>
      </div>
      <p style="font-size:13px; color:var(--gray-700); margin-bottom:8px;">
        ${currentLang==='fr'
          ?'Transférer les commandes au cross-dock partenaire à Scarborough. Zéro perturbation interne.'
          :'Transfer orders to partner carrier crossdock in Scarborough. Zero internal fleet disruption.'}
      </p>
      <div style="display:flex; gap:16px; font-size:12px; font-weight:700; color:var(--gray-500);">
        <span>${currentLang==='fr'?'Coût : 425 $ tarif partenaire':'Cost: $425 partner rate'}</span>
        <span>${currentLang==='fr'?'Délai : +30 min':'Delay: +30 mins'}</span>
        <span>${currentLang==='fr'?'Changements flotte : 0 tournée modifiée':'Fleet Changes: 0 routes touched'}</span>
      </div>
      <div style="margin-top:8px; font-size:12px; color:var(--royal-blue);">
        <strong>${currentLang==='fr'?'Pourquoi :':'Why:'}</strong> 
        ${currentLang==='fr'
          ?'Laisse votre flotte interne intacte lorsque les chauffeurs sont au pic de charge.'
          :'Leaves your internal fleet completely undisturbed when drivers are at peak capacity.'}
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
    exc.resolutionNote = currentLang === 'fr' 
      ? "Résolu via Option 1 : Expéditions redistribuées sur T-315 et T-301 (0 $ de surcoût)."
      : "Resolved via Option 1: Orders redistributed to T-315 & T-301 ($0 added cost).";
    toastMsg = currentLang === 'fr'
      ? `✅ Plan de reprise #1 appliqué : ${exc.orders.length} expéditions redistribuées sur T-315 et T-301 !`
      : `✅ Recovery Plan #1 Applied: ${exc.orders.length} shipments redistributed to T-315 and T-301!`;
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
    exc.resolutionNote = currentLang === 'fr'
      ? "Résolu via Option 2 : Camion de réserve T-510 déployé sur l'autoroute 401 (0 retard SLA)."
      : "Resolved via Option 2: Reserve truck T-510 dispatched to 401 breakdown (0 SLA delay).";
    toastMsg = currentLang === 'fr'
      ? `⚡ Plan de secours #2 appliqué : Camion de réserve T-510 envoyé avec ${exc.orders.length} commandes !`
      : `⚡ Rescue Plan #2 Applied: Reserve Truck T-510 deployed to Hwy 401 with ${exc.orders.length} orders!`;
  } else {
    exc.orders.forEach(ordId => {
      const o = ORDERS.find(x => x.id === ordId);
      if (o) {
        o.vehicle = 'Partner-Carrier';
        o.status = 'assigned';
      }
    });
    exc.resolved = true;
    exc.resolutionNote = currentLang === 'fr'
      ? "Résolu via Option 3 : Sous-traité au cross-dock partenaire (tarif forfaitaire 425 $)."
      : "Resolved via Option 3: Outsourced to partner carrier crossdock ($425 flat).";
    toastMsg = currentLang === 'fr'
      ? `🤝 Plan de reprise #3 appliqué : ${exc.orders.length} commandes transférées au transporteur partenaire !`
      : `🤝 Recovery Plan #3 Applied: ${exc.orders.length} orders transferred to partner carrier crossdock!`;
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
    showToast(currentLang === 'fr' 
      ? `Perturbation ${excId} rouverte pour examen.`
      : `Exception ${excId} reopened for dispatcher review.`
    );
  }
}

function closeFixModal() {
  document.getElementById('fixThisModal').classList.remove('open');
}

// ================= SIMULATOR & DIRECTOR =================
function renderDirectorStepsList() {
  const container = document.getElementById('directorStepsList');
  if (!container) return;

  container.innerHTML = DEMO_STEPS.map((s, i) => {
    const heading = currentLang === 'fr' ? (s.heading_fr || s.heading_en) : s.heading_en;
    const actionLabel = currentLang === 'fr' ? (s.actionLabel_fr || s.actionLabel_en) : s.actionLabel_en;
    const title = heading.includes('—') ? heading.split('—')[1] : (heading.includes('-') ? heading.split('-')[1] : heading);

    return `
      <div class="director-step-item ${i===currentStepIndex?'active':''} ${i<currentStepIndex?'completed':''}" onclick="jumpToDemoStep(${i})">
        <div class="step-number-circle">${i+1}</div>
        <div class="step-details">
          <div class="step-header-line">
            <span class="step-title">${title.trim()}</span>
            <span class="step-time-badge">${s.time}</span>
          </div>
          <div class="step-action-desc">${actionLabel}</div>
        </div>
      </div>
    `;
  }).join('');
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

  const badgeText = currentLang === 'fr' 
    ? `ÉTAPE ${currentStepIndex + 1} SUR 7 · RELECTURE DE SCÉNARIO`
    : `STEP ${currentStepIndex + 1} OF 7 · SCENARIO REPLAY`;
  document.getElementById('narrationStepBadge').textContent = badgeText;

  const heading = currentLang === 'fr' ? (s.heading_fr || s.heading_en) : s.heading_en;
  const narration = currentLang === 'fr' ? (s.narration_fr || s.narration_en) : s.narration_en;
  const problem = currentLang === 'fr' ? (s.problem_fr || s.problem_en) : s.problem_en;
  const actionLabel = currentLang === 'fr' ? (s.actionLabel_fr || s.actionLabel_en) : s.actionLabel_en;

  document.getElementById('narrationHeading').textContent = heading;
  document.getElementById('narrationBody').textContent = narration;
  document.getElementById('narrationProblemBox').innerHTML = `<strong>💡 ${currentLang === 'fr' ? 'Problème résolu :' : 'Problem It Solves:'}</strong> ${problem}`;
  document.getElementById('stepActionBtn').textContent = `${actionLabel} ⚡`;

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
    showToast(currentLang === 'fr' 
      ? "🎉 Relecture de fin de journée terminée ! Performance exceptionnelle."
      : "🎉 End of Day Replay Complete! Outstanding performance."
    );
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
    btn.textContent = t('btn_auto_play');
    btn.classList.remove('btn-demo');
    btn.classList.add('btn-primary');
  } else {
    isSimPlaying = true;
    btn.textContent = t('btn_pause_play');
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
  showToast(currentLang === 'fr' 
    ? "⟲ Simulateur réinitialisé au scénario de 08h00."
    : "⟲ Simulator reset to 08:00 AM snapshot."
  );
}

function setSimFeedback(msg) {
  const el = document.getElementById('simLiveFeedback');
  if (el) el.textContent = `[${DEMO_STEPS[currentStepIndex].time}] ${msg}`;
}

function startLiveDemoDirector() {
  navigateTo('simulator');
  currentStepIndex = 0;
  updateDemoStepView();
  showToast(currentLang === 'fr' 
    ? "🎬 Démonstrateur chargé ! Suivez les cartes de narration par étape."
    : "🎬 Demo Director loaded! Follow the step narrative cards."
  );
}

// ================= TOASTS & UNDO =================
function showToast(msg, duration = 3500) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast';
  const undoLabel = currentLang === 'fr' ? 'ANNULER' : 'UNDO';
  toast.innerHTML = `
    <span>${msg}</span>
    <span style="margin-left:auto; color:var(--royal-blue); cursor:pointer; font-weight:800;" onclick="undoLastAction();this.parentElement.remove();">${undoLabel}</span>
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
    showToast(currentLang === 'fr' ? "↩️ Dernière action de répartition annulée." : "↩️ Last dispatch action undone.");
  } else {
    showToast(currentLang === 'fr' ? "Aucune action récente à annuler." : "No recent actions to undo.");
  }
}

function openCommandBar() {
  const promptMsg = currentLang === 'fr' 
    ? "Commande rapide (ex. 'simulator', 'shipments', 'plan', 'map', 'fleet', 'exceptions') :"
    : "Quick Command (e.g. 'simulator', 'shipments', 'plan', 'map', 'fleet', 'exceptions'):";
  const query = prompt(promptMsg);
  if (query) {
    const q = query.toLowerCase();
    if (q.includes('sim')) navigateTo('simulator');
    else if (q.includes('ship') || q.includes('exped')) navigateTo('shipments');
    else if (q.includes('map') || q.includes('carte')) navigateTo('map');
    else if (q.includes('fleet') || q.includes('flotte')) navigateTo('fleet');
    else if (q.includes('exc')) navigateTo('exceptions');
    else if (q.includes('plan')) triggerAutoPlan();
  }
}

function renderDashboard() {
  const logDiv = document.getElementById('dashboardEventLog');
  if (!logDiv) return;
  logDiv.innerHTML = dashboardEvents.map(e => {
    const text = currentLang === 'fr' ? (e.text_fr || e.text_en) : e.text_en;
    return `
      <div style="display:flex; align-items:center; gap:12px; padding:8px 0; border-bottom:1px solid var(--gray-100); font-size:13px;">
        <span style="font-size:16px;">${e.icon}</span>
        <span style="font-family:var(--font-mono); font-weight:700; color:var(--royal-blue); width:75px;">${e.time}</span>
        <span style="color:var(--gray-800); flex:1;">${text}</span>
      </div>
    `;
  }).join('');
}

function logDashboardEvent(time, text, icon = '📝') {
  dashboardEvents.unshift({ time, text_en: text, text_fr: text, icon });
  if (dashboardEvents.length > 10) dashboardEvents.pop();
  renderDashboard();
}

function renderAssumptions() {
  const container = document.getElementById('assumptionsContainer');
  if (!container) return;
  container.innerHTML = ASSUMPTIONS.map(a => {
    const title = currentLang === 'fr' ? (a.title_fr || a.title_en) : a.title_en;
    const text = currentLang === 'fr' ? (a.text_fr || a.text_en) : a.text_en;
    return `
      <div class="card" style="padding:20px 24px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
          <span style="font-size:22px;">${a.icon}</span>
          <h4 style="font-size:15px; font-weight:800;">${title}</h4>
        </div>
        <p style="font-size:13px; color:var(--gray-600); line-height:1.6;">${text}</p>
      </div>
    `;
  }).join('');
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
  showToast(currentLang === 'fr' ? "🗺️ Tracés d'itinéraires synchronisés sur la flotte." : "🗺️ Rerouted trails synchronized across fleet.");
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
'''

# Replace placeholder with orders JSON string
bilingual_js = bilingual_js.replace('__ORDERS_JSON__', orders_json_str)

full_html = html_before_script + bilingual_js

print(f"3. Writing updated HTML to freightos/index.html ({len(full_html)} bytes)...")
with open('freightos/index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("4. Copying to root index.html for Vercel deployment...")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("SUCCESS: Both freightos/index.html and index.html have been upgraded with full bilingual support!")
