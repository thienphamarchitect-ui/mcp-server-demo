# Engine bản đồ: tài liệu tham chiếu

## Mục lục
1. File và thứ tự nạp
2. Cấu hình SCENE
3. Camera
4. Phần tử chữ/thẻ
5. timeline.js, âm thanh, SFX
6. Kích thước ảnh nền (vì sao cần plan_map.py)
7. Lệnh render

## 1. File và thứ tự nạp
```
<project>/
  render.html  engine.js  scene.js  timeline.js   (sao chép từ assets/template/, rồi sửa scene.js + timeline.js)
  fonts/        Source Sans 3 (latin + vietnamese, 600/700/900)
  assets/       map_config.js map_sat_clean.jpg det1..N.jpg  + ảnh báo (*_card.png) do bạn thêm
  vo/           s*.wav (TTS gốc) -> f*.wav (vo_prep.sh)
```
render.html nạp: `assets/map_config.js` (MAPCFG do fetch_map.py tạo) → `timeline.js` (TL) → `engine.js` → `scene.js`.
`scene.js` gọi `initEngine(SCENE)` trước khi gọi `line()/paper()/chip()...`. Mở bằng `file://` nên mọi đường dẫn là tương đối.
`render(t)` thuần theo thời gian: tất cả trạng thái tính từ `t` (không CSS animation), nên chụp từng khung cho kết quả xác định.

## 2. Cấu hình SCENE (scene.js)
| Khoá | Ý nghĩa |
|---|---|
| `brand` | `{t1,t2,loc,demo}`: tên + dòng phụ (góc trên trái), nhãn địa điểm (phải), nhãn "BẢN DEMO" (vàng). Bỏ khoá nào thì ẩn. |
| `pins` | `[{id,lat,lon,label,side:'R'|'L'}]`. id hiện trong chấm. **Thứ tự phải khớp `--pins` của fetch_map.py** (ảnh chi tiết det1..N). |
| `route` | `[[lat,lon],...]` đi qua các ghim; vẽ bằng đường cong Catmull-Rom. `[]` nếu không có tuyến. Đây là tuyến **minh hoạ**: luôn ghi chú trên màn hình. |
| `train` | `{t0,t1}`: tàu chạy hết tuyến trong khoảng này (tốc độ đều); vệt neon vẽ dần sau tàu; ghim chuyển cyan + xung khi tàu qua. `null` = không có tàu (ghim sáng sẵn). |
| `places` | `[[tên,lat,lon,sMin,sMax]]` nhãn địa danh, chỉ hiện khi scale camera trong [sMin,sMax] (vd. 0–0.6 cho toàn cảnh, 1.3–9 khi zoom sâu). |
| `rings` | `[{lat,lon,r,t0,t1,col}]` vòng xung 3 lớp; `r` là bán kính px **ảnh nền** (zoom MAPCFG.z; ~18 m/px ở z13 vĩ độ 16° → 230px ≈ 4,2 km). |
| `labwin` | `{idGhim:[[a,b] | {pass:[da,db]}]}` cửa sổ hiện nhãn; `{pass}` tính từ lúc tàu qua ghim. |
| `dim` | `[[a,b]]` tối bản đồ 38% khi có thẻ/số liệu đè (nên dùng cho mọi đoạn có nhiều chữ). |
| `ov` | `{scale, center}`: scale toàn cảnh (lấy từ plan_map.py), `center` [lat,lon] tuỳ chọn (mặc định tâm bbox tuyến). |
| `credit` | dòng ghi nguồn ảnh (mặc định Esri); `''` để ẩn. |

## 3. Camera
Tâm khung đặt ở (540, 1000). `cam` gồm ba pha nối tiếp:
1. **Toàn cảnh** từ 0 đến đầu pha sau, đẩy chậm `push` (mặc định +10%).
2. **Bám tàu** (`follow:[tBắtĐầu,tKếtThúc,giâyZoomVào,scale]`): camera trượt từ toàn cảnh tới vị trí tàu, rồi đi theo (nhìn trước 2% chiều dài).
3. **Keyframe** `keys:[[t,đích,scale],...]`: vị trí easeInOut, scale nội suy mũ (zoom đều mắt). Đích: `'OV'` toàn cảnh, id ghim, `'END'` cuối tuyến, `[lat,lon,dyPx]`, `{px:[x,y]}`.
Mẫu bay kiểu Google Earth: toàn cảnh → zoom vào vị trí (scale 1,9–2,3 dùng ảnh chi tiết z14) → đẩy chậm trong lúc hiện số liệu → zoom ra.
Ảnh chi tiết (det*.jpg) tự hiện khi scale > 1,05 (đủ nét ở 2,3). Cảnh nền chuyển MAP → DARK → MAP: camera giữa hai cảnh bản đồ không nhìn thấy, tự nội suy; chỉ cần keyframe đầu của cảnh bản đồ sau đặt đúng vị trí mong muốn.

## 4. Phần tử chữ/thẻ (toạ độ y = tâm; khung 1080x1920; chừa ~250px đáy cho giao diện nền tảng)
| Hàm | Dùng cho |
|---|---|
| `line(text,cls,cap,y,tin,tout,opt)` | chữ/số IN HOA. `cls`: `'w'` trắng, `'c'` cyan, `'r'` đỏ. `cap` = chiều cao chữ hoa (px). `anim`: `track` (mặc định), `hero` (phóng 1,7→1), `count` (`count:[from,to,suffix,plus]`), `pulse`. `sfx`/`g` đổi âm. Tự thu nhỏ nếu rộng > 950px. |
| `paper(img,tag,y,w,tin,tout,rot,{dark})` | thẻ ảnh báo trắng + nhãn nguồn đỏ ("TÊN BÁO · NGÀY"). |
| `chip(icon,text,y,tin,tout)` | viên thuốc gạch đầu dòng, trượt từ trái. Text ≤ ~22 ký tự. |
| `src(text,y,tin,tout)` / `note(text,y,tin,tout)` | dòng nguồn 30px / ghi chú 28px (không tự thu nhỏ: ≤ ~60 ký tự). |
| `raw(html,tin,tout,'fade'|'pop')` | tuỳ ý: nút `.cta`, câu miễn trừ `.disc`. |
`tin` = lúc giọng đọc chạm từ khoá (lấy từ khoảng lặng của vo_prep.sh), `tout` = đầu cảnh sau.
`FX.flash=[[t,dur,max]]`, `FX.glow=[[t,dur]]`, `FX.sweep=[[t]]`; `sfx(t,name,gainDb)` thêm âm riêng.

## 5. timeline.js, âm thanh, SFX
Xem chú thích đầu `assets/template/timeline.js`. `drop` nên đặt vào câu chốt/tiêu đề chính (nhạc vào full beat + impact + flash). `audio.py` mix giọng + nhạc tổng hợp (Am–F–C–G, 100 BPM) + SFX, ducking nhạc dưới giọng, loudnorm −14 LUFS.
SFX có sẵn: `whoosh pop ting impact riser shutter heartbeat notify cash sparkle`.
Gắn: whoosh cho chuyển cảnh/zoom ra; pop chữ trắng; ting giá trị cyan; impact số lớn; riser trước drop; shutter khi thẻ báo vào; sparkle cho tên/CTA.

## 6. Kích thước ảnh nền
Ở scale `s`, ảnh nền phải phủ `540/s` px sang hai bên, `1000/s` px lên trên và `920/s` px xuống dưới tính từ tâm camera, nếu không mép ảnh lộ nền navy. Tuyến chạy chéo nên bbox "vừa tuyến" luôn thiếu, nhất là chiều dọc.
`python3 scripts/plan_map.py --route "lat,lon;lat,lon;..."` tính sẵn scale + bbox + lệnh `fetch_map.py`. (Metro Đà Nẵng – Chu Lai: tuyến 2948x3858px ở z13 → s=0,32 → bbox LAT 15,25–16,25 × LON 108,10–108,78 → ảnh 4352x6144, ~420 ô.)
`seafix.py` làm đồng màu mặt biển, giả định biển ở mép **phải**. Bản đầu (ngưỡng chặt) để lại các mảng sáng hình chữ nhật ven bờ; bản hiện tại nới ngưỡng và giãn mặt nạ 1 vòng — vẫn mất vài đảo nhỏ. Kiểm tra thumbnail sau khi tải.

## 7. Lệnh render
```bash
node scripts/render.js <project> preview 3.5 14.9 29.2          # xem nhanh vài thời điểm -> <project>/prev/t*.jpg
bash scripts/make_video.sh <project> out_v1.mp4                 # render đủ (3 tiến trình) + mix + MP4; 84s ≈ 6 phút -> chạy nền
bash scripts/make_video.sh <project> out_v2.mp4 315 1015        # chỉ render lại khung 315–1015 rồi ghép
ffmpeg -i out_v1.mp4 -c:v libx264 -preset slow -crf 26 -c:a copy -movflags +faststart nho.mp4   # 87MB -> ~30MB để gửi
```
Cần: Node + Playwright/Chromium, ffmpeg, Python3 + numpy, Pillow, scipy (`pip install scipy` nếu thiếu).
