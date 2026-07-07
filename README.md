# BMA Congestion Analysis — Spatial Lineage Dashboard

**FY 2566–2568 (2023–2025)** · Portfolio Project by © Prapawadee W.

[![Made by](https://img.shields.io/badge/Made_by-Prapawadee_W.-0B3B6F)](#)
[![Org](https://img.shields.io/badge/Org-BMA_Traffic_%26_Transportation-1E5AA6)](#)
[![Stack](https://img.shields.io/badge/Stack-Python_%7C_Chart.js_%7C_Leaflet-4A90E2)](#)
[![Map](https://img.shields.io/badge/Map-OpenStreetMap_(ODbL)-success)](https://www.openstreetmap.org/copyright)

---

## 📋 ภาพรวม / Overview

Dashboard เชิงโต้ตอบ (Interactive) เพื่อแสดงผลการวิเคราะห์จุดปัญหาการจราจรติดขัดในกรุงเทพมหานคร
ครอบคลุมปีงบประมาณ 2566–2568 โดยมีจุดเน้น:

- **Multi-agency intervention** — แสดงบทบาทของหน่วยงานหลายฝ่ายในการแก้ไขปัญหา
- **Spatial Lineage Story** — เล่าวิวัฒนาการของ inventory จากการร้องเรียน → กรอง TE → focused
- **Persistent Hotspots & Corridors** — ระบุพื้นที่ที่ต้องการ priority
- **Methodology Showcase** — แสดงเทคนิคทางสถิติและเครื่องมือที่ใช้

## 🗂 บริบทของข้อมูล / Data Context

| ปีงบประมาณ | จำนวนจุด | แหล่งข้อมูล | ขอบเขต |
|---|---|---|---|
| **2566** | 266 | เรื่องร้องเรียน · บช.น. · สำนักงานเขต | กทม. + นอก กทม. |
| **2567** | 127 | วิเคราะห์ Traffic Engineering (สจส. × สนข.) | กทม. + นอก กทม. |
| **2568** | 77 | TE วิเคราะห์เพิ่มเติม | เน้น กทม. |

**สำคัญ:** การลดลงของจำนวนจุดไม่ใช่ตัวชี้ "การแก้สำเร็จ" ทั้งหมด แต่เป็นการ refine inventory ตามมิติวิศวกรรมจราจรอย่างเป็นระบบ

## 🔄 อัปเดตข้อมูลล่าสุด / Latest Data Update (ก.ค. 2569)

ปรับสถานะ 21 จุดตามรายงาน **"จุดฝืดที่ยังไม่ได้ดำเนินการ"** (สจส.):

| กลุ่มสถานะ | จำนวนจุด | หมายเหตุ |
|---|---|---|
| ✅ แก้ไขแล้วเสร็จ | 5 | ปรับ progress เป็น 100% ในชุดข้อมูล |
| 🔨 กำลังดำเนินการ (สนย.) | 1 | ปรับปรุงสะพานข้ามคลองแสนแสบ |
| 🚧 ติดพื้นที่ก่อสร้างรถไฟฟ้า (ม่วง/ส้ม) | 5 | รอคืนผิวจราจรจาก รฟม. |
| 🏛 นอกอำนาจ กทม. / ติดหน่วยงานอื่น | 3 | ทช. · กทพ. · ตำรวจ (สน.วิภาวดี) |
| ⛔ ข้อจำกัดกายภาพ | 3 | ถนนแคบ/ช่องลอดต่ำ ไม่เอื้อต่อการแก้ไข |
| 💰 รองบประมาณปี 2569 (ไฟ adaptive) | 2 | อยู่ระหว่างอนุมัติจ้าง |
| 👮 มาตรการชั่วคราว (กวดขันจราจร) | 2 | ยังไม่แก้ที่สาเหตุเชิงกายภาพ |

> **ข้อค้นพบ:** จุดค้างดำเนินการส่วนใหญ่ติดข้อจำกัดเชิงโครงสร้าง (รถไฟฟ้า/อำนาจหน้าที่/กายภาพ) ไม่ใช่ความล่าช้าของหน่วยดำเนินการ · ดูรายละเอียดที่แท็บ "สถานะ · Status" ใน dashboard และไฟล์ `data/sheets/13_Pending_Update.json`

## 🏛 หน่วยงานดำเนินการ / Implementing Agencies

- **สจส.** — สำนักการจราจรและขนส่ง (หน่วยหลัก)
- **สนย.** — สำนักการโยธา (งานก่อสร้าง/โครงสร้าง)
- **สำนักเทศกิจ** — กวดขันความเป็นระเบียบ
- **สนข. (50 เขต)** — รับเรื่อง/ประสานในพื้นที่
- **บช.น.** — บังคับใช้กฎจราจร

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/BMA-Statistics-PW/BMA-Congestion-Problem.git
cd BMA-Congestion-Problem

# Run local static server
python -m http.server 8080
# Open http://localhost:8080
```

## 📁 Project Structure

```
BMA-Congestion-Problem/
├── index.html                  # Main interactive dashboard (this file)
├── data/
│   ├── combined_data.json      # Consolidated 3-year dataset
│   ├── all_points.geojson      # Geo-located points (470)
│   └── sheets/
│       ├── 10_Spatial_Lineage.json
│       ├── 11_Corridors.json
│       └── ...                 # Other sheet exports
├── data.xlsx                   # Source Excel workbook
├── scripts/
│   └── convert_xlsx_to_data.ps1
└── README.md
```

## 🔬 Methodology Highlights

| Method | Tech | Purpose |
|---|---|---|
| **Haversine Distance Matching** | numpy · threshold 250m | Cross-year point lineage |
| **K-Means Clustering** | scikit-learn · k=6 | Solution pattern grouping |
| **DBSCAN Corridor Clustering** | scikit-learn · eps=400m | Corridor identification |
| **Kernel Density Estimation** | scipy.stats · Gaussian | Hot zone detection |
| **Inferential Statistics** | scipy.stats | Spearman ρ, Kruskal-Wallis, χ² |

## 📊 Key Findings

1. **Persistent Hotspots — 23 จุด** ปรากฏใน inventory ทั้ง 3 ปี (Spatial match ≤250m)
2. **25 Persistent Corridors** ที่ active ทั้ง 3 ปี (DBSCAN) — เหมาะกับ corridor-level intervention
3. **Multi-measure approach** (≥3 มาตรการ) มีอัตราความสำเร็จสูงกว่า single-measure อย่างมีนัยสำคัญ (Spearman ρ=0.141, p=0.044)
4. **Zone differences are significant** — Kruskal-Wallis H=19.83, p=0.001 — ควรมีกลยุทธ์เฉพาะโซน

## 🗺 OpenStreetMap Compliance

- Tile source: `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
- Attribution: © OpenStreetMap contributors (ODbL)
- References: [OSM Copyright](https://www.openstreetmap.org/copyright) · [Tile Policy](https://operations.osmfoundation.org/policies/tiles/)

## 👤 About the Analyst

**© Prapawadee W.**
Professional-Level Statistician
กลุ่มงานสถิติและวิจัย กองนโยบายและแผนงาน
สำนักการจราจรและขนส่ง กรุงเทพมหานคร

*Statistics & Research Group, Policy & Planning Division,
Traffic and Transportation Department, Bangkok Metropolitan Administration*

---

## 📜 License & Usage

จัดทำขึ้นเพื่อประโยชน์สาธารณะและสนับสนุนการตัดสินใจเชิงนโยบาย ไม่อนุญาตให้นำไปใช้แสวงหาผลประโยชน์ส่วนบุคคล

For public-sector and research use only. Commercial use not permitted.
