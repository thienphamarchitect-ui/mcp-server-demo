---
name: lam-video-bds
description: Quy trình làm trọn một video ngắn dọc 9:16 dạng "MAP EXPLAINER" cho người tư vấn bất động sản — từ ý tưởng (tin hạ tầng/quy hoạch/thị trường đang nóng, câu hook), nghiên cứu số liệu có nguồn, kịch bản theo giây, cá nhân hoá người dẫn, tài nguyên (bản đồ vệ tinh, ảnh báo chứng, B-roll, giọng AI hoặc giọng nhân bản đã được đồng ý), dựng (text, motion, graphic, sound effect, phụ đề), kiểm soát chất lượng, đến đăng bài. Dùng skill này khi người dùng muốn "làm video bất động sản", "video phân tích khu vực / tuyến metro / dự án / sân bay", "kịch bản video + dựng", "video TikTok/Reels/Shorts BĐS có bản đồ", "làm tiếp video như video Metro Đà Nẵng của Khánh Linh", hoặc hỏi về quy trình, định dạng, B-roll, phiếu yêu cầu, chuẩn chữ/chuyển động/âm thanh — kể cả khi họ chỉ nói "làm cho tôi một video về [tên khu vực]". Bước dựng gọi skill dung-ban-do.
---

# Làm video BĐS — MAP EXPLAINER

MAP EXPLAINER là video dọc 60–90 s của một người tư vấn bất động sản: biến **một tin hạ tầng/quy hoạch/thị trường đang nóng** thành **quan điểm đầu tư hai chiều** ("kỳ vọng có điều kiện"), dùng **bản đồ vệ tinh làm xương sống hình ảnh**, **số liệu có nguồn** làm bằng chứng, **một khung 3 tiêu chí** làm cách nhìn riêng, rồi kết bằng **mốc theo dõi + lời mời hành động**. Một video = 1 chủ đề + 1 thông điệp + 1 khung tiêu chí + 1 CTA.

Skill này lo **quy trình và chuẩn nội dung** (từ ý tưởng tới đăng bài). Việc dựng hình/âm thanh do skill `dung-ban-do` làm (engine, render, mix); skill này nói *khi nào* và *dựng cái gì*. Đường dẫn `references/…`, `assets/…` tính từ thư mục skill này. Thuật ngữ (`tin`, `drop`, `bgs`, "tiếng"…): `references/thuat-ngu.md`.

Người dùng làm việc từng bước và duyệt giữa chừng: **giao sản phẩm theo bước**, hỏi **từng câu một** khi cần thêm thông tin, và dừng ở các điểm duyệt (✅) thay vì làm một lèo tới video.

## Bắt đầu: phiếu yêu cầu (v1 rồi v2)
Điền `assets/phieu-yeu-cau.md` — **v1 trước khi viết kịch bản nháp** (chủ đề, hook, kết luận, khu vực, số liệu, biến thể, CTA); **v2 sau khi người dẫn xác nhận** (3 tiêu chí thật, câu chuyện cá nhân, quan hệ lợi ích, kênh liên hệ, tư liệu). Thiếu trường nào thì hỏi từng câu, theo thứ tự ưu tiên: (1) việc **chặn** được dựng — kênh liên hệ, quyền dùng giọng/B-roll, tiêu chí của người dẫn; (2) việc đổi nội dung — quan hệ lợi ích, câu chuyện cá nhân; (3) việc có mặc định hợp lý — giữ mặc định và nêu rõ.

**Chỉ dùng điều người dẫn xác nhận** (số năm, kinh nghiệm, câu chuyện khách). Khi chưa có thì viết chỗ giữ chỗ và đánh dấu: số chưa kiểm `[… ✱]`, việc người dẫn phải điền `[NGƯỜI DẪN: …]`; kịch bản đang chứa chỗ giữ chỗ gắn nhãn "NHÁP – chờ người dẫn" và **không dựng thành video cuối**.

**Chạy tự động, không ai để hỏi:** giao kịch bản nháp + **danh sách câu hỏi đã sắp ưu tiên** (không tự bịa câu trả lời); giả định không giọng nhân bản, có nhãn "BẢN DEMO" nếu dùng giọng AI mẫu, có dòng "tuyến minh hoạ" và nguồn ảnh; nêu các giả định ở cuối.
**Người dẫn chưa có tiêu chí riêng:** đề xuất tiêu chí chung theo biến thể (`references/bien-the.md`) và đánh dấu "đề xuất – chờ người dẫn duyệt"; đừng đưa câu chuyện cá nhân.

## Quy trình 9 bước
| # | Bước | Làm gì | Sản phẩm | Duyệt |
|---|---|---|---|---|
| 1 | Ý tưởng | chọn tin nóng (kiểm trạng thái hiện tại của đối tượng), góc nhìn, hook đối lập hoặc "trả lời trước", biến thể A–E | phiếu v1: hook + kết luận | ✅ |
| 2 | Phân tích mẫu | nếu có video mẫu: trích khung, đo tiết tấu (`dung-ban-do`: `references/phan-tich-video-mau.md`) | bảng giai đoạn | |
| 3 | Số liệu | tìm tin, **mở bài gốc**, ghi số + ngày + nguồn, cắt ảnh báo chứng | bảng số liệu ✔/✱ | |
| 4 | Kịch bản nháp | bảng 6 cột (dưới), cấu trúc + số liệu, chỗ người dẫn để giữ chỗ; danh sách cần kiểm chứng | kịch bản nháp | ✅ cấu trúc + số liệu |
| 5 | Cá nhân hoá | hỏi từng câu: tên/chức danh, kinh nghiệm thật, quan điểm, quan hệ lợi ích, kênh liên hệ | phiếu v2 | ✅ |
| — | Kịch bản cuối | điền phần người dẫn, đếm lại số tiếng/độ dài | kịch bản cuối | ✅ |
| 6 | Tài nguyên | ảnh vệ tinh + tuyến minh hoạ, ảnh báo, B-roll, giọng | assets, `s*.wav` | |
| 7 | Giọng đọc | tách câu, số bằng chữ, TTS, **nhận dạng ngược** số/tên riêng, lấy mốc khoảng lặng | wav + mốc | |
| 8 | Dựng | `scene.js` + `timeline.js` theo chuẩn, xem trước, render | MP4 | ✅ |
| 9 | QC, giao, đăng | checklist, ảnh bìa, caption, nhãn AI, commit | MP4 + ghi chú | ✅ |

**Bảng kịch bản — 6 cột:** `Giây | Khối | Hình | Lời đọc (+số tiếng) | Chữ trên màn hình | SFX/nhạc`. Cột "SFX/nhạc" ghi mốc `drop`, ting/pop theo thẻ; nếu chưa dựng thì ghi "theo chuẩn". Mẫu: `assets/kich-ban-mau-metro-linh.md` (biến thể A, 90 s), `assets/kich-ban-mau-b-san-bay-60s.md` (biến thể B, 60 s).

## Các chuẩn cần đọc đúng lúc
- **Bước 1, 4** → `references/dang-video-map-explainer.md` (6 khối, bảng thời gian 60/90 s, thành phần bắt buộc, khi nào không dùng) và `references/bien-the.md` (5 biến thể, chi tiết biến thể B).
- **Bước 3, 9** → `references/tuan-thu-noi-dung.md`: cái được/không được nói, miễn trừ, quan hệ lợi ích, nhãn AI, quyền hình ảnh/flycam.
- **Bước 6** → `references/b-roll.md` và `assets/nguon-b-roll.md` (mẫu bảng nguồn). Quy tắc tiếng: người dẫn xuất hiện trên hình và nói thì dùng giọng thật của họ (giọng AI không khớp khẩu hình); giọng AI chỉ cho voice-over.
- **Bước 8** → `references/chuan-text-motion-graphic-sfx.md`: cỡ chữ, bản đồ vùng y, thời gian hiển thị, motion, đồ hoạ, SFX và mix — bảng thông số thật của engine, dùng thay vì đoán.
- **Bước 9** → `assets/checklist-qc-dang.md`.

## Nguyên tắc (và lý do)
- **Trung thực trước.** Người xem bỏ tiền thật; một con số hay chính sách sai làm hỏng uy tín người đăng. Số chưa mở bài gốc ghi "chưa kiểm". Điều kiện tài chính chỉ nêu đúng tài liệu gốc kèm "áp dụng theo chính sách từng thời điểm"; nêu quan hệ lợi ích; không hứa lợi nhuận.
- **Quan điểm hai chiều.** Có cả lý do kỳ vọng lẫn lý do chờ; nói thẳng cái chưa chắc.
- **Một khối một con số chính.** Số phụ thành chữ nhỏ; tiết tấu theo thông tin chứ không theo quãng đường.
- **Giọng nhân bản chỉ khi người đó đồng ý** (ghi sự xác nhận trong README dự án), gắn nhãn AI trên video và bật nhãn nội dung AI của nền tảng.
- **Tuyến/ranh giới/vòng km tự vẽ ghi "minh hoạ".** Ảnh Esri và ảnh báo chỉ cho demo; bản thương mại cần nguồn có giấy phép.
- **Người rõ mặt trong B-roll cần đồng ý;** bỏ nhạc/logo bên thứ ba.
- **Không nghe được âm thanh** — nói rõ phần nào đã kiểm bằng nhận dạng giọng/đo loudness, phần nào người dùng phải tự nghe.

## Giao việc và báo cáo
Cuối mỗi bước: sản phẩm, phần đã kiểm, phần chưa kiểm (số liệu chưa đối chiếu, toạ độ ước lượng, nhạc/SFX chưa nghe), việc cần người dùng quyết. Gửi file nhẹ (MP4 nén `-crf 26`). Lưu vào nhánh riêng, không commit ảnh vệ tinh nặng (ghi lệnh tái tạo trong README dự án).

## Tài nguyên
- `references/` — `quy-trinh-chi-tiet.md`, `dang-video-map-explainer.md`, `bien-the.md`, `tuan-thu-noi-dung.md`, `b-roll.md`, `chuan-text-motion-graphic-sfx.md`, `thuat-ngu.md`
- `assets/` — `phieu-yeu-cau.md`, `kich-ban-mau-metro-linh.md`, `kich-ban-mau-b-san-bay-60s.md`, `nguon-b-roll.md`, `checklist-qc-dang.md`
- Skill liên quan: **`dung-ban-do`** (engine, render, mix, scripts).
