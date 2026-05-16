# BMA Congestion Problem Dashboard (FY 2566-2568)

## Executive Summary
This repository presents an official portfolio dashboard for congestion friction points in Bangkok,
covering fiscal years 2566-2568 (2023-2025). The objective is to communicate:

- What was collected (inventory)
- What was carried forward and filtered each year
- Where persistent bottlenecks remain
- Which intervention patterns appear to be most effective

Key topline values used in this portfolio:

- FY 2566: 266 points
- FY 2567: 127 points
- FY 2568: 77 points
- Persistent 3-year geo-matched points: 23
- Persistent corridors (DBSCAN): 25

## Portfolio Deliverables
- Formal dashboard page with KPI, trend, zone comparison, and hotspot map
- Policy-oriented findings section in Thai and English
- OpenStreetMap-based geospatial visualization for chronic congestion points
- GitHub Pages-ready static site structure

## Methodology (High-level)
1. Annual point inventory and engineering filtering
2. Cross-year spatial lineage matching (threshold 250m)
3. Corridor clustering via DBSCAN for corridor-level intervention insights
4. Comparative progress analysis by zone and intervention type

## OpenStreetMap Compliance
This project uses OpenStreetMap tiles for interactive visualization and follows attribution requirements.

- Tile source: https://tile.openstreetmap.org/{z}/{x}/{y}.png
- Attribution shown in map control and footer:
  - Data and map tiles copyright OpenStreetMap contributors
  - ODbL notice linked via OpenStreetMap copyright page

References:
- https://www.openstreetmap.org/copyright
- https://operations.osmfoundation.org/policies/tiles/

## Run Locally
Open `index.html` directly in browser, or use a static server.

PowerShell example:

```powershell
# from repository root
python -m http.server 8080
# then open http://localhost:8080
```

## Publish via GitHub Pages
1. Push this repository to GitHub
2. Go to Settings > Pages
3. Source: Deploy from a branch
4. Branch: `main`, folder `/ (root)`
5. Save and wait for deployment

## Data Notes
- This portfolio contains curated dashboard-ready indicators and hotspot coordinates for presentation use.
- For operational reporting, keep master analytical datasets in governed internal storage and update this dashboard from validated exports.

## Owner
Prapawadee W
Statistics and Research Group
Policy and Planning Division
Traffic and Transportation Department, BMA
