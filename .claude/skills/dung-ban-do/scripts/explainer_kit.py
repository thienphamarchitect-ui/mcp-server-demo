"""Khối dựng sẵn cho MAP EXPLAINER 60 s (dùng trong spec.py): mỗi hàm trả về một câu {k, say, bg, dim, els}.
Bố cục theo chuẩn text/motion trong skill lam-video-bds (hero cap 150–230, nhãn 40–66, chip 58, src y≈1700)."""
BRAND = {'t1': 'KHÁNH LINH', 't2': 'ĐẦU TƯ BĐS HẠNG SANG ĐÀ NẴNG', 'loc': 'ĐÀ NẴNG · 2026', 'demo': 'BẢN DEMO · GIỌNG ĐỌC AI MẪU'}
DISC_BASE = 'Nội dung tham khảo, không phải lời khuyên đầu tư · Điều kiện vay theo chính sách từng thời điểm'

def h1(say, label, hero, q1, q2, hero_cap=190, bg='MAP'):
    els = [('L', label, 'w', 58, 430, 0.0, 1.0, {'sfx': 'whoosh'})]
    if hero: els.append(('L', hero, 'c', hero_cap, 620, 0.12, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -3}))
    els += [('L', q1, 'w', 84, 880, 0.55, 1.0)]
    if q2: els.append(('L', q2, 'c', 92, 1010, 0.72, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -5}))
    return {'k': 'h1', 'say': say, 'bg': bg, 'els': els}

def h2(say, concl, concl_cap=96, name='KHÁNH LINH', title='ĐẦU TƯ BĐS HẠNG SANG ĐÀ NẴNG', bg='MAP'):
    return {'k': 'h2', 'say': say, 'bg': bg, 'els': [
        ('L', name, 'c', 150, 540, 0.0, 1.0, {'anim': 'hero', 'sfx': 'sparkle'}),
        ('L', title, 'w', 48, 690, 0.1, 1.0),
        ('L', concl, 'r', concl_cap, 1280, 0.55, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -4})]}

def ctx(say, label, big, big_cap, sub, extra=None, note=None, bg='MAP', dim=True, big_opt=None):
    els = [('L', label, 'w', 56, 560, 0.0, 1.0, {'sfx': 'whoosh'}),
           ('L', sub, 'w', 46, 1010, 0.25, 1.0),
           ('L', big, 'c', big_cap, 800, 0.35, 1.0, big_opt or {'anim': 'hero', 'sfx': 'impact', 'g': -3})]
    if extra: els += extra
    if note: els.append(('S', note, 1700, 0.15, 1.0))
    return {'k': 'ctx', 'say': say, 'bg': bg, 'dim': dim, 'els': els}

def evid(say, label, parts, src_text, k='ev', bg='DARK', extra=None):
    """parts: [(nhãn nhỏ, số lớn, cap, opts)] tối đa 2 cặp"""
    els = [('L', label, 'c', 84, 560, 0.0, 1.0, {'sfx': 'whoosh'})]
    ys = [(830, 960), (1230, 1360)]
    for i, (lab, num, cap, op) in enumerate(parts):
        f = 0.30 + 0.3 * i
        els += [('L', lab, 'w', 44, ys[i][0], f, 1.0), ('L', num, 'c' if i == 0 else 'w', cap, ys[i][1], f + 0.08, 1.0, op or {'anim': 'hero', 'sfx': 'impact', 'g': -3})]
    if extra: els += extra
    els.append(('S', src_text, 1700, 0.25, 1.0))
    return {'k': k, 'say': say, 'bg': bg, 'dim': True, 'els': els}

def bridge(say, l1, l2, l3):
    return {'k': 'b1', 'say': say, 'bg': 'DARK', 'els': [
        ('L', l1, 'w', 76, 560, 0.0, 1.0, {'sfx': 'whoosh'}), ('L', l2, 'w', 76, 690, 0.35, 1.0), ('L', l3, 'c', 92, 830, 0.7, 1.0)]}

def b2(say='Ba tiêu chí.', sub='DÒNG TIỀN'):
    return {'k': 'b2', 'say': say, 'bg': 'DARK', 'els': [
        ('L', '3 TIÊU CHÍ', 'c', 230, 860, 0.05, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': 0}),
        ('L', sub, 'w', 110, 1050, 0.2, 1.0)]}

def crit(k, n, say, title, sub, extra, bg='MAP', title_cap=190, dim=False):
    els = [('L', 'TIÊU CHÍ %d' % n, 'w', 62, 300, 0.0, 1.0, {'sfx': 'whoosh'}),
           ('L', title, 'c', title_cap, 540, 0.08, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -3}),
           ('L', sub, 'w', 42, 730, 0.2, 1.0)]
    return {'k': k, 'say': say, 'bg': bg, 'dim': dim, 'els': els + (extra or [])}

def moc(say, chips, head='MÌNH CHỜ 3 MỐC', bg='MAP'):
    els = [('L', head, 'c', 130, 480, 0.0, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -3})]
    for i, (ic, t) in enumerate(chips): els.append(('C', ic, t, 920 + 150 * i, 0.15 + 0.22 * i, 1.0))
    return {'k': 'moc', 'say': say, 'bg': bg, 'dim': True, 'els': els}

def cta(say, line, disc, who='NHẮN KHÁNH LINH', bg='MAP'):
    return {'k': 'cta', 'say': say, 'bg': bg, 'dim': True, 'els': [
        ('L', line, 'w', 44, 1400 - 80, 0.0, 1.0),
        ('R', '<div class="cta" style="top:1360px"><span style="display:inline-block;transform:scaleX(.86)">%s</span></div>' % who, 0.1, 1.0, 'pop'),
        ('X', 'pop', 0.1, 0), ('X', 'sparkle', 0.12, -4),
        ('R', '<div class="disc">%s</div>' % disc, 0.0, 1.0, 'fade')]}
