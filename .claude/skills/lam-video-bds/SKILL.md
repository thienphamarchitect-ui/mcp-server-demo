---
name: lam-video-bds
description: Quy trình làm trọn một video ngắn dọc 9:16 dạng "MAP EXPLAINER" cho người tư vấn bất động sản — từ ý tưởng (tin hạ tầng/quy hoạch/thị trường đang nóng, câu hook), nghiên cứu số liệu có nguồn, kịch bản theo giây, cá nhân hoá người dẫn, tài nguyên (bản đồ vệ tinh, ảnh báo chứng, B-roll, giọng AI hoặc giọng nhân bản đã được đồng ý), dựng (text, motion, graphic, sound effect, phụ đề), kiểm soát chất lượng, đến đăng bài. Dùng skill này khi người dùng muốn "làm video bất động sản", "video phân tích khu vực / tuyến metro / dự án / sân bay", "kịch bản video + dựng", "video TikTok/Reels/Shorts BĐS có bản đồ", "làm tiếp video như video Metro Đà Nẵng của Khánh Linh", hoặc hỏi về quy trình, định dạng, B-roll, phiếu yêu cầu, chuẩn chữ/chuyển động/âm thanh — kể cả khi họ chỉ nói "làm cho tôi một video về [tên khu vực]". Bước dựng gọi skill dung-ban-do.
---

# Làm video BĐS — MAP EXPLAINER

MAP EXPLAINER là video dọc 60–90 s của một người tư vấn bất động sản: biến **một tin hạ tầng/quy hoạch/thị trường đang nóng** thành **quan điểm đầu tư hai chiều** ("kỳ vọng có điều kiện"), dùng **bản đồ vệ tinh làm xương sống hình ảnh**, **số liệu có nguồn** làm bằng chứng, **một khung 3 tiêu chí** làm cách nhìn riêng, rồi kết bằng **mốc theo dõi + lời mời hành động**. Một video = 1 chủ đề + 1 thông điệp + 1 khung tiêu chí + 1 CTA.

Skill này lo **quy trình và chuẩn nội dung** (từ ý tưởng tới đăng bài). Việc dựng hình/âm thanh do skill `dung-ban-do` làm (engine bản đồ, render, mix); skill này chỉ nói *khi nào* và *dựng cái gì*. Đường dẫn `references/…`, `assets/…` tính từ thư mục của skill này.

Người dùng làm việc từng bước và duyệt giữa chừng: **giao sản phẩm theo bước** (kịch bản → bản nháp → bản cuối), hỏi **từng câu một** khi cần thêm thông tin, và dừng ở các điểm duyệt bên dưới thay vì làm một lèo tới video.

## Bắt đầu: phiếu yêu cầu
Điền `assets/phieu-yeu-cau.md` (10 trường: chủ đề, câu hook, kết luận, khu vực/tuyến, số liệu, 3 tiêu chí, 3 mốc theo dõi, người dẫn, CTA, tư liệu). Trường nào thiếu thì hỏi từng câu; riêng *thông tin cá nhân và quan điểm của người dẫn* chỉ dùng điều người đó xác nhận, không tự bịa số năm kinh nghiệm hay câu chuyện khách hàng. Khi chạy tự động và không có ai để hỏi: giả định không giọng nhân bản, có nhãn "BẢN DEMO" nếu dùng giọng AI mẫu, có dòng "tuyến minh hoạ" và ghi nguồn ảnh, rồi nói rõ các giả định ở cuối.

## Quy trình 9 bước
| # | Bước | Làm gì | Sản phẩm | Duyệt |
|---|---|---|---|---|
| 1 | Ý tưởng | chọn tin nóng, góc nhìn riêng của người dẫn, hook đối lập hoặc "trả lời trước" | hook + kết luận một dòng | ✅ |
| 2 | Phân tích mẫu | nếu có video mẫu: trích khung, đo tiết tấu, lớp hình, mã màu (skill `dung-ban-do`: `references/phan-tich-video-mau.md` của skill đó) | bảng giai đoạn/tốc độ | |
| 3 | Số liệu | tìm tin, **mở bài gốc**, ghi số + ngày + nguồn, cắt ảnh báo chứng | bảng số liệu ✔/✱ | |
| 4 | Kịch bản | bảng giây \| hình \| lời \| chữ \| SFX, ~245 từ cho 90 s, kèm danh sách cần kiểm chứng | kịch bản cuối | ✅ |
| 5 | Cá nhân hoá | tên/chức danh, kinh nghiệm thật, quan điểm, quan hệ lợi ích, kênh liên hệ | kịch bản có người dẫn | ✅ |
| 6 | Tài nguyên | ảnh vệ tinh + tuyến minh hoạ, ảnh báo, B-roll, giọng | assets, `s*.wav` | |
| 7 | Giọng đọc | tách câu, số bằng chữ, TTS, **nhận dạng ngược** số/tên riêng, lấy mốc khoảng lặng | wav + mốc | |
| 8 | Dựng | `scene.js` + `timeline.js` theo chuẩn text/motion/graphic/SFX, xem trước, render | MP4 | ✅ |
| 9 | QC, giao, đăng | checklist, ảnh bìa, caption, nhãn AI, commit | MP4 + ghi chú | ✅ |

Chi tiết từng bước, thời gian ước tính và nút thắt: `references/quy-trinh-chi-tiet.md`.

## Các chuẩn cần đọc đúng lúc
- **Bước 1, 4** → `references/dang-video-map-explainer.md`: cấu trúc 6 khối (hook → bối cảnh bản đồ → bằng chứng → 3 tiêu chí → mốc theo dõi → CTA), thành phần bắt buộc, 5 biến thể, khi nào không dùng. Mẫu kịch bản đã duyệt: `assets/kich-ban-mau-metro-linh.md`.
- **Bước 6** → `references/b-roll.md`: loại B-roll, bố cục toàn khung/PiP, quy tắc dựng, tách khung, giới hạn kỹ thuật, bản quyền. *Quy tắc về tiếng*: người dẫn xuất hiện trên hình và nói thì phải dùng giọng thật của họ (giọng AI không khớp khẩu hình); giọng AI chỉ dùng cho voice-over.
- **Bước 8** → `references/chuan-text-motion-graphic-sfx.md`: cỡ chữ, vùng an toàn, thời gian hiển thị, từng hoạt ảnh (thời lượng, easing), camera, đồ hoạ, bộ SFX và mix. Đây là bảng thông số thật của engine, dùng nó thay vì đoán.
- **Bước 9** → `assets/checklist-qc-dang.md`.

## Nguyên tắc (và lý do)
- **Trung thực trước.** Người xem bỏ tiền thật; một con số hay chính sách sai làm hỏng uy tín người đăng. Số chỉ lấy từ tóm tắt tìm kiếm mà chưa mở bài gốc phải ghi "chưa kiểm". Điều kiện tài chính chỉ nêu đúng tài liệu gốc kèm "áp dụng theo chính sách từng thời điểm"; nêu quan hệ lợi ích; không hứa lợi nhuận.
- **Quan điểm hai chiều.** Luôn có cả lý do kỳ vọng lẫn lý do chờ; nói thẳng cái chưa chắc ("mới ở bước đề xuất").
- **Một ý một con số.** Số phụ thành chữ trên màn hình, không bắt người đọc đọc nhiều số; tiết tấu theo thông tin chứ không theo quãng đường.
- **Giọng nhân bản chỉ khi người đó đồng ý** (ghi lại sự xác nhận trong README dự án), gắn nhãn AI trên video và bật nhãn nội dung AI của nền tảng. Không tự tạo giọng của người thật khi chưa rõ sự đồng ý.
- **Tuyến/ranh giới tự vẽ phải ghi "minh hoạ".** Ảnh vệ tinh Esri và ảnh báo chỉ dùng cho demo; bản thương mại cần nguồn có giấy phép.
- **Người xuất hiện rõ mặt trong B-roll cần đồng ý;** bỏ nhạc/logo bên thứ ba trong clip.
- **Không nghe được âm thanh** — nói rõ phần nào đã kiểm bằng nhận dạng giọng/đo loudness và phần nào người dùng phải tự nghe.

## Giao việc và báo cáo
Cuối mỗi bước: nêu sản phẩm, phần đã kiểm, phần chưa kiểm (số liệu chưa đối chiếu, toạ độ ước lượng, nhạc/SFX chưa nghe), việc cần người dùng quyết. Gửi file nhẹ (MP4 nén `-crf 26`). Lưu bản làm việc vào nhánh riêng của repo, không commit ảnh vệ tinh nặng (ghi lệnh tái tạo trong README dự án).

## Tài nguyên
- `references/` — `quy-trinh-chi-tiet.md`, `dang-video-map-explainer.md`, `b-roll.md`, `chuan-text-motion-graphic-sfx.md`
- `assets/` — `phieu-yeu-cau.md`, `kich-ban-mau-metro-linh.md`, `checklist-qc-dang.md`
- Skill liên quan: **`dung-ban-do`** (engine bản đồ, render, mix; có `scene.js` mẫu, `plan_map.py`, `make_captions.py`, `voicestudio_tts.py`…).
