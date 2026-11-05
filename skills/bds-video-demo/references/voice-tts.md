# Giọng đọc AI tiếng Việt

## Lựa chọn (theo thứ tự ưu tiên)

1. **Speko MCP** (nếu tài khoản có kết nối Speko) — chất lượng tốt nhất, có kiểm tra bằng nhận dạng giọng.
   - Giọng đã dùng và đạt: **Cartesia "Minh – Conversational Partner"**, `voice: "0e58d60a-2f1a-4252-81bd-3db6af45fb41"`, `model: "sonic-3.5"`, nam, tiếng Việt bản ngữ, lặp lại ổn định giữa các lần gọi.
   - Lựa chọn khác: ElevenLabs "Chinh – Northern Male" (`a1l7pVQbs9gSUbJwzceV`, `eleven_v3_conversational`). Tìm thêm: `voices_search(language="vi", gender="male")`. Không đoán voice id từ trí nhớ — lấy từ kết quả tìm.
   - Gọi:
     ```json
     {"text": "...", "intent": {"language": "vi"}, "voice": "<id>", "model": "sonic-3.5",
      "constraints": {"allowedProviders": {"tts": ["cartesia"]}}}
     ```
   - Kết quả quá lớn nên được lưu vào file JSON trong `tool-results/`. Giải mã:
     `jq -r .audio_base64 <file> | base64 -d > <project>/vo/sN.wav` và lấy `jq -r .url <file>` (link ký 15 phút).
   - **Kiểm tra bắt buộc**: `audio_transcribe(audio_url=<url>, language="vi")` cho các đoạn có số tiền, tên riêng, tên dự án. So sánh với kịch bản; sai thì sửa text và tạo lại.
   - Chi phí: báo người dùng (vài cent cho một video 60s). Kiểm tra số dư `credits_balance_get` nếu cần.
2. **gTTS** (`pip install gtts`, cần `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt` sau proxy) — giọng nữ Google Translate, miễn phí, chất lượng demo.
3. **edge-tts không chạy được sau proxy agent** (dùng WebSocket) — đừng mất thời gian.

## Viết lời cho TTS

- **Mỗi câu/cụm ý là một file** (s1, s2, …) để căn thời gian chính xác và sửa từng đoạn.
- **Viết số bằng chữ**: "bảy mươi phần trăm", "ba nghìn năm trăm hai mươi lăm tỷ đồng", "quý ba năm nay". Đọc lại từng số so với nguồn.
- Tên tiếng Anh khó đọc → đổi sang tiếng Việt trong lời ("đá cẩm thạch", "kính hộp cách nhiệt", "đèn chiếu sáng từ Đức") nhưng giữ tên gốc trên màn hình (MARBLE, LOW-E, OCCHIO). Tên dự án như "Regal Complex" đọc ổn — vẫn kiểm tra bằng transcribe.
- Muốn có khoảng ngắt kịch tính: dùng "..." trong text **và** cắt file ra hai phần, chèn thêm im lặng ở timeline (ví dụ "đáng tiền nhất... | Ngũ Hành Sơn" cắt tại 2,2s, thêm 0,6s lặng, drop nhạc ngay lúc bắt đầu từ khoá).

## Chuẩn hoá & căn thời gian

```bash
bash scripts/vo_prep.sh <project> 1.06
```
- Tăng tốc 1.06x (Cartesia đã nhanh; với giọng người thật dùng 1.2x).
- In `silence_start/end` mỗi file → ánh xạ từng cụm từ với mốc thời gian để đặt `tin` của chữ/số/thẻ báo đúng lúc giọng đọc tới.
- Đặt timeline: `start(s1)=0.25`, các đoạn sau cách 0,3–0,45s. Ghi vào `timeline.js > vo` dạng `["f6.wav", start, srcFrom, srcTo|null]`.
- audio.py tự chuẩn RMS từng đoạn, nén nhẹ, ducking nhạc dưới giọng, loudnorm −14 LUFS / −1 dBTP.

Không nghe được audio trong môi trường này → luôn nói rõ với người dùng phần nào đã kiểm bằng nhận dạng giọng và phần nào (nhạc/SFX) họ cần nghe thử.
