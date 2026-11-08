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
| `pins` | `[{id,lat,lon,label,side:'R'|'L',dy,dx,dot}]`. id hiện trong chấm. `dy/dx`: dời nhãn (px màn hình; dùng khi hai ghim cùng vĩ độ làm nhãn đè nhau). `dot:true`: chấm nhỏ không số (ga phụ). Ghim xám trước khi tàu qua, cyan sau; **không có `train` thì tất cả cyan ngay từ đầu**. Ảnh chi tiết det1..N **không gắn với id ghim** (xem mục 6). |
| `route` | `[[lat,lon],...]` đi qua các ghim; vẽ bằng đường cong Catmull-Rom. `[]` nếu không có tuyến. Đây là tuyến **minh hoạ**: luôn ghi chú trên màn hình. |
| `train` | `{t0,t1}`: tàu chạy hết tuyến trong khoảng này (tốc độ đều); vệt neon vẽ dần sau tàu; ghim chuyển cyan + xung khi tàu qua. `null` = không có tàu (ghim sáng sẵn). |
| `places` | `[[tên,lat,lon,sMin,sMax]]` nhãn địa danh, chỉ hiện khi scale camera trong [sMin,sMax] (vd. 0–0.6 cho toàn cảnh, 1.3–9 khi zoom sâu). |
| `rings` | `[{lat,lon,r|km,t0,t1,col,static,label,labAng}]`. Mặc định là vòng xung 3 lớp nở tới 1,2R. `km` đổi sang px theo vĩ độ (hàm `kmToPx(km,lat)`); `r` là px ảnh nền. `static:true`: vòng bán kính **cố định** nét đứt + nền mờ + đường bán kính + nhãn `label` (đặt ở góc `labAng` độ, mặc định −35°, luôn nằm trong khung), sóng xung nở đúng tới R. |
| `labwin` | `{idGhim:[[a,b] | {pass:[da,db]}]}` cửa sổ hiện nhãn; `{pass}` tính từ lúc tàu qua ghim. **Ghim không khai `labwin` thì không bao giờ hiện nhãn** (kể cả khi không có tàu). |
| `dim` | `[[a,b]]` tối bản đồ 38% khi có thẻ/số liệu đè (nên dùng cho mọi đoạn có nhiều chữ). |
| `ov` | `{scale, center}`: scale toàn cảnh (plan_map.py in sẵn `ov.scale` và `ov.center`). Không khai `center` thì lấy tâm bbox của tuyến, hoặc của các ghim nếu `route` rỗng. |
| `credit` | dòng ghi nguồn ảnh (mặc định Esri); `''` để ẩn. |

## 3. Camera
Tâm khung đặt ở (540, 1000). `cam` gồm ba pha nối tiếp:
1. **Toàn cảnh** từ 0 đến đầu pha sau, đẩy chậm `push` (mặc định +10%).
2. **Bám tàu** (`follow:[tBắtĐầu,tKếtThúc,giâyZoomVào,scale]`): camera trượt từ toàn cảnh tới vị trí tàu, rồi đi theo (nhìn trước 2% chiều dài).
3. **Keyframe** `keys:[[t,đích,scale],...]`: vị trí easeInOut, scale nội suy mũ (zoom đều mắt). Đích: `'OV'` toàn cảnh, id ghim, `'END'` cuối tuyến, `[lat,lon,dyPx]`, `{px:[x,y]}`. `dyPx` > 0 làm camera nhìn thấp hơn điểm đó, tức nội dung **dời lên** trên khung (dùng để chừa chỗ cho thẻ phía dưới); < 0 dời xuống.
Mẫu bay kiểu Google Earth: toàn cảnh → zoom vào vị trí (scale 1,9–2,3 dùng ảnh chi tiết z14) → đẩy chậm trong lúc hiện số liệu → zoom ra.
Ảnh chi tiết (det*.jpg) tự hiện khi scale > 1,05 (đủ nét ở 2,3). Cảnh nền chuyển MAP → DARK → MAP: camera giữa hai cảnh bản đồ không nhìn thấy, tự nội suy; chỉ cần keyframe đầu của cảnh bản đồ sau đặt đúng vị trí mong muốn.

## 4. Phần tử chữ/thẻ (toạ độ y = tâm; khung 1080x1920; chừa ~250px đáy cho giao diện nền tảng)
| Hàm | Dùng cho |
|---|---|
| `line(text,cls,cap,y,tin,tout,opt)` | chữ/số IN HOA. `cls`: `'w'` trắng, `'c'` cyan, `'r'` đỏ. `cap` = chiều cao chữ hoa (px). `anim`: `track` (mặc định), `hero` (phóng 1,7→1), `count` (`count:[from,to,suffix,plus,decimals]`; `decimals:1` cho "19,7"; định dạng Việt 1.234,5; **không dùng cho năm** vì ra "2.027"), `pulse`. `sfx`/`g` đổi âm. Tự thu nhỏ nếu rộng > 950px. |
| `paper(img,tag,y,w,tin,tout,rot,{dark})` | thẻ ảnh báo trắng + nhãn nguồn đỏ ("TÊN BÁO · NGÀY"). |
| `chip(icon,text,y,tin,tout)` | viên thuốc gạch đầu dòng, trượt từ trái. Text ≤ ~22 ký tự. |
| `src(text,y,tin,tout)` / `note(text,y,tin,tout)` | dòng nguồn 30px / ghi chú 28px (không tự thu nhỏ: ≤ ~60 ký tự). |
| `raw(html,tin,tout,'fade'|'pop')` | tuỳ ý: nút `.cta`, câu miễn trừ `.disc`. |
| `captions(list,{y:1560,size:50})` | phụ đề đốt cứng `[[t0,t1,'câu có *từ nhấn*'],...]`, vùng an toàn y 1560–1670, viền đen, nảy nhẹ 0,14 s. Tạo `captions.js` từ lời đọc: `python3 scripts/make_captions.py --lines loi-doc.txt --project <project>` (cần timeline.js + vo/f*.wav), nạp `<script src="captions.js">` trước `engine.js` trong render.html rồi `captions(window.CAPTIONS)`. Chỉ bật ở cảnh không có thẻ nào ở y ≥ 1560. |
| `clip(mẫu,soKhung,fps,tin,tout,{x,y,w,h,radius,border,shadow,fit,loop,from,fade})` | ghép cảnh quay (người dẫn, cảnh trám) bằng **chuỗi ảnh** tách sẵn: `ffmpeg -i in.mp4 -vf "fps=30,scale=1080:-2" clips/a/%05d.jpg`, rồi `clip('clips/a/%05d.jpg',90,30,20,23,{x:60,y:520,w:480,h:640,radius:30,border:'4px solid #05F4E8',shadow:true})`. Vẽ lên canvas theo đúng khung `t` nên render xác định; `render.js` chờ ảnh nạp xong. Toàn khung: bỏ x,y,w,h (mặc định 1080×1920, `fit:'cover'`). Tiếng của clip: thêm vào `timeline.vo` (đã cắt từ video). Tạo clip lúc dựng **trước** các `line()` để chữ nằm trên clip. |
`tin` = lúc giọng đọc chạm từ khoá (lấy từ khoảng lặng của vo_prep.sh), `tout` = đầu cảnh sau.
`FX.flash=[[t,dur,max]]`, `FX.glow=[[t,dur]]`, `FX.sweep=[[t]]`; `sfx(t,name,gainDb)` thêm âm riêng.

## 5. timeline.js, âm thanh, SFX
Xem chú thích đầu `assets/template/timeline.js`. `drop` nên đặt vào câu chốt/tiêu đề chính (nhạc vào full beat + impact + flash). `audio.py` mix giọng + nhạc tổng hợp (Am–F–C–G, 100 BPM) + SFX, ducking nhạc dưới giọng, loudnorm −14 LUFS.
**Video không giọng đọc / cảnh ngắn:** `"vo": []` hợp lệ — `make_video.sh` cho ra MP4 chỉ nhạc + SFX. `drop` = khoảnh khắc nhạc vào full beat + flash: đặt vào **câu/thẻ chốt** (vd. thẻ số cuối của cảnh tuyến + tàu: drop ≈ lúc thẻ hiện, ~9,4s trong 12s; `breakdown` = [drop−1,85, drop−0,15] để nhạc mỏng dần rồi im trước drop; `outro` = total − 1,2..2,5s). Nếu không có khoảnh khắc nào đáng nhấn (cảnh ví dụ `example-ring`, 10s) đặt drop ≈ 40% độ dài (~4s). `beatsFrom` ≥ 1,5s.
**Khung cuối:** engine làm mờ dần sang đen trong 0,6s cuối (`TL.total`); khi trích ảnh xem trước nên lấy trước mốc đó.
**Nhãn `places` và nhãn ghim không tự co vào mép khung** — nhãn ghim `side:'R'` bị cắt khi ghim nằm ở nửa phải khung và `side:'L'` khi ở nửa trái: chọn `side` ngược phía có chỗ trống (ghim sát mép phải → `'L'`; sát mép trái, vd. Thủ Đức ở ví dụ Metro HCM → `'R'`). Chỉ nhãn `label` của vòng `static` được kẹp trong khung (x 130–950, y 260–1640): nó dồn vào vùng y≈260 khi zoom sâu nên đừng đặt tiêu đề `line()` ở y≈150–400, hoặc đổi `labAng`. Nhãn địa danh chỉ bật ở khoảng scale phù hợp (`sMin,sMax`).
SFX có sẵn: `whoosh pop ting impact riser shutter heartbeat notify cash sparkle`.
Gắn: whoosh cho chuyển cảnh/zoom ra; pop chữ trắng; ting giá trị cyan; impact số lớn; riser trước drop; shutter khi thẻ báo vào; sparkle cho tên/CTA.

## 6. Kích thước ảnh nền
Ở scale `s`, ảnh nền phải phủ `540/s` px sang hai bên, `1000/s` px lên trên và `920/s` px xuống dưới tính từ tâm camera, nếu không mép ảnh lộ nền navy. Tâm camera không chỉ ở giữa tuyến: pha bám tàu đi qua **mọi điểm của tuyến** ở scale follow (1,15–1,4), zoom sâu vào một điểm thì scale 1,9–2,3, nên vùng cần phủ là **hợp** của các trường hợp đó.
`python3 scripts/plan_map.py --route "lat,lon;..." [--follow-scale 1.15] [--extra "lat,lon;..." --extra-scale 2.0] [--ring "lat,lon,km"]` tính sẵn `ov.scale`, `ov.center`, bbox (đã cộng đủ lề) và lệnh `fetch_map.py`. Cảnh không có tàu bám: `--follow-scale 0`. **Ảnh chi tiết det1..N** (ô z+1) chỉ là ảnh tự hiện khi scale > 1,05 quanh các điểm `--pins`; không liên quan tới id ghim trong scene.js. Chọn `--pins` là những nơi sẽ zoom sâu (`plan_map.py` mặc định lấy các điểm `--extra`); ngoài vùng ±~500px quanh điểm đó ảnh chi tiết hết (không zoom quá ~2,3). **Tuyến dài mà camera bám tàu ở scale ≥ 1,3:** đừng thêm nhiều ảnh chi tiết (dễ vượt 1500 ô) — tăng `--zoom` của ảnh nền lên 1 bậc (ảnh nền sắc nét, ~4 lần số ô). Ca Metro HCM dùng zoom 15 cho 19,7 km, ~400 ô. (Metro Đà Nẵng – Chu Lai: tuyến 2948x3858px ở z13 → s=0,32 → bbox LAT 15,25–16,25 × LON 108,10–108,78 → ảnh 4352x6144, ~420 ô.)
`seafix.py --sea right|left|top|bottom|none` (và `fetch_map.py --sea ...`) làm đồng màu mặt biển; chọn cạnh ảnh mà biển chạm vào (mặc định `right`; có thể ghép `right,bottom`). Nước đục phù sa (cửa sông Mekong…) và hồ không nhận ra được — vẫn còn mảng ghép ô ở đó; chấp nhận hoặc che bằng nhãn. Bản đầu (ngưỡng chặt) để lại các mảng sáng hình chữ nhật ven bờ; bản hiện tại nới ngưỡng và giãn mặt nạ 1 vòng — vẫn mất vài đảo nhỏ. Kiểm tra thumbnail sau khi tải.

## 7. Lệnh render
(`render.js` dừng ngay với thông báo rõ nếu trang có lỗi JS; kiểm cú pháp: `node --check scene.js engine.js timeline.js`.)
```bash
node scripts/render.js <project> preview 3.5 14.9 29.2          # xem nhanh vài thời điểm -> <project>/prev/t*.jpg
bash scripts/make_video.sh <project> out_v1.mp4                 # render đủ (3 tiến trình) + mix + MP4; 84s ≈ 6 phút -> chạy nền
bash scripts/make_video.sh <project> out_v2.mp4 315 1015        # chỉ render lại khung 315–1015 rồi ghép
ffmpeg -i out_v1.mp4 -c:v libx264 -preset slow -crf 26 -c:a copy -movflags +faststart nho.mp4   # 87MB -> ~30MB để gửi
```
Cần: Node + Playwright/Chromium, ffmpeg, Python3 + numpy, Pillow, scipy (`pip install scipy` nếu thiếu).
