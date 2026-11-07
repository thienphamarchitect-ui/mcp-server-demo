/* timeline.js — thời gian tổng, nhạc, giọng đọc, nền. Sửa theo từng video.
 *  total: độ dài video (s).   drop: lúc nhạc vào full beat + impact (đặt vào câu chốt/ tiêu đề chính).
 *  music: start (vào nhạc), beatsFrom (bắt đầu kick nhẹ), breakdown [a,b] (nhạc mỏng dần a→b, im b→drop), outro (sau mốc này chỉ còn pad)
 *  vo: ["f1.wav", tBắtĐầu, cắtTừ, cắtĐến|null] — f*.wav do vo_prep.sh tạo từ vo/s*.wav
 *  bgs: ["MAP"|"DARK", vào, ra, 0] — các đoạn chồng ~0,35s để crossfade. MAP = cảnh bản đồ (engine.js), DARK = nền tối + lưới + hạt. */
window.TL = {
  "fps": 30, "total": 20.0, "drop": 8.0,
  "music": {"start": 0.3, "beatsFrom": 3.0, "breakdown": [6.0, 7.85], "outro": 17.0},
  "vo": [["f1.wav", 0.40, 0, null]],
  "bgs": [["MAP", 0, 10.2, 0], ["DARK", 9.8, 20.0, 0]]
}
