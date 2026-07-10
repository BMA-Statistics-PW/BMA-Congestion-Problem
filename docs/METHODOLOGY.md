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

| หน่วยนับ | นิยาม | ค่า ณ 10 ก.ค. 2569 |
|---|---|---|
| **รายการรายปี (records)** | แถวข้อมูลของแต่ละปี จุดที่ติดตามต่อเนื่องจะปรากฏซ้ำทุกปีที่ติดตาม | 2566 = 266 · 2567 = 127 · 2568 = 77 (รวม 470) |
| **จุดจริง (unique locations)** | จุดพิกัดเดียวกัน (ละติจูด/ลองจิจูด ตรงกันที่ 6 ตำแหน่งทศนิยม) นับเป็นหนึ่ง | จุดติดตามปี 2567+2568 = **156** (204 รายการ − ต่อเนื่อง 48) |
| **สถานะจุดจริง** | ใช้สถานะ **ปีล่าสุด** ของจุดนั้น | เสร็จสิ้น 133 (85.3%) · บางส่วน 15 · ติดปัญหาดำเนินการ 8 |

ข้อกำหนดเพิ่มเติม:

- **ห้ามรวมสถิติสถานะสองปีเป็นก้อนเดียว** เพราะจุดต่อเนื่อง 48 จุดจะถูกนับซ้ำ — รายงานแยกรายปี หรือใช้ฐานจุดจริงเท่านั้น
- **ความคืบหน้าเฉลี่ย (mean progress)** เป็นแบบ milestone-based ให้น้ำหนักเท่ากันทุกจุด และรายงาน**แยกรายปีเท่านั้น** (2567 = 86.1% · 2568 = 76.9%)
- คำเรียกกลุ่มสถานะ: ใช้ **"ติดปัญหาดำเนินการ"** แทน "ยังไม่เริ่ม" และใช้ **"นอกอำนาจ กทม."** สำหรับจุดของหน่วยงานอื่น
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

ชีตวิเคราะห์ 01–07, 09–12 เป็นผลลัพธ์ pipeline สถิติรุ่นก่อน (สถิติเชิงอนุมาน, KDE, DBSCAN, K-Means) เก็บไว้เป็น methodology snapshot — dashboard ใช้เฉพาะ 11_Corridors (snapshot) และ 13_Pending_Update ซึ่ง rebuild_data.py สร้างใหม่อัตโนมัติจากจุดจริงที่สถานะปีล่าสุดยังไม่ 100% พร้อมเหตุผลจากคอลัมน์หมายเหตุของไฟล์ต้นทาง

## Portfolio Scope

This repository is prepared for portfolio communication and demonstration.
Use governed operational datasets for official internal reporting.

---
© Prapawadee_W. · Statistics & Research Group, Policy & Planning Division, Traffic and Transportation Department, BMA
