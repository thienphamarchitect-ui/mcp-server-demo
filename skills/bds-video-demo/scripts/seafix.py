# Làm đồng màu mặt biển trên ảnh vệ tinh ghép (xoá các mảng ô lệch màu, vệt răng cưa sáng ven bờ).
# Giả định biển nằm ở mép PHẢI/ trên-phải/ dưới-phải của ảnh (bờ biển miền Trung VN). Đảo xanh được giữ lại.
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
SEA = np.array([14, 38, 58], np.float32)
def fix(src, dst, ds=4):
    im = Image.open(src).convert('RGB'); W, H = im.size
    sm = np.asarray(im.resize((W // ds, H // ds), Image.BILINEAR)).astype(np.float32)
    R, G, B = sm[..., 0], sm[..., 1], sm[..., 2]; lum = .3 * R + .59 * G + .11 * B
    # độ mịn cục bộ
    m1 = ndimage.uniform_filter(lum, 5); m2 = ndimage.uniform_filter(lum * lum, 5); std = np.sqrt(np.maximum(m2 - m1 * m1, 0))
    sand = (R - B > 14) & (lum > 110)
    seaish = (B > R + 4) & (lum < 130)
    green = (G > B + 4) | (G > R + 12)
    cand = ((std < 6.5) & ~sand & ~green) | seaish
    lab, n = ndimage.label(cand)
    # vùng nối với mép phải (biển Đông)
    edge = np.unique(np.concatenate([lab[:, -3:].ravel(), lab[:3, W // ds // 2:].ravel(), lab[-3:, W // ds * 2 // 3:].ravel()]))
    edge = edge[edge > 0]
    # chỉ giữ thành phần lớn
    sizes = ndimage.sum(np.ones_like(lab), lab, edge)
    keep = edge[sizes > 400]
    mask = np.isin(lab, keep)
    mask = ndimage.binary_closing(mask, iterations=2)
    filled = ndimage.binary_fill_holes(mask); holes = filled & ~mask
    hl, hn = ndimage.label(holes)
    if hn:
        gfrac = ndimage.mean(green.astype(np.float32), hl, np.arange(1, hn + 1)); hs = ndimage.sum(np.ones_like(hl), hl, np.arange(1, hn + 1))
        island = np.isin(hl, np.arange(1, hn + 1)[(gfrac > 0.35) & (hs > 60)])
    else: island = np.zeros_like(mask)
    mask = filled & ~island & ~ndimage.binary_dilation(sand, iterations=1)
    mk = Image.fromarray((mask * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(ds * 1.5))
    k = np.asarray(mk).astype(np.float32)[..., None] / 255
    a = np.asarray(im).astype(np.float32)
    out = a * (1 - k * .94) + SEA * (k * .94)
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst, quality=87)
if __name__ == '__main__':
    # python3 seafix.py in1.jpg out1.jpg [in2.jpg out2.jpg ...]
    for s, d in zip(sys.argv[1::2], sys.argv[2::2]): fix(s, d); print('ok', d)
