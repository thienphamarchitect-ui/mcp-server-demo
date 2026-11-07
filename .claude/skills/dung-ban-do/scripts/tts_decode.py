#!/usr/bin/env python3
"""Giải mã các file kết quả audio_synthesize (Speko) bị lưu vì quá lớn thành <project>/vo/s1.wav, s2.wav... theo thứ tự gọi.

  python3 -I tts_decode.py <thư mục tool-results> <project>

Mỗi lần gọi audio_synthesize, kết quả (JSON có audio_base64 + url) được lưu thành
tool-results/mcp-Speko-audio_synthesize-<mốc thời gian>.txt. Sắp theo mốc thời gian = thứ tự đã gọi = s1, s2, ...
Cũng ghi vo/urls.json (link ký có hiệu lực 15 phút) để chạy audio_transcribe kiểm tra số liệu/tên riêng.
Nếu đã có file s*.wav từ lần trước, dùng --start N để đánh số tiếp.
"""
import sys, json, base64, glob, os
if len(sys.argv) < 3: sys.exit(__doc__)
D, P = sys.argv[1], sys.argv[2]
start = int(sys.argv[sys.argv.index('--start') + 1]) if '--start' in sys.argv else 1
files = sorted(glob.glob(os.path.join(D, 'mcp-Speko-audio_synthesize-*.txt')), key=lambda f: int(f.rsplit('-', 1)[1].split('.')[0]))
os.makedirs(os.path.join(P, 'vo'), exist_ok=True); urls = {}
for i, f in enumerate(files, start):
    d = json.load(open(f))
    open(os.path.join(P, 'vo', f's{i}.wav'), 'wb').write(base64.b64decode(d['audio_base64'])); urls[i] = d['url']
    print(i, round(d['duration_seconds'], 2), 's', d.get('provider'), d.get('model'))
json.dump(urls, open(os.path.join(P, 'vo', 'urls.json'), 'w'))
