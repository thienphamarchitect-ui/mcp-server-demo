import math, os, json, urllib.request, ssl, concurrent.futures as cf, io, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
Z = 13
LAT0, LAT1, LON0, LON1 = 15.45, 16.40, 107.90, 108.66
ctx = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
def tx(lon): return (lon + 180) / 360 * 2 ** Z
def ty(lat):
    la = math.radians(lat); return (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * 2 ** Z
x0, x1 = int(tx(LON0)), int(tx(LON1)); y0, y1 = int(ty(LAT1)), int(ty(LAT0))
cache = os.path.join(D, 'tilecache'); os.makedirs(cache, exist_ok=True)
def get(x, y):
    p = os.path.join(cache, f'{Z}_{x}_{y}.jpg')
    if not os.path.exists(p):
        u = f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{y}/{x}'
        req = urllib.request.Request(u, headers={'User-Agent': 'KTS-Thien-video-demo/1.0'})
        for k in range(3):
            try:
                data = urllib.request.urlopen(req, context=ctx, timeout=30).read(); open(p, 'wb').write(data); break
            except Exception as e:
                if k == 2: raise
    return x, y, p
jobs = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
print('tiles', len(jobs))
W, H = (x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256
img = Image.new('RGB', (W, H))
with cf.ThreadPoolExecutor(6) as ex:
    for x, y, p in ex.map(lambda a: get(*a), jobs):
        img.paste(Image.open(p).convert('RGB'), ((x - x0) * 256, (y - y0) * 256))
img.save(os.path.join(D, 'assets', 'map_sat.jpg'), quality=88)
meta = dict(z=Z, x0=x0, y0=y0, W=W, H=H)
json.dump(meta, open(os.path.join(D, 'assets', 'map_meta.json'), 'w'))
print(meta)
def px(lat, lon): return ((tx(lon) - x0) * 256, (ty(lat) - y0) * 256)
for n, (la, lo) in {'thuanphuoc': (16.0917, 108.2222), 'nhs': (16.003, 108.263), 'hoian': (15.8801, 108.338), 'lienchieu': (16.12, 108.13)}.items():
    print(n, [round(v) for v in px(la, lo)])
