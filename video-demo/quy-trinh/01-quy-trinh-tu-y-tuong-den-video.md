# Quy trình làm video bất động sản có bản đồ: từ ý tưởng đến xuất bản

Bản NHÁP để duyệt. Rút ra từ video "Metro Đà Nẵng – Chu Lai – Khánh Linh" (83,8 s, 9:16) và đã bổ sung phần còn thiếu sau khi rà soát. Chuẩn text/motion/graphic/SFX ở file `02-chuan-text-motion-graphic-sfx.md`.

## A. Rà soát: đã tối ưu chưa?

| Hạng mục | Tình trạng | Ghi chú |
|---|---|---|
| Chuỗi nghiên cứu → kịch bản → dựng → giao | ✅ chạy trọn 1 video | video v1 + skill `dung-ban-do` thử 2 vòng, 20/20 tiêu chí |
| Render xác định, tự mix âm thanh | ✅ | ~5 s render cho mỗi giây video, 3 tiến trình song song |
| Chuẩn text/motion/graphic/SFX bằng thông số thật | ✅ **bổ sung lần này** | file 02 |
| Phụ đề đốt cứng | ✅ **bổ sung** | `captions()` + `make_captions.py` (±0,2 s) |
| Ghép cảnh quay (người dẫn, cảnh trám) | ✅ **bổ sung** | `clip()` bằng chuỗi ảnh tách từ video; đã thử đúng |
| Kiểm soát chất lượng (QC) và đăng bài | ✅ **bổ sung** | mục E, F dưới đây |
| Căn mốc chữ theo giọng | ⚠ thủ công | lấy từ khoảng lặng; mất ~10–15 phút mỗi video |
| Vẽ tuyến theo đường thật | ⚠ tốn thời gian (~40% công) | có `grid_overlay.py` hỗ trợ dò toạ độ |
| Giọng người thật (Linh) | ⏳ chờ | credential RunPod/VoiceStudio chưa áp dụng ở phiên này |
| Polygon khu vực, thanh km tỷ lệ thật, logo ảnh | ❌ chưa có | video mẫu gốc có; engine chỉ có thể bù bằng `rings`/`raw()` |
| Camera nghiêng 3D | ❌ chưa có | engine nhìn thẳng từ trên xuống |
| Nhạc/SFX chất lượng thư viện, stereo, EQ giọng | ❌ chưa có | SFX và nhạc đang tổng hợp |
| Cảnh người dẫn, cảnh trám thật | ❌ chưa có tư liệu | thư mục Drive chưa mở được; `clip()` sẵn sàng |

Kết luận: **quy trình đã đủ để làm ra video có bản đồ + số liệu + giọng đọc + phụ đề + cảnh quay**; các mục ❌ là nâng cấp tuỳ chọn, không chặn việc làm video.

## B. Quy trình 9 bước

### 1. Ý tưởng (10 phút) — ✅ duyệt
- **Chọn chủ đề nóng**: tìm tin mới trong 7 ngày (hạ tầng, quy hoạch, thị trường). Ví dụ: metro 266.000 tỷ.
- **Góc nhìn riêng của nhân vật** (khác biệt so với báo): Linh nhìn theo *dòng tiền*.
- **Hook** dạng câu hỏi đối lập hoặc "trả lời trước": "…kỳ vọng hay nên chờ?"; "kỳ vọng thì có, nhưng đừng mua chỉ vì metro."
- Chốt: độ dài (60–90 s), nền tảng, mục tiêu hành động (nhắn Linh), điều cấm (không hứa lợi nhuận).
- Sản phẩm: 1 câu hook + 1 câu kết luận + danh sách ý chính.

### 2. Phân tích video mẫu (10 phút) — nếu có mẫu
`ffmpeg` trích 1 khung/giây, ghép contact sheet 6×2, cắt dải HUD đọc km theo giây, đo tốc độ. Ghi: giai đoạn, lớp hình, mã màu, tiết tấu. Nói rõ phần engine chưa có.

### 3. Số liệu (10–15 phút)
- `WebSearch` rồi **mở bài gốc** (`WebFetch`), ghi số + ngày + nguồn; cắt ảnh báo chứng (`capture_news.js`) và crop gọn.
- Phân loại: ✔ đã đối chiếu bài gốc / ✱ chỉ từ tóm tắt tìm kiếm (phải ghi "chưa kiểm").
- Chính sách vay/ưu đãi: chỉ nêu đúng các con số trong tài liệu gốc (ví dụ slide hội thảo), kèm "điều kiện áp dụng theo chính sách từng thời điểm".

### 4. Kịch bản (10–15 phút) — ✅ duyệt
- **Mạch**: trả lời trước → tuyến/khu vực → cái đang chạy thật (số liệu) → các tiêu chí → mốc theo dõi + CTA.
- **Giữ chân người xem**: 3 giây đầu có chữ lớn + chuyển động; mở một "vòng lặp" ("3 tiêu chí") rồi trả đúng; số liệu mới mỗi 10–15 s; sự kiện hình mới mỗi 1,5–3 s.
- **Bảng giây | hình | lời | chữ trên màn hình | SFX/nhạc**; lời đọc ~2,7 từ/giây (90 s ≈ 245 từ).
- Kèm danh sách cần kiểm chứng và câu miễn trừ.

### 5. Cá nhân hoá người dẫn (hỏi từng câu) — ✅ duyệt
Tên + chức danh, số năm và lĩnh vực kinh nghiệm (chỉ điều có thật), quan điểm/tiêu chí, mối quan hệ lợi ích (ví dụ với chủ đầu tư), kênh liên hệ, tư liệu quay. Đưa đoạn quan điểm thành "cho Linh xác nhận".

### 6. Tài nguyên (20–40 phút)
- **Ảnh vệ tinh**: `plan_map.py` (vùng phủ cho mọi vị trí camera) → `fetch_map.py --sea …`; tuyến minh hoạ bằng `grid_overlay.py`; luôn ghi "tuyến minh hoạ".
- **Ảnh báo chứng**: `capture_news.js` + crop.
- **Cảnh quay**: người dẫn/cảnh trám → tách khung (`ffmpeg … clips/a/%05d.jpg`) → `clip()`.
- **Giọng**: xem bước 7.

### 7. Giọng đọc (10–20 phút)
Tách thành 12–15 câu, mỗi câu một file; số viết bằng chữ; từ khó đọc đổi trong lời (giữ nguyên trên màn hình). Hai nguồn:
- **Giọng AI mẫu** (Speko): nhanh, dùng cho demo, gắn nhãn "BẢN DEMO · GIỌNG ĐỌC AI MẪU".
- **Giọng của người dẫn** (VoiceStudio, đã được người đó đồng ý): `scripts/voicestudio_tts.py`; nhãn "GIỌNG AI · ĐÃ ĐƯỢC … ĐỒNG Ý"; bật nhãn nội dung AI của nền tảng khi đăng.
Sau đó **luôn nhận dạng ngược** các câu có số/tên riêng, rồi `vo_prep.sh` để lấy khoảng lặng làm mốc. `make_captions.py` tạo phụ đề từ chính các file này.

### 8. Dựng (30–40 phút + render)
1. `cp -r assets/template/. <project>/`; viết `scene.js` + `timeline.js` theo chuẩn file 02 (cỡ chữ, vùng an toàn, thời gian hiển thị, motion, SFX).
2. **Căn mốc**: `tin` = lúc giọng chạm từ khoá; `drop` vào câu chốt.
3. Xem trước các mốc chính bằng contact sheet **và 1–2 khung đầy đủ độ phân giải**; sửa chồng chữ/tràn mép.
4. Render chạy nền (`make_video.sh`, ~5 s/giây video); nén bản gửi `-crf 26`.

### 9. QC, giao, đăng, đóng gói — ✅ duyệt
Xem mục E (QC), F (đăng), G (đóng gói).

## C. Điểm dừng cần người duyệt
Hook & góc nhìn (1) → kịch bản cuối (4) → thông tin cá nhân + quan điểm (5) → bản nháp video (8) → bản đăng (9).

## D. Phân công thời gian (ước tính cho video 90 s)
Ý tưởng 10′ · Phân tích mẫu 10′ · Số liệu 15′ · Kịch bản 15′ · Cá nhân hoá 10′ · Tài nguyên 30′ · Giọng 15′ · Dựng 40′ + render 7′ · QC + giao 15′ ≈ **2,5–3 giờ** cho video đầu; các video sau (có skill + dữ liệu sẵn) ~1–1,5 giờ. Nút thắt: vẽ tuyến theo đường thật, căn mốc thủ công, giọng nhân bản.

## E. Checklist QC trước khi giao
**Nội dung**
- [ ] Mọi con số khớp bài gốc; số chưa kiểm được ghi rõ trong ghi chú giao.
- [ ] Có dòng nguồn trên màn hình cho từng nhóm số liệu; có câu miễn trừ "không phải lời khuyên đầu tư".
- [ ] Không hứa lợi nhuận; điều kiện vay có "áp dụng theo chính sách từng thời điểm"; nêu quan hệ lợi ích.
- [ ] Tuyến vẽ tự do có chữ "minh hoạ".
**Hình**
- [ ] Xem khung đầu + khung cuối + 1 khung giữa mỗi cảnh ở độ phân giải đầy đủ: không chồng chữ, không tràn mép, bản đồ phủ kín khung.
- [ ] Chữ đọc được trên điện thoại (≥ 30px cho chữ nhỏ nhất, trừ miễn trừ).
- [ ] Thẻ/CTA không nằm dưới y 1670.
**Âm thanh**
- [ ] Tạo giọng không sai số/tên riêng (nhận dạng ngược); phụ đề khớp giọng.
- [ ] `ebur128`: −14 ± 1 LUFS, đỉnh ≤ −1 dBTP; không SFX đè từ khoá.
- [ ] Người duyệt tự nghe giọng/nhạc/SFX (tôi không nghe được).
**Kỹ thuật**: `ffprobe` đúng 1080×1920, 30 fps, thời lượng; file ≤ ~100 MB (nén `-crf 26`).

## F. Đăng bài
- **Ảnh bìa**: khung hook (số lớn + câu hỏi): `ffmpeg -ss 3.5 -i out.mp4 -frames:v 1 bia.jpg`.
- **Tiêu đề/caption**: 1 câu hook + 1 dòng nguồn + 3–5 hashtag (#batdongsandanang #metrodanang …); không nêu lợi nhuận chắc chắn.
- **Nhãn**: bật "nội dung do AI tạo" khi dùng giọng AI; ghi nguồn ảnh Esri; ảnh Esri/ảnh báo chỉ cho demo — bản thương mại cần nguồn có giấy phép.
- Kiểm giới hạn độ dài/dung lượng hiện hành của từng nền tảng trước khi tải.

## G. Đóng gói và tái sử dụng
Mỗi video: `lời đọc` (.txt), `scene.js`, `timeline.js`, ảnh báo chứng, ghi chú nguồn + trạng thái kiểm, file MP4 → commit vào nhánh riêng; không commit ảnh vệ tinh nặng (tái tạo bằng lệnh trong README).
Cập nhật bài học vào `bai-hoc.md` sau mỗi video.

## H. Việc còn mở (chờ bạn quyết)
1. Credential RunPod/VoiceStudio chưa áp dụng → mở phiên mới để tạo giọng Linh, dựng v2.
2. Tư liệu quay người dẫn + cảnh trám (thư mục Drive).
3. Kênh liên hệ của Linh cho khung cuối.
4. Có làm tiếp polygon khu vực + thanh km + logo cho engine không (cần nếu muốn đúng phong cách video mẫu).
