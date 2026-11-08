/* scene.js — ví dụ HUD kiểu video mẫu gốc: polygon khu vực + thanh km tỷ lệ thật + logo, trên nền tuyến + tàu.
 * Cộng thêm vào SCENE của assets/example-metro/scene.js (tuyến, ghim, tàu, camera giữ nguyên). Các toạ độ polygon dưới đây
 * chỉ là HÌNH MINH HOẠ quanh Hội An / KCN Điện Nam – Điện Ngọc / sân bay Chu Lai — dùng ranh giới thật (quy hoạch, OSM) khi làm video thật.
 * Kích thước màn hình: thẻ khu vực cao ~75px, HUD km chiếm y 1434–1630 (tránh đặt chữ lớn ở vùng này khi bật thanh km). */
Object.assign(window.SCENE, {
  // kind: kcn (vàng cam, KCN/khu kinh tế) | dothi (đỏ, khu đô thị) | cang (tím) | sanbay (cam) | xanh (xanh lá, ranh đô thị/du lịch) | hanhchinh (xanh dương, ranh hành chính)
  zones: [
    { name: 'Hội An', kind: 'xanh', pts: [[15.905, 108.305], [15.905, 108.360], [15.862, 108.368], [15.855, 108.312]], t0: 14.5, t1: 20, dx: -30, lead: 130 },
    { name: 'KCN Điện Nam – Điện Ngọc', kind: 'kcn', pts: [[15.955, 108.262], [15.955, 108.300], [15.925, 108.305], [15.925, 108.268]], t0: 13.5, t1: 19, dx: 40, lead: 120 },
    { name: 'Sân bay Chu Lai', kind: 'sanbay', pts: [[15.43, 108.66], [15.43, 108.72], [15.39, 108.72], [15.39, 108.66]], t0: 18.5, t1: 20.5, lead: 100 }
  ],            // t0,t1: thời gian hiện (viền vẽ dần 0,8s); anchor:[lat,lon] đổi điểm gắn thẻ; dx,lead: lệch ngang / cao của đường dẫn (px màn hình); smin,smax: chỉ hiện thẻ trong khoảng scale camera
  kmbar: { title: 'METRO ĐÀ NẴNG – CHU LAI', subtitle: 'MÔ PHỎNG HƯỚNG TUYẾN', total: 103.8, stops: [0, 4, 8.8, 16.7, 23.2, 29, 54.3, 66, 75.4, 95, 103.8], t0: 12.9, t1: 21 },   // đầu thanh chạy theo SCENE.train; stops = km cộng dồn từng ga
  logo: { src: 'assets/logo.png', w: 120 }   // thay bằng logo thật (nền trắng bo góc); nhãn địa điểm tự lùi trái
});
// đặt TRƯỚC initEngine(window.SCENE);
