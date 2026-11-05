---
name: bds-video-demo
description: "Làm video ngắn phân tích bất động sản Việt Nam từ A đến Z: nghiên cứu số liệu thật từ báo uy tín (DKRA, CBRE, Tuổi Trẻ, CafeF, VnExpress, bảng giá đất), viết kịch bản (tổng, video ngắn 60–75s, kịch bản sản xuất đầy đủ), cắt ảnh tiêu đề/đoạn số liệu bài báo làm 'báo chứng', tạo giọng đọc AI tiếng Việt, dựng video demo dọc 9:16 có motion graphic, thẻ số liệu cyan, bản đồ vệ tinh thật bay zoom in/zoom out vào từng khu vực, sound effect và nhạc nền, xuất MP4. Dùng skill này bất cứ khi nào người dùng muốn kịch bản hoặc video về 'khu vực nào tăng giá', thị trường nhà đất một tỉnh/thành, giới thiệu chủ đầu tư hay dự án (Regal, Vinhomes, Sun Group...), cần 'dẫn chứng số liệu', 'cắt hình bài báo', 'video demo có voice', 'bản đồ thật', 'zoom vào vị trí' — kể cả khi họ chỉ nói 'làm video TikTok/Reels về BĐS Đà Nẵng' mà không nhắc tới skill."
---

# Video phân tích BĐS: nghiên cứu → kịch bản → video demo

Quy trình này đã chạy trọn vẹn cho video "Đà Nẵng: 4 vùng tăng giá + Regal Group" (55s, 1080x1920). Template và script đi kèm là bản tổng quát hoá của video đó; phần nội dung cụ thể (thành phố, khu vực, dự án) thay theo yêu cầu mới.

Người dùng thường đi theo từng bước và duyệt kết quả giữa chừng, nên **giao sản phẩm từng bước** (kịch bản → ảnh báo → video), gửi file sớm và hỏi phản hồi, đừng làm một lèo tới MP4 rồi mới cho xem.

## Bước 1 — Nghiên cứu số liệu
Đọc `references/research-and-script.md` mục 1–2. Tóm tắt:
- Tìm song song nhiều truy vấn (WebSearch extended cho tin mới), mở từng bài bằng WebFetch để lấy **nguyên văn số liệu + ngày đăng**.
- Ưu tiên báo cáo thị trường (DKRA/CBRE/Savills), văn bản nhà nước (bảng giá đất, quyết định quy hoạch), báo chính thống. Bài "nội dung được tài trợ" không dùng làm bằng chứng.
- **Trung thực trước đã**: thị trường giảm thì nói giảm và biến thành luận điểm; bảng giá đất ≠ giá giao dịch; không nói "chứng nhận xanh" nếu không tìm thấy; số lệch giữa nguồn thì dùng số an toàn. Lý do: khán giả là người bỏ tiền thật, một con số sai phá uy tín kênh.

## Bước 2 — Kịch bản
Ba cấp, chi tiết trong `references/research-and-script.md` mục 4–5: (1) kịch bản tổng 2–4 phút, (2) video ngắn 60–75s theo giây với 3 hook A/B, (3) kịch bản sản xuất đầy đủ có shot list + lời đọc teleprompter + bản cắt 60s + checklist pháp lý. Lưu `.md` trong repo/thư mục làm việc và gửi file.

## Bước 3 — Ảnh báo
```bash
node scripts/capture_news.js news.json <project>/assets      # mẫu: assets/template/news.example.json
```
Ghép thumbnail và **tự xem lại** (h1 là logo, quảng cáo đè, đoạn tô vàng dính ảnh → crop lại bằng PIL).

## Bước 4 — Giọng đọc
Đọc `references/voice-tts.md`. Mỗi câu một file, số viết bằng chữ, tên tiếng Anh khó đọc thì Việt hoá trong lời. Speko/Cartesia "Minh" nếu có; **luôn transcribe lại** đoạn có số/tên riêng để bắt lỗi. Rồi:
```bash
bash scripts/vo_prep.sh <project> 1.06     # tăng tốc + in khoảng lặng để căn mốc
```

## Bước 5 — Dựng
1. `cp -r assets/template/. <project>/` (render.html, timeline.js, fonts/).
2. Bản đồ thật (nếu có cảnh khu vực):
   `python3 scripts/fetch_map.py <project> --bbox LAT0 LAT1 LON0 LON1 --pins "lat,lon;..."`
   Không có bản đồ → tạo `assets/map_config.js` tối thiểu (xem `references/render-template.md` mục 1).
3. Sửa `timeline.js` (vo, bgs, total, drop, music) và các khối `// SCENE` trong `render.html` theo kịch bản; mốc `tin` lấy từ khoảng lặng của vo_prep. Hàm, hệ thiết kế, camera bản đồ: `references/render-template.md`.
4. Xem thử → sửa → render:
   ```bash
   node scripts/render.js <project> preview 3.6 12.4 29.9
   bash scripts/make_video.sh <project> out_v1.mp4
   ```
   Trích vài khung từ MP4 và tự xem trước khi gửi. Sửa một đoạn: `make_video.sh <project> out_v2.mp4 <fromFrame> <toFrame>`.

## Môi trường & phụ thuộc
- Node + Playwright/Chromium (`require('playwright')`), ffmpeg, Python 3 với numpy, Pillow, scipy.
- Sau proxy có CA riêng: Python dùng `SSL_CERT_FILE`; fetch_map.py tự nhận `/root/.ccr/ca-bundle.crt` nếu có. edge-tts không chạy sau proxy (WebSocket).
- Font Source Sans 3 có sẵn trong `assets/template/fonts/` (OFL).

## Khi giao kết quả
- Gửi file (SendUserFile/present) ở mỗi bước; commit/push nếu đang trong repo.
- Nói rõ: phần nào đã kiểm (khung hình đã xem, lời đọc đã transcribe), phần nào người dùng cần tự nghe (nhạc/SFX); chi phí TTS nếu dùng dịch vụ trả phí; ảnh trong bài báo và ảnh vệ tinh chỉ dùng cho demo, bản đăng công khai cần B-roll/bản đồ có giấy phép; video chưa có người dẫn nếu chưa nhận footage.
- Phản hồi hay gặp: "đổi thành bản đồ thật" (dùng fetch_map.py), "thêm zoom in/out" (camera CAM kiểu bay: toàn cảnh → zoom sâu → đẩy chậm → zoom ra), chữ tràn, nhãn chồng nhau.

## Tài nguyên
- `scripts/capture_news.js` cắt tiêu đề/đoạn số liệu/ảnh bài báo
- `scripts/fetch_map.py` + `scripts/seafix.py` ảnh vệ tinh nền + chi tiết + làm sạch biển → `map_config.js`
- `scripts/vo_prep.sh` chuẩn hoá giọng, in khoảng lặng
- `scripts/render.js` chụp khung hình; `scripts/audio.py` nhạc + SFX + mix; `scripts/make_video.sh` toàn bộ
- `assets/template/` render.html (9 cảnh mẫu Đà Nẵng), timeline.js, news.example.json, fonts
- `references/research-and-script.md`, `references/voice-tts.md`, `references/render-template.md`
