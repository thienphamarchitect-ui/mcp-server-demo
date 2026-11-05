# Template dựng: render.html + timeline.js

## Mục lục
1. Cấu trúc thư mục dự án
2. Hệ thiết kế (Style DNA)
3. Các hàm tạo phần tử
4. Ảnh nền & hiệu ứng toàn khung
5. Cảnh bản đồ bay zoom in / zoom out
6. SFX & nhạc
7. Quy trình xem thử → render → sửa một đoạn

---

## 1. Cấu trúc dự án

```
<project>/
  render.html  timeline.js        (copy từ assets/template/, rồi sửa)
  fonts/                          (Source Sans 3 600/700/900, latin + vietnamese)
  assets/  *_head.png *_quote.png *_img*.png  map_sat_clean.jpg det*.jpg map_config.js
  vo/      s*.wav (gốc TTS) -> f*.wav (vo_prep.sh)
  frames/  prev/  sfx.json  mix.wav
```
`render.html` mở bằng file:// nên mọi đường dẫn là tương đối. `map_config.js` do `fetch_map.py` tạo; nếu video không có bản đồ, tạo file tối thiểu `window.MAPCFG={z:13,x0:0,y0:0,W:1080,H:1920,src:'',det:[]};` và xoá entry `MAP` trong `bgs`.

`render(t)` là hàm **thuần theo thời gian** (không dùng CSS animation): mọi trạng thái tính từ `t`, nên chụp từng frame ra kết quả xác định.

## 2. Hệ thiết kế (phong cách KTS Thiện / REF001)

- Khung 1080x1920, 30fps. Nền navy `#06121C`, nhấn **cyan `#05F4E8`**, trắng; đỏ `#FF4D5E` chỉ cho số giảm; vàng `#FFE600` cho tô highlight trên ảnh báo.
- Font **Source Sans 3 Black**, `scaleX(.86)`, IN HOA, bóng đen nhiều lớp + glow cyan cho giá trị.
- Cỡ theo cap height (px): label 44–66 · value 100–150 · hero number 190–230. Hàm `line()` nhận cap, tự tính font-size = cap/0.66.
- Vùng chữ tiêu đề y 300–560 (trên), thẻ báo y 560–1150 (giữa), số lớn y 1250–1650, chừa 250px đáy cho UI nền tảng.
- `window.fit()` tự thu nhỏ dòng nào rộng > 950px (gọi sẵn trong render.js) — không cần tự canh.
- Góc trên: thương hiệu (`#brand`: tên + dòng phụ), nhãn `#loc` (TP · năm), thanh tiến trình cyan.
- Đổi thương hiệu: sửa `.t1/.t2` trong `#brand` và `#loc`.

## 3. Hàm tạo phần tử (khai báo ở mục `/* ---------- ELEMENTS`)

| Hàm | Dùng cho | Hoạt ảnh |
|---|---|---|
| `line(text, cls, cap, y, tin, tout, opt)` | chữ/số; `cls`: `'w'` trắng, `'c'` cyan, `'r'` đỏ | `track` (giãn chữ→co, mặc định), `hero` (phóng 1.7→1), `count` (đếm số: `count:[from,to,suffix,plusSign]`), `pulse` |
| `paper(src, tag, y, w, tin, tout, rot, {dark})` | thẻ ảnh báo trắng bo góc + nhãn đỏ "TÊN BÁO · NGÀY" (dark=nhãn viền cyan, dùng cho "Nguồn: chủ đầu tư") | trượt lên có nảy, đẩy chậm, ra trượt trái; tự gắn SFX whoosh + shutter |
| `chip(icon, text, y, tin, tout)` | gạch đầu dòng dạng viên thuốc (vật liệu, tiện ích) | trượt từ trái; SFX notify |
| `src(text, y, tin, tout)` | dòng nguồn/chú thích nhỏ | fade |
| `raw(html, tin, tout, type)` | phần tử tuỳ ý (nút CTA `.cta`, `.disc` disclaimer) | `pop` hoặc `fade` |

`opt.sfx` đổi âm (mặc định: `'pop'` cho trắng, `'ting'` cho cyan; `false` để tắt), `opt.g` gain dB.
Mỗi cảnh viết thành một khối `// SCENE n – ...`. Đặt `tin` trùng lúc giọng đọc chạm từ khoá (từ vo_prep.sh), `tout` = đầu cảnh sau.

## 4. Ảnh nền & hiệu ứng

`timeline.js > bgs`: `[src, in, out, dir]` — `src` là ảnh (Ken Burns, dir ±1 hướng trôi, có lớp grade tối trên/dưới), `'DARK'` (nền gradient + lưới + hạt), `'MAP'` (cảnh bản đồ). Các entry chồng 0,2–0,35s để crossfade.
Hiệu ứng: `FLASH [[t, dur, max]]` (chớp trắng: đầu video, drop), `GLOW [[t,dur]]` (quầng cyan), `SWEEP [[t]]` (vệt sáng quét qua thẻ báo), light-leak + sáng dần ở 1,3s cuối.

## 5. Bản đồ bay zoom in / zoom out

1. Tải ảnh: `python3 scripts/fetch_map.py <project> --bbox LAT0 LAT1 LON0 LON1 --pins "lat,lon;lat,lon;..."` (thứ tự ghim = số 1,2,3…).
2. Trong render.html mục MAP:
   - `PINS={k:[...geo(lat,lon),'NHÃN']}` — cùng toạ độ đã truyền `--pins`.
   - `PLACES=[[lat,lon,'TÊN ĐỊA DANH'],...]` — nhãn địa danh thật (bán đảo, sông, sân bay, biển).
   - `DEEP` (scale khi zoom sâu, 2.0 = nét với ảnh chi tiết z14), `PUSH` (scale cuối khi đẩy chậm).
   - `CAM=[[t,cx,cy,scale],...]` keyframe camera (toạ độ px ảnh nền). Mẫu mỗi vùng: toàn cảnh `OV` → ~1s zoom vào `C(k,60)` scale DEEP → giữ/đẩy tới PUSH trong lúc hiện thẻ báo/số → ~0,85s zoom ra `OV` (gắn whoosh qua `ZOOMOUT`). Vùng "đáng tiền nhất": giữ toàn cảnh khi đọc open-loop, zoom thẳng vào đúng lúc drop.
   - `PINACT={k:[tOn,tOff]}` (ghim nhấp nháy), `LABOUT={k:t}` (ẩn nhãn ghim khi thẻ báo vào), `DIM=[[a,b]]` (tối map 38% khi có thẻ).
   - Scale nội suy theo hàm mũ (zoom đều mắt); vị trí theo easeInOut.
3. Ghi nguồn ảnh vệ tinh ở góc dưới (đã có sẵn). Esri World Imagery hợp lý cho demo có ghi nguồn; video quảng cáo thương mại nên dùng nguồn có giấy phép (Google Maps/Mapbox) hoặc flycam.
4. `seafix.py` làm đồng màu biển (giả định biển ở mép phải). Kiểm tra thumbnail sau khi tải: còn vệt răng cưa → tăng ngưỡng; mất đảo → đảo phải có màu xanh để được giữ.

## 6. SFX & nhạc

- `sfx(t, name, gainDb)` gom vào `window.SFX_LIST` → render.js ghi `sfx.json` → audio.py tổng hợp: `whoosh pop ting impact riser shutter heartbeat notify cash sparkle`.
- Gắn: whoosh cho mọi chuyển cảnh/zoom ra; pop cho chữ trắng; ting cho giá trị cyan; impact cho số lớn/drop; cash cho số tiền; riser + heartbeat trước drop; shutter khi thẻ báo vào; sparkle cho tên dự án/CTA.
- Nhạc tổng hợp (Am–F–C–G 100 BPM) theo `timeline.js > music`: `start` (vào nhạc), `beatsFrom` (bắt đầu kick nhẹ), `breakdown:[a,b]` (nhạc mỏng dần a→b, im lặng b→drop), `outro` (sau mốc này chỉ còn pad). `drop` = lúc full beat + impact + flash. Lưới beat tự căn để phách 1 rơi đúng `drop`.
- Người dùng có nhạc riêng → thay phần MUSIC trong audio.py bằng việc nạp file nhạc, căn drop của bài vào `TL.drop`.

## 7. Quy trình

```bash
node scripts/render.js <project> preview 3.6 12.4 29.9 47.5     # xem nhanh vài thời điểm
python3 - <<'EOF'   # ghép thumbnail để tự xem (Read ảnh)
EOF
bash scripts/make_video.sh <project> out_v1.mp4               # render đủ + mix + MP4 (~3–5 phút cho 55s)
bash scripts/make_video.sh <project> out_v2.mp4 315 1015      # chỉ render lại frame 315–1015 rồi ghép lại
```
Sau khi ghép: trích 6–10 khung bằng `ffmpeg -ss T -frames:v 1` và tự xem trước khi gửi. Lỗi thường gặp: chữ tràn (fit() xử lý), số đếm có dấu "+" sai (chỉ bật `plusSign` cho mức tăng), nhãn ghim chồng nhau ở cảnh tổng hợp (ẩn nhãn, chỉ để số), thẻ báo che ghim (bình thường — ghim đã hiện trước khi thẻ vào).
