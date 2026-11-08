# Thuật ngữ và vị trí file (dành cho bước dựng)

Skill này chỉ nói *dựng cái gì*; cách dựng nằm ở skill **`dung-ban-do`** (đường dẫn dưới đây tính từ thư mục skill đó).

| Thuật ngữ | Nghĩa |
|---|---|
| `scene.js` | file nội dung riêng của video: cấu hình bản đồ `SCENE` (ghim, tuyến, vòng, polygon, camera…) + các dòng chữ/thẻ theo từng cảnh |
| `timeline.js` | tổng thời lượng, giọng đọc (`vo`), nền (`bgs`: MAP/DARK theo khoảng thời gian), nhạc, `drop` |
| `tin` / `tout` | giây phần tử bắt đầu / kết thúc hiển thị; `tin` = lúc giọng chạm từ khoá (từ khoảng lặng của `vo_prep.sh`) |
| `vo` | danh sách file giọng `["f3.wav", tBắtĐầu, cắtTừ, cắtĐến]` (f*.wav do `vo_prep.sh` tạo từ s*.wav) |
| `bgs` | các đoạn nền: `MAP` (bản đồ) hoặc `DARK` (nền tối + lưới + hạt), chồng nhau 0,3 s để crossfade |
| `drop` | giây nhạc vào full beat + impact + flash; đặt vào câu/thẻ chốt |
| `line()` `paper()` `chip()` `src()` `note()` `raw()` | chữ, thẻ báo, viên thuốc, dòng nguồn, ghi chú, HTML tuỳ ý |
| `count` | tuỳ chọn của `line()` để đếm số (`count:[0,19.7,' KM',false,1]`); không dùng cho năm |
| `clip()` / `captions()` | ghép cảnh quay bằng chuỗi ảnh / phụ đề đốt cứng |
| `zones` `kmbar` `logo` `rings` `pins` | polygon khu vực, thanh km, logo, vòng xung/bán kính, ghim |
| ✔ / ✱ | số đã đối chiếu bài gốc / chỉ từ tóm tắt tìm kiếm (chưa kiểm) |
| "tiếng" | âm tiết tách bằng dấu cách (đơn vị đếm lời đọc) |

## Vị trí trong skill `dung-ban-do`
- Engine và khung: `assets/template/` (`render.html`, `engine.js`, `scene.js`, `timeline.js`, `fonts/`).
- Ví dụ: `assets/example-metro/` (tuyến + tàu + giọng, `loi-doc.txt`, `news.json`), `assets/example-ring/` (ghim + vòng km, không giọng), `assets/example-hud/` (polygon + thanh km + logo).
- Script: `plan_map.py`, `fetch_map.py`, `grid_overlay.py`, `capture_news.js`, `tts_decode.py`, `voicestudio_tts.py`, `vo_prep.sh`, `make_captions.py`, `render.js`, `make_video.sh`.
- Tài liệu: `references/engine.md` (API), `bai-hoc.md` (lỗi đã gặp), `phan-tich-video-mau.md` (phân tích video mẫu).
- Mẫu hồ sơ trong skill này: `assets/phieu-yeu-cau.md`, `assets/nguon-b-roll.md`, `assets/checklist-qc-dang.md`; file lời đọc `loi-doc.txt` = mỗi dòng một đoạn giọng, số viết bằng chữ, dòng bắt đầu bằng `#` là chú thích.
