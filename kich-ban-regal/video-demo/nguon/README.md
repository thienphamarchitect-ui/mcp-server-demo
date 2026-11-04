# Nguồn dựng video demo

- `render.html` + `timeline.js`: đồ họa chuyển động (mỗi khung hình = `render(t)`), toàn bộ chữ, thẻ số liệu, ảnh báo, bản đồ, SFX cue.
- `render.js`: chụp từng khung hình bằng Playwright → `frames/`.
  - Xem thử: `node render.js preview 3.5 14.9`
  - Render đủ: `node render.js full`
- `audio.py`: ghép giọng đọc (`vo/f*.wav`), nhạc nền 100 BPM tổng hợp, SFX tổng hợp, ducking, loudnorm −14 LUFS → `mix.wav`.
- Ghép: `ffmpeg -framerate 30 -i frames/f%05d.jpg -i mix.wav -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest out.mp4`
- `prep.js`: cắt tiêu đề, đoạn số liệu và ảnh từ các bài báo → `assets/`.

Giọng đọc: AI (Cartesia "Minh", tiếng Việt) qua Speko, tăng tốc 1.06x. `vo/s*.wav` là bản gốc, `vo/f*.wav` là bản đã tăng tốc.
