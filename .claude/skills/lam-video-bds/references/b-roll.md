# B-roll (cảnh trám) trong MAP EXPLAINER

## B-roll là gì, dùng để làm gì
B-roll (cảnh trám) là các đoạn quay ngắn phủ lên lời đọc để **minh hoạ điều đang nói** và **đổi hình**, người xem không phải nhìn mãi một nền bản đồ. Trong dạng video này bản đồ + số liệu vẫn là xương sống; B-roll chiếm khoảng **30–40%** thời lượng, không hơn, và luôn phục vụ câu đang đọc.

## Có 3 loại tư liệu, mỗi loại một cách dùng
| Loại | Ví dụ | Cách dùng | Tiếng |
|---|---|---|---|
| **Người dẫn** (talking head) | Linh nói trước camera ở đoạn mở và kết | toàn khung hoặc khung nhỏ bo góc | **dùng tiếng thật của người đó** |
| **B-roll địa điểm / hoạt động** | sông Hàn, cầu Rồng, bãi biển, sân bay, khách du lịch, căn hộ, nội thất, dọn phòng, check-in | PiP cạnh bản đồ, hoặc toàn khung thay nền DARK | **tắt tiếng**, giọng đọc phủ lên |
| **Tư liệu/tài liệu** | slide chính sách, bản vẽ, ảnh báo | dùng thẻ `paper()` (không phải clip) | không có |

**Quy tắc vàng về tiếng:** giọng AI nhân bản không khớp khẩu hình. Khi người dẫn **xuất hiện trên hình và nói**, phải dùng giọng thật của họ (đưa tiếng vào `timeline.vo`). Giọng AI chỉ dùng cho các đoạn **voice-over** phủ B-roll hoặc bản đồ.

## Hai kiểu bố cục
- **Toàn khung (full-bleed)**: clip thay nền, chữ nằm trên; thêm lớp tối phía sau chữ (gradient 55%) để đọc được. Dùng ở cảnh nền DARK, hoặc khi nội dung là "hình ảnh" (nội thất, khách sạn).
- **Khung nhỏ (PiP)** bo góc 30, viền cyan 4, đổ bóng, đặt cạnh bản đồ hoặc dưới thẻ số liệu (ví dụ 480×640 tại x 60, y 520). Dùng khi bản đồ vẫn là nhân vật chính.

## Quy tắc dựng
1. Mỗi clip **1,5–3 giây** (tối đa 5); cắt theo ý chứ không theo nhịp nhạc; đoạn liền nhau ≥ 2 clip khác cảnh.
2. **Khớp từ khoá**: clip khách sạn xuất hiện khi giọng nói "khách sạn ven biển", không sớm hơn 0,1 s.
3. Không đặt clip lên cảnh đang có thẻ báo/chip lớn cùng vùng; nếu đè chữ thì dùng PiP hoặc dim.
4. Vào/ra mờ 0,2 s (mặc định của `clip()`), kèm `whoosh` −3 dB khi đổi cảnh lớn.
5. Ảnh tĩnh làm B-roll: đẩy chậm 100% → 108% trong suốt đoạn (tách thành chuỗi khung bằng ffmpeg `zoompan` — chưa thử trong phiên này) để không đơ.
6. Màu: nếu clip quá sáng/rực, hạ sáng/độ bão hoà khi tách khung (`-vf eq=brightness=-0.05:saturation=0.9`) để hợp nền navy.

## Chuẩn bị tư liệu
**Quay mới (khuyến nghị):** dọc 9:16, 4K hoặc 1080p, 30 fps, 5 giây mỗi cảnh, máy ổn định (gimbal hoặc tay vịn), ánh sáng tốt, không chữ/logo bên thứ ba. Người dẫn: mic cài áo, nền gọn, nói từng câu theo `loi-doc.txt`.
**Dùng có sẵn (Drive):** liệt kê file theo thư mục, xem nhanh (khung đầu/giữa/cuối), chọn 3–5 s đẹp nhất. Chỉ mở/dùng thư mục mà người dùng nói rõ được phép; nếu B-roll nằm trên máy chủ ảo (pod), cần cách truy cập an toàn (cổng HTTP tạm + credential theo tên miền, hoặc Drive) và bật pod trong lúc tải.

**Tách khung (mỗi clip một thư mục):**
```bash
# cắt 4s từ giây 12, ép về 1080x1920 (cắt giữa nếu quay ngang), bỏ tiếng
ffmpeg -ss 12 -t 4 -i nguon.mov -an \
  -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 3 clips/a/%05d.jpg
ls clips/a | wc -l      # = số khung (120 cho 4s)
```
Quay ngang: dùng làm PiP (`fit:'cover'`) hoặc chấp nhận cắt giữa; không kéo giãn.

## Dùng trong `scene.js` (tạo clip **trước** các `line()` để chữ nằm trên)
```js
// toàn khung, nền cho cảnh "VẬN HÀNH" (55–67 s): 3 clip nối nhau
clip('clips/noithat/%05d.jpg', 90, 30, 55.0, 58.0, {fit:'cover'});
clip('clips/donphong/%05d.jpg', 90, 30, 58.0, 61.0, {fit:'cover'});
raw('<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(3,10,18,.55),rgba(3,10,18,.35) 40%,rgba(3,10,18,.7))"></div>', 55.0, 67.0);
// khung nhỏ cạnh bản đồ (41–55 s)
clip('clips/kssongHan/%05d.jpg', 90, 30, 44.0, 47.0, {x:60,y:520,w:480,h:640,radius:30,border:'4px solid #05F4E8',shadow:true});
```
Nhớ thêm khoảng thời gian cảnh trong `timeline.bgs`: cảnh dùng clip toàn khung nên là `["DARK", …]` (hoặc `MAP` nếu clip chỉ là PiP).
**Người dẫn nói trên hình:** tách tiếng `ffmpeg -i nguon.mov -vn -ar 48000 -ac 1 vo/linh_mo.wav`, thêm `["linh_mo.wav", tBắtĐầu, 0, null]` vào `timeline.vo`, đổi `tin` của chữ/phụ đề theo khoảng lặng của file đó. Âm thanh trong B-roll thông thường **không** đưa vào mix (audio.py chuẩn hoá mọi file vo về cùng mức tiếng nói).

## Giới hạn kỹ thuật đã đo
- Clip toàn khung 1080p: 240 khung (2 clip × 4 s) làm tăng bộ nhớ trình duyệt khoảng +170 MB mỗi tiến trình (đỉnh ~910 MB so với ~740 MB không clip). `make_video.sh` chạy 3 tiến trình → khoảng 3 GB. Mỗi khung JPG chất lượng 3 ≈ 115 KB (4 s ≈ 14 MB).
- Khuyến nghị: ≤ ~20 clip, mỗi clip ≤ 5 s (150 khung), tổng B-roll ≤ ~40 s. Chưa thử vượt mức này.
- Thời gian chụp thử tăng nhẹ (2 khung xem trước: 4,0 s → 4,3–4,9 s, chủ yếu do nạp ảnh).
- `clip()` ghép **hình**; chưa phối hợp tiếng quay + tiếng AI cùng lúc ngoài cách `timeline.vo` ở trên.

## Bản quyền và quyền riêng tư
Chỉ dùng tư liệu mình quay hoặc được cấp phép; người xuất hiện rõ mặt cần đồng ý; không logo/biển hiệu bên thứ ba rõ nét; bỏ nhạc trong clip (đã `-an`); flycam theo quy định địa phương; công trình/dự án của chủ đầu tư cần phép dùng hình ảnh. Mỗi video giữ file `nguon-b-roll.md`: tên file, nguồn, người quay, cho phép dùng đến ngày nào.

## Ví dụ: kế hoạch B-roll cho video Metro Đà Nẵng – Khánh Linh (90 s)
| Giây | Nội dung đang nói | B-roll đề xuất | Kiểu |
|---|---|---|---|
| 0–14 | hook "metro 266 nghìn tỷ… kỳ vọng hay nên chờ?" | Linh nói trước camera 4–5 s + 2 cảnh Đà Nẵng (cầu Rồng, sông Hàn) mỗi cảnh 2 s | toàn khung |
| 14–22 | tuyến 103 km | **không B-roll** — để bản đồ | — |
| 22–35 | khách lưu trú, khách quốc tế | khách du lịch, sân bay, biển Mỹ Khê (3 clip × 3 s) | PiP hoặc toàn khung DARK |
| 35–41 | "ba tiêu chí" | Linh nói trước camera | toàn khung |
| 41–55 | vị trí, khách sạn ven biển/sông Hàn | khách sạn ven biển, pháo hoa (2–3 clip) | PiP cạnh bản đồ |
| 55–67 | vận hành, 7 năm nội thất, 3 năm lưu trú | nội thất căn hộ, dọn phòng, check-in, kiểm tra chi phí (3–4 clip) — **cảnh cá nhân mạnh nhất** | toàn khung |
| 67–80 | vốn vay (thẻ 10% – 24 tháng – 0%) | Linh tư vấn khách/ký hồ sơ (nếu khách đồng ý) hoặc không B-roll, giữ thẻ số liệu | PiP nhỏ |
| 80–90 | mốc theo dõi + CTA | Linh nhìn camera "nhắn Linh nhé" | toàn khung |
Tổng ≈ 32–38 s (~40%).
