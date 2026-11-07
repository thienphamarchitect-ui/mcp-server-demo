/* scene.js — Sân bay Long Thành, vòng bán kính 20 km. Ví dụ cho cảnh KHÔNG có tuyến/tàu và KHÔNG có giọng đọc (timeline.js: vo: []).
 * Dùng: rings[{km, static:true, label}] (vòng cố định + nhãn), pins[].dy (dời nhãn), pins[].dot (ghim nhỏ không số), count có thập phân.
 * Chuẩn bị ảnh nền:
 *   python3 scripts/plan_map.py --route "<các ghim>" --follow-scale 0 --extra "<điểm zoom sâu>" --extra-scale 2.2 --ring "lat,lon,20"
 *   rồi chạy lệnh fetch_map.py nó in ra (thêm --sea bottom nếu biển ở phía nam).
 * Không có route => engine lấy tâm toàn cảnh là tâm bbox các ghim; muốn ghi đè: ov:{center:[lat,lon],scale}. */
window.SCENE = {
  brand: { t1: 'SÂN BAY LONG THÀNH', t2: 'VÙNG PHỦ SÓNG 20 KM', loc: 'ĐỒNG NAI · 2026' },
  pins: [
    { id: 1, lat: 10.7726, lon: 107.0450, label: 'SÂN BAY LONG THÀNH', side: 'R', dy: 70 },   // dy: dời nhãn xuống 70px để khỏi đè nhãn khác
    { id: 2, lat: 10.7725, lon: 106.6980, label: 'TP.HCM', side: 'R' },
    { id: 3, lat: 10.9447, lon: 106.8243, label: 'BIÊN HÒA', side: 'R' },
    { id: 4, lat: 10.3460, lon: 107.0843, label: 'VŨNG TÀU', side: 'L' },
    { id: 5, lat: 10.60, lon: 107.05, label: '', dot: true }                                 // chấm nhỏ, không số, không nhãn
  ],
  route: [], places: [],
  rings: [{ lat: 10.7726, lon: 107.0450, km: 20, static: true, label: '20 KM', labAng: -40, t0: 0.8, t1: 10 }],   // km -> px tự tính theo vĩ độ
  train: null, ov: { scale: 0.31 },
  labwin: { 1: [[0.5, 10]], 2: [[0.5, 10]], 3: [[0.5, 10]], 4: [[0.5, 10]] },   // KHÔNG có tàu => nhãn chỉ hiện khi khai labwin
  dim: [],
  cam: { push: 0.06, keys: [[0.1, 'OV', 0.31], [1.4, 'OV', 0.33], [4.4, 1, 1.9], [6, 1, 2.2], [9.4, 'OV', 0.31]] }   // vào sân bay rồi ra
};
initEngine(window.SCENE);
line('VÙNG PHỦ SÓNG', 'w', 60, 330, 0.4, 10);
line('19,7 KM', 'c', 150, 1400, 1.0, 10, { anim: 'count', count: [0, 19.7, ' KM', false, 1] });   // [from,to,suffix,plus,decimals]
