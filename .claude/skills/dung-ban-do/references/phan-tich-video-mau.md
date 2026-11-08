# Phân tích video bản đồ mẫu: "Mô phỏng hướng tuyến Metro Đà Nẵng – Chu Lai"

Video mẫu: 61 giây, 576x1024 (9:16), 30fps, có logo L&D (Invest & Develop) góc trên phải, watermark Google Earth dưới đáy.
Tài liệu này ghi lại cách video đó được làm để áp dụng cho video khác. Phần "công cụ" là suy luận từ hình ảnh, chưa xác nhận.

## 1. Cấu trúc theo thời gian
| Giây | Nội dung |
|---|---|
| 0–5 | **Teaser toàn tuyến**: camera bay lướt dọc bờ biển, các nhãn điểm chính hiện dần để người xem thấy cả tuyến, rồi lia về điểm đầu. |
| 6–46 | **Chạy tàu dọc tuyến**: camera nghiêng ~60°, bám tàu. Sau tàu là vệt neon cyan, phía trước là đường mờ. Nhãn hiện khi tàu tới gần, biến mất khi đã qua. |
| 46–53 | **Cao trào**: camera orbit quanh điểm cuối (Chu Lai), vòng tròn vàng đồng tâm phát xung, polygon khu vực tô viền (cảng, khu kinh tế, khu đô thị, sân bay). |
| 54–61 | **Pull-back** lùi ra toàn cảnh, giữ 4–5s với mọi nhãn cùng hiện — khung "chốt" để nhớ. |

**Tiết tấu không đều (quan trọng)**: đoạn dày điểm quan trọng tàu chạy ~1,8 km/s; đoạn thưa dân cư ~3 km/s. Thời gian dừng nhiều ở chỗ có thông tin, lướt nhanh ở chỗ trống, nên 104 km vẫn gọn trong ~40s.

## 2. Các lớp hình ảnh (từ dưới lên)
1. Ảnh vệ tinh 3D kiểu Google Earth, camera nghiêng, hướng nhìn bám theo tuyến.
2. Vệt tuyến cyan phát sáng, vẽ dần sau tàu.
3. Đoàn tàu 3D 4 toa trắng đỏ, đúng phối cảnh.
4. Polygon khu vực vẽ dính mặt đất: vàng = KCN, cyan = ranh hành chính, tím = cảng, cam = sân bay, xanh lá = khu đô thị, đỏ = điểm nhấn.
5. Nhãn 2 kiểu: (a) nút giao/nhà ga — pill nền navy, viền + chấm màu, chữ trắng; (b) khu vực — thẻ trắng, sọc màu bên trái, dòng nhỏ "KHU VỰC" phía trên, tên đậm phía dưới. Mọi nhãn có đường dẫn mảnh xuống đúng điểm.
6. HUD đáy: gradient tối; dòng nhỏ cyan "MÔ PHỎNG HƯỚNG TUYẾN"; tiêu đề trắng đậm; **thanh tiến độ km** với các chấm ga đặt **theo tỷ lệ km thật**, thanh tô cyan dần, số km chạy theo đầu thanh.
7. Logo cố định góc trên phải. Giữ dòng ghi nguồn ảnh (Google Earth).

## 3. Mã màu nhãn nút giao (suy đoán)
Xanh dương = nút giao thông thường; đỏ = nút giao nối KCN/cảng/sân bay (đầu mối kinh tế); vàng/cam = đô thị, du lịch (Tam Kỳ, Hội An). Chọn mã màu cố định cho từng loại và giữ xuyên suốt video.

## 4. Kỹ thuật cần giữ khi làm video khác
- Mở bằng teaser toàn tuyến → đi theo tuyến → một cao trào có vòng xung → pull-back chốt.
- Tốc độ theo thông tin, không theo quãng đường.
- Nhãn hiện khi tàu tới gần, mất khi qua: mỗi lúc 3–5 nhãn.
- Thanh km tỷ lệ thật giúp người xem biết "đã đi được bao xa".
- Vòng tròn xung = "bán kính X km quanh dự án".

## 5. Cách phân tích một video mẫu mới
**Nếu video mẫu chính là video được mô tả ở trên** (61s, 576x1024, logo L&D): coi các mục 1–4 là giả thuyết, vẫn trích khung để xác nhận vài số liệu (km theo giây, nhãn) rồi mới trả lời; đừng chép lại nguyên văn.
```bash
V=video.mov; mkdir -p frames sheets
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 $V
ffmpeg -v error -i $V -vf "fps=1,scale=288:-1" frames/f_%03d.jpg        # f_001 = giây 0
# contact sheet 12 khung (6x2): số tấm = ceil(độ_dài/12); sheet i, ô k (k=0..11, trái→phải, trên→dưới) ≈ giây 12*i + k
N=$(python3 -c "import math;print(math.ceil($(ffprobe -v error -show_entries format=duration -of csv=p=0 $V)/12))")
for i in $(seq 0 $((N-1))); do ffmpeg -v error -y -start_number $((i*12+1)) -framerate 1 -i frames/f_%03d.jpg -vf tile=6x2 -frames:v 1 sheets/sheet_$i.jpg; done
# CHÚ Ý: fps=1 lấy khung gần đầu mỗi giây nên lệch tới ±0,5s so với mốc 'giây N'. Cần số chính xác (km, mốc nhãn) thì trích đúng giây: ffmpeg -ss N -i $V -frames:v 1 ...
ffmpeg -i $V -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"   # điểm cắt cảnh; KHÔNG in gì = một cú máy liên tục (cũng là một kết luận)
ffmpeg -ss 15 -i $V -frames:v 1 full15.png      # khung đủ độ phân giải để đọc HUD/nhãn (ô 288px thường không đọc nổi số km)
# dải HUD km tại nhiều mốc, xếp chồng để đọc một lượt (chỉnh y/h theo vị trí thanh km trong video: ở video mẫu ~ y=800..870 trên khung 1024)
for t in 6 12 20 28 36 44 46; do ffmpeg -v error -y -ss $t -i $V -frames:v 1 -vf "crop=iw:90:0:800,scale=iw*2:-1" km_$t.png; done
ffmpeg -v error -y $(for t in 6 12 20 28 36 44 46; do echo -n "-i km_$t.png "; done) -filter_complex vstack=7 km_strip.png
# vị trí các chấm ga trên thanh -> km: (x_chấm − x_đầu_thanh) / (x_cuối_thanh − x_đầu_thanh) × tổng_km; đọc x bằng PIL (cột pixel sáng/trắng dọc dải) rồi gán tên theo thứ tự nhãn xuất hiện — video không ghi tên trên thanh, nên gán là suy ra
# lấy màu thật (hex): python3 -c "from PIL import Image;print('#%02X%02X%02X'%Image.open('full15.png').convert('RGB').getpixel((x,y)))" (lấy ở lõi nét, tránh viền mờ/glow)
ffmpeg -i $V -af volumedetect -vn -f null -     # có âm thanh không
ffmpeg -i $V -af silencedetect=noise=-40dB:d=1 -vn -f null - 2>&1 | grep silence   # khoảng lặng
ffmpeg -i $V -af ebur128 -vn -f null - 2>&1 | grep -E 'I:|LRA:'               # độ to tích hợp
```
Cảnh báo khi diễn giải: (1) scene-detect không in gì chỉ nói **không có cắt cứng** ở ngưỡng 0,25 — cú mờ chồng (dissolve) có thể lọt; xác nhận bằng contact sheet rằng khung liền mạch. (2) LUFS/LRA phẳng và không có khoảng lặng gợi ý nhạc nền liên tục nhưng **không chứng minh** có hay không lời bình; muốn biết thì nghe, hoặc đưa file (qua URL tải được) cho `audio_transcribe` xem có chữ không. Nói rõ phần nào chưa nghe.
Xem từng sheet (Read ảnh), ghi lại: mốc thời gian từng giai đoạn, số km theo giây (để suy ra tốc độ), kiểu nhãn, màu, HUD. Âm thanh chỉ đo được mức to/khoảng lặng, không nghe được nội dung — nói rõ.

**Khung trả lời cho người dùng:** (1) thông số + cái đã kiểm chứng; (2) cấu trúc theo giây; (3) tiết tấu (bảng km/giây); (4) các lớp hình ảnh; (5) video KHÔNG có gì; (6) công thức áp dụng + **khoảng cách với engine** (bảng bên dưới) + dữ liệu cần người dùng chuẩn bị; (7) phần chưa chắc (công cụ gốc, hex màu, âm thanh).

## 6. Khoảng cách giữa video mẫu và engine hiện có
| Trong video mẫu | Engine `dung-ban-do` | Cách xử lý |
|---|---|---|
| Camera nghiêng ~60°, orbit | **Chưa có**: nhìn thẳng từ trên xuống, chỉ pan/zoom | chấp nhận nhìn từ trên xuống; hoặc thêm CSS `perspective/rotateX` cho lớp bản đồ (cần phát triển) |
| Polygon khu vực tô viền theo màu (đã xác nhận: vàng cam = KCN/khu kinh tế; **đỏ = Khu đô thị Chu Lai**; tím = cảng; cam = sân bay; **xanh lá = ranh Hội An + KĐT Vịnh An Hòa**; cyan = ranh Tam Kỳ) | **Có** (`zones`, `kind` theo đúng mã màu này) | cần ranh giới thật (quy hoạch/OSM) |
| Thẻ "KHU VỰC" trắng + sọc màu | **Có** (thẻ của `zones`) | — |
| Thanh tiến độ km có chấm ga tỷ lệ thật | **Có** (`kmbar`) | cần km cộng dồn từng ga |
| Logo cố định góc trên phải | **Có** (`logo`) | cần file logo của người dùng |
| Tàu 4 toa, vệt neon, nhãn, ghim, vòng xung | **Có** (`train`, `pins`, `rings`) | dùng trực tiếp |
| Ghim ga phụ không nhãn | Có (`dot:true`) | — |
