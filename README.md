# BMA Congestion Analysis — Spatial Lineage Dashboard

**FY 2566–2568 (2023–2025)** · Portfolio Project by © Prapawadee W.

[![Made by](https://img.shields.io/badge/Made_by-Prapawadee_W.-0073ce)](#)
[![Org](https://img.shields.io/badge/Org-BMA_Traffic_%26_Transportation-0d8cd8)](#)
[![Stack](https://img.shields.io/badge/Stack-Python_%7C_Chart.js_%7C_Leaflet-6fa7e3)](#)
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
| **2566** | 266 | เรื่องร้องเรียน · บช.น. · สำนักงานเขต | กทม. + นอกอำนาจ กทม. |
| **2567** | 127 | วิเคราะห์ Traffic Engineering (สจส. × สนข.) | กทม. + นอกอำนาจ กทม. |
| **2568** | 77 | TE วิเคราะห์เพิ่มเติม | เน้น กทม. |

**สำคัญ:** การลดลงของจำนวนจุดไม่ใช่ตัวชี้ "การแก้สำเร็จ" ทั้งหมด แต่เป็นการ refine inventory ตามมิติวิศวกรรมจราจรอย่างเป็นระบบ

## 🔄 อัปเดตข้อมูลล่าสุด / Latest Data Update (10 ก.ค. 2569)

**รอบตรวจทานชุดข้อมูลรวม 3 ปี** (ไฟล์ `BMA_จุดฝืดรวมปี 2566-2568.xlsx` ฉบับแก้ไข):

| รายการปรับปรุง | จำนวน | หมายเหตุ |
|---|---|---|
| 📝 ปรับชื่อจุดให้เป็นมาตรฐานเดียวกัน | 37 จุด | ชื่อสั้น กระชับ สื่อประเภทปัญหา (คอขวด/แยก/ป้ายรถประจำทาง) |
| 📍 แก้ไขพิกัด | 6 จุด | หน้าตลาดคลองเตย (รัชดาภิเษก) · จุดกลับรถลาดพร้าว 130/2 (2 ปี) · ตลาดนัดจตุจักร 2 ถนนสุวินทวงศ์ · จุดกลับรถ รพ.เวชการุณย์รัศมิ์ · จุดกลับรถโตโยต้าภูมิพัฒนา |
| 🔁 ทบทวนสถานะ (progress) | 8 รายการ | จุด 0% ที่เริ่มประสานงานแล้วปรับเป็น 5% (คอขวดถนนหัวหมาก ปี 2567 คงสถานะเสร็จสิ้น 100% ตามรายงาน สจส. — ยืนยัน 10 ก.ค. 2569) |
| 🧭 แยกจุดที่เคยกำกวม | 2 จุด | **"แยกมักกะสัน"** (เสร็จสิ้นปี 2568) ≠ **"แยกหมอเหล็ง"** (ติดแนวรถไฟฟ้าสายสีส้ม) — คนละแยก ห่างกัน ~120 ม. |
| 🏛 ระบุหน่วยงานรับผิดชอบ | 1 จุด | ทางเชื่อมมอเตอร์เวย์–พระราม 9 (สวนหลวง) = **ทล.** |

**สรุปสถิติหลังตรวจทานรอบล่าสุด (ณ 13 ก.ค. 2569 — ไฟล์ "BMA_จุดฝืดรวมปี_2566-2568_ตรวจทาน13กค2569.xlsx"):**

- **เกณฑ์นับจุด (PW ยืนยัน 11 ก.ค. 2569):** จุดพิกัดห่างกัน **<20 ม. = จุดเดียวกัน** (ต่างกันแค่ชื่อ) ยกเว้น (1) พื้นที่ถนนบางบอน — จุดจริงอยู่ชิดกัน รวมเฉพาะชื่อตรงกัน (2) ประเภทปัญหาต่างกัน (ป้ายรถเมล์/คอขวด/ทางแยก/ช่วงถนน/จุดกลับรถ) ไม่รวมเป็นจุดเดียว — เข้ารหัสเป็น `cluster_id` ในทุกชั้นข้อมูล
- **เกณฑ์คิด % (PW ยืนยัน 11 ก.ค. 2569):** จุดของหน่วยงานอื่น (ทล./ทช./กทพ./รฟท.) **ไม่นำมาคิดเปอร์เซ็นต์** — ติดตามเฉพาะจุดของ กทม.
- แถวข้อมูลรวม 3 ปี 470 แถว = **จุดจริงไม่ซ้ำ 375 จุด** · จุดเดียวกันปี 2566↔2567 = 31 จุด · 2567↔2568 = 48 จุด · ครบทั้ง 3 ปี = 13 จุด
- ปี 2567: ทั้งหมด 127 จุด = นอกอำนาจ กทม. 28 + **กทม. 99 จุด → เสร็จสิ้น 66 (66.7%) · อยู่ระหว่างดำเนินการ 30 (30.3%) · ติดปัญหาอุปสรรค 3 (3.0%)** (สถานะ ณ ปีงบประมาณ)
- ปี 2568: ทั้งหมด 77 จุด = นอกอำนาจ กทม. 1 + **กทม. 76 จุด → เสร็จสิ้น 57 (75.0%) · อยู่ระหว่างดำเนินการ 12 (15.8%) · ติดปัญหาอุปสรรค 7 (9.2%)**
- **สรุปรวมจุดจริง 2567+2568 เฉพาะ กทม. (จุดเดียวกันนับ 1, สถานะปีล่าสุด): 127 จุด → เสร็จสิ้น 108 (85.0%) · อยู่ระหว่างดำเนินการ 12 (9.4%) · ติดปัญหาอุปสรรค 7 (5.5%)**
- จุดติดแนวก่อสร้างรถไฟฟ้า 4 จุดจริง: แยกซังฮี้ · คอขวดถนนสามเสนก่อนถึงแยกซังฮี้ (สายสีม่วง) · จุดกลับรถใกล้แยกพญาไท · แยกหมอเหล็ง (สายสีส้ม)
- **เกณฑ์สถานะ:** `0%` = ติดปัญหาอุปสรรค · `1–99%` = อยู่ระหว่างดำเนินการ · `100%` = เสร็จสิ้น — ใช้ชุดคำนี้ทุกหน้าของ dashboard
- หัวข้อ "สถานะจุดที่ยังดำเนินการไม่แล้วเสร็จ" แสดง**จุดจริงคงค้าง 19 จุด (เฉพาะ กทม.)** (ติดปัญหาอุปสรรค 7 · อยู่ระหว่างดำเนินการ 12) พร้อมข้อความปัญหาอุปสรรครายจุดจากคอลัมน์หมายเหตุ — สร้างอัตโนมัติโดย `scripts/rebuild_data.py`
- การตรวจทานรอบนี้: แก้พิกัดจุดปี 2566 จำนวน 16 จุดให้ตรงกับจุดเดียวกันในปี 2567 · เปลี่ยนชื่อ 13 จุด (มาตรฐานเดียวกับปีล่าสุด) · แก้เขต 1 จุด (แยกคลองขวาง → หนองแขม) · แก้พิกัดหมู่บ้านสัมมากร (2566)

### รอบก่อนหน้า (ก.ค. 2569) — ปรับสถานะ 21 จุดตามรายงาน **"จุดฝืดที่ยังไม่ได้ดำเนินการ"** (สจส.):

| กลุ่มสถานะ | จำนวนจุด | หมายเหตุ |
|---|---|---|
| ✅ แก้ไขแล้วเสร็จ | 5 | ปรับ progress เป็น 100% ในชุดข้อมูล |
| 🔨 อยู่ระหว่างดำเนินการ (สนย.) | 1 | ปรับปรุงสะพานข้ามคลองแสนแสบ |
| 🚧 พื้นที่ก่อสร้างรถไฟฟ้า (ม่วง/ส้ม) | 5 | รอคืนผิวจราจรจาก รฟม. |
| 🏛 นอกอำนาจ กทม. / ข้อจำกัดหน่วยงานภายนอก | 3 | ทช. · กทพ. · ตำรวจ (สน.วิภาวดี) |
| ⛔ ข้อจำกัดทางกายภาพ | 3 | ถนนแคบ/ช่องลอดต่ำ ไม่เอื้อต่อการแก้ไข |
| 💰 อยู่ระหว่างของบประมาณ (สัญญาณไฟ adaptive ปี 2569) | 2 | อยู่ระหว่างอนุมัติจ้าง |
| 👮 ใช้มาตรการชั่วคราว (กวดขันจราจร) | 2 | ยังไม่แก้ที่สาเหตุเชิงกายภาพ |

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
├── data.xlsx                   # Source Excel workbook (13 sheets)
├── docs/
│   ├── METHODOLOGY.md          # Counting rules & analytical methodology
│   └── DATA_DICTIONARY.md      # Field definitions (combined_data.json)
├── scripts/
│   ├── rebuild_data.py         # Rebuild all data layers from source xlsx
│   └── convert_xlsx_to_data.ps1
└── README.md
```

### 🔁 การอัปเดตข้อมูลรอบถัดไป / Updating the Data

เมื่อได้ไฟล์รวม 3 ปีฉบับใหม่ ให้รันสคริปต์เดียวจบ — ทุกชั้นข้อมูล (JSON · GeoJSON · data.xlsx ชีต 08/13 · manifest) จะถูกสร้างใหม่ให้ตรงกัน 100% และ dashboard จะคำนวณตัวเลขใหม่เองทั้งหมด:

```bash
python scripts/rebuild_data.py "BMA_จุดฝืดรวมปี 2566-2568.xlsx" .
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

1. **Persistent Hotspots — 22 จุด** ปรากฏใน inventory ทั้ง 3 ปี (Spatial match ≤250m, คำนวณสดจากพิกัดฉบับตรวจทาน 10 ก.ค. 2569)
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
