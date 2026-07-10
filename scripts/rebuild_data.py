#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_data.py — สร้างชั้นข้อมูลทั้งหมดของ repo BMA-Congestion-Problem
จากไฟล์ต้นทาง "BMA_จุดฝืดรวมปี 2566-2568.xlsx" (คอลัมน์หลักมาตรฐาน 3 ปี)

อัปเดต: data/combined_data.json, data/sheets/08_Combined_Data.json,
        data/all_points.geojson, data/sheets/13_Pending_Update.json (สร้างใหม่
        จากจุดจริงที่ยังไม่แล้วเสร็จ + เหตุผลล่าสุด), data.xlsx (ชีต 08 + 13),
        data/manifest.json

วิธีใช้:  python scripts/rebuild_data.py "<ไฟล์รวม 3 ปี.xlsx>" <path repo>
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
NOTE_COLS = {2567: '[เฉพาะปี] หมายเหตุ การดำเนินงาน/ปัญหาอุปสรรค',
             2568: '[เฉพาะปี] หมายเหตุ ปัญหาอุปสรรค'}

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
            '_note': str(d.get(NOTE_COLS.get(year), '') or '').strip(),
        }
        if year in SOL_COLS:
            keys = ['sol_traffic_mgmt','sol_enforcement','sol_signal','sol_physical','sol_busbay','sol_cctv']
            for k, col in zip(keys, SOL_COLS[year]):
                rec[k] = yn(d.get(col))
        else:
            for k in ['sol_traffic_mgmt','sol_enforcement','sol_signal','sol_physical','sol_busbay','sol_cctv']:
                rec[k] = None
        out.append(rec)
    return out

def classify(note, progress):
    """สถานะตามเกณฑ์ตัวเลขในไฟล์ต้นทาง (ยืนยันโดยผู้ใช้ 10 ก.ค. 2569):
    0 = ติดปัญหาอุปสรรค · 0<x<100 = อยู่ระหว่างดำเนินการ · 100 = เสร็จสิ้น
    หมายเหตุปัญหาอุปสรรคใช้ข้อความจากคอลัมน์หมายเหตุของไฟล์ต้นทางตรง ๆ"""
    status = 'ติดปัญหาอุปสรรค' if progress == 0 else 'อยู่ระหว่างดำเนินการ'
    return status, (note or None)

def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    raw = []
    for y in (2566, 2567, 2568):
        raw += load_rows(wb, y)
    rows = [{f: r[f] for f in FIELDS} for r in raw]
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

    # 3) 13_Pending_Update — จุดจริง (พิกัด 6 ตำแหน่ง) ที่สถานะปีล่าสุดยังไม่ 100%
    key = lambda r: f"{r['latitude']:.6f},{r['longitude']:.6f}"
    tracked = [r for r in raw if int(r['year']) in (2567, 2568) and r['progress_pct'] is not None]
    latest, years = {}, {}
    for r in tracked:
        k = key(r); years.setdefault(k, set()).add(int(r['year']))
        if k not in latest or r['year'] > latest[k]['year']: latest[k] = r
    unresolved = sorted([(k, r) for k, r in latest.items() if r['progress_pct'] < 100],
                        key=lambda t: (t[1]['progress_pct'], -t[1]['year'], t[1]['point_id']))
    p13 = []
    for i, (k, r) in enumerate(unresolved, start=1):
        grp, txt = classify(r['_note'], r['progress_pct'])
        p13.append({'ลำดับ': i,
                    'ปี': '/'.join(str(x) for x in sorted(years[k])),
                    'ชื่อจุด': re.sub(r'\s+', ' ', str(r['point_name'])).strip(),
                    'เขต': r['district'], 'ผู้รับผิดชอบ': r['agency_main'],
                    'คืบหน้า (%)': r['progress_pct'],
                    'สถานะ': grp, 'หมายเหตุ': txt,
                    'lat': r['latitude'], 'lon': r['longitude'], 'โซน': r['zone']})
    with open(f'{REPO}/data/sheets/13_Pending_Update.json', 'w', encoding='utf-8') as f:
        json.dump(p13, f, ensure_ascii=False, indent=1)

    # 4) data.xlsx — ชีต 08 (header แถว 3, ข้อมูลเริ่มแถว 4) + ชีต 13
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
    ws13 = wx['13_Pending Update']
    ws13.cell(row=1, column=1, value=f'จุดที่ยังดำเนินการไม่แล้วเสร็จ — สถานะล่าสุดจากชุดข้อมูลรวม 3 ปี · จุดจริง {len(p13)} จุด')
    cols13 = ['ลำดับ','ปี','ชื่อจุด','เขต','ผู้รับผิดชอบ','คืบหน้า (%)','สถานะ','หมายเหตุ','lat','lon','โซน']
    if ws13.max_row > 3:
        ws13.delete_rows(4, ws13.max_row - 3)
    for j in range(1, ws13.max_column + 1):
        ws13.cell(row=3, column=j, value=None)
    for j, c in enumerate(cols13, start=1):
        ws13.cell(row=3, column=j, value=c)
    for i, rec in enumerate(p13, start=4):
        for j, c in enumerate(cols13, start=1):
            ws13.cell(row=i, column=j, value=rec[c])
    wx.save(f'{REPO}/data.xlsx')

    # 5) manifest.json
    man = json.load(open(f'{REPO}/data/manifest.json', encoding='utf-8'))
    try:
        import zoneinfo
        now = datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Bangkok'))
    except Exception:
        now = datetime.datetime.now()
    be = now.replace(year=now.year + 543)
    ts = be.strftime('%Y-%m-%dT%H:%M:%SZ')
    man['generated_at_utc'] = ts
    man['updated_at'] = ts
    man['update_note'] = f'rebuild จากไฟล์รวม 3 ปี — จุดค้างดำเนินการล่าสุด {len(p13)} จุด'
    with open(f'{REPO}/data/manifest.json', 'w', encoding='utf-8') as f:
        json.dump(man, f, ensure_ascii=False, indent=2)

    print('rows:', counts, '| pending:', len(p13))
    print('OK — rebuilt all data layers')

if __name__ == '__main__':
    main()
