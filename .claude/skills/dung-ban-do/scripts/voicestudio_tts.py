#!/usr/bin/env python3
"""Tạo giọng đọc bằng VoiceStudio (API kiểu OpenAI) -> <out>/s1.wav, s2.wav ... (mỗi dòng của --lines một file).

  python3 voicestudio_tts.py --base https://<podid>-3900.proxy.runpod.net --lines loi-doc.txt --out <project>/vo \
        --voice-name "Giọng Linh" [--pod <podId>] [--start N] [--only 3,5]
  python3 voicestudio_tts.py --base ... --list          # chỉ liệt kê giọng (id + tên)

Khoá lấy từ biến môi trường, KHÔNG nhận qua tham số và không bao giờ in ra:
  VOICESTUDIO_API_KEY  (bắt buộc)   RUNPOD_API_KEY  (chỉ cần nếu pod đang tắt và có --pod)
Pod RunPod tự tắt sau ~5 phút rảnh: /health lỗi + có --pod + có RUNPOD_API_KEY thì script gọi
POST https://rest.runpod.io/v1/pods/<pod>/start rồi chờ /health (tối đa 5 phút).
Mạng cần mở tới 2 tên miền: rest.runpod.io và <podid>-3900.proxy.runpod.net.
Sau khi có s*.wav: bash vo_prep.sh <project> 1.0 rồi căn lại mốc tin/tout trong scene.js (thời lượng giọng mới khác giọng cũ).
"""
import argparse, json, os, ssl, sys, time, urllib.request, urllib.error, wave

ap = argparse.ArgumentParser()
ap.add_argument('--base', required=True); ap.add_argument('--lines'); ap.add_argument('--out')
ap.add_argument('--voice-name', default='', help='tên (hoặc id) giọng trong VoiceStudio'); ap.add_argument('--voice-id', default='')
ap.add_argument('--model', default='tts-1'); ap.add_argument('--format', default='wav'); ap.add_argument('--pod', default='')
ap.add_argument('--start', type=int, default=1, help='số thứ tự của dòng đầu (mặc định 1)'); ap.add_argument('--only', default='', help='chỉ tạo các số này, vd. 3,5')
ap.add_argument('--list', action='store_true'); ap.add_argument('--speed', type=float, default=0, help='nếu API hỗ trợ tham số speed (0 = bỏ qua)')
A = ap.parse_args()
BASE = A.base.rstrip('/'); KEY = os.environ.get('VOICESTUDIO_API_KEY', ''); RK = os.environ.get('RUNPOD_API_KEY', '')
CA = os.environ.get('SSL_CERT_FILE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else None)
CTX = ssl.create_default_context(cafile=CA) if CA else ssl.create_default_context()

def req(method, url, key='', body=None, timeout=120):
    h = {'User-Agent': 'dung-ban-do/1.0'}
    if key: h['Authorization'] = 'Bearer ' + key
    data = None
    if body is not None: data = json.dumps(body).encode('utf-8'); h['Content-Type'] = 'application/json'
    r = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, context=CTX, timeout=timeout) as resp: return resp.status, resp.read()
    except urllib.error.HTTPError as e: return e.code, e.read()
    except Exception as e: return 0, str(e).encode()

def healthy():
    c, b = req('GET', BASE + '/health', timeout=20); return c == 200

if not healthy():
    if A.pod and RK:
        print('Pod chưa sẵn sàng -> gọi start...'); c, b = req('POST', f'https://rest.runpod.io/v1/pods/{A.pod}/start', RK, timeout=60)
        print('start: HTTP', c)
        for i in range(60):
            time.sleep(5)
            if healthy(): print('Pod sẵn sàng sau ~%ds' % ((i + 1) * 5)); break
        else: sys.exit('Pod không sẵn sàng sau 5 phút (kiểm tra bảng điều khiển RunPod).')
    else: sys.exit('/health lỗi. Bật pod (cần --pod và RUNPOD_API_KEY) hoặc kiểm tra mạng/địa chỉ.')
if not KEY: sys.exit('Thiếu VOICESTUDIO_API_KEY trong biến môi trường (thêm vào cài đặt môi trường; không dán khoá vào chat).')

c, b = req('GET', BASE + '/v1/audio/voices', KEY)
if c != 200: sys.exit(f'Liệt kê giọng lỗi: HTTP {c} {b[:200].decode("utf-8", "replace")}')
V = json.loads(b); V = V.get('voices') or V.get('data') or V if isinstance(V, dict) else V
vid = A.voice_id
name_of = lambda v: v.get('name') or v.get('voice_name') or v.get('id') or ''
id_of = lambda v: v.get('id') or v.get('voice_id') or v.get('name')
if A.list or not (vid or A.voice_name):
    for v in V: print(f'{id_of(v)}\t{name_of(v)}')
    sys.exit(0)
if not vid:
    m = [v for v in V if A.voice_name.lower() in (name_of(v).lower(), str(id_of(v)).lower())] or [v for v in V if A.voice_name.lower() in name_of(v).lower()]
    if not m: sys.exit('Không thấy giọng "%s". Có: %s' % (A.voice_name, ', '.join(name_of(v) for v in V)))
    if len(m) > 1: print('Nhiều giọng khớp, dùng cái đầu:', ', '.join(name_of(v) for v in m))
    vid = id_of(m[0]); print('Giọng:', name_of(m[0]))
if not (A.lines and A.out): sys.exit('cần --lines và --out')
lines = [l.strip() for l in open(A.lines, encoding='utf-8').read().splitlines() if l.strip() and not l.lstrip().startswith('#')]
only = {int(x) for x in A.only.split(',') if x.strip()}; os.makedirs(A.out, exist_ok=True); total = 0.0
for i, text in enumerate(lines, A.start):
    if only and i not in only: continue
    body = {'model': A.model, 'voice': vid, 'input': text, 'response_format': A.format}
    if A.speed: body['speed'] = A.speed
    for k in range(3):
        c, b = req('POST', BASE + '/v1/audio/speech', KEY, body, timeout=300)
        if c == 200 and b[:4] == b'RIFF': break
        print(f'  s{i}: lần {k + 1} lỗi HTTP {c} {b[:120].decode("utf-8", "replace") if c != 200 else "(không phải WAV)"}'); time.sleep(2 * (k + 1))
    else: sys.exit(f'Dòng {i} thất bại.')
    p = os.path.join(A.out, f's{i}.wav'); open(p, 'wb').write(b)
    try:
        with wave.open(p) as w: d = w.getnframes() / w.getframerate()
    except Exception: d = 0
    total += d; print(f's{i}.wav  {d:5.2f}s  {len(text)} ký tự')
print(f'Xong. Tổng ~{total:.1f}s. Tiếp: bash vo_prep.sh {A.out.rsplit("/vo", 1)[0]} 1.0  rồi chạy audio_transcribe/nghe kiểm tra số liệu & tên riêng.')
