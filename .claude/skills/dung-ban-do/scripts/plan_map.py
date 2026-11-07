#!/usr/bin/env python3
"""Lập kế hoạch vùng ảnh nền cho cảnh bản đồ 9:16: chọn scale toàn cảnh và bbox đủ phủ kín khung ở MỌI vị trí camera.

  python3 plan_map.py --route "lat,lon;lat,lon;..." [--follow-scale 1.15] [--extra "lat,lon;..."] [--ring "lat,lon,km;..."]
                      [--zoom 13] [--fit 940 1320] [--cy 1000] [--margin 1.12]

Vì sao cần: camera đặt tâm khung ở (540, cy). Ở scale s, ảnh nền phải phủ 540/s px sang trái/phải, cy/s px lên trên và
(1920-cy)/s px xuống dưới tính từ tâm camera; thiếu thì mép ảnh lộ nền navy. Tâm camera không chỉ ở giữa tuyến:
  * pha toàn cảnh: tâm ở giữa tuyến, scale s (tính từ --fit);
  * pha bám tàu: tâm đi qua mọi điểm của tuyến ở scale --follow-scale (mặc định 1.15; đặt 0 nếu không có tàu bám);
  * zoom sâu vào điểm / thẻ cuối: thêm các điểm đó vào --extra (scale --extra-scale, mặc định 2.0);
  * vòng bán kính: --ring "lat,lon,km" — 4 điểm cực của vòng được tính vào khung TOÀN CẢNH (để vòng không bị cắt) khi chọn scale.
Script lấy HỢP của các vùng đó rồi cộng --margin (mặc định 1,12). Tuyến ngắn (s > 0,9) tự tăng zoom để ảnh nét.
In ra: bbox, lệnh fetch_map.py, và ov.center / ov.scale để dán vào scene.js.
"""
import argparse, math, sys

ap = argparse.ArgumentParser()
ap.add_argument('--route', required=True, help='"lat,lon;lat,lon;..." — các điểm của tuyến hoặc các ghim')
ap.add_argument('--extra', default='', help='điểm camera còn phải tới (thẻ cuối, điểm zoom sâu...)')
ap.add_argument('--ring', default='', help='"lat,lon,km;..." vòng bán kính cần nằm trọn trong vùng phủ')
ap.add_argument('--follow-scale', type=float, default=1.15, help='scale camera khi bám tàu dọc tuyến (cam.follow[3]); đặt 0 nếu KHÔNG có tàu bám (cảnh chỉ có ghim/vòng)')
ap.add_argument('--extra-scale', type=float, default=2.0, help='scale camera ở các điểm --extra (zoom sâu / thẻ cuối)')
ap.add_argument('--zoom', type=int, default=13)
ap.add_argument('--fit', nargs=2, type=float, default=[940, 1320], help='vùng (rộng, cao) px trên khung 1080x1920 để toàn tuyến nằm gọn (chừa chỗ cho chữ)')
ap.add_argument('--cy', type=float, default=1000, help='toạ độ y tâm camera trên khung (engine.js dùng 1000)')
ap.add_argument('--margin', type=float, default=1.12)
ap.add_argument('--pins', default='', help='điểm tải ảnh chi tiết z+1 (chỉ cần ở nơi sẽ zoom sâu, scale > 1,05); mặc định: các điểm đầu/giữa/cuối')
A = ap.parse_args()
parse = lambda s, n=2: [tuple(map(float, p.split(','))) for p in s.split(';') if p.strip()]
pts = parse(A.route); extra = parse(A.extra); rings = parse(A.ring)
if len(pts) < 2: sys.exit('cần >= 2 điểm')

def to_px(lat, lon, z):
    n = 256 * 2 ** z; x = (lon + 180) / 360 * n; la = math.radians(lat)
    return x, (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n
def to_ll(x, y, z):
    n = 256 * 2 ** z; return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180
def km_px(km, lat, z): return km * 1000 / (156543.03392804097 * math.cos(math.radians(lat)) / 2 ** z)

z = A.zoom
while True:
    px = [to_px(la, lo, z) for la, lo in pts]
    ring_pts = []
    for la, lo, km in rings:
        r = km_px(km, la, z); cx0, cy0 = to_px(la, lo, z)
        ring_pts += [(cx0 + r, cy0), (cx0 - r, cy0), (cx0, cy0 + r), (cx0, cy0 - r)]
    allp = px + [to_px(la, lo, z) for la, lo in extra] + ring_pts
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    ext = lambda pp: (max(p[0] for p in pp) - min(p[0] for p in pp), max(p[1] for p in pp) - min(p[1] for p in pp))
    w2, h2 = ext(px + ring_pts) if ring_pts else (w, h)           # tuyến + vòng phải nằm gọn trong khung toàn cảnh
    s = min(A.fit[0] / max(w2, 1), A.fit[1] / max(h2, 1))
    if s > 0.9 and z < 16: z += 1; continue
    break
sf = max(A.follow_scale, s)
cx, cyy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2           # tâm toàn cảnh = tâm bbox của TUYẾN (đúng như engine.js)
rects = []                                                           # (x0, x1, y0, y1) cần phủ
rects.append((cx - 540 / s, cx + 540 / s, cyy - A.cy / s, cyy + (1920 - A.cy) / s))
if A.follow_scale > 0:
    for (x, y) in px:
        rects.append((x - 540 / sf, x + 540 / sf, y - A.cy / sf, y + (1920 - A.cy) / sf))
se = max(A.extra_scale, s)
for (x, y) in [to_px(la, lo, z) for la, lo in extra]:
    rects.append((x - 540 / se, x + 540 / se, y - A.cy / se, y + (1920 - A.cy) / se))
x0 = min(r[0] for r in rects); x1 = max(r[1] for r in rects); y0 = min(r[2] for r in rects); y1 = max(r[3] for r in rects)
mx, my = (x1 - x0) * (A.margin - 1) / 2, (y1 - y0) * (A.margin - 1) / 2
x0 -= mx; x1 += mx; y0 -= my; y1 += my
lat1, lon0 = to_ll(x0, y0, z); lat0, lon1 = to_ll(x1, y1, z)
tiles = math.ceil((x1 - x0) / 256 + 1) * math.ceil((y1 - y0) / 256 + 1)
ovlat, ovlon = to_ll(cx, cyy, z)
pins = A.pins or ';'.join(f'{la},{lo}' for la, lo in (pts if len(pts) <= 6 else [pts[0], pts[len(pts) // 3], pts[2 * len(pts) // 3], pts[-1]]))
print(f'zoom={z}  ov.scale = {s:.3f}  (tuyến {w:.0f}x{h:.0f}px ở zoom {z}; follow/keys dùng scale ≤ {sf:.2f})')
print(f'ov.center = [{ovlat:.4f}, {ovlon:.4f}]   <- dán vào SCENE.ov khi KHÔNG có route (chỉ ghim/vòng) hoặc muốn ghi đè')
print(f'bbox: LAT {lat0:.3f} {lat1:.3f}   LON {lon0:.3f} {lon1:.3f}   (~{tiles} ô nền, ảnh ~{x1 - x0:.0f}x{y1 - y0:.0f}px)')
print(f'\npython3 fetch_map.py <project> --bbox {lat0:.3f} {lat1:.3f} {lon0:.3f} {lon1:.3f} --zoom {z} --detail-zoom {z + 1} --pins "{pins}" --sea <right|bottom|left|top|none>')
if tiles > 1500: print('CẢNH BÁO: >1500 ô — giảm --zoom 1 bậc hoặc thu hẹp vùng.')
print('Ảnh chi tiết (det1..N) KHÔNG gắn với id ghim: chỉ là ô z+1 tự hiện khi scale camera > 1,05. Chọn --pins là các nơi sẽ zoom sâu.')
print('--sea: hướng của biển so với ảnh (mặc định right). Nước đục phù sa/hồ không nhận ra được -> dùng --sea none.')
