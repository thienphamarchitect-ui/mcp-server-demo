/* scene.js — nội dung riêng của một video. Sao chép file này, sửa SCENE và các dòng bên dưới.
 * Xem assets/example-metro/scene.js để có ví dụ đầy đủ 8 cảnh, và references/engine.md để biết từng tuỳ chọn. */
window.SCENE = {
  brand: { t1: 'TÊN KÊNH', t2: 'DÒNG PHỤ', loc: 'THÀNH PHỐ · 2026', demo: '' },   // demo: 'BẢN DEMO · GIỌNG ĐỌC AI MẪU' nếu dùng giọng AI
  pins: [
    { id: 1, lat: 0, lon: 0, label: 'ĐIỂM ĐẦU', side: 'R' },
    { id: 2, lat: 0, lon: 0, label: 'ĐIỂM CUỐI', side: 'L' }
  ],
  route: [],                       // [[lat,lon],...] đi qua các ghim theo thứ tự; để [] nếu không có tuyến
  places: [],                      // [['TÊN', lat, lon, sMin, sMax], ...]
  rings: [],                       // [{lat,lon,r,t0,t1,col}]
  train: null,                     // {t0,t1} nếu có tàu/đường vẽ dần
  ov: { scale: 0.32 },
  labwin: {},
  dim: [],
  cam: { keys: [] }                // [[t, đích, scale], ...]
};
initEngine(window.SCENE);

// SCENE 1: line(text, 'w'|'c'|'r', cap, y, tin, tout, {anim:'hero'|'count'|'pulse'})  — tin/tout lấy từ mốc giọng đọc
// line('TIÊU ĐỀ', 'w', 66, 420, 0.4, 3.0);
// line('266.000 TỶ', 'c', 210, 620, 1.0, 3.0, {anim:'hero', sfx:'impact', g:-3});
// paper('assets/bai_bao.png', 'TÊN BÁO · NGÀY', 460, 900, 2.0, 6.0);
// chip('◆', 'ĐIỂM NHẤN', 920, 3.0, 6.0);
// src('Nguồn: ...', 1700, 1.0, 6.0);

// Phụ đề từ lời đọc (xem references/engine.md): captions(window.CAPTIONS, {y: 1560});
// Cảnh quay: clip('clips/a/%05d.jpg', soKhung, 30, tin, tout, {x:60, y:520, w:480, h:640, radius:30});

FX.flash = [[0, 0.5, 1]];   // [t, thời lượng, độ sáng tối đa]
FX.glow = [];               // [t, thời lượng]
FX.sweep = [];              // [t] vệt sáng quét qua thẻ báo
