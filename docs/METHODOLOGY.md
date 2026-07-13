# Methodology Note

**BMA Congestion Analysis — FY 2566–2568** · ปรับปรุงล่าสุด 10 ก.ค. 2569

## Objective

Provide an interpretable, policy-facing view of traffic congestion friction points across FY 2566-2568.

## Analytical Framing

1. Inventory by year
2. Spatial carry-over and drop-out between consecutive years
3. Persistent hotspot identification
4. Corridor-level prioritization

## หน่วยนับ / Counting Rules (สำคัญ — ใช้ให้ตรงทุกครั้งที่อ้างอิงตัวเลข)

| หน่วยนับ | นิยาม | ค่า ณ 13 ก.ค. 2569 |
|---|---|---|
| **รายการรายปี (records)** | แถวข้อมูลของแต่ละปี จุดที่ติดตามต่อเนื่องจะปรากฏซ้ำทุกปีที่ติดตาม | 2566 = 266 · 2567 = 127 · 2568 = 77 (รวม 470) |
| **จุดจริง (unique locations / `cluster_id`)** | จุดพิกัดห่างกัน **<20 ม. = จุดเดียวกัน** ยกเว้น (1) พื้นที่ถนนบางบอน รวมเฉพาะชื่อตรงกัน (2) ประเภทปัญหาต่างกันไม่รวมเป็นจุดเดียว — คำนวณใน `scripts/rebuild_data.py` เก็บเป็นฟิลด์ `cluster_id` | รวม 3 ปี = **375 จุด** · จุดติดตามปี 2567+2568 เฉพาะ กทม. = **127** |
| **ฐานคิดเปอร์เซ็นต์** | **เฉพาะจุดของ กทม.** — จุดนอกอำนาจ กทม. (ทล./ทช./กทพ./รฟท.) แสดงแยก ไม่นำมาคิด % | 2567: กทม. 99 (นอกอำนาจ 28) · 2568: กทม. 76 (นอกอำนาจ 1) |
| **สถานะจุดจริง** | ใช้สถานะ **ปีล่าสุด** ของจุดนั้น (ฐาน กทม.) | เสร็จสิ้น 109 (85.8%) · อยู่ระหว่างดำเนินการ 12 (9.4%) · ติดปัญหาอุปสรรค 6 (4.7%) |

ข้อกำหนดเพิ่มเติม:

- **ห้ามรวมสถิติสถานะสองปีเป็นก้อนเดียว** เพราะจุดต่อเนื่อง 48 จุดจะถูกนับซ้ำ — รายงานแยกรายปี หรือใช้ฐานจุดจริง (`cluster_id`) เท่านั้น
- **สถานะรายปีเป็นแบบ point-in-time** ตามไฟล์ต้นทาง (ปี 2567 = สถานะ ณ ปีงบ 2567) — จุดต่อเนื่องที่เสร็จในปี 2568 จะนับเสร็จในสถิติ "จุดจริง" ผ่านกฎสถานะปีล่าสุด
- **ความคืบหน้าเฉลี่ย (mean progress)** เป็นแบบ milestone-based ให้น้ำหนักเท่ากันทุกจุด ฐานเฉพาะ กทม. และรายงาน**แยกรายปีเท่านั้น** (2567 = 82.9% · 2568 = 81.7%)
- **เกณฑ์และคำเรียกสถานะ:** `100%` = **เสร็จสิ้น** · `1–99%` = **อยู่ระหว่างดำเนินการ** · `0%` = **ติดปัญหาอุปสรรค** — ใช้ชุดคำนี้เหมือนกันทุกหน้า และใช้ **"นอกอำนาจ กทม."** สำหรับจุดของหน่วยงานอื่น
- **ตัวอย่างข้อยกเว้นกฎ 20 ม. (PW ยืนยัน 11 ก.ค. 2569):** พาต้าปิ่นเกล้า = 2 จุด (ป้ายรถเมล์ + คอขวด ปัญหาต่อเนื่องกัน) · บางบอน = 2 จุด (คอขวดหน้าตลาด + แยกสุขาภิบาล) · ราชประสงค์ = 2 จุด (ทางแยก + ช่วงถนนพระราม 1 เป็น corridor ต่อเนื่องกัน)
- จุดชื่อคล้ายกันอาจเป็นคนละจุดจริง (เช่น "แยกพญาไท" ≠ "จุดกลับรถใกล้แยกพญาไท", "แยกมักกะสัน" ≠ "แยกหมอเหล็ง") — ตรวจพิกัดก่อนจับคู่เสมอ

## Cross-year Lineage — มี 2 วิธี ต้องระบุวิธีทุกครั้งที่อ้างอิง

1. **Name-based matching** — จับคู่ชื่อจุด (ตัดช่องว่าง) ข้ามปี ใช้ในชีตวิเคราะห์ 12_New & Dropout
2. **Spatial matching (≤250 m, Haversine)** — ใช้ใน dashboard (คำนวณสดทุกครั้งที่เปิดหน้า) และชีต 10_Spatial Lineage

สองวิธีให้ตัวเลขต่างกันได้ (เช่น carry-over จากปี 2566: name-based = 66 จุด, spatial = 62 จุด ในชุดข้อมูลรุ่นก่อน) — **อย่านำตัวเลขสองวิธีมาปนกัน**

## Interpretation Guidance

- A lower count in later years does not necessarily imply full resolution.
- Changes may also reflect filtering criteria, ownership transfer, and scope boundaries.
- **Drop-out ≠ แก้เสร็จ**: จุดปี 2566 ที่ไม่ถูกจับคู่ในปีถัดไป (~200 จุด) อาจอยู่นอกขอบเขต Traffic Engineering หรือส่งต่อหน่วยงานอื่น (ทล./ตำรวจ/รฟม./กปน.) — ห้ามสรุปว่า "ยังไม่ได้ดำเนินการ" โดยไม่ระบุ caveat นี้
- Persistent points and corridors are treated as priority candidates for structural intervention.

## Data Pipeline

`BMA_จุดฝืดรวมปี 2566-2568.xlsx` (คอลัมน์หลักมาตรฐาน 3 ปี) → `scripts/rebuild_data.py` → `data/combined_data.json` = `data/sheets/08_Combined_Data.json` = `data/all_points.geojson` = `data.xlsx` ชีต 08 (ตรงกัน 100%) → dashboard คำนวณ KPI ทั้งหมดสดจากข้อมูล (ไม่มีตัวเลข hard-code)

ชีตวิเคราะห์ 01–07, 09–12 เป็นผลลัพธ์ pipeline สถิติรุ่นก่อน (สถิติเชิงอนุมาน, KDE, DBSCAN, K-Means) เก็บไว้เป็น methodology snapshot — dashboard ใช้เฉพาะ 11_Corridors (snapshot) และ 13_Pending_Update ซึ่ง rebuild_data.py สร้างใหม่อัตโนมัติจากจุดจริงที่สถานะปีล่าสุดยังไม่ 100% (จำแนก 0% = ติดปัญหาอุปสรรค / 1–99% = อยู่ระหว่างดำเนินการ) พร้อมข้อความปัญหาอุปสรรคจากคอลัมน์หมายเหตุของไฟล์ต้นทาง

## Portfolio Scope

This repository is prepared for portfolio communication and demonstration.
Use governed operational datasets for official internal reporting.

---
© Prapawadee_W. · Statistics & Research Group, Policy & Planning Division, Traffic and Transportation Department, BMA
