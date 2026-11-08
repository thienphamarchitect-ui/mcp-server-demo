# Phần 1 — B-roll (cảnh trám) dùng như thế nào
# Phần 2 — Định nghĩa dạng video "MAP EXPLAINER" để áp dụng cho các video sau

Bản NHÁP để duyệt, bổ sung cho `01-quy-trinh-…` và `02-chuan-…`.

---

# PHẦN 1. B-ROLL

## 1.1 B-roll là gì, dùng để làm gì
B-roll (cảnh trám) là các đoạn quay ngắn phủ lên lời đọc để **minh hoạ điều đang nói** và **đổi hình**, người xem không phải nhìn mãi một nền bản đồ. Trong dạng video này bản đồ + số liệu vẫn là xương sống; B-roll chiếm khoảng **30–40%** thời lượng, không hơn, và luôn phục vụ câu đang đọc.

## 1.2 Có 3 loại tư liệu, mỗi loại một cách dùng
| Loại | Ví dụ | Cách dùng | Tiếng |
|---|---|---|---|
| **Người dẫn** (talking head) | Linh nói trước camera ở đoạn mở và kết | toàn khung hoặc khung nhỏ bo góc | **dùng tiếng thật của người đó** |
| **B-roll địa điểm / hoạt động** | sông Hàn, cầu Rồng, bãi biển, sân bay, khách du lịch, căn hộ, nội thất, dọn phòng, check-in | PiP cạnh bản đồ, hoặc toàn khung thay nền DARK | **tắt tiếng**, giọng đọc phủ lên |
| **Tư liệu/tài liệu** | slide chính sách, bản vẽ, ảnh báo | dùng thẻ `paper()` (không phải clip) | không có |

**Quy tắc vàng về tiếng:** giọng AI nhân bản không khớp khẩu hình. Khi người dẫn **xuất hiện trên hình và nói**, phải dùng giọng thật của họ (đưa tiếng vào `timeline.vo`). Giọng AI chỉ dùng cho các đoạn **voice-over** phủ B-roll hoặc bản đồ.

## 1.3 Hai kiểu bố cục
- **Toàn khung (full-bleed)**: clip thay nền, chữ nằm trên; thêm lớp tối phía sau chữ (gradient 55%) để đọc được. Dùng ở cảnh nền DARK, hoặc khi nội dung là "hình ảnh" (nội thất, khách sạn).
- **Khung nhỏ (PiP)** bo góc 30, viền cyan 4, đổ bóng, đặt cạnh bản đồ hoặc dưới thẻ số liệu (ví dụ 480×640 tại x 60, y 520). Dùng khi bản đồ vẫn là nhân vật chính.

## 1.4 Quy tắc dựng
1. Mỗi clip **1,5–3 giây** (tối đa 5); cắt theo ý chứ không theo nhịp nhạc; đoạn liền nhau ≥ 2 clip khác cảnh.
2. **Khớp từ khoá**: clip khách sạn xuất hiện khi giọng nói "khách sạn ven biển", không sớm hơn 0,1 s.
3. Không đặt clip lên cảnh đang có thẻ báo/chip lớn cùng vùng; nếu đè chữ thì dùng PiP hoặc dim.
4. Vào/ra mờ 0,2 s (mặc định của `clip()`), kèm `whoosh` −3 dB khi đổi cảnh lớn.
5. Ảnh tĩnh làm B-roll: đẩy chậm 100% → 108% trong suốt đoạn (tách thành chuỗi khung bằng ffmpeg `zoompan` — chưa thử trong phiên này) để không đơ.
6. Màu: nếu clip quá sáng/rực, hạ sáng/độ bão hoà khi tách khung (`-vf eq=brightness=-0.05:saturation=0.9`) để hợp nền navy.

## 1.5 Chuẩn bị tư liệu
**Quay mới (khuyến nghị):** dọc 9:16, 4K hoặc 1080p, 30 fps, 5 giây mỗi cảnh, máy ổn định (gimbal hoặc tay vịn), ánh sáng tốt, không chữ/logo bên thứ ba. Người dẫn: mic cài áo, nền gọn, nói từng câu theo `loi-doc.txt`.
**Dùng có sẵn (Drive):** liệt kê file theo thư mục, xem nhanh (khung đầu/giữa/cuối), chọn 3–5 s đẹp nhất. Thư mục bạn chia sẻ ban đầu tôi chưa mở được; thư mục "video chung", "Thiện", "Linh" và các file `RegalHomes_*.mp4` đã thấy nhưng **chưa mở** — cần bạn cho biết thư mục nào được phép dùng.

**Tách khung (mỗi clip một thư mục):**
```bash
# cắt 4s từ giây 12, ép về 1080x1920 (cắt giữa nếu quay ngang), bỏ tiếng
ffmpeg -ss 12 -t 4 -i nguon.mov -an \
  -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 3 clips/a/%05d.jpg
ls clips/a | wc -l      # = số khung (120 cho 4s)
```
Quay ngang: dùng làm PiP (`fit:'cover'`) hoặc chấp nhận cắt giữa; không kéo giãn.

## 1.6 Dùng trong `scene.js` (tạo clip **trước** các `line()` để chữ nằm trên)
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

## 1.7 Giới hạn kỹ thuật đã đo
- Clip toàn khung 1080p: 240 khung (2 clip × 4 s) làm tăng bộ nhớ trình duyệt khoảng +170 MB mỗi tiến trình (đỉnh ~910 MB so với ~740 MB không clip). `make_video.sh` chạy 3 tiến trình → khoảng 3 GB. Mỗi khung JPG chất lượng 3 ≈ 115 KB (4 s ≈ 14 MB).
- Khuyến nghị: ≤ ~20 clip, mỗi clip ≤ 5 s (150 khung), tổng B-roll ≤ ~40 s. Chưa thử vượt mức này.
- Thời gian chụp thử tăng nhẹ (2 khung xem trước: 4,0 s → 4,3–4,9 s, chủ yếu do nạp ảnh).
- `clip()` ghép **hình**; chưa phối hợp tiếng quay + tiếng AI cùng lúc ngoài cách `timeline.vo` ở trên.

## 1.8 Bản quyền và quyền riêng tư
Chỉ dùng tư liệu mình quay hoặc được cấp phép; người xuất hiện rõ mặt cần đồng ý; không logo/biển hiệu bên thứ ba rõ nét; bỏ nhạc trong clip (đã `-an`); flycam theo quy định địa phương; công trình/dự án của chủ đầu tư cần phép dùng hình ảnh. Mỗi video giữ file `nguon-b-roll.md`: tên file, nguồn, người quay, cho phép dùng đến ngày nào.

## 1.9 Kế hoạch B-roll cho video Metro Đà Nẵng – Khánh Linh (90 s)
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

---

# PHẦN 2. ĐỊNH NGHĨA DẠNG VIDEO "MAP EXPLAINER"

**Tên gọi:** MAP EXPLAINER (tên tiếng Việt: *Bản đồ giải thích quan điểm đầu tư*). Khi yêu cầu video mới, chỉ cần nói "làm một MAP EXPLAINER về …" kèm 10 trường ở mục 2.4.

## 2.1 Định nghĩa
Video dọc ngắn (60–90 s) của một **người tư vấn bất động sản**, biến **một tin hạ tầng/quy hoạch/thị trường đang nóng** thành **quan điểm đầu tư rõ ràng**, dùng **bản đồ vệ tinh làm xương sống hình ảnh**, **số liệu có nguồn** làm bằng chứng, **một khung 3 tiêu chí** làm cách nhìn riêng, và kết bằng **mốc theo dõi + lời mời hành động**. Quan điểm luôn hai chiều ("kỳ vọng có điều kiện"), không hứa lợi nhuận.

**Một video = 1 chủ đề + 1 thông điệp + 1 khung tiêu chí + 1 CTA.**

## 2.2 Thông số
- 9:16, 1080×1920, 30 fps, H.264, **60–90 s** (không quá 120 s); lời đọc ~2,7 từ/giây (90 s ≈ 245 từ).
- Một người dẫn (giọng + tuỳ chọn khuôn mặt); xưng "mình", câu ≤ 20 từ.
- Màu/chữ/chuyển động/SFX theo `02-chuan-…`.

## 2.3 Cấu trúc 6 khối (tỷ lệ thời lượng, ví dụ video 90 s)
| Khối | Tỷ lệ | Giây (90 s) | Nội dung | Hình chính |
|---|---|---|---|---|
| 1. **Hook trả lời trước** | 12–15% | 0–13 | câu hỏi đối lập + kết luận một dòng + giới thiệu người dẫn | chữ hero + bản đồ toàn cảnh (+ người dẫn) |
| 2. **Bối cảnh bản đồ** | 8–12% | 13–22 | sự kiện/tuyến/khu vực là gì, mốc thời gian | tuyến phát sáng + tàu, hoặc ghim + vòng km |
| 3. **Bằng chứng số liệu** | 15–20% | 22–36 | 1–2 số "đang chạy thật" có nguồn | thẻ số cyan + ảnh báo chứng |
| 4. **Khung 3 tiêu chí** | 30–35% | 36–80 | 3 tiêu chí chọn sản phẩm, mỗi tiêu chí 1 số/1 bằng chứng + câu chuyện cá nhân | bản đồ zoom / chip / thẻ số liệu / B-roll |
| 5. **Mốc theo dõi** | 5–8% | 80–86 | 3 mốc cần chờ để thay đổi quan điểm | 3 chip + bản đồ toàn cảnh |
| 6. **CTA + miễn trừ** | 5–8% | 86–90 | lời mời nhắn tư vấn, nguồn, miễn trừ | nút CTA + dòng nhỏ |

## 2.4 Phiếu yêu cầu (brief) — 10 trường để làm video mới
1. **Chủ đề / sự kiện nóng** + ngày tin. 2. **Câu hỏi hook** (đối lập). 3. **Kết luận một dòng**.
4. **Khu vực/tuyến**: điểm đầu–cuối, các ghim, toạ độ hoặc tên (+ có tàu/vòng km?).
5. **Số liệu** (≥ 2) kèm nguồn + ngày. 6. **3 tiêu chí** của người dẫn (mỗi cái 1 dòng + 1 số/bằng chứng).
7. **3 mốc theo dõi**. 8. **Người dẫn**: tên, chức danh, kinh nghiệm thật, quan điểm, quan hệ lợi ích.
9. **CTA**: kênh liên hệ. 10. **Tư liệu**: B-roll, người dẫn quay, ảnh báo, giọng (AI mẫu hay giọng người dẫn đã đồng ý).

## 2.5 Thành phần bắt buộc / tuỳ chọn
**Bắt buộc:** hook dạng câu hỏi; ≥ 1 cảnh bản đồ (tuyến/ghim/vòng); ≥ 2 số liệu có nguồn trên màn hình; khung 3 tiêu chí; 3 mốc theo dõi; dòng nguồn; câu miễn trừ; brand + CTA; nhãn "minh hoạ" khi tuyến/vòng tự vẽ; nhãn AI khi dùng giọng AI.
**Tuỳ chọn:** B-roll, người dẫn trên hình, phụ đề, ảnh báo chứng, vòng bán kính, thanh km.

## 2.6 Năm biến thể
| Biến thể | Khi dùng | Hình bản đồ |
|---|---|---|
| **A. Tuyến hạ tầng** | metro, cao tốc, vành đai | tuyến + tàu + ghim ga (video Metro Đà Nẵng) |
| **B. Bán kính tiện ích** | sân bay, khu công nghiệp, trung tâm tài chính | ghim + vòng bán kính km tĩnh (mẫu `example-ring`) |
| **C. So sánh hai khu** | "khu nào đáng mua hơn" | hai vòng/hai màu, thẻ so sánh |
| **D. Tin chính sách/thị trường** | lãi suất, bảng giá đất | nền DARK + thẻ số liệu, bản đồ chỉ ở 1–2 cảnh |
| **E. Dòng thời gian dự án** | tiến độ khởi công → vận hành | tuyến + các mốc năm trên bản đồ |

## 2.7 Giọng điệu và nguyên tắc nội dung
Trả lời trước rồi mới giải thích; nêu **cả lý do kỳ vọng lẫn lý do chờ**; một ý một con số; nói thẳng cái chưa chắc ("mới ở bước đề xuất"); không cam kết lợi nhuận; điều kiện tài chính chỉ nêu đúng tài liệu gốc kèm "áp dụng theo chính sách từng thời điểm"; công khai quan hệ lợi ích.

## 2.8 Khi nào KHÔNG dùng dạng này
Nội dung không có địa điểm cụ thể; chỉ muốn giới thiệu một dự án (dùng video giới thiệu dự án); cần phỏng vấn hoặc tư vấn dài; không có số liệu đáng tin để dẫn.

## 2.9 Thước đo sau đăng (theo dõi để cải tiến)
Giữ chân ở giây 3 và giây 15; tỷ lệ xem hết; số lượt nhắn tư vấn từ CTA; so sánh các hook khác nhau trên cùng chủ đề.
