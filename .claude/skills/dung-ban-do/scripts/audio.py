# Mix âm thanh: giọng đọc + nhạc nền tổng hợp (Am-F-C-G, 100 BPM) + SFX tổng hợp + ducking + loudnorm -14 LUFS.
#   python3 audio.py <projectDir>
# Đọc <project>/timeline.js (window.TL = {...JSON...}): total, drop, vo, music; và <project>/sfx.json (do render.js ghi).
# Giọng đọc lấy từ <project>/vo/<file>. Kết quả: <project>/mix.wav
import json, subprocess, numpy as np, os, sys
from scipy.signal import lfilter
D = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
_tl = open(os.path.join(D, 'timeline.js'), encoding='utf-8').read()
TLJ = json.loads(_tl[_tl.index('{'):_tl.rindex('}') + 1])
SR = 48000; TOTAL = float(TLJ['total']); DROP = float(TLJ['drop'])
MUS = TLJ.get('music', {})
M_START = MUS.get('start', 0.3); M_BEATS = MUS.get('beatsFrom', 4.4)
M_BREAK = MUS.get('breakdown', [DROP - 2.9, DROP - 0.77]); M_OUTRO = MUS.get('outro', TOTAL - 7.5)
N = int(TOTAL * SR); rng = np.random.default_rng(7)
t_all = np.arange(N) / SR
def load(f):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def env(n, a=0.005, r=None, curve=6):
    t = np.arange(n) / SR; e = np.minimum(1, t / max(a, 1e-4))
    if r: e *= np.exp(-curve * t / r)
    return e

def place(buf, x, at, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[:len(buf) - i]; buf[i:i + len(x)] += x * g

def lp(x, k):  # one-pole lowpass, k in (0,1)
    return lfilter([k], [1, -(1 - k)], x)

def bp_noise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)

# ---------- SFX ----------
def s_whoosh():
    n = int(0.55 * SR); t = np.arange(n) / SR
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR)
    y = np.fft.irfft(X * np.exp(-((f - 2500) / 2500) ** 2), n)
    e = np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 2
    sweep = np.sin(2 * np.pi * np.cumsum(300 + 1400 * t / 0.55) / SR) * 0.15
    y = y / np.abs(y).max() * e + sweep * e; return y * 0.7
def s_pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = 900 * np.exp(-t * 30) + 250; return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.05, 5) * 0.8
def s_ting():
    n = int(0.9 * SR); t = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * fr * t) for fr, a in [(1568, 1), (2352, .5), (3136, .3), (4704, .15)])
    return y * env(n, 0.002, 0.5, 5) * 0.35
def s_impact():
    n = int(1.6 * SR); t = np.arange(n) / SR
    f = 110 * np.exp(-t * 6) + 42; y = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 1.2, 4)
    y += bp_noise(n, 60, 3000) * env(n, 0.001, 0.25, 8) * 0.5
    return np.tanh(y * 1.6) * 0.9
def s_riser():
    n = int(2.3 * SR); t = np.arange(n) / SR
    y = bp_noise(n, 800, 9000) * (t / 2.3) ** 2 * 0.5
    y += np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / 2.3) ** 2) / SR) * (t / 2.3) ** 2 * 0.25
    return y
def s_shutter():
    n = int(0.16 * SR); y = np.zeros(n)
    for at in (0, 0.07):
        i = int(at * SR); m = int(0.03 * SR); y[i:i + m] += bp_noise(m, 2000, 9000) * env(m, 0.0005, 0.02, 6)
    return y * 0.6
def s_heart():
    n = int(0.7 * SR); y = np.zeros(n)
    for at, a in ((0, 1), (0.22, 0.7)):
        m = int(0.25 * SR); tt = np.arange(m) / SR
        place(y, np.sin(2 * np.pi * (60 * np.exp(-tt * 8) + 40) * tt) * env(m, 0.003, 0.18, 6) * a, at)
    return np.tanh(y * 2) * 0.9
def s_notify():
    n = int(0.45 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 1318 * t) * env(n, 0.002, 0.2, 6)
    y2 = np.sin(2 * np.pi * 1976 * t) * env(n, 0.002, 0.25, 6); out = y * 0.4; place(out, y2[:n - int(0.08 * SR)] * 0.35, 0.08)
    return out
def s_cash():
    out = s_ting() * 0.8; n = len(out)
    for k in range(6):
        m = int(0.04 * SR); place(out, bp_noise(m, 3000, 12000) * env(m, 0.0005, 0.03, 6) * 0.3, 0.05 + k * 0.045)
    return out
def s_sparkle():
    n = int(1.0 * SR); out = np.zeros(n)
    for k in range(9):
        m = int(0.35 * SR); tt = np.arange(m) / SR; fr = 2500 + 3500 * rng.random()
        place(out, np.sin(2 * np.pi * fr * tt) * env(m, 0.002, 0.2, 6) * 0.12, k * 0.07)
    return out
SFXF = dict(whoosh=s_whoosh, pop=s_pop, ting=s_ting, impact=s_impact, riser=s_riser, shutter=s_shutter,
            heartbeat=s_heart, notify=s_notify, cash=s_cash, sparkle=s_sparkle)
bank = {k: f() for k, f in SFXF.items()}

sfx = np.zeros(N)
for ev in json.load(open(os.path.join(D, 'sfx.json'))):
    place(sfx, bank[ev['name']], ev['t'], 10 ** ((ev['g'] - 6) / 20))

# ---------- MUSIC (100 BPM, Am-F-C-G) ----------
BEAT = 0.6; off = DROP % BEAT
def midi(m): return 440 * 2 ** ((m - 69) / 12)
CH = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]
ROOT = [45, 41, 36, 43]
music = np.zeros(N); drums = np.zeros(N)
def section_gain(t):  # 0 = im lặng (khoảng lặng trước drop)
    if t < M_START: return 0
    if M_BREAK[1] <= t < DROP: return 0
    return 1
def is_full(t): return DROP <= t < M_OUTRO
def is_pre(t): return M_BEATS <= t < M_BREAK[0]

beats = np.arange(off, TOTAL, BEAT)
for bi, bt in enumerate(beats):
    if section_gain(bt) == 0: continue
    bar = int(round((bt - off) / BEAT)) // 4; ci = bar % 4; pos = int(round((bt - off) / BEAT)) % 4
    dark = M_BREAK[0] <= bt < M_BREAK[1]
    # pad on bar start
    if pos == 0:
        n = int(BEAT * 4 * SR); tt = np.arange(n) / SR
        pad = np.zeros(n)
        nh = 3 if dark else 6
        for m in CH[ci]:
            for det in (-0.12, 0.12):
                fr = midi(m + 12) * 2 ** (det / 12)
                for h in range(1, nh + 1): pad += np.sin(2 * np.pi * fr * h * tt + h) / h ** 1.3
        e = np.minimum(1, tt / 0.6) * np.minimum(1, (tt[-1] - tt) / 0.3 + 0.0)
        place(music, pad * e * 0.018, bt)
        if is_full(bt) or is_pre(bt):  # sub bass
            fr = midi(ROOT[ci]); bass = np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(4 * np.pi * fr * tt)
            for k in range(8):
                i0 = int(k * BEAT / 2 * SR); m = int(BEAT / 2 * SR)
                seg = bass[i0:i0 + m] * env(m, 0.005, 0.28, 3) * (1 if is_full(bt) else 0.45)
                place(music, seg * 0.16, bt + k * BEAT / 2)
    # arp 8th notes
    if not dark:
        for k in range(2):
            m = int(0.32 * SR); tt = np.arange(m) / SR; note = CH[ci][(pos * 2 + k) % 3] + 24
            pl = (np.sin(2 * np.pi * midi(note) * tt) + 0.3 * np.sin(4 * np.pi * midi(note) * tt)) * env(m, 0.002, 0.18, 6)
            place(music, pl * (0.05 if is_full(bt) else 0.032), bt + k * BEAT / 2)
    # drums
    if is_full(bt) or is_pre(bt):
        m = int(0.4 * SR); tt = np.arange(m) / SR
        kick = np.sin(2 * np.pi * np.cumsum(150 * np.exp(-tt * 25) + 45) / SR) * env(m, 0.001, 0.3, 5)
        if is_full(bt) or pos in (0, 2): place(drums, np.tanh(kick * 2) * (0.5 if is_full(bt) else 0.3), bt)
        hm = int(0.06 * SR); hat = bp_noise(hm, 7000, 16000) * env(hm, 0.0005, 0.04, 6)
        place(drums, hat * (0.12 if is_full(bt) else 0.06), bt + BEAT / 2)
        if is_full(bt) and pos in (1, 3):
            cm = int(0.25 * SR); clap = bp_noise(cm, 900, 6000) * env(cm, 0.001, 0.12, 6)
            place(drums, clap * 0.22, bt)
music = lp(music, 0.35) + drums
music *= np.clip(1 - (t_all - (TOTAL - 2.0)) / 2.0, 0, 1)  # outro fade

# ---------- VOICE ----------
TL = TLJ['vo']
voice = np.zeros(N)
for f, at, a, b in TL:
    fp = os.path.join(D, 'vo', f)
    if not os.path.exists(fp): sys.exit(f'Thiếu file giọng đọc: {fp} (chạy vo_prep.sh trước)')
    x = load(fp); x = x[int(a * SR): (int(b * SR) if b else None)]
    x = x / (np.sqrt(np.mean(x[np.abs(x) > 0.005] ** 2)) + 1e-9) * 0.12
    fade = int(0.01 * SR); x[:fade] *= np.linspace(0, 1, fade); x[-fade:] *= np.linspace(1, 0, fade)
    place(voice, x, at)
# light compression + presence
voice = np.tanh(voice * 2.2) / 2.2
# ducking envelope
ve = np.convolve(np.abs(voice), np.ones(int(0.15 * SR)) / int(0.15 * SR), 'same')
duck = 1 - 0.55 * np.clip(ve / 0.03, 0, 1)
mix = voice * 1.0 + music * duck * 0.9 + sfx * 0.55
mix /= np.abs(mix).max() * 1.05
st = np.stack([mix, mix], 1).astype(np.float32)
st.tofile(os.path.join(D, 'mix.f32'))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', os.path.join(D, 'mix.f32'),
                '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9', '-ar', '48000', os.path.join(D, 'mix.wav')], check=True)
print('ok')
