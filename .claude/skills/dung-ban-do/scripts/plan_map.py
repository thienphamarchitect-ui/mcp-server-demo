#!/usr/bin/env python3
"""Lập kế hoạch vùng ảnh nền cho cảnh bản đồ 9:16: chọn scale toàn cảnh và bbox đủ phủ kín khung.

  python3 plan_map.py --route "16.0439,108.1994;15.8801,108.338;15.4065,108.7054" [--zoom 13] [--fit 940 1320] [--cy 1000]

Vì sao cần: camera đặt tâm khung ở (540, cy). Ở scale s, ảnh nền phải phủ 540/s px sang trái/phải và cy/s px lên trên,
(1920-cy)/s px xuống dưới tính từ tâm camera; nếu thiếu, mép ảnh lộ nền navy. Tuyến chạy chéo thì bbox "vừa tuyến"
luôn thiếu -> phải mở rộng, đặc biệt theo chiều dọc. Script tính sẵn bbox và in lệnh fetch_map.py tương ứng.
Nếu s > 0.9 (tuyến ngắn) script tự tăng zoom để ảnh nền không bị vỡ khi phóng to.
"""
import argparse, math, sys

ap = argparse.ArgumentParser()
ap.add_argument('--route', required=True, help='"lat,lon;lat,lon;..." — các điểm của tuyến (hoặc các ghim) theo thứ tự')
ap.add_argument('--zoom', type=int, default=13)
ap.add_argument('--fit', nargs=2, type=float, default=[940, 1320], help='vùng (rộng, cao) px trên khung 1080x1920 để toàn tuyến nằm gọn (chừa chỗ cho chữ)')
ap.add_argument('--cy', type=float, default=1000, help='toạ độ y của tâm camera trên khung (engine.js dùng 1000)')
ap.add_argument('--margin', type=float, default=1.04)
ap.add_argument('--pins', default='', help='ghim cho fetch_map (mặc định: điểm đầu, các điểm giữa tuỳ chọn, điểm cuối)')
A = ap.parse_args()
pts = [tuple(map(float, p.split(','))) for p in A.route.split(';') if p.strip()]
if len(pts) < 2: sys.exit('cần >= 2 điểm')

def to_px(lat, lon, z):
    n = 256 * 2 ** z; x = (lon + 180) / 360 * n; la = math.radians(lat)
    return x, (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n
def to_ll(x, y, z):
    n = 256 * 2 ** z; return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180

z = A.zoom
while True:
    px = [to_px(la, lo, z) for la, lo in pts]
    xs = [p[0] for p in px]; ys = [p[1] for p in px]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = min(A.fit[0] / max(w, 1), A.fit[1] / max(h, 1))
    if s > 0.9 and z < 16: z += 1; continue          # tuyến ngắn: tăng zoom để ảnh nền nét
    break
cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
L, R = 540 / s * A.margin, 540 / s * A.margin
T, B = A.cy / s * A.margin, (1920 - A.cy) / s * A.margin
lat1, lon0 = to_ll(cx - L, cy - T, z); lat0, lon1 = to_ll(cx + R, cy + B, z)
tiles = math.ceil((R + L) / 256 + 1) * math.ceil((T + B) / 256 + 1)
pins = A.pins or ';'.join(f'{la},{lo}' for la, lo in (pts if len(pts) <= 6 else [pts[0], pts[len(pts) // 3], pts[2 * len(pts) // 3], pts[-1]]))
print(f'zoom={z}  scale toàn cảnh (ov.scale) = {s:.3f}   tuyến {w:.0f}x{h:.0f}px ở zoom {z}')
print(f'bbox: LAT {lat0:.3f} {lat1:.3f}   LON {lon0:.3f} {lon1:.3f}   (~{tiles} ô nền)')
print(f'\npython3 fetch_map.py <project> --bbox {lat0:.3f} {lat1:.3f} {lon0:.3f} {lon1:.3f} --zoom {z} --detail-zoom {z + 1} --pins "{pins}"')
if tiles > 1500: print('CẢNH BÁO: >1500 ô — giảm --zoom 1 bậc hoặc thu hẹp vùng.')
print('Lưu ý: seafix.py giả định biển ở MÉP PHẢI ảnh. Nếu biển ở hướng khác, dùng --no-seafix hoặc sửa seafix.py.')
print('Ghi chú: ghim trong --pins phải cùng thứ tự với pins[] trong scene.js để ảnh chi tiết (det1..N) khớp ghim 1..N.')
