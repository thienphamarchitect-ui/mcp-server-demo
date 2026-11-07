---
name: dung-ban-do
description: Dựng đoạn video bản đồ vệ tinh dọc 9:16 kiểu Google Earth — tuyến metro/đường sắt/cao tốc/vành đai phát sáng, tàu chạy dọc tuyến, camera bay (toàn cảnh → bám tàu → zoom sâu → zoom ra), ghim và nhãn, vòng xung radar, thẻ số liệu cyan, thẻ báo chứng, thanh tiến độ km, giọng đọc AI và nhạc/SFX, xuất MP4. Dùng skill này bất cứ khi nào người dùng nói "dựng bản đồ", "làm video bản đồ", "bản đồ bay zoom", "mô phỏng hướng tuyến", "tuyến metro/đường mới chạy qua đâu", "quy hoạch trên bản đồ vệ tinh", muốn phân tích/bắt chước một video bản đồ mẫu, hoặc cần cảnh bản đồ (Đà Nẵng, TP.HCM, Hà Nội...) cho video bất động sản/hạ tầng/du lịch, kể cả khi họ chỉ nói "làm video có bản đồ" mà không nhắc tên skill.
---

# Dựng bản đồ

Skill này đóng gói cách làm video "Metro Đà Nẵng – Chu Lai – Khánh Linh" (83,8s, 1080x1920): ảnh vệ tinh thật + một **engine HTML/SVG xác định theo thời gian** (chụp từng khung bằng Playwright) + giọng đọc AI + nhạc/SFX. Engine tách khỏi nội dung: mỗi video chỉ viết `scene.js` và `timeline.js`.

Người dùng hay đi từng bước và duyệt giữa chừng, nên **giao sản phẩm theo bước** (kịch bản → preview bản đồ → video) thay vì làm một lèo tới MP4.

## Quy trình

**1. Hiểu mục tiêu.** Hỏi/tìm: tuyến hoặc khu vực nào, có video mẫu không, giọng ai (xem mục Giọng), số liệu nào lên màn hình, nền tảng đăng. Có video mẫu → đọc `references/phan-tich-video-mau.md` mục 4–6: trích khung, đo tiết tấu, ghi lại cấu trúc/mã màu/HUD, rồi đối chiếu bảng **khoảng cách với engine** (video mẫu có camera 3D nghiêng, polygon khu vực, thanh km, logo — engine hiện chưa có; nói thẳng với người dùng và đề xuất cách bù).

**2. Số liệu và kịch bản.** Đối chiếu từng con số với bài gốc (WebFetch/`scripts/capture_news.js`), ghi nguồn + ngày. Viết kịch bản theo mạch: *trả lời trước → tuyến/khu vực → cái đang chạy thật (số liệu) → các tiêu chí → mốc theo dõi + kêu gọi*. Mỗi ý một con số; dữ liệu phụ để thành chữ trên màn hình, không bắt người đọc đọc nhiều số. Lời đọc ~2,7 từ/giây.

**3. Vùng ảnh nền.**
```bash
python3 scripts/plan_map.py --route "lat,lon;lat,lon;..." [--follow-scale 1.15] [--extra "điểm zoom sâu" --extra-scale 2.0] [--ring "lat,lon,km"]
python3 scripts/fetch_map.py <project> --bbox ... --pins "lat,lon;..." --sea right      # lệnh này do plan_map in sẵn
```
`plan_map.py` in `ov.scale`, `ov.center`, bbox đã cộng lề cho mọi vị trí camera (toàn cảnh, bám tàu, zoom sâu). Cảnh không có tàu: `--follow-scale 0`. `--sea` là cạnh ảnh mà biển chạm vào (right/bottom/left/top/none). Xem thumbnail ảnh nền, kiểm mép biển (nước đục phù sa vẫn còn mảng ghép ô).

**2b. Tuyến.** Không có dữ liệu tuyến chính thức thì vẽ tuyến **minh hoạ** qua các ghim (bám địa hình hợp lý, đặt thumbnail để kiểm tra không đi vào biển), và ghi "Tuyến minh hoạ, chưa phải phương án được phê duyệt" trên màn hình.

**4. Giọng đọc.** Đọc `references/bai-hoc.md` mục Giọng. Mỗi câu một file, số bằng chữ → `audio_synthesize` → `scripts/tts_decode.py` → **`audio_transcribe` kiểm tra** → `bash scripts/vo_prep.sh <project> 1.0` (in khoảng lặng để căn mốc).

**5. Dựng.**
1. `cp -r assets/template/. <project>/`; thêm `assets/` do fetch_map tạo; ảnh báo chứng (`capture_news.js`, rồi crop bằng PIL cho gọn).
2. Viết `scene.js` (SCENE + các dòng `line()/paper()/chip()...`) và `timeline.js` (mốc giọng đọc từ vo_prep, `bgs`, `drop`). Bắt đầu từ `assets/example-metro/` (tuyến + tàu + giọng đọc, 8 cảnh) hoặc `assets/example-ring/` (chỉ ghim + vòng bán kính km, không giọng đọc: `vo: []` cho ra MP4 chỉ nhạc + SFX). Tài liệu từng tuỳ chọn: `references/engine.md`.
3. `node scripts/render.js <project> preview t1 t2 ...` → ghép contact sheet, **xem cả khung đầy đủ** → sửa chồng chữ/tràn mép → lặp.
4. `bash scripts/make_video.sh <project> out.mp4` (chạy nền, ~6 phút cho 84s). Nén bản gửi: `ffmpeg ... -crf 26`.

**6. Kiểm và giao.** `ffprobe` + loudness (`ebur128`) + trích ~12 khung từ MP4 để xem lại. Gửi file (SendUserFile) kèm: phần đã kiểm (khung hình, STT), phần người dùng phải tự nghe (nhạc/SFX), số liệu chưa đối chiếu bài gốc, điều khoản ảnh vệ tinh/báo.

## Nguyên tắc (và lý do)
- **Trung thực trước đã.** Một con số hoặc một chính sách vay sai làm hỏng uy tín người đăng; nêu đúng điều tài liệu gốc ghi, thêm "áp dụng theo chính sách từng thời điểm", nêu quan hệ lợi ích, không hứa lợi nhuận.
- **Giọng AI là demo.** Không nhân bản giọng người thật nếu chưa có đồng ý của họ; gắn nhãn "BẢN DEMO · GIỌNG ĐỌC AI MẪU"; bản đăng để người thật thu.
- **Ảnh vệ tinh Esri và ảnh báo chỉ cho demo.** Bản thương mại cần nguồn có giấy phép hoặc flycam.
- **Tiết tấu theo thông tin, không theo quãng đường**: chậm ở chỗ có số liệu, lướt ở chỗ trống (học từ video mẫu).
- **Không có người dẫn/cảnh trám thì nói rõ** — video chỉ có bản đồ, chữ và thẻ số liệu.

## Tài nguyên
- `assets/template/` — `render.html`, `engine.js` (dùng chung), `scene.js` (khung trống), `timeline.js`, `fonts/`
- `assets/example-metro/` — `scene.js` + `timeline.js` + `news.json` của video Metro Đà Nẵng – Chu Lai (8 cảnh, 83,8s, có giọng đọc)
- `assets/example-ring/` — cảnh không tuyến/không giọng: vòng bán kính cố định, ghim lệch nhãn, ghim nhỏ, số thập phân
- `scripts/` — `plan_map.py` (bbox + ov), `fetch_map.py` + `seafix.py --sea` (ảnh nền), `capture_news.js`, `tts_decode.py`, `vo_prep.sh`, `render.js`, `audio.py`, `make_video.sh`
- `references/` — `phan-tich-video-mau.md` (cách làm video mẫu + cách phân tích video mới), `engine.md` (API đầy đủ), `bai-hoc.md` (lỗi đã gặp)
- Cần: Node + Playwright/Chromium, ffmpeg, Python3 + numpy/Pillow/scipy (`pip install scipy`).
