#!/usr/bin/env python3
"""Đặt lưới toạ độ lên ảnh nền để dò vị trí ga/điểm bằng mắt và đọc ngược pixel -> lat/lon.

  python3 grid_overlay.py <project> --center LAT,LON [--size 1400] [--step 0.005] [--poly "lat,lon;..."] [--mark "lat,lon;..."] [--out grid.jpg]
  python3 grid_overlay.py <project> --px2ll "x,y;x,y"      # đổi pixel ảnh nền -> lat/lon (x,y trong ảnh map_sat_clean.jpg)

Dùng khi không có toạ độ chính thức (WebSearch/Nominatim/Overpass thường không trả hoặc bị proxy chặn): cắt vùng quanh --center,
vẽ lưới lat/lon có nhãn mỗi --step độ (0,005° ≈ 550 m), vẽ đường --poly (tuyến hiện tại) và --mark (các ga) để chỉnh dần.
Đọc ảnh bằng công cụ Read, chỉnh toạ độ, chạy lại. Sai số ước lượng bằng mắt thường vài chục–200 m: ghi "vị trí gần đúng" trên video.
"""
import argparse, json, math, os, re, sys
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument('project')
ap.add_argument('--center'); ap.add_argument('--size', type=int, default=1400, help='cạnh vùng cắt, px ảnh nền')
ap.add_argument('--step', type=float, default=0.005); ap.add_argument('--poly', default=''); ap.add_argument('--mark', default='')
ap.add_argument('--px2ll', default=''); ap.add_argument('--out', default='grid.jpg'); ap.add_argument('--raw', action='store_true', help='dùng map_sat_raw.jpg')
A = ap.parse_args()
P = os.path.abspath(A.project); txt = open(os.path.join(P, 'assets', 'map_config.js'), encoding='utf-8').read()
C = json.loads(txt[txt.index('{'):txt.rindex('}') + 1]); Z, X0, Y0 = C['z'], C['x0'], C['y0']
def to_px(lat, lon):
    n = 2 ** Z; x = (lon + 180) / 360 * n; la = math.radians(lat)
    return (x - X0) * 256, ((1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n - Y0) * 256
def to_ll(x, y):
    n = 2 ** Z; X = (x / 256 + X0) / n; Y = (y / 256 + Y0) / n
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * Y)))), X * 360 - 180
pr = lambda s: [tuple(map(float, p.split(','))) for p in s.split(';') if p.strip()]
if A.px2ll:
    for x, y in pr(A.px2ll): la, lo = to_ll(x, y); print(f'({x:.0f},{y:.0f}) -> {la:.5f},{lo:.5f}')
    sys.exit()
if not A.center: sys.exit('cần --center hoặc --px2ll')
la0, lo0 = map(float, A.center.split(',')); cx, cy = to_px(la0, lo0)
im = Image.open(os.path.join(P, 'assets', 'map_sat_raw.jpg' if A.raw else 'map_sat_clean.jpg')).convert('RGB')
h = A.size // 2; box = (int(cx - h), int(cy - h), int(cx + h), int(cy + h)); cr = im.crop(box); d = ImageDraw.Draw(cr, 'RGBA')
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: f = ImageFont.load_default()
S = lambda x, y: (x - box[0], y - box[1])
lat_a, lon_a = to_ll(*box[:2]); lat_b, lon_b = to_ll(*box[2:])
g = math.floor(min(lat_a, lat_b) / A.step) * A.step
while g < max(lat_a, lat_b):
    y = S(0, to_px(g, lon_a)[1])[1]; d.line([(0, y), (cr.width, y)], fill=(255, 255, 0, 130), width=1); d.text((4, y + 2), f'{g:.4f}', fill=(255, 255, 0, 255), font=f); g += A.step
g = math.floor(min(lon_a, lon_b) / A.step) * A.step
while g < max(lon_a, lon_b):
    x = S(to_px(la0, g)[0], 0)[0]; d.line([(x, 0), (x, cr.height)], fill=(0, 255, 255, 130), width=1); d.text((x + 3, cr.height - 26), f'{g:.4f}', fill=(0, 255, 255, 255), font=f); g += A.step
if A.poly:
    pts = [S(*to_px(*p)) for p in pr(A.poly)]; d.line(pts, fill=(255, 60, 60, 230), width=4)
    for p in pts: d.ellipse([p[0] - 5, p[1] - 5, p[0] + 5, p[1] + 5], outline=(255, 255, 255, 255), width=2)
for i, p in enumerate(pr(A.mark), 1):
    x, y = S(*to_px(*p)); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(5, 244, 232, 230)); d.text((x + 12, y - 12), str(i), fill=(255, 255, 255, 255), font=f)
cr.save(A.out, quality=88); print('ghi', A.out, cr.size, f'(pixel gốc {box})')
