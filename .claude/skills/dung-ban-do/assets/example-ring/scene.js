/* scene.js — Sân bay Long Thành, vòng bán kính 20 km. Ví dụ cho cảnh KHÔNG có tuyến/tàu và KHÔNG có giọng đọc (timeline.js: vo: []).
 * Dùng: rings[{km, static:true, label}] (vòng cố định + nhãn), pins[].dy (dời nhãn), pins[].dot (ghim nhỏ không số), count có thập phân.
 * Chuẩn bị ảnh nền:
 *   python3 scripts/plan_map.py --route "<CHÍNH CÁC GHIM, lat,lon;...>" --follow-scale 0 --extra "<điểm zoom sâu>" --extra-scale 2.2 --ring "lat,lon,20"
 *   rồi chạy lệnh fetch_map.py nó in ra (đặt --sea đúng hướng biển: ở đây biển ở phía nam => --sea bottom).
 * Toạ độ trong ví dụ là XẤP XỈ (sân bay ±500 m, ba thành phố lấy khu trung tâm) — kiểm tra lại khi dùng thật.
 * Không có route => engine lấy tâm toàn cảnh là tâm bbox các ghim (= ov.center plan_map in ra nếu bạn truyền các ghim vào --route). */
window.SCENE = {
  brand: { t1: 'SÂN BAY LONG THÀNH', t2: 'VÙNG PHỦ SÓNG 20 KM', loc: 'ĐỒNG NAI · 2026' },
  pins: [
    { id: 1, lat: 10.7726, lon: 107.0450, label: 'SÂN BAY LONG THÀNH', side: 'L', dy: 110 },  // side 'L' vì ghim ở nửa phải khung (nhãn không tự co vào mép); dy dời nhãn xuống để khỏi đè nhãn TP.HCM
    { id: 2, lat: 10.7725, lon: 106.6980, label: 'TP.HCM', side: 'R' },
    { id: 3, lat: 10.9447, lon: 106.8243, label: 'BIÊN HÒA', side: 'R' },
    { id: 4, lat: 10.3460, lon: 107.0843, label: 'VŨNG TÀU', side: 'L' },
    { id: 5, lat: 10.60, lon: 107.05, label: '', dot: true }                                 // chấm nhỏ, không số; không khai labwin => không bao giờ hiện nhãn (dùng cho ga phụ)
  ],
  route: [], places: [],
  rings: [{ lat: 10.7726, lon: 107.0450, km: 20, static: true, label: '20 KM', labAng: -40, t0: 0.8, t1: 10 }],   // km -> px tự tính theo vĩ độ
  train: null, ov: { scale: 0.305 },   // lấy từ plan_map.py (ov.scale)
  labwin: { 1: [[0.5, 10]], 2: [[0.5, 10]], 3: [[0.5, 10]], 4: [[0.5, 10]] },   // KHÔNG có tàu => nhãn chỉ hiện khi khai labwin
  dim: [],
  cam: { push: 0.06, keys: [[0.1, 'OV', 0.31], [1.4, 'OV', 0.33], [4.4, 1, 1.9], [6, 1, 2.2], [9.4, 'OV', 0.31]] }   // vào sân bay rồi ra
};
initEngine(window.SCENE);
// Tiêu đề: brand ở góc trên trái đã đủ; chừa vùng y≈150–400 trống vì chip "20 KM" bị kẹp vào đó khi zoom sâu (đổi labAng nếu cần).
// Ví dụ số thập phân (bỏ comment để thử): line('19,7 KM', 'c', 150, 1400, 1.0, 10, { anim: 'count', count: [0, 19.7, ' KM', false, 1] });   // [from,to,suffix,plus,decimals]
