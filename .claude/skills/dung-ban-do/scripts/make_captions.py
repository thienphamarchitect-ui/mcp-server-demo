#!/usr/bin/env python3
"""Tạo phụ đề (captions.js) từ lời đọc + mốc giọng trong timeline.js.

  python3 make_captions.py --lines loi-doc.txt --project <project> [--max-words 5] [--max-chars 30] [--out <project>/captions.js]

Mỗi dòng lời đọc ứng với vo/f<N>.wav (N = số thứ tự dòng, như vo_prep.sh) và có mốc bắt đầu trong timeline.js > vo.
Dòng được cắt thành cụm ≤ --max-words từ / ≤ --max-chars ký tự (ưu tiên cắt sau dấu câu), thời gian chia theo số ký tự trong
khoảng giọng thật (bỏ phần lặng đầu/cuối file). Độ chính xác ±0,2s; cần chính xác hơn thì lấy mốc từ audio_transcribe(word_timestamps=true).
Dùng trong scene.js:   <script src="captions.js"></script> (thêm vào render.html)  rồi  captions(window.CAPTIONS, {y:1560});
Bọc từ cần nhấn bằng *...* trong captions.js (chữ cyan). Phụ đề đè lên thẻ số liệu y≥1560 -> dời thẻ lên hoặc bỏ phụ đề ở cảnh đó.
"""
import argparse, json, os, re, subprocess, wave
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('--lines', required=True); ap.add_argument('--project', required=True)
ap.add_argument('--max-words', type=int, default=5); ap.add_argument('--max-chars', type=int, default=30); ap.add_argument('--out')
A = ap.parse_args(); P = os.path.abspath(A.project)
tl = open(os.path.join(P, 'timeline.js'), encoding='utf-8').read(); TL = json.loads(tl[tl.index('{'):tl.rindex('}') + 1])
lines = [l.strip() for l in open(A.lines, encoding='utf-8').read().splitlines() if l.strip() and not l.lstrip().startswith('#')]
starts = {}
for f, at, a, b in TL['vo']:
    n = int(re.search(r'f(\d+)\.wav', f).group(1))
    if a == 0 and b is None: starts[n] = at
def speech_span(path):
    with wave.open(path) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
    env = np.convolve(np.abs(x), np.ones(int(0.02 * sr)) / int(0.02 * sr), 'same'); on = np.where(env > 0.02)[0]
    return (on[0] / sr, on[-1] / sr) if len(on) else (0, len(x) / sr)
def chunks(text):
    words = text.split(); out = []; cur = []
    for w in words:
        cur.append(w)
        if len(cur) >= A.max_words or len(' '.join(cur)) >= A.max_chars or re.search(r'[,.:;?!]$', w) and len(cur) >= 2: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return out
CAP = []
for n, text in enumerate(lines, 1):
    p = os.path.join(P, 'vo', f'f{n}.wav')
    if n not in starts or not os.path.exists(p): print(f'bỏ qua dòng {n}: thiếu mốc hoặc file'); continue
    s0, s1 = speech_span(p); cs = chunks(text); tot = sum(len(c) for c in cs) or 1; t = starts[n] + s0; dur = s1 - s0
    for c in cs:
        d = dur * len(c) / tot; CAP.append([round(t, 2), round(t + d + 0.08, 2), c]); t += d
out = A.out or os.path.join(P, 'captions.js')
open(out, 'w', encoding='utf-8').write('window.CAPTIONS = [\n' + ',\n'.join(json.dumps(c, ensure_ascii=False) for c in CAP) + '\n];\n'); print(len(CAP), 'phụ đề ->', out)
