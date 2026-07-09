#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_data.py — สร้างชั้นข้อมูลทั้งหมดของ repo BMA-Congestion-Problem
จากไฟล์ต้นทาง "BMA_จุดฝืดรวมปี 2566-2568.xlsx" (คอลัมน์หลักมาตรฐาน 3 ปี)

อัปเดต: data/combined_data.json, data/sheets/08_Combined_Data.json,
        data/all_points.geojson, data.xlsx (ชีต 08, ชื่อจุดชีต 13),
        data/sheets/13_Pending_Update.json (ชื่อจุดมาตรฐาน), data/manifest.json
© Prapawadee_W. · Traffic and Transportation Department, BMA
"""
import json, re, sys, datetime
import openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else "source.xlsx"
REPO = sys.argv[2] if len(sys.argv) > 2 else "."

SHEETS = {2566: '2566 (266 จุด)', 2567: '2567 (127 จุด)', 2568: '2568 (77 จุด)'}
FIELDS = ['year','point_id','point_name','point_type','district','zone','road','cause',
          'peak_time','agency_main','solution_group','progress_pct',
          'sol_traffic_mgmt','sol_enforcement','sol_signal','sol_physical','sol_busbay','sol_cctv',
          'latitude','longitude']
SOL_COLS = {  # ชื่อคอลัมน์ Yes/No รายปี (แผน 6 มาตรการ)
    2567: ['[เฉพาะปี] บริหารจัดการระบบจราจร/ ข้อบังคับการจราจร','[เฉพาะปี] กวดขันวินัยจราจร',
           '[เฉพาะปี] ปรับหรือติดตั้งสัญญาณไฟจราจร','[เฉพาะปี] ปรับลักษณะกายภาพ',
           '[เฉพาะปี] จัดทำ Bus Bay หรือ Bus Priority','[เฉพาะปี] ติดกล้อง CCTV'],
    2568: ['[เฉพาะปี] บริหารจัดการระบบจราจร ข้อบังคับการจราจร','[เฉพาะปี] กวดขันวินัยจราจร',
           '[เฉพาะปี] ปรับ ติดตั้งสัญญาณไฟจราจร','[เฉพาะปี] ปรับกายภาพ',
           '[เฉพาะปี] Bus Bay หรือ Bus Priority','[เฉพาะปี] ติดกล้อง CCTV'],
}

def yn(v):
    s = str(v or '').strip().lower()
    if s == 'yes': return 1.0
    if s == 'no':  return 0.0
    return None

def fnum(v):
    if v is None or str(v).strip() == '': return None
    return float(v)

def stxt(v):
    if v is None: return None
    s = str(v)
    return s if s.strip() != '' else None

def load_rows(wb, year):
    ws = wb[SHEETS[year]]
    hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    out = []
    for raw in ws.iter_rows(min_row=2, values_only=True):
        if raw[0] is None and raw[1] is None: continue
        d = dict(zip(hdr, raw))
        rec = {
            'year': float(year),
            'point_id': float(d['รหัสจุด']),
            'point_name': stxt(d['ชื่อจุด/บริเวณ']),
            'point_type': stxt(d['ประเภทปัญหา']),
            'district': stxt(d['เขต']),
            'zone': stxt(d['กลุ่มเขต/โซน']),
            'road': stxt(d['ถนน']),
            'cause': stxt(d['สาเหตุเบื้องต้น']),
            'peak_time': stxt(d.get('[เฉพาะปี] ช่วงเวลาที่การจราจรติดขัด')) if year == 2566 else None,
            'agency_main': stxt(d['หน่วยงานรับผิดชอบหลัก']),
            'solution_group': stxt(d['กลุ่มแนวทางแก้ไข']),
            'progress_pct': fnum(d['ความคืบหน้า/สถานะ']),
            'latitude': float(d['ละติจูด']),
            'longitude': float(d['ลองจิจูด']),
        }
        if year in SOL_COLS:
            keys = ['sol_traffic_mgmt','sol_enforcement','sol_signal','sol_physical','sol_busbay','sol_cctv']
            for k, col in zip(keys, SOL_COLS[year]):
                rec[k] = yn(d.get(col))
        else:
            for k in ['sol_traffic_mgmt','sol_enforcement','sol_signal','sol_physical','sol_busbay','sol_cctv']:
                rec[k] = None
        out.append({f: rec[f] for f in FIELDS})
    return out

def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    rows = []
    for y in (2566, 2567, 2568):
        rows += load_rows(wb, y)
    counts = {y: sum(1 for r in rows if int(r['year']) == y) for y in (2566, 2567, 2568)}
    assert counts == {2566: 266, 2567: 127, 2568: 77}, counts

    # 1) combined_data.json + 08_Combined_Data.json
    for path in ('data/combined_data.json', 'data/sheets/08_Combined_Data.json'):
        with open(f'{REPO}/{path}', 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)

    # 2) all_points.geojson (properties ไม่มี latitude/longitude)
    feats = []
    for r in rows:
        props = {k: v for k, v in r.items() if k not in ('latitude', 'longitude')}
        feats.append({'type': 'Feature',
                      'geometry': {'type': 'Point', 'coordinates': [r['longitude'], r['latitude']]},
                      'properties': props})
    with open(f'{REPO}/data/all_points.geojson', 'w', encoding='utf-8') as f:
        json.dump({'type': 'FeatureCollection', 'features': feats}, f, ensure_ascii=False, indent=1)

    # 3) data.xlsx — ชีต 08 (header แถว 3, ข้อมูลเริ่มแถว 4)
    wx = openpyxl.load_workbook(f'{REPO}/data.xlsx')
    ws8 = wx['08_Combined Data']
    hdr8 = [ws8.cell(row=3, column=c).value for c in range(1, ws8.max_column + 1)]
    assert hdr8[:20] == FIELDS, hdr8
    if ws8.max_row > 3:
        ws8.delete_rows(4, ws8.max_row - 3)
    for i, r in enumerate(rows, start=4):
        for j, f in enumerate(FIELDS, start=1):
            v = r[f]
            if f in ('year', 'point_id') and v is not None: v = int(v)
            ws8.cell(row=i, column=j, value=v)

    # 4) ชื่อจุดมาตรฐานในชีต 13 + JSON 13 (จับคู่ด้วยพิกัด ~4 ตำแหน่ง + ปี)
    def k4(lat, lon): return (round(float(lat), 4), round(float(lon), 4))
    by_coord = {}
    for r in rows:
        by_coord.setdefault((int(r['year']), k4(r['latitude'], r['longitude'])), r)
    p13 = json.load(open(f'{REPO}/data/sheets/13_Pending_Update.json', encoding='utf-8'))
    renamed = 0
    for rec in p13:
        yrs = [int(y) for y in re.findall(r'25\d\d', str(rec.get('ปี', '')))]
        m = None
        for yr in sorted(yrs, reverse=True):  # ปีล่าสุดก่อน
            m = by_coord.get((yr, k4(rec['lat'], rec['lon'])))
            if m: break
        if m and re.sub(r'\s+', ' ', str(m['point_name'])) != re.sub(r'\s+', ' ', str(rec['ชื่อจุด'])):
            rec['ชื่อจุด'] = re.sub(r'\s+', ' ', str(m['point_name'])).strip()
            renamed += 1
    with open(f'{REPO}/data/sheets/13_Pending_Update.json', 'w', encoding='utf-8') as f:
        json.dump(p13, f, ensure_ascii=False, indent=1)
    ws13 = wx['13_Pending Update']
    hdr13 = {ws13.cell(row=1, column=c).value: c for c in range(1, ws13.max_column + 1)}
    if 'ชื่อจุด' in hdr13 and 'ลำดับ' in hdr13:
        for i, rec in enumerate(p13, start=2):
            ws13.cell(row=i, column=hdr13['ชื่อจุด'], value=rec['ชื่อจุด'])
    wx.save(f'{REPO}/data.xlsx')

    # 5) manifest.json
    man = json.load(open(f'{REPO}/data/manifest.json', encoding='utf-8'))
    now = datetime.datetime.now(datetime.timezone.utc)
    be = now.replace(year=now.year + 543)
    man['updated_at'] = be.strftime('%Y-%m-%dT%H:%M:%SZ')
    man['update_note'] = ('ปรับปรุงตามไฟล์รวม 3 ปีฉบับแก้ไข (10 ก.ค. 2569): ชื่อจุดมาตรฐาน 37 จุด, '
                          'พิกัดแก้ไข 6 จุด, สถานะ 9 รายการ, แยก "แยกมักกะสัน"/"แยกหมอเหล็ง" ชัดเจน, '
                          'หน่วยงานปี 2568 จุดมอเตอร์เวย์-พระราม 9 = ทล.')
    with open(f'{REPO}/data/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(man, f, ensure_ascii=False, indent=2)

    print('rows:', counts, '| sheet13 renamed:', renamed)
    print('OK — rebuilt all data layers')

if __name__ == '__main__':
    main()
