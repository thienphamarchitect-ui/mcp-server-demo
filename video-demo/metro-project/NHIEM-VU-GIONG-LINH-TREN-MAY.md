# Nhiệm vụ cho phiên Claude Code chạy trên máy DESKTOP-IFK2BLL (thư mục RegalComplex)

Dán nội dung dưới đây làm tin nhắn đầu tiên của phiên chạy trên máy đó (cần cài Claude Code, `git`, `ffmpeg`, Python 3, Node + Playwright).

---
Repo `thienphamarchitect-ui/mcp-server-demo`, nhánh `claude/metro-video-demo`. Đọc `video-demo/metro-project/README.md` và skill `.claude/skills/dung-ban-do/SKILL.md`.

Mục tiêu: dựng video v2 "Metro Đà Nẵng – Khánh Linh" bằng **giọng của Linh** (Linh đã đồng ý nhân bản giọng; ghi lại sự đồng ý trong README).

1. VoiceStudio chạy trên máy này (ứng dụng VoiceStudio.sh). Xác định cổng cục bộ (mặc định thử `http://localhost:3900`), kiểm tra `GET /health` và `GET /v1/audio/voices`, lấy ID của "Giọng Linh". Nếu máy có khoá VoiceStudio thì đọc từ biến môi trường `VOICESTUDIO_API_KEY`, không in khóa ra.
2. Tách `video-demo/metro-project/loi-doc.txt` thành từng câu, tạo giọng bằng `.claude/skills/dung-ban-do/scripts/voicestudio_tts.py` (tự nhận `localhost`, không cần khoá RunPod).
3. Nhận dạng ngược các câu có số/tên riêng, chạy `vo_prep.sh` lấy mốc, cập nhật `timeline.js` và `scene.js` theo thời lượng mới.
4. Đổi nhãn demo thành "GIỌNG AI · ĐÃ ĐƯỢC LINH ĐỒNG Ý"; bật nhãn nội dung AI của nền tảng khi đăng.
5. Render (`make_video.sh`), kiểm ebur128 (−14 ± 1 LUFS), xuất `metro-da-nang-khanh-linh-demo-v2.mp4` (nén `-crf 26`), commit + push nhánh trên.
6. Nếu B-roll nằm trong thư mục RegalComplex: liệt kê file, chọn 3–5 s, tách khung theo `.claude/skills/lam-video-bds/references/b-roll.md`, ghi `nguon-b-roll.md`.

Trong báo cáo, nêu phần nào đã kiểm bằng máy và phần nào Linh phải tự nghe. Không hứa lợi nhuận; giữ nguyên các dòng nguồn và miễn trừ.
---
