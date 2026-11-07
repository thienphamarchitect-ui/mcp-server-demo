import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SEA = np.array([14, 38, 58], np.float32)
def fix(src, dst, ds=4, sea='right'):
    # sea: các cạnh ảnh mà biển chạm vào, phân tách bằng dấu phẩy: right,left,top,bottom hoặc 'none' (chỉ copy)
    sides = [x.strip() for x in str(sea).split(',') if x.strip()]
    if sides == ['none']:
        import shutil; shutil.copy(src, dst); return
    im = Image.open(src).convert('RGB'); W, H = im.size
    sm = np.asarray(im.resize((W // ds, H // ds), Image.BILINEAR)).astype(np.float32)
    R, G, B = sm[..., 0], sm[..., 1], sm[..., 2]; lum = .3 * R + .59 * G + .11 * B
    m1 = ndimage.uniform_filter(lum, 5); m2 = ndimage.uniform_filter(lum * lum, 5); std = np.sqrt(np.maximum(m2 - m1 * m1, 0))
    sand = (R - B > 22) & (lum > 120)
    seaish = (B >= R) & (lum < 175) & (G <= B + 25)
    green = (G > B + 6) | (G > R + 14)
    cand = ((std < 9) & ~sand & ~green & (B >= R - 6)) | seaish
    lab, n = ndimage.label(cand)
    seeds = []                                                           # vùng nối với cạnh biển
    if 'right' in sides: seeds += [lab[:, -3:].ravel(), lab[:3, W // ds // 2:].ravel(), lab[-3:, W // ds * 2 // 3:].ravel()]
    if 'left' in sides: seeds += [lab[:, :3].ravel(), lab[:3, :W // ds // 2].ravel(), lab[-3:, :W // ds // 3].ravel()]
    if 'bottom' in sides: seeds += [lab[-3:, :].ravel()]
    if 'top' in sides: seeds += [lab[:3, :].ravel()]
    if not seeds: seeds = [lab[:, -3:].ravel()]
    edge = np.unique(np.concatenate(seeds))
    edge = edge[edge > 0]
    sizes = ndimage.sum(np.ones_like(lab), lab, edge)
    keep = edge[sizes > 400]
    mask = np.isin(lab, keep)
    mask = ndimage.binary_closing(mask, iterations=3)
    filled = ndimage.binary_fill_holes(mask); holes = filled & ~mask
    hl, hn = ndimage.label(holes)
    if hn:
        gfrac = ndimage.mean(green.astype(np.float32), hl, np.arange(1, hn + 1)); hs = ndimage.sum(np.ones_like(hl), hl, np.arange(1, hn + 1))
        island = np.isin(hl, np.arange(1, hn + 1)[(gfrac > 0.35) & (hs > 60)])
    else: island = np.zeros_like(mask)
    mask = filled & ~island & ~ndimage.binary_dilation(sand, iterations=1)
    mask = ndimage.binary_dilation(mask, iterations=1) & ~sand
    mk = Image.fromarray((mask * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(ds * 1.8))
    k = np.asarray(mk).astype(np.float32)[..., None] / 255
    a = np.asarray(im).astype(np.float32)
    out = a * (1 - k * .96) + SEA * (k * .96)
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst, quality=87)
if __name__ == '__main__':
    # python3 seafix.py [--sea right|left|top|bottom|none] in1.jpg out1.jpg [in2.jpg out2.jpg ...]
    a = sys.argv[1:]; sea = 'right'
    if a and a[0] == '--sea': sea = a[1]; a = a[2:]
    for s, d in zip(a[0::2], a[1::2]): fix(s, d, sea=sea); print('ok', d)
