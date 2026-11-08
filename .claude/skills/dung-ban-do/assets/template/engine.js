/* engine.js — engine dựng bản đồ vệ tinh 9:16 (1080x1920).
 * Dùng chung cho mọi video. Nội dung riêng nằm ở scene.js (cấu hình SCENE + các dòng line()/paper()/chip()...).
 * render(t) là hàm THUẦN theo thời gian t (giây): mọi trạng thái tính từ t, không dùng CSS animation,
 * nên chụp từng khung bằng scripts/render.js cho kết quả xác định.
 *
 * Thứ tự nạp trong render.html: assets/map_config.js (MAPCFG) -> timeline.js (TL) -> engine.js -> scene.js
 * scene.js phải gọi initEngine(SCENE) trước khi gọi line()/paper()/...
 */
const W = 1080, H = 1920;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
const eOut = x => 1 - Math.pow(1 - x, 3);
const eExpo = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const eBack = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const eIO = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
// màu theo loại khu vực (đúng mã màu video mẫu): vàng cam = KCN/khu kinh tế; đỏ = khu đô thị; tím = cảng; cam = sân bay; xanh lá = ranh đô thị/du lịch; xanh dương = ranh hành chính
const ZCOL = { kcn: '#FFC21A', dothi: '#FF4D5E', cang: '#A78BFA', sanbay: '#FF9A3C', xanh: '#34D399', hanhchinh: '#4DD2FF' };
let ZONES = [], KM = null, kmEl = {};
const SFX = []; const sfx = (t, name, g = 0) => SFX.push({ t: +t.toFixed(3), name, g });
window.SFX_LIST = SFX;
// hiệu ứng toàn khung — scene.js ghi đè: flash [[t,dur,max]], glow [[t,dur]], sweep [[t]]
const FX = { flash: [[0, 0.5, 1]], glow: [], sweep: [] };
// ảnh cần nạp trước khi chụp khung (clip()); render.js chờ window.READY()
const READY_LIST = []; window.READY = () => Promise.all(READY_LIST);

/* ---------- trạng thái bản đồ (điền trong initEngine) ---------- */
let CFG, MZ, MX0, MY0, PINS = {}, ROUTE = [], OVC = [0, 0], OVS = 0.32, RL = 1, RINGS = [], DIM = [], KEYS = [];
let mapimg, rlayer, rbase, rg, trainEl, pinEls = {}, placeEls = [], pinT = {}, LABWIN = {}, TRAIN = null;
let bgEls = [], dots = [];

function geo(lat, lon) {                       // lat/lon -> toạ độ px trong ảnh nền (zoom MAPCFG.z)
  const n = 2 ** MZ, x = (lon + 180) / 360 * n, la = lat * Math.PI / 180;
  const y = (1 - Math.log(Math.tan(la) + 1 / Math.cos(la)) / Math.PI) / 2 * n;
  return [(x - MX0) * 256, (y - MY0) * 256];
}
// km -> px ảnh nền ở vĩ độ lat (Web Mercator, ô 256px): m/px = 156543.03 * cos(lat) / 2^z
const kmToPx = (km, lat) => km * 1000 / (156543.03392804097 * Math.cos(lat * Math.PI / 180) / 2 ** MZ);
window.kmToPx = kmToPx;
function smoothPath(pts) {                     // Catmull-Rom -> Bezier: đường cong mượt qua các điểm
  let d = `M${pts[0][0]},${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    d += ` C${p1[0] + (p2[0] - p0[0]) / 6},${p1[1] + (p2[1] - p0[1]) / 6} ${p2[0] - (p3[0] - p1[0]) / 6},${p2[1] - (p3[1] - p1[1]) / 6} ${p2[0]},${p2[1]}`;
  }
  return d;
}
// đích camera: 'OV' (toàn cảnh) | id ghim (số) | 'END' (cuối tuyến) | [lat,lon,dyPx] | {px:[x,y]}
function target(tg) {
  if (tg === 'OV') return OVC.slice();
  if (tg === 'END') return ROUTE[ROUTE.length - 1].slice();
  if (typeof tg === 'number') return PINS[tg].slice(0, 2);
  if (Array.isArray(tg)) { const p = geo(tg[0], tg[1]); return [p[0], p[1] + (tg[2] || 0)]; }
  return tg.px.slice();
}

function initEngine(cfg) {
  CFG = cfg; MZ = MAPCFG.z; MX0 = MAPCFG.x0; MY0 = MAPCFG.y0;
  // --- thương hiệu (góc trên) ---
  const b = cfg.brand || {};
  document.getElementById('brand').innerHTML = b.t1 ? `<div class="bar"></div><div><div class="t1">${b.t1}</div><div class="t2">${b.t2 || ''}</div></div>` : '';
  document.getElementById('loc').textContent = b.loc || ''; document.getElementById('loc').style.display = b.loc ? '' : 'none';
  document.getElementById('demo').textContent = b.demo || ''; document.getElementById('demo').style.display = b.demo ? '' : 'none';
  // --- dữ liệu hình học ---
  (cfg.pins || []).forEach(p => { PINS[p.id] = [...geo(p.lat, p.lon), p.label, p.side || 'L', p.dy || 0, p.dx || 0, !!p.dot]; });
  ROUTE = (cfg.route || []).map(p => geo(p[0], p[1]));
  const RD = ROUTE.length ? smoothPath(ROUTE) : '';
  const allPts = ROUTE.length ? ROUTE : Object.values(PINS).map(p => p.slice(0, 2));
  const RX = allPts.map(p => p[0]), RY = allPts.map(p => p[1]);
  OVC = cfg.ov && cfg.ov.center ? geo(cfg.ov.center[0], cfg.ov.center[1]) : [(Math.min(...RX) + Math.max(...RX)) / 2, (Math.min(...RY) + Math.max(...RY)) / 2];
  OVS = (cfg.ov && cfg.ov.scale) || 0.32;
  TRAIN = cfg.train || null;
  const credit = cfg.credit === undefined ? 'Ảnh vệ tinh: Esri, Maxar, Earthstar Geographics' : cfg.credit;
  const det = (MAPCFG.det || []).map(m => `<img class="det" src="${m.src}" style="position:absolute;left:${m.x}px;top:${m.y}px;width:${m.w}px;height:${m.h}px;opacity:0;-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 62%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 62%,transparent 100%)">`).join('');
  document.getElementById('mapwrap').innerHTML = `
<div id="mapimg" style="position:absolute;left:0;top:0;width:${MAPCFG.W}px;height:${MAPCFG.H}px;transform-origin:0 0;filter:saturate(1.08) brightness(1.12) contrast(1.08)"><img src="${MAPCFG.src}" style="position:absolute;left:0;top:0">${det}</div>
<div id="rlayer" style="position:absolute;left:0;top:0;width:${MAPCFG.W}px;height:${MAPCFG.H}px;transform-origin:0 0">
 <svg width="${MAPCFG.W}" height="${MAPCFG.H}" style="position:absolute;left:0;top:0;overflow:visible">
  <path id="rbase" d="${RD}" fill="none" stroke="rgba(255,255,255,.55)" stroke-linecap="round"/>
  <path id="rg3" d="${RD}" fill="none" stroke="#05F4E8" stroke-linecap="round" opacity=".16"/>
  <path id="rg2" d="${RD}" fill="none" stroke="#05F4E8" stroke-linecap="round" opacity=".38"/>
  <path id="rg1" d="${RD}" fill="none" stroke="#05F4E8" stroke-linecap="round"/>
  <path id="rg0" d="${RD}" fill="none" stroke="#fff" stroke-linecap="round" opacity=".9"/>
  <g id="zones"></g>
  <g id="rings"></g>
  <g id="train"><rect x="-74" y="-20" width="148" height="40" rx="20" fill="rgba(5,244,232,.35)"/><rect x="-66" y="-14" width="132" height="28" rx="14" fill="#fff" stroke="#05F4E8" stroke-width="3"/><rect x="-54" y="-8" width="20" height="9" rx="3" fill="#06121C"/><rect x="-26" y="-8" width="20" height="9" rx="3" fill="#06121C"/><rect x="2" y="-8" width="20" height="9" rx="3" fill="#06121C"/><rect x="30" y="-8" width="20" height="9" rx="3" fill="#06121C"/><rect x="-64" y="4" width="128" height="7" rx="3" fill="#E3172F"/></g>
 </svg></div>
<div id="mapdim" style="position:absolute;inset:0;background:#030A12;opacity:0"></div>
<div style="position:absolute;inset:0;background:rgba(4,30,48,.12);mix-blend-mode:multiply"></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(3,10,18,.78) 0%,rgba(3,10,18,.15) 28%,rgba(3,10,18,.0) 50%,rgba(3,10,18,.25) 75%,rgba(3,10,18,.85) 100%)"></div>
<div id="places"></div><div id="pins"></div>
${credit ? `<div style="position:absolute;right:40px;bottom:44px;color:rgba(255,255,255,.6);font-family:SS;font-weight:600;font-size:22px">${credit}</div>` : ''}`;
  mapimg = document.getElementById('mapimg'); rlayer = document.getElementById('rlayer'); rbase = document.getElementById('rbase');
  rg = [3, 2, 1, 0].map(i => document.getElementById('rg' + i)); trainEl = document.getElementById('train');
  RL = ROUTE.length ? rg[2].getTotalLength() : 1;
  // --- thời điểm tàu đi qua từng ghim (theo chiều dài đường) ---
  const pinFrac = {};
  for (const k of Object.keys(PINS)) {
    let best = 0, bd = 1e18;
    if (ROUTE.length) for (let i = 0; i <= 600; i++) { const q = rg[2].getPointAtLength(RL * i / 600); const d = (q.x - PINS[k][0]) ** 2 + (q.y - PINS[k][1]) ** 2; if (d < bd) { bd = d; best = i / 600; } }
    pinFrac[k] = best;
    pinT[k] = TRAIN ? TRAIN.t0 + best * (TRAIN.t1 - TRAIN.t0) : -1;
  }
  // --- nhãn ghim: {id:[[a,b] | {pass:[da,db]}]} ---
  for (const k of Object.keys(PINS)) {
    LABWIN[k] = ((cfg.labwin || {})[k] || []).map(w => Array.isArray(w) ? w : [pinT[k] + w.pass[0], pinT[k] + w.pass[1]]);
  }
  for (const [k, [x, y, l, side, ldy, ldx, dot]] of Object.entries(PINS)) {
    const d = document.createElement('div'); d.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0'; const right = side === 'R';
    d.innerHTML = `<div class="ring" style="position:absolute;border:5px solid #05F4E8;border-radius:50%"></div>
 <div class="core" style="position:absolute;border-radius:50%;background:#05F4E8;box-shadow:0 0 30px #05F4E8,0 0 8px #fff;display:flex;align-items:center;justify-content:center;color:#06121C;font-family:SS;font-weight:900"><span>${dot ? '' : k}</span></div>
 <div class="lab" style="position:absolute;top:${-34 + ldy}px;${right ? `left:${60 + ldx}px` : `right:${60 + ldx}px`};white-space:nowrap;background:rgba(6,18,28,.88);border:3px solid #05F4E8;border-radius:14px;padding:8px 20px;color:#fff;font-family:SS;font-weight:900;font-size:34px;box-shadow:0 10px 30px rgba(0,0,0,.5)"><span style="display:inline-block;transform:scaleX(.86);transform-origin:${right ? 'left' : 'right'}">${l}</span></div>`;
    document.getElementById('pins').appendChild(d); pinEls[k] = d;
  }
  // --- nhãn địa danh: [tên, lat, lon, sMin, sMax] — chỉ hiện khi scale camera nằm trong [sMin,sMax] ---
  placeEls = (cfg.places || []).map(([n, la, lo, smin, smax]) => {
    const d = document.createElement('div'); const [x, y] = geo(la, lo);
    d.style.cssText = 'position:absolute;left:0;top:0;white-space:nowrap;color:rgba(255,255,255,.78);font-family:SS;font-weight:700;font-size:26px;letter-spacing:4px;text-shadow:0 2px 10px #000;transform-origin:0 0';
    d.textContent = n; document.getElementById('places').appendChild(d); return { d, x, y, smin, smax };
  });
  // --- vòng xung (radar): {lat,lon,r(px ảnh nền),t0,t1,col} ---
  RINGS = (cfg.rings || []).map(r => ({ ...r, c: geo(r.lat, r.lon), r: r.km ? kmToPx(r.km, r.lat) : r.r, col: r.col || '#FFE600' }));
  const ringG = document.getElementById('rings'), NS = 'http://www.w3.org/2000/svg';
  const mk = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); ringG.appendChild(e); return e; };
  for (const R of RINGS) {
    if (R.static) {                              // vòng bán kính cố định: nét đứt + nền mờ + đường bán kính + nhãn
      R.base = mk('circle', { cx: R.c[0], cy: R.c[1], fill: R.col, 'fill-opacity': 0.06, stroke: R.col, 'stroke-linecap': 'round' });
      R.spoke = mk('line', { x1: R.c[0], y1: R.c[1], stroke: R.col, 'stroke-linecap': 'round' });
      if (R.label) { R.lab = document.createElement('div'); R.lab.style.cssText = 'position:absolute;left:0;top:0;white-space:nowrap;background:#FFE600;color:#06121C;font-family:SS;font-weight:900;font-size:34px;padding:6px 20px;border-radius:30px;box-shadow:0 8px 24px rgba(0,0,0,.5);transform-origin:0 0'; R.lab.innerHTML = `<span style="display:inline-block;transform:scaleX(.86)">${R.label}</span>`; document.getElementById('places').appendChild(R.lab); }
    }
    R.els = [0, 1, 2].map(() => mk('circle', { cx: R.c[0], cy: R.c[1], fill: 'none', stroke: R.col }));
  }
  DIM = cfg.dim || [];
  // --- vùng khu vực: {name,kind|color,pts:[[lat,lon],...],t0,t1,anchor:[lat,lon],dx,lead,smin,smax} ---
  const zonesG = document.getElementById('zones'), places = document.getElementById('places');
  const mkz = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); zonesG.appendChild(e); return e; };
  ZONES = (cfg.zones || []).map(z => {
    const pts = z.pts.map(p => geo(p[0], p[1])), col = z.color || ZCOL[z.kind] || '#FFE600', d = 'M' + pts.map(p => p.join(',')).join(' L') + ' Z';
    const an = z.anchor ? geo(z.anchor[0], z.anchor[1]) : [pts.reduce((a, p) => a + p[0], 0) / pts.length, pts.reduce((a, p) => a + p[1], 0) / pts.length];
    const R = { z, col, an, fill: mkz('path', { d, fill: col, 'fill-opacity': 0, stroke: 'none' }), glow: mkz('path', { d, fill: 'none', stroke: col, 'stroke-linejoin': 'round', pathLength: 1 }), line: mkz('path', { d, fill: 'none', stroke: col, 'stroke-linejoin': 'round', pathLength: 1 }) };
    const lead = z.lead === undefined ? 110 : z.lead, dx = z.dx || 0, w = document.createElement('div');
    w.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0';
    w.innerHTML = `<svg width="1" height="1" style="position:absolute;left:0;top:0;overflow:visible"><line x1="0" y1="0" x2="${dx}" y2="${-lead}" stroke="${col}" stroke-width="3"/><circle cx="0" cy="0" r="7" fill="${col}" stroke="#fff" stroke-width="2"/></svg>
<div class="zcard" style="position:absolute;left:${dx}px;top:${-lead}px;transform:translate(-50%,-100%);background:#fff;border-radius:10px;border-left:9px solid ${col};padding:7px 20px 7px 16px;box-shadow:0 10px 30px rgba(0,0,0,.5);white-space:nowrap">
<div style="font-family:SS;font-weight:700;font-size:15px;letter-spacing:2px;color:${col};line-height:1">${z.tag || 'KHU VỰC'}</div><div style="font-family:SS;font-weight:900;font-size:30px;color:#0B0F14;line-height:1.15">${z.name}</div></div>`;
    places.appendChild(w); R.card = w; R.cardEl = w.querySelector('.zcard'); return R;
  });
  // --- thanh tiến độ km tỷ lệ thật (HUD đáy): {title,subtitle,total,stops:[km...],t0,t1,x0,x1,y} ---
  KM = cfg.kmbar || null;
  if (KM) {
    const x0 = KM.x0 || 90, x1 = KM.x1 || 990, y = KM.y || 1590, tot = KM.total;
    const k = document.createElement('div'); k.style.cssText = 'position:absolute;inset:0;opacity:0;pointer-events:none';
    k.innerHTML = `<div style="position:absolute;left:0;right:0;bottom:0;height:640px;background:linear-gradient(180deg,rgba(3,10,18,0),rgba(3,10,18,.9) 55%)"></div>
<div style="position:absolute;left:0;width:1080px;top:${y - 156}px;text-align:center;color:var(--cy);font-family:SS;font-weight:700;font-size:26px;letter-spacing:4px;text-shadow:0 2px 10px #000">${KM.subtitle || ''}</div>
<div style="position:absolute;left:0;width:1080px;top:${y - 124}px;text-align:center;color:#fff;font-family:SS;font-weight:900;font-size:56px;text-transform:uppercase;text-shadow:0 3px 14px #000"><span style="display:inline-block;transform:scaleX(.86)">${KM.title || ''}</span></div>
<div style="position:absolute;left:${x0}px;width:${x1 - x0}px;top:${y - 2}px;height:4px;background:rgba(255,255,255,.35);border-radius:2px"></div>
<div id="kmfill" style="position:absolute;left:${x0}px;top:${y - 3}px;height:6px;width:0;background:var(--cy);border-radius:3px;box-shadow:0 0 16px var(--cy)"></div>
${(KM.stops || []).map(v => `<div class="kmdot" data-km="${v}" style="position:absolute;left:${x0 + (x1 - x0) * v / tot - 8}px;top:${y - 8}px;width:16px;height:16px;border-radius:50%;box-sizing:border-box;background:#06121C;border:3px solid #fff"></div>`).join('')}
<div id="kmhead" style="position:absolute;left:0;top:${y - 11}px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 0 18px var(--cy),0 0 4px #fff"></div>
<div id="kmtxt" style="position:absolute;left:0;width:200px;top:${y + 22}px;text-align:center;color:#fff;font-family:SS;font-weight:700;font-size:28px;text-shadow:0 2px 10px #000"></div>`;
    document.getElementById('mapwrap').appendChild(k); kmEl = { root: k, fill: k.querySelector('#kmfill'), head: k.querySelector('#kmhead'), txt: k.querySelector('#kmtxt'), dots: [...k.querySelectorAll('.kmdot')], x0, x1, tot };
  }
  // --- logo cố định (góc trên phải): {src,w,h,radius,bg,pad}; nhãn địa điểm/demo tự lùi sang trái ---
  if (cfg.logo) {
    const L = cfg.logo, w = L.w || 120, h = L.h || w, lg = document.createElement('div');
    lg.id = 'logo'; lg.style.cssText = `position:absolute;right:54px;top:56px;width:${w}px;height:${h}px;border-radius:${L.radius === undefined ? 22 : L.radius}px;background:${L.bg || '#fff'};padding:${L.pad === undefined ? 10 : L.pad}px;box-sizing:border-box;box-shadow:0 8px 24px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center`;
    lg.innerHTML = `<img src="${L.src}" style="max-width:100%;max-height:100%;object-fit:contain">`; document.getElementById('stage').appendChild(lg);
    const im = lg.querySelector('img'); READY_LIST.push(new Promise(r => { im.onload = r; im.onerror = r; }));
    document.getElementById('loc').style.right = (54 + w + 24) + 'px'; document.getElementById('demo').style.right = (54 + w + 24) + 'px';
  }
  KEYS = ((cfg.cam || {}).keys || []).map(([t, tg, s]) => { const p = target(tg); return [t, p[0], p[1], s]; });
  // --- nền ---
  bgEls = TL.bgs.map(([src, i, o, dir]) => {
    let el = null;
    if (src === 'DARK') { el = document.createElement('div'); el.className = 'bg'; el.innerHTML = '<div class="dark"></div><div class="grid"></div>'; document.getElementById('bgs').appendChild(el); }
    return { el, src, i, o, dir };
  });
  const fxEl = document.getElementById('fx');
  for (let i = 0; i < 40; i++) { const d = document.createElement('div'); d.className = 'dot'; fxEl.appendChild(d); dots.push({ d, x: (i * 197) % 1080, y: (i * 331) % 1920, s: .3 + ((i * 7) % 10) / 10, sz: 4 + (i % 4) * 3 }); }
}

/* ---------- camera ---------- */
const trainP = t => TRAIN ? clamp((t - TRAIN.t0) / (TRAIN.t1 - TRAIN.t0)) : 0;
const rpt = p => rg[2].getPointAtLength(RL * clamp(p));
// cam: {push:0.10, follow:[tStart,tEnd,settleSec,scale], keys:[[t,đích,scale],...]}
function camAt(t) {
  const c = CFG.cam || {}, push = c.push === undefined ? 0.10 : c.push, f = c.follow;
  const t1 = f ? f[0] : (KEYS.length ? KEYS[0][0] : 1);
  if (t < t1) { const k = lin(t, 0, t1); return [OVC[0], OVC[1], OVS * (1 + push * k)]; }       // 1) toàn cảnh, đẩy chậm
  if (f && t < f[1]) {                                                                          // 2) bám theo tàu
    const p = trainP(t), q = rpt(Math.min(1, p + 0.02)), k = eIO(lin(t, f[0], f[0] + f[2])), s0 = OVS * (1 + push), s1 = f[3];
    return [OVC[0] + (q.x - OVC[0]) * k, OVC[1] + (q.y - OVC[1]) * k, s0 * Math.pow(s1 / s0, k)];
  }
  for (let i = 0; i < KEYS.length - 1; i++) {                                                   // 3) keyframe: vị trí easeInOut, scale nội suy mũ
    const a = KEYS[i], b = KEYS[i + 1];
    if (t >= a[0] && t <= b[0]) { const k = eIO(lin(t, a[0], b[0])); return [a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k, a[3] * Math.pow(b[3] / a[3], k)]; }
  }
  if (!KEYS.length) return [OVC[0], OVC[1], OVS];
  return t < KEYS[0][0] ? KEYS[0].slice(1) : KEYS[KEYS.length - 1].slice(1);
}

function renderMap(t) {
  const [cx, cy, s] = camAt(t), ox = 540 - cx * s, oy = 1000 - cy * s;                         // tâm khung dọc đặt ở y=1000
  const tf = `translate(${ox}px,${oy}px) scale(${s})`; mapimg.style.transform = tf; rlayer.style.transform = tf;
  const dop = clamp((s - 1.05) / 0.45); for (const im of document.querySelectorAll('.det')) im.style.opacity = dop;   // ảnh chi tiết hiện dần khi zoom sâu
  let dm = 0; for (const [a, b] of DIM) dm = Math.max(dm, Math.min(lin(t, a, a + 0.4), 1 - lin(t, b - 0.3, b)));
  document.getElementById('mapdim').style.opacity = dm * 0.38;                                  // tối bản đồ khi có thẻ/số liệu đè lên
  for (const p of placeEls) { p.d.style.transform = `translate(${p.x * s + ox}px,${p.y * s + oy}px) translate(-50%,-50%)`; p.d.style.opacity = (s >= p.smin && s <= p.smax) ? 0.85 : 0; }
  // tuyến: nét mờ có dash chạy (teaser) + nét neon vẽ dần theo tàu (4 lớp để giả glow, không dùng filter cho nhẹ)
  const p = trainP(t), sw = w => w / s;
  rbase.setAttribute('stroke-width', sw(5)); rbase.setAttribute('stroke-dasharray', `${sw(16)} ${sw(12)}`); rbase.setAttribute('stroke-dashoffset', -t * sw(30));
  rbase.style.opacity = lin(t, 0.6, 1.6) * (p >= 1 ? 0 : 1);
  const wd = [26, 14, 6, 2.5]; rg.forEach((e, i) => { e.setAttribute('stroke-width', sw(wd[i])); e.setAttribute('stroke-dasharray', `${RL * p} ${RL * 3}`); e.style.display = p > 0 ? '' : 'none'; });
  // tàu: kích thước cố định theo màn hình (scale 1/s), xoay theo hướng đường
  const tv = !!TRAIN && ROUTE.length > 0 && t >= TRAIN.t0 - 0.3 && t < TRAIN.t1 + 1.2; trainEl.style.display = tv ? '' : 'none';
  if (tv) {
    const q = rpt(p), q2 = rpt(Math.min(1, p + 0.004)), q1 = rpt(Math.max(0, p - 0.004)), ang = Math.atan2(q2.y - q1.y, q2.x - q1.x) * 180 / Math.PI;
    trainEl.setAttribute('transform', `translate(${q.x},${q.y}) rotate(${ang}) scale(${1 / s})`);
    trainEl.style.opacity = lin(t, TRAIN.t0 - 0.3, TRAIN.t0) * (1 - lin(t, TRAIN.t1 + 0.3, TRAIN.t1 + 1.2));
  }
  for (const R of RINGS) {
    const on = t >= R.t0 && t < R.t1, vis = on ? lin(t, R.t0, R.t0 + 0.5) * (1 - lin(t, R.t1 - 0.4, R.t1)) : 0;
    if (R.static) {
      R.base.style.display = R.spoke.style.display = on ? '' : 'none';
      R.base.setAttribute('r', R.r); R.base.setAttribute('stroke-width', sw(4)); R.base.setAttribute('stroke-dasharray', `${sw(26)} ${sw(16)}`); R.base.style.opacity = vis;
      const a = (R.labAng === undefined ? -35 : R.labAng) * Math.PI / 180, ex = R.c[0] + R.r * Math.cos(a), ey = R.c[1] + R.r * Math.sin(a);
      R.spoke.setAttribute('x2', ex); R.spoke.setAttribute('y2', ey); R.spoke.setAttribute('stroke-width', sw(3)); R.spoke.setAttribute('stroke-dasharray', `${sw(12)} ${sw(10)}`); R.spoke.style.opacity = vis * 0.9;
      if (R.lab) { const lx = clamp(ex * s + ox, 130, 950), ly = clamp(ey * s + oy, 260, 1640); R.lab.style.transform = `translate(${lx}px,${ly}px) translate(-50%,-50%)`; R.lab.style.opacity = on ? vis : 0; }   // nhãn luôn nằm trong khung
    }
    R.els.forEach((c, i) => {                    // sóng xung: ring thường nở tới 1,2R; ring static nở đúng tới R
      if (!on) { c.style.display = 'none'; return; } c.style.display = '';
      const ph = (((t - R.t0) * 0.55 + i / 3) % 1); c.setAttribute('r', R.static ? R.r * (0.15 + 0.85 * ph) : R.r * (0.25 + 0.95 * ph)); c.setAttribute('stroke-width', sw(5));
      c.style.opacity = (1 - ph) * vis;
    });
  }
  // vùng khu vực: viền vẽ dần + nền mờ + thẻ trắng có sọc màu và đường dẫn
  for (const R of ZONES) {
    const z = R.z, on = t >= z.t0 && t < z.t1 + 0.1, prog = eOut(lin(t, z.t0, z.t0 + 0.8)), out = 1 - lin(t, z.t1 - 0.4, z.t1), v = on ? out : 0;
    R.line.style.display = R.glow.style.display = R.fill.style.display = on ? '' : 'none';
    R.line.setAttribute('stroke-width', sw(4)); R.line.setAttribute('stroke-dasharray', `${prog} 1`); R.line.style.opacity = v;
    R.glow.setAttribute('stroke-width', sw(11)); R.glow.setAttribute('stroke-dasharray', `${prog} 1`); R.glow.style.opacity = v * 0.35;
    R.fill.setAttribute('fill-opacity', 0.13 * prog); R.fill.style.opacity = v;
    const showCard = on && (z.smin === undefined || s >= z.smin) && (z.smax === undefined || s <= z.smax);
    R.card.style.display = showCard ? '' : 'none';
    if (showCard) { const k = t - z.t0 - 0.3, x = eBack(clamp(k / 0.35)); R.card.style.transform = `translate(${R.an[0] * s + ox}px,${R.an[1] * s + oy}px)`; R.cardEl.style.transform = `translate(-50%,-100%) scale(${0.8 + 0.2 * x})`; R.card.style.opacity = clamp(k / 0.15) * out; }
  }
  // thanh km: đầu thanh chạy theo tàu; chấm ga sáng cyan khi tàu đã qua
  if (KM) {
    const a = KM.t0 === undefined ? 0 : KM.t0, b = KM.t1 === undefined ? TL.total : KM.t1, vis = lin(t, a, a + 0.4) * (1 - lin(t, b - 0.4, b));
    kmEl.root.style.opacity = vis;
    if (vis > 0) {
      const km = KM.total * (TRAIN ? trainP(t) : lin(t, a, b)), x = kmEl.x0 + (kmEl.x1 - kmEl.x0) * km / KM.total;
      kmEl.fill.style.width = (x - kmEl.x0) + 'px'; kmEl.head.style.left = (x - 11) + 'px';
      kmEl.txt.style.left = (clamp(x, kmEl.x0 + 30, kmEl.x1 - 30) - 100) + 'px'; kmEl.txt.textContent = fmtNum(km, ' km', false, 1);
      for (const d of kmEl.dots) { const lit = +d.dataset.km <= km + 0.05; d.style.background = lit ? '#05F4E8' : '#06121C'; d.style.borderColor = lit ? '#05F4E8' : '#fff'; }
    }
  }
  // ghim: xám trước khi tàu qua, cyan + xung khi tàu tới, nhãn theo cửa sổ thời gian
  const tEnd = TRAIN ? TRAIN.t1 : -1;
  for (const k of Object.keys(PINS)) {
    const d = pinEls[k], [x, y] = PINS[k]; d.style.transform = `translate(${x * s + ox}px,${y * s + oy}px)`;
    const lit = t >= pinT[k] || t >= tEnd, act = TRAIN ? (t >= pinT[k] && t < pinT[k] + 1.3) : false;
    const inA = eBack(lin(t, pinT[k], pinT[k] + 0.4)), pulse = act ? (1 + 0.18 * Math.sin((t - pinT[k]) * 8)) : 1;
    const cr = (act ? 30 * pulse * (0.6 + 0.4 * inA) : (lit ? 20 : 14)) * (PINS[k][6] ? 0.55 : 1), core = d.querySelector('.core');
    core.style.width = core.style.height = (2 * cr) + 'px'; core.style.left = core.style.top = (-cr) + 'px'; core.style.fontSize = (cr * 1.1) + 'px';
    core.style.background = lit ? '#05F4E8' : 'rgba(150,190,200,.75)';
    const ring = d.querySelector('.ring'), ph = ((t - pinT[k]) * 70) % 80, rr = act ? 34 + ph : 0;
    ring.style.width = ring.style.height = (2 * rr) + 'px'; ring.style.left = ring.style.top = (-rr - 5) + 'px'; ring.style.opacity = act ? 1 - ph / 80 : 0;
    let lo = 0; for (const [a, b] of LABWIN[k]) lo = Math.max(lo, Math.min(lin(t, a, a + 0.3), 1 - lin(t, b - 0.3, b)));
    d.querySelector('.lab').style.opacity = lo; d.style.opacity = (s < 0.2) ? 0 : 1;
  }
}

/* ---------- phần tử chữ / thẻ (gọi trong scene.js) ---------- */
const E = []; const els = document.getElementById('els');
// line(text, cls 'w'|'c'|'r', cap(px chiều cao chữ hoa), y(tâm), tin, tout, {anim:'track'|'hero'|'count'|'pulse', count:[from,to,suffix,plus,decimals], sfx, g})
// count: số có dấu chấm ngàn (2.027) KHÔNG dùng cho năm — dùng line tĩnh. decimals=1 cho '19,7'.
function line(text, cls, cap, y, tin, tout, opt = {}) {
  const el = document.createElement('div'); el.className = 'line ' + cls; const fs = cap / 0.66;
  el.style.fontSize = fs + 'px'; el.style.top = (y - fs * 0.27 - cap / 2) + 'px'; el.style.height = fs + 'px'; el.style.lineHeight = fs + 'px';
  el.innerHTML = `<span>${text}</span>`; els.appendChild(el); E.push({ type: 'line', el, tin, tout, anim: opt.anim || 'track', count: opt.count, cap, y, fs });
  if (opt.sfx !== false) sfx(tin, opt.sfx || (cls === 'c' ? 'ting' : 'pop'), opt.g || 0); return el;
}
function paper(src, tag, y, w, tin, tout, rot = -2, opt = {}) {          // thẻ ảnh báo trắng + nhãn nguồn
  const el = document.createElement('div'); el.className = 'paper'; el.style.width = w + 'px'; el.style.marginLeft = (-w / 2 - 18) + 'px'; el.style.top = y + 'px';
  el.innerHTML = `<div class="tag ${opt.dark ? 'dark2' : ''}">${tag}</div><img src="${src}">`; els.appendChild(el); E.push({ type: 'paper', el, tin, tout, rot }); sfx(tin, 'whoosh', -2); sfx(tin + 0.32, 'shutter', -3); return el;
}
function chip(icon, text, y, tin, tout) {                                 // viên thuốc trượt từ trái
  const el = document.createElement('div'); el.className = 'chip'; el.style.top = y + 'px';
  el.innerHTML = `<div class="ic">${icon}</div><span style="display:inline-block;transform:scaleX(.86);transform-origin:left">${text}</span>`; els.appendChild(el); E.push({ type: 'chip', el, tin, tout }); sfx(tin, 'notify', -1); return el;
}
function src(text, y, tin, tout) { const el = document.createElement('div'); el.className = 'src'; el.style.top = y + 'px'; el.textContent = text; els.appendChild(el); E.push({ type: 'fade', el, tin, tout }); }
function note(text, y, tin, tout) { const el = document.createElement('div'); el.className = 'note'; el.style.top = y + 'px'; el.textContent = text; els.appendChild(el); E.push({ type: 'fade', el, tin, tout }); }
// captions([[t0,t1,'câu có *từ nhấn*'],...], {y:1560,size:50}) — phụ đề đốt cứng, vùng an toàn y≈1560–1670. Tạo danh sách từ lời đọc bằng scripts/make_captions.py.
function captions(list, o = {}) {
  const y = o.y === undefined ? 1560 : o.y, fs = o.size || 50;
  for (const [t0, t1, text] of list) {
    const el = document.createElement('div'); el.className = 'cap'; el.style.top = y + 'px'; el.style.fontSize = fs + 'px';
    el.innerHTML = String(text).replace(/\*(.+?)\*/g, '<b>$1</b>'); els.appendChild(el); E.push({ type: 'cap', el, tin: t0, tout: t1 });
  }
}
// clip(mẫuTênFile, soKhung, fps, tin, tout, {x,y,w,h,radius,border,shadow,fit:'cover'|'contain',loop,from,fade,start})
// Ghép cảnh quay (người dẫn, cảnh trám) bằng CHUỖI ẢNH đã tách sẵn: ffmpeg -i in.mp4 -vf "fps=30,scale=1080:-2" clips/a/%05d.jpg
// (tách khung bằng ffmpeg để render xác định từng khung; âm thanh của clip trộn riêng ở audio.py/timeline vo). Mẫu tên: 'clips/a/%05d.jpg'.
function clip(pat, n, fps, tin, tout, o = {}) {
  const w = o.w || 1080, h = o.h || 1920, cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  cv.style.cssText = `position:absolute;left:${o.x || 0}px;top:${o.y || 0}px;width:${w}px;height:${h}px;${o.radius ? `border-radius:${o.radius}px;` : ''}${o.border ? `border:${o.border};box-sizing:border-box;` : ''}${o.shadow ? 'box-shadow:0 30px 80px rgba(0,0,0,.55);' : ''}`;
  const imgs = [];
  for (let i = 1; i <= n; i++) { const im = new Image(); READY_LIST.push(new Promise(r => { im.onload = r; im.onerror = r; })); im.src = pat.replace(/%0?(\d*)d/, (m, d) => String(i + (o.start || 0)).padStart(+d || 0, '0')); imgs.push(im); }
  els.appendChild(cv); E.push({ type: 'clip', el: cv, tin, tout, imgs, fps, n, loop: o.loop !== false, fit: o.fit || 'cover', ctx: cv.getContext('2d'), w, h, fade: o.fade === undefined ? 0.2 : o.fade, from: o.from || 0 });
  return cv;
}
function raw(html, tin, tout, type = 'fade') { const d = document.createElement('div'); d.innerHTML = html; const el = d.firstElementChild; els.appendChild(el); E.push({ type, el, tin, tout }); return el; }

// dec = số chữ số thập phân (mặc định 0). Định dạng Việt: 1.234,5 — tự viết để không phụ thuộc ICU của Chromium.
function fmtNum(v, suf, plus, dec = 0) {
  const f = Math.abs(v).toFixed(dec), [ip, fp] = f.split('.'), neg = v < 0 && +f > 0;
  return (neg ? '-' : (plus && +f > 0 ? '+' : '')) + ip.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (fp ? ',' + fp : '') + suf;
}
// thu nhỏ dòng nào rộng > 950px (render.js gọi 1 lần sau khi nạp trang)
window.fit = function () {
  for (const e of E) {
    if (e.type !== 'line') continue; const el = e.el, sp = el.querySelector('span'); el.style.display = ''; const txt = sp.textContent;
    if (e.count) sp.textContent = fmtNum(e.count[1], e.count[2], e.count[3], e.count[4]);
    const w = sp.getBoundingClientRect().width; sp.textContent = txt;
    if (w > 950) { const fs = e.fs * 950 / w; el.style.fontSize = fs + 'px'; el.style.height = fs + 'px'; el.style.lineHeight = fs + 'px'; el.style.top = (e.y - fs * 0.27 - fs * 0.66 / 2) + 'px'; }
    el.style.display = 'none';
  }
};

window.render = function (t) {
  for (const b of bgEls) {
    if (!b.el) continue; const op = Math.min(lin(t, b.i, b.i + 0.35), 1 - lin(t, b.o - 0.35, b.o));
    b.el.style.opacity = op; if (op <= 0) { b.el.style.display = 'none'; continue; } b.el.style.display = 'block';
    const g = b.el.querySelector('.grid'); if (g) g.style.transform = `translateY(${(t * 30) % 90}px)`;
  }
  const mw = document.getElementById('mapwrap'); let mop = 0;
  for (const b of bgEls) { if (b.src !== 'MAP') continue; mop = Math.max(mop, Math.min(lin(t, b.i, b.i + 0.3), 1 - lin(t, b.o - 0.3, b.o))); }
  mw.style.opacity = mop; mw.style.display = mop > 0 ? '' : 'none'; if (mop > 0) renderMap(t);
  const dop = Math.max(mop * 0.6, ...bgEls.filter(b => b.src === 'DARK').map(b => Math.min(lin(t, b.i, b.i + .3), 1 - lin(t, b.o - .3, b.o))));
  for (const p of dots) { p.d.style.opacity = .45 * dop; const y = (p.y - t * 40 * p.s) % 1920; p.d.style.transform = `translate(${p.x}px,${y < 0 ? y + 1920 : y}px)`; p.d.style.width = p.d.style.height = p.sz + 'px'; }
  for (const e of E) {
    const el = e.el; if (t < e.tin || t >= e.tout + 0.2) { el.style.display = 'none'; continue; } el.style.display = '';
    const k = t - e.tin, ko = lin(t, e.tout - 0.12, e.tout); let op = 1 - ko;
    if (e.type === 'line') {
      const sp = el.querySelector('span');
      if (e.anim === 'track') { const x = eExpo(clamp(k / 0.45)); sp.style.letterSpacing = ((1 - x) * 0.55) + 'em'; el.style.filter = `blur(${(1 - x) * 10}px)`; op *= clamp(k / 0.15); el.style.transform = ''; }
      else if (e.anim === 'hero' || e.anim === 'count') {
        const x = eExpo(clamp(k / 0.35)); el.style.transform = `scale(${1.7 - 0.7 * x})`; el.style.filter = `blur(${(1 - x) * 8}px)`; op *= clamp(k / 0.12); sp.style.letterSpacing = '0';
        if (e.count) { const [a, b, suf] = e.count; const c = eOut(clamp(k / 0.7)); sp.textContent = fmtNum(a + (b - a) * c, suf, e.count[3], e.count[4]); }
      } else if (e.anim === 'pulse') { const s = 1 + 0.06 * Math.sin(k * 9); el.style.transform = `scale(${s})`; op *= clamp(k / 0.2) * (0.75 + 0.25 * Math.sin(k * 9)); }
      el.style.opacity = op;
    } else if (e.type === 'paper') {
      const x = eBack(clamp(k / 0.55)), y = (1 - x) * 700, r = e.rot + (1 - x) * 10, s = (0.88 + 0.12 * x) * (1 + 0.03 * clamp(k / 4)), outx = -eIO(ko) * 1100;
      el.style.transform = `translate(${outx}px,${y}px) rotate(${r}deg) scale(${s})`; el.style.opacity = clamp(k / 0.15) * (1 - ko * 0.3);
    } else if (e.type === 'cap') {
      const x = eBack(clamp(k / 0.14)); el.style.transform = `scale(${0.92 + 0.08 * x})`; el.style.opacity = clamp(k / 0.06) * (1 - ko);
    } else if (e.type === 'clip') {
      let idx = Math.floor((k + e.from) * e.fps); idx = e.loop ? ((idx % e.n) + e.n) % e.n : Math.min(e.n - 1, idx);
      const im = e.imgs[idx], c = e.ctx; c.clearRect(0, 0, e.w, e.h);
      if (im && im.naturalWidth) { const sc = (e.fit === 'contain' ? Math.min : Math.max)(e.w / im.naturalWidth, e.h / im.naturalHeight), dw = im.naturalWidth * sc, dh = im.naturalHeight * sc; c.drawImage(im, (e.w - dw) / 2, (e.h - dh) / 2, dw, dh); }
      el.style.opacity = clamp(k / e.fade) * (1 - lin(t, e.tout - e.fade, e.tout));
    } else if (e.type === 'chip') { const x = eBack(clamp(k / 0.45)); el.style.transform = `translateX(${(1 - x) * -500}px)`; el.style.opacity = clamp(k / 0.12) * (1 - ko); }
    else if (e.type === 'pop') { const x = eBack(clamp(k / 0.5)), s = (0.3 + 0.7 * x) * (1 + 0.03 * Math.sin(Math.max(0, k - 0.5) * 6)); el.style.transform = `scale(${s})`; el.style.opacity = clamp(k / 0.1) * (1 - ko); }
    else el.style.opacity = clamp(k / 0.3) * (1 - ko);
  }
  let fl = 0; for (const [a, d, m] of FX.flash) if (t >= a && t < a + d) fl = Math.max(fl, m * (1 - (t - a) / d)); document.getElementById('flash').style.opacity = fl;
  let gl = 0; for (const [a, d] of FX.glow) if (t >= a && t < a + d) gl = Math.max(gl, Math.sin(Math.PI * (t - a) / d) * 0.8); document.getElementById('glow').style.opacity = gl;
  const sw = document.getElementById('sweep'); let swo = 0, swx = -400; for (const [a] of FX.sweep) if (t >= a + 0.4 && t < a + 1.2) { const p = (t - a - 0.4) / 0.8; swo = Math.sin(Math.PI * p); swx = -300 + p * 1700; } sw.style.opacity = swo; sw.style.left = swx + 'px';
  document.getElementById('prog').style.width = (t / TL.total * 1080) + 'px';
  document.getElementById('stage').style.opacity = 1 - lin(t, TL.total - 0.6, TL.total);
};
