"""Chép lời audio/video tiếng Việt bằng Whisper chạy cục bộ (faster-whisper).

  python3 chep_loi.py <file.mp3|mp4|wav> out.txt [model=medium]

Cài một lần: pip install faster-whisper   (sau proxy: SSL_CERT_FILE=/root/.ccr/ca-bundle.crt)
Âm thanh được ffmpeg giải mã thành PCM 16 kHz rồi đưa thẳng vào mô hình, tránh lỗi lệch phiên bản thư viện PyAV.
Kết quả có mốc thời gian từng câu: "[  12.3-  15.8] nội dung". 2,5 phút âm thanh mất khoảng 3 phút trên CPU với model medium.
Bản chép có thể sai chính tả vài chỗ; đủ để phân tích cấu trúc lập luận, KHÔNG dùng làm trích dẫn nguyên văn.
"""
import subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "medium"
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, dtype=np.float32)
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="vi", beam_size=5, vad_filter=True)
with open(out, "w", encoding="utf-8") as f:
    for s in segs:
        line = f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}"
        print(line, flush=True)
        f.write(line + "\n")
