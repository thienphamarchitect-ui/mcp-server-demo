#!/usr/bin/env python3
"""Sinh scene.js + timeline.js cho video MAP EXPLAINER ~60 s từ một file mô tả (spec) và mốc thời gian của giọng đọc.

  python3 build_explainer.py <spec.py> <project> [--words words.json] [--vo f1.wav] [--vo-offset 0.5]

spec.py định nghĩa: SCENE (dict cấu hình bản đồ, không có tt), CAM (danh sách (khóaCâu, tỷ lệ, đích, scale)),
SENT (danh sách câu: {k, say, bg:'MAP'|'DARK', dim:bool, els:[...]}), DISC (html miễn trừ), BRAND.
Mốc: nếu có --words (JSON [{text,start_ms,end_ms}] từ audio_transcribe word_timestamps) thì căn từng câu theo lời thật
(căn chuỗi từ bằng difflib); nếu không, ước lượng theo số tiếng (2,8 tiếng/giây) để xem thử.
Phần tử els: ('L',text,cls,cap,y,f0,f1,opts) ('C',icon,text,y,f0,f1) ('S',text,y,f0,f1) ('N',text,y,f0,f1)
('P',img,tag,y,w,f0,f1,rot) ('R',html,f0,f1,mode); f0/f1 là tỷ lệ 0..1 trong câu (f1=1 tới hết câu).
"""
import sys, os, re, json, importlib.util, difflib, subprocess, unicodedata

def load_spec(path):
    s = importlib.util.spec_from_file_location('spec', path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def norm(w):
    w = unicodedata.normalize('NFC', w.lower())
    return re.sub(r'[^\w]', '', w)

def tokens(text): return [t for t in (norm(x) for x in text.split()) if t]

def align(sents, words):
    """trả [(start_s, end_s)] cho từng câu"""
    a, idx = [], []
    for s in sents:
        idx.append(len(a)); a += tokens(s['say'])
    b = [norm(w['text']) for w in words]
    keep = [i for i, t in enumerate(b) if t]; bt = [b[i] for i in keep]
    sm = difflib.SequenceMatcher(None, a, bt, autojunk=False)
    amap = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): amap[blk.a + k] = keep[blk.b + k]
    out = []
    n = len(a)
    for i, s in enumerate(sents):
        i0 = idx[i]; i1 = idx[i + 1] if i + 1 < len(sents) else n
        first = next((amap[j] for j in range(i0, i1) if j in amap), None)
        last = next((amap[j] for j in range(i1 - 1, i0 - 1, -1) if j in amap), None)
        out.append((first, last))
    # lấp chỗ trống bằng nội suy theo chỉ số từ
    res = []
    for i, (f, l) in enumerate(out):
        if f is None: f = (res[-1][2] + 1) if res else 0
        if l is None or l < f: l = f
        res.append((words[f]['start_ms'] / 1000, words[l]['end_ms'] / 1000, l))
    return [(r[0], r[1]) for r in res]

def estimate(sents, rate=2.8):
    t, out = 0.0, []
    for s in sents:
        d = len(s['say'].split()) / rate; out.append((t, t + d)); t += d + 0.25
    return out

def js(x): return json.dumps(x, ensure_ascii=False)

def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    spec, P = load_spec(a[0]), a[1]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    off = float(opt('--vo-offset', 0.5)); vo = opt('--vo', 'f1.wav')
    sents = spec.SENT
    if opt('--times'):
        tm = [(x[0] + off, x[1] + off) for x in json.load(open(opt('--times')))]
    elif opt('--words'):
        tm = align(sents, json.load(open(opt('--words'))))
        tm = [(s + off, e + off) for s, e in tm]
    else:
        tm = [(s + off, e + off) for s, e in estimate(sents)]
    # câu i chạy từ start_i tới start_{i+1}
    T0 = [t[0] for t in tm]; T0[0] = 0.0
    T1 = [T0[i + 1] if i + 1 < len(T0) else tm[-1][1] + 0.4 for i in range(len(T0))]
    tail = float(getattr(spec, 'TAIL', 3.0)); total = round(tm[-1][1] + tail, 1)
    T1[-1] = total
    S = {s['k']: i for i, s in enumerate(sents)}
    # --- timeline.js
    bgs = []
    for i, s in enumerate(sents):
        bg = s.get('bg', 'DARK')
        if bgs and bgs[-1][0] == bg: bgs[-1][2] = T1[i]
        else: bgs.append([bg, T0[i] if i else 0, T1[i], 0])
    for j, b in enumerate(bgs):
        if j: b[1] = round(b[1] - 0.2, 2)
        b[2] = round(b[2] + (0.2 if j + 1 < len(bgs) else 0), 2)
    bgs[0][1] = 0; bgs[-1][2] = total
    dk = T0[S[getattr(spec, 'DROP_AT', 'b2')]] + 0.6
    TL = {'fps': 30, 'total': total, 'drop': round(dk, 2),
          'music': {'start': 0.3, 'beatsFrom': 6.5, 'breakdown': [round(dk - 1.85, 2), round(dk - 0.15, 2)], 'outro': round(total - 4.0, 2)},
          'vo': [[vo, off, 0, None]], 'bgs': [[b[0], round(b[1], 2), round(b[2], 2), 0] for b in bgs]}
    open(os.path.join(P, 'timeline.js'), 'w').write('window.TL = ' + json.dumps(TL, ensure_ascii=False, indent=1) + '\n')
    # --- scene.js
    SC = dict(spec.SCENE)
    SC['brand'] = spec.BRAND
    dim = []
    for i, s in enumerate(sents):
        if s.get('dim'):
            if dim and abs(dim[-1][1] - T0[i]) < 0.05: dim[-1][1] = round(T1[i], 2)
            else: dim.append([round(T0[i], 2), round(T1[i], 2)])
    SC['dim'] = dim
    keys = [[0.1, 'OV', SC.get('ov', {}).get('scale', 0.4)]]
    for (k, f, tgt, sc) in spec.CAM:
        i = S[k]; t = round(T0[i] + f * (T1[i] - T0[i]), 2)
        if t <= keys[-1][0]: t = round(keys[-1][0] + 0.1, 2)
        keys.append([t, tgt, sc])
    keys.append([total, 'OV', SC.get('ov', {}).get('scale', 0.4)])
    SC['cam'] = {'push': SC.get('push', 0.06), 'keys': keys}
    # nhãn ghim: lwin = {id: [(khóaCâu_từ, khóaCâu_đến)]}
    lw = {}
    for pid, wins in getattr(spec, 'LABELS', {}).items():
        lw[pid] = [[round(T0[S[x]], 2), round(T1[S[y]], 2)] for x, y in wins]
    SC['labwin'] = lw
    # vòng/zones theo câu: trường 'ks' = (khóa_từ, khóa_đến) thay cho t0,t1
    for key in ('rings', 'zones'):
        for r in SC.get(key, []):
            if 'ks' in r:
                x, y = r.pop('ks'); r['t0'] = round(T0[S[x]], 2); r['t1'] = round(T1[S[y]], 2)
    out = ['/* sinh bởi build_explainer.py — sửa spec.py rồi chạy lại, đừng sửa tay */',
           'window.SCENE = ' + json.dumps(SC, ensure_ascii=False, indent=1) + ';', 'initEngine(window.SCENE);']
    sfxl = []
    for i, s in enumerate(sents):
        t0, t1 = T0[i], T1[i]; d = t1 - t0
        out.append(f'// [{s["k"]}] {t0:.2f}-{t1:.2f}: {s["say"]}')
        for e in s.get('els', []):
            typ = e[0]
            if typ == 'L':
                _, text, cls, cap, y, g0, g1, *op = e; op = op[0] if op else {}
                out.append(f'line({js(text)},{js(cls)},{cap},{y},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f},{js(op)});')
            elif typ == 'C':
                _, ic, text, y, g0, g1 = e
                out.append(f'chip({js(ic)},{js(text)},{y},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f});')
            elif typ == 'S':
                _, text, y, g0, g1 = e; out.append(f'src({js(text)},{y},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f});')
            elif typ == 'N':
                _, text, y, g0, g1 = e; out.append(f'note({js(text)},{y},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f});')
            elif typ == 'P':
                _, img, tag, y, w, g0, g1, rot = e
                out.append(f'paper({js(img)},{js(tag)},{y},{w},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f},{rot});')
            elif typ == 'R':
                _, html, g0, g1, mode = e
                out.append(f'raw({js(html)},{t0 + g0 * d:.2f},{t0 + g1 * d:.2f},{js(mode)});')
            elif typ == 'X':   # sfx tuyệt đối theo tỷ lệ: ('X', name, f, gain)
                _, name, g0, gain = e; sfxl.append((t0 + g0 * d, name, gain))
        if i and s.get('bg') != sents[i - 1].get('bg'): sfxl.append((t0 - 0.05, 'whoosh', -3))
        if s.get('whoosh'): sfxl.append((t0 + 0.02, 'whoosh', -3))
    for t, n, g in sfxl: out.append(f'sfx({t:.2f},{js(n)},{g});')
    out.append('sfx(0,"impact",-6);')
    out.append(f'sfx({dk - 0.75:.2f},"riser",-4);')
    out.append(f'FX.flash=[[0,0.5,1],[{dk:.2f},0.35,0.9]];')
    out.append(f'FX.glow=[[{dk + 0.3:.2f},1.6]];')
    out.append('FX.sweep=[];')
    open(os.path.join(P, 'scene.js'), 'w').write('\n'.join(out) + '\n')
    json.dump({'T0': T0, 'T1': T1, 'total': total}, open(os.path.join(P, 'times.json'), 'w'))
    print('tổng', total, 's;', ' '.join(f'{s["k"]}@{T0[i]:.1f}' for i, s in enumerate(sents)))

if __name__ == '__main__': main()
