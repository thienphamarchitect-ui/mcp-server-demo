"""Tải ảnh vệ tinh thật (Esri World Imagery) cho cảnh bản đồ bay zoom in/out.

  python3 fetch_map.py <projectDir> --bbox LAT_MIN LAT_MAX LON_MIN LON_MAX \
      --pins "15.8801,108.338;16.072,108.232;16.075,108.125;16.003,108.263" [--zoom 13] [--detail-zoom 14] [--no-seafix]

Kết quả trong <project>/assets/:
  map_sat_clean.jpg   ảnh nền toàn vùng (zoom 13 mặc định)
  det1.jpg, det2.jpg  ảnh chi tiết (zoom 14) quanh từng ghim, để zoom sâu không bị vỡ
  map_config.js       window.MAPCFG = {z,x0,y0,W,H,src,det:[{x,y,w,h,src}]}  (render.html đọc file này)

Chọn bbox: khung dọc 9:16 ở toàn cảnh scale ~0.36 cần ~5300 px chiều cao ảnh ở z13
=> vùng vĩ độ ~0.9–1.0°, kinh độ ~0.7–0.8°. Biển nên nằm ở mép phải (seafix giả định vậy).
Ghi nguồn trên video: "Ảnh vệ tinh: Esri, Maxar, Earthstar Geographics".
"""
import argparse, math, os, json, ssl, urllib.request, concurrent.futures as cf, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('project'); ap.add_argument('--bbox', nargs=4, type=float, required=True)
ap.add_argument('--pins', default=''); ap.add_argument('--zoom', type=int, default=13)
ap.add_argument('--detail-zoom', type=int, default=14); ap.add_argument('--half', nargs=2, type=float, default=[470, 820],
                help='nửa kích thước vùng chi tiết quanh ghim, px theo zoom nền')
ap.add_argument('--no-seafix', action='store_true')
ap.add_argument('--sea', default='right', help='cạnh ảnh mà biển chạm vào: right|left|top|bottom (ghép bằng dấu phẩy) hoặc none')
A = ap.parse_args()
P = os.path.abspath(A.project); AS = os.path.join(P, 'assets'); os.makedirs(AS, exist_ok=True)
CACHE = os.path.join(P, 'tilecache'); os.makedirs(CACHE, exist_ok=True)
CA = os.environ.get('SSL_CERT_FILE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else None)
ctx = ssl.create_default_context(cafile=CA) if CA else ssl.create_default_context()
def tile(z, x, y):
    p = os.path.join(CACHE, f'{z}_{x}_{y}.jpg')
    if not os.path.exists(p):
        u = f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        req = urllib.request.Request(u, headers={'User-Agent': 'bds-video-demo/1.0'})
        for k in range(3):
            try: open(p, 'wb').write(urllib.request.urlopen(req, context=ctx, timeout=30).read()); break
            except Exception:
                if k == 2: raise
    return p
def txf(lon, z): return (lon + 180) / 360 * 2 ** z
def tyf(lat, z):
    la = math.radians(lat); return (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * 2 ** z
def mosaic(z, x0, x1, y0, y1):
    jobs = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
    img = Image.new('RGB', ((x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256))
    with cf.ThreadPoolExecutor(6) as ex:
        for (x, y), p in zip(jobs, ex.map(lambda a: tile(z, *a), jobs)):
            img.paste(Image.open(p).convert('RGB'), ((x - x0) * 256, (y - y0) * 256))
    return img, len(jobs)
Z = A.zoom; LAT0, LAT1, LON0, LON1 = A.bbox
x0, x1 = int(txf(LON0, Z)), int(txf(LON1, Z)); y0, y1 = int(tyf(LAT1, Z)), int(tyf(LAT0, Z))
base, n = mosaic(Z, x0, x1, y0, y1); print('nền:', n, 'ô', base.size)
raw = os.path.join(AS, 'map_sat_raw.jpg'); base.save(raw, quality=88)
cfg = dict(z=Z, x0=x0, y0=y0, W=base.width, H=base.height, src='assets/map_sat_clean.jpg', det=[])
dz = A.detail_zoom; F = 2 ** (dz - Z); HX, HY = A.half
pins = [tuple(map(float, s.split(','))) for s in A.pins.split(';') if s.strip()]
for i, (la, lo) in enumerate(pins, 1):
    cx = (txf(lo, Z) - x0) * 256; cy = (tyf(la, Z) - y0) * 256
    tx0 = int(math.floor((x0 * 256 + cx - HX) * F / 256)); ty0 = int(math.floor((y0 * 256 + cy - HY) * F / 256))
    tx1 = int(math.floor((x0 * 256 + cx + HX) * F / 256)); ty1 = int(math.floor((y0 * 256 + cy + HY) * F / 256))
    im, n = mosaic(dz, tx0, tx1, ty0, ty1)
    out = os.path.join(AS, f'det{i}_raw.jpg'); im.save(out, quality=86)
    cfg['det'].append(dict(x=tx0 * 256 / F - x0 * 256, y=ty0 * 256 / F - y0 * 256, w=im.width / F, h=im.height / F, src=f'assets/det{i}.jpg'))
    print(f'chi tiết {i}:', n, 'ô')
if A.no_seafix:
    import shutil
    shutil.copy(raw, os.path.join(AS, 'map_sat_clean.jpg'))
    for i in range(1, len(pins) + 1): shutil.copy(os.path.join(AS, f'det{i}_raw.jpg'), os.path.join(AS, f'det{i}.jpg'))
else:
    from seafix import fix
    fix(raw, os.path.join(AS, 'map_sat_clean.jpg'), sea=A.sea)
    for i in range(1, len(pins) + 1): fix(os.path.join(AS, f'det{i}_raw.jpg'), os.path.join(AS, f'det{i}.jpg'), sea=A.sea)
open(os.path.join(AS, 'map_config.js'), 'w').write('window.MAPCFG = ' + json.dumps(cfg) + ';\n')
print('map_config.js:', json.dumps(cfg)[:300])
