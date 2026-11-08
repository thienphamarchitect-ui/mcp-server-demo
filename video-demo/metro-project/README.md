# Dự án video Metro Đà Nẵng – Chu Lai (Khánh Linh) — dựng lại / đổi giọng

Bản v1 (giọng AI mẫu): `../metro-da-nang-khanh-linh-demo-v1.mp4`. Thư mục này giữ phần không tái tạo nhanh được.

## Dựng lại dự án (skill `dung-ban-do`, đường dẫn tính từ `.claude/skills/dung-ban-do/`)
```bash
P=/tmp/metro && mkdir -p $P/assets $P/vo
cp -r assets/template/. $P/ && cp assets/example-metro/scene.js $P/scene.js
cp ../../../video-demo/metro-project/assets/*.png $P/assets/          # ảnh báo chứng đã crop
python3 scripts/fetch_map.py $P --bbox 15.25 16.25 108.10 108.78 --sea right \
   --pins "16.0439,108.1994;15.8801,108.338;15.5736,108.474;15.4065,108.7054"   # ảnh vệ tinh Esri (~420 ô)
```
`timeline.js` của v1 (mốc theo giọng AI mẫu): `timeline.js.v1-giong-ai-mau`. Giọng mới có thời lượng khác nên phải căn lại `vo[]` trong timeline.js
và các mốc `tin/tout` trong scene.js (lấy từ khoảng lặng của `vo_prep.sh`).

## Đổi sang giọng VoiceStudio (RunPod)
Xác nhận: người dùng cho biết **Linh đã đồng ý** dùng giọng AI nhân bản của mình cho video này (ngày 8/11/2026, xác nhận trong cuộc trò chuyện). Khi đăng vẫn bật nhãn nội dung AI của nền tảng; nhãn góc phải video đổi thành "GIỌNG AI · ĐÃ ĐƯỢC LINH ĐỒNG Ý".

```bash
# Cần biến môi trường VOICESTUDIO_API_KEY (và RUNPOD_API_KEY nếu pod đang tắt). Pod tự tắt sau 5 phút rảnh.
python3 scripts/voicestudio_tts.py --base https://xb1rpph9a63wa4-3900.proxy.runpod.net --pod xb1rpph9a63wa4 \
   --lines ../../../video-demo/metro-project/loi-doc.txt --out $P/vo --voice-name "Giọng Linh"
bash scripts/vo_prep.sh $P 1.0
```
Sau đó kiểm tra số liệu/tên riêng bằng nhận dạng giọng nói, căn lại mốc, đổi nhãn góc phải (giọng AI nhân bản được Linh đồng ý), render: `bash scripts/make_video.sh $P out_v2.mp4`.
