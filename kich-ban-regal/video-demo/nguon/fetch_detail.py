import math, os, json, urllib.request, ssl, concurrent.futures as cf
import numpy as np
from PIL import Image, ImageFilter
D = os.path.dirname(os.path.abspath(__file__))
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
MX0, MY0 = 6551, 3717  # gốc ảnh z13
Z = 14; F = 2 ** (Z - 13)
PINS = {1: (15.8801, 108.338), 2: (16.072, 108.232), 3: (16.075, 108.125), 4: (16.003, 108.263)}
HX, HY = 470, 820  # nửa vùng chi tiết, tính bằng px z13
def g13(lat, lon):
    n = 2 ** 13; x = (lon + 180) / 360 * n; la = math.radians(lat)
    y = (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n
    return (x - MX0) * 256, (y - MY0) * 256
cache = os.path.join(D, 'tilecache'); os.makedirs(cache, exist_ok=True)
def get(x, y):
    p = os.path.join(cache, f'{Z}_{x}_{y}.jpg')
    if not os.path.exists(p):
        u = f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{y}/{x}'
        req = urllib.request.Request(u, headers={'User-Agent': 'KTS-Thien-video-demo/1.0'})
        for k in range(3):
            try: open(p, 'wb').write(urllib.request.urlopen(req, context=ctx, timeout=30).read()); break
            except Exception:
                if k == 2: raise
    return p
def clean(im):  # đồng màu mặt biển như ảnh z13
    a = np.asarray(im).astype(np.float32); R, G, B = a[..., 0], a[..., 1], a[..., 2]; lum = .3 * R + .59 * G + .11 * B
    m = (((B > R + 6) & (B >= G - 8) & (lum < 120)) | ((B > R + 12) & (B > G + 2) & (lum < 225))).astype(np.uint8) * 255
    mk = np.asarray(Image.fromarray(m).filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
    out = a * (1 - mk * .88) + np.array([14, 38, 58], np.float32) * (mk * .88)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))
meta = {}
for k, (la, lo) in PINS.items():
    cx, cy = g13(la, lo)
    # biên vùng theo px z13 -> chỉ số ô z14
    bx0, by0 = cx - HX, cy - HY
    tx0 = int(math.floor((MX0 * 256 + bx0) * F / 256)); ty0 = int(math.floor((MY0 * 256 + by0) * F / 256))
    tx1 = int(math.floor((MX0 * 256 + cx + HX) * F / 256)); ty1 = int(math.floor((MY0 * 256 + cy + HY) * F / 256))
    jobs = [(x, y) for x in range(tx0, tx1 + 1) for y in range(ty0, ty1 + 1)]
    img = Image.new('RGB', ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    with cf.ThreadPoolExecutor(6) as ex:
        for (x, y), p in zip(jobs, ex.map(lambda a: get(*a), jobs)):
            img.paste(Image.open(p).convert('RGB'), ((x - tx0) * 256, (y - ty0) * 256))
    clean(img).save(os.path.join(D, 'assets', f'det{k}.jpg'), quality=86)
    # vị trí góc trên trái của ảnh chi tiết trong hệ px z13, và tỉ lệ 1/F
    meta[k] = dict(x=tx0 * 256 / F - MX0 * 256, y=ty0 * 256 / F - MY0 * 256, w=img.width / F, h=img.height / F, src=f'assets/det{k}.jpg')
    print(k, len(jobs), 'tiles', meta[k])
json.dump(meta, open(os.path.join(D, 'assets', 'det_meta.json'), 'w'))
