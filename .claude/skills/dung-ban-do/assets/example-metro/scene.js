/* scene.js — Metro Đà Nẵng – Chu Lai (Khánh Linh), bản demo 83,8s. Ví dụ đầy đủ cho engine.js.
 * Phần 1: cấu hình bản đồ (SCENE). Phần 2: các dòng chữ/thẻ theo từng cảnh, mốc thời gian lấy từ giọng đọc (vo_prep.sh). */
window.SCENE = {
  brand: { t1: 'KHÁNH LINH', t2: 'ĐẦU TƯ BĐS HẠNG SANG ĐÀ NẴNG', loc: 'ĐÀ NẴNG · 2026', demo: 'BẢN DEMO · GIỌNG ĐỌC AI MẪU' },
  // ghim: id hiện trong chấm; side 'R' = nhãn nằm bên phải ghim, 'L' = bên trái
  pins: [
    { id: 1, lat: 16.0439, lon: 108.1994, label: 'SÂN BAY ĐÀ NẴNG', side: 'R' },
    { id: 2, lat: 15.8801, lon: 108.338, label: 'HỘI AN', side: 'L' },
    { id: 3, lat: 15.5736, lon: 108.474, label: 'TAM KỲ', side: 'L' },
    { id: 4, lat: 15.4065, lon: 108.7054, label: 'SÂN BAY CHU LAI', side: 'L' }
  ],
  // tuyến MINH HOẠ: đi qua các ghim, bám dải đồng bằng ven biển (KHÔNG phải phương án được phê duyệt)
  route: [[16.0439, 108.1994], [16.030, 108.212], [16.003, 108.243], [15.972, 108.270], [15.940, 108.298], [15.910, 108.322], [15.8801, 108.338], [15.840, 108.358], [15.790, 108.385], [15.730, 108.415], [15.660, 108.447], [15.5736, 108.474], [15.520, 108.515], [15.470, 108.580], [15.430, 108.655], [15.4065, 108.7054]],
  places: [['SƠN TRÀ', 16.115, 108.285, 0, .6], ['CÙ LAO CHÀM', 15.9535, 108.5105, 0, .6], ['BIỂN ĐÔNG', 15.70, 108.62, 0, .6], ['MỸ KHÊ', 16.040, 108.255, 1.3, 9], ['SÔNG HÀN', 16.068, 108.222, 1.3, 9]],
  rings: [{ lat: 16.045, lon: 108.228, r: 230, t0: 38.75, t1: 49.7, col: '#FFE600' }],
  train: { t0: 12.9, t1: 19.7 },                  // tàu chạy hết tuyến trong khoảng này (tốc độ đều)
  ov: { scale: 0.32 },                            // scale toàn cảnh; xem scripts/plan_map.py để chọn bbox ảnh nền khớp
  // nhãn ghim: [a,b] tuyệt đối, hoặc {pass:[da,db]} tính từ lúc tàu qua ghim
  labwin: { 1: [[12.9, 15.0]], 2: [{ pass: [-0.1, 1.9] }, [21.1, 23.4]], 3: [{ pass: [-0.1, 1.9] }], 4: [{ pass: [-0.1, 1.5] }] },
  dim: [[14.6, 20.7], [23.4, 32.8], [43.0, 49.6], [74.0, 83.8]],   // tối bản đồ khi có thẻ/số liệu
  cam: {
    push: 0.10,                                   // đẩy nhẹ toàn cảnh 0 -> follow[0]
    follow: [12.0, 19.9, 1.4, 0.8],               // [bắt đầu, kết thúc, giây zoom vào, scale] bám theo tàu
    keys: [                                       // sau đó: [t, đích, scale]; đích = 'OV' | id ghim | 'END' | [lat,lon,dyPx]
      [19.9, 'END', 0.8], [21.6, 'OV', 0.32], [23.2, [15.962, 108.268], 0.95], [32.9, [15.962, 108.268, 30], 1.18],
      [37.7, [16.045, 108.222, 40], 1.9], [49.8, [16.045, 108.2254, 40], 2.3],
      [72.7, 'OV', 0.33], [83.8, 'OV', 0.30]
    ]
  }
};
initEngine(window.SCENE);

// SCENE 1 – HOOK (0 – 12.0): "Khách hỏi mình nhiều nhất: metro 266 nghìn tỷ..., đáng kỳ vọng hay nên chờ?"
line('KHÁCH HỎI NHIỀU NHẤT','w',60,470,0.5,2.2,{sfx:'whoosh'});
line('METRO ĐÀ NẴNG – CHU LAI','w',54,420,2.2,6.4);
line('266.000 TỶ','c',210,620,2.3,6.4,{anim:'hero',sfx:'impact',g:-3});
line('ĐÁNG KỲ VỌNG','w',92,860,4.7,6.4);
line('HAY NÊN CHỜ?','c',92,990,5.2,6.4,{anim:'hero',sfx:'impact',g:-5});
// f2 @6.5: "Mình là Khánh Linh, và mình nghĩ: kỳ vọng thì có, nhưng đừng mua chỉ vì metro."
line('KHÁNH LINH','c',150,540,6.7,12.0,{anim:'hero',sfx:'sparkle'});
line('ĐẦU TƯ BĐS HẠNG SANG ĐÀ NẴNG','w',48,690,7.2,12.0);
line('KỲ VỌNG THÌ CÓ','c',100,1280,9.0,10.1);
line('ĐỪNG MUA CHỈ VÌ METRO','r',84,1280,10.1,12.0,{anim:'hero',sfx:'impact',g:-4});
// SCENE 2 – METRO (12.0 – 20.9): "Tuyến dài hơn 103 cây số, nhưng mới ở bước đề xuất: dự kiến khởi công 2027, vận hành 2032."
line('TUYẾN MÔ PHỎNG','w',56,330,12.2,20.8,{sfx:'whoosh'});
paper('assets/tcct_card.png','TẠP CHÍ CÔNG THƯƠNG · 21/04/2026',460,900,14.5,20.8,-2);
line('103 KM','c',200,1330,13.1,16.0,{anim:'count',count:[0,103,' KM'],sfx:'impact',g:-3});
line('KHỞI CÔNG DỰ KIẾN','w',46,1240,16.1,18.5);
line('2027','c',210,1410,17.2,18.5,{anim:'hero',sfx:'impact',g:-3});
line('VẬN HÀNH DỰ KIẾN','w',46,1240,18.6,20.8);
line('2032','c',210,1410,19.4,20.8,{anim:'hero',sfx:'impact',g:-3});
src('Tuyến minh hoạ, chưa phải phương án được phê duyệt',1700,13.0,20.8);
// SCENE 3 – ĐANG CHẠY THẬT (20.9 – 32.8)
line('THỨ ĐANG CHẠY THẬT','c',90,350,21.1,32.7,{sfx:'whoosh'});
paper('assets/vnp_card.png','VIETNAMPLUS · 05/10/2026',470,900,23.5,29.4,2);
note('Trung tâm tài chính quốc tế: có cơ quan điều hành từ 9/1/2026',800,25.0,32.6);
note('Nhà ga quốc tế sân bay Đà Nẵng đang được mở rộng',850,25.4,32.6);
line('LƯỢT KHÁCH LƯU TRÚ · 9 THÁNG','w',44,1230,24.7,28.0);
line('15,86 TRIỆU','c',200,1370,25.6,28.0,{anim:'hero',sfx:'impact',g:-3});
line('GẦN MỘT NỬA LÀ KHÁCH QUỐC TẾ','w',44,1230,28.0,32.6);
line('7,73 TRIỆU','c',200,1370,28.2,32.6,{anim:'hero',sfx:'impact',g:-3});
chip('◆','BĐS DÒNG TIỀN ĐÀ NẴNG',1530,30.0,32.6);
src('Doanh thu lưu trú, ăn uống 52.945 tỷ đồng (+26,2%) · Nguồn: VietnamPlus',1700,24.7,32.6);
// SCENE 4 – CẦU NỐI (32.8 – 37.9)
line('NHƯNG KHÁCH ĐÔNG','w',76,560,33.0,35.9,{sfx:'whoosh'});
line('CHƯA CHẮC CĂN NÀO','w',76,690,33.6,35.9);
line('CŨNG CÓ DÒNG TIỀN','c',92,830,34.6,35.9);
sfx(35.3,'riser',-4);
line('3 TIÊU CHÍ','c',230,860,36.0,37.9,{anim:'hero',sfx:'impact',g:0});
line('DÒNG TIỀN','w',110,1050,36.3,37.9);
// SCENE 5 – TIÊU CHÍ 1: VỊ TRÍ (37.9 – 49.5)
line('TIÊU CHÍ 1','w',62,300,38.0,49.4,{sfx:'whoosh'});
line('VỊ TRÍ','c',200,540,38.75,49.4,{anim:'hero',sfx:'impact',g:-3});
line('DƯ ĐỊA TĂNG GIÁ · HÚT KHÁCH THẬT','w',42,730,39.6,49.4);
line('DỊP LỄ HỘI PHÁO HOA DIFF 2026','c',44,1100,42.2,49.4);
line('VEN BIỂN · SÔNG HÀN','w',40,1180,43.5,49.4);
line('95%','c',150,1305,45.0,49.4,{anim:'count',count:[0,95,'%'],sfx:'impact',g:-3});
line('KHÁCH SẠN 3 SAO TRỞ XUỐNG','w',40,1470,46.4,49.4);
line('55%','w',150,1595,47.8,49.4,{anim:'count',count:[0,55,'%'],sfx:'ting'});
src('Công suất phòng dịp DIFF 2026 · Nguồn: Báo Văn Hóa',1710,43.5,49.4);
// SCENE 6 – TIÊU CHÍ 2: VẬN HÀNH (49.4 – 60.3)
line('TIÊU CHÍ 2','w',62,300,49.6,60.2,{sfx:'whoosh'});
line('VẬN HÀNH','c',190,540,50.3,60.2,{anim:'hero',sfx:'impact',g:-3});
chip('◆','3 NĂM LƯU TRÚ',800,51.45,60.2);
chip('▣','7 NĂM NỘI THẤT',950,53.17,60.2);
line('TIỀN NẰM Ở CHI PHÍ','c',90,1200,54.6,56.8);
line('CÙNG DOANH THU','w',64,1230,56.9,60.2);
line('VẬN HÀNH TỐT','c',96,1370,57.9,60.2);
line('GIỮ LẠI NHIỀU HƠN','c',120,1540,58.7,60.2,{anim:'hero',sfx:'impact',g:-3});
// SCENE 7 – TIÊU CHÍ 3: VỐN VAY (60.3 – 73.0)
line('TIÊU CHÍ 3','w',58,235,60.5,72.9,{sfx:'whoosh'});
line('VỐN VAY','c',150,410,61.1,72.9,{anim:'hero',sfx:'impact',g:-3});
line('DỰ ÁN REGAL COMPLEX','c',58,555,62.3,72.9,{sfx:'sparkle'});
line('VỐN TỰ CÓ','w',40,700,64.3,72.9);
line('10%','c',150,855,64.9,72.9,{anim:'count',count:[0,10,'%'],sfx:'impact',g:-3});
line('ÂN HẠN NỢ GỐC','w',40,975,65.9,72.9);
line('24 THÁNG','c',150,1130,66.6,72.9,{anim:'count',count:[0,24,' THÁNG'],sfx:'impact',g:-3});
line('HỖ TRỢ LÃI SUẤT · ĐẾN 30/03/2028','w',40,1250,67.9,72.9);
line('0%','c',150,1405,68.9,72.9,{anim:'hero',sfx:'impact',g:-3});
chip('◆','MBBANK · CN ĐÀ NẴNG',1540,71.7,72.9);
src('Điều kiện áp dụng theo chính sách từng thời điểm · Nguồn: Regal Group',1700,64.3,72.9);
// SCENE 8 – KẾT (73.0 – 83.8)
line('CÒN METRO,','w',64,330,73.5,83.5,{sfx:'whoosh'});
line('MÌNH CHỜ 3 MỐC','c',130,480,74.5,83.5,{anim:'hero',sfx:'impact',g:-3});
chip('①','NHÀ ĐẦU TƯ CHÍNH THỨC',920,76.1,83.5);
chip('②','KHỞI CÔNG THẬT',1070,77.25,83.5);
chip('③','VỊ TRÍ GA',1220,78.1,83.5);
line('PHÂN TÍCH KHU BẠN QUAN TÂM','w',44,1400,79.2,83.5);
raw(`<div class="cta" style="top:1445px"><span style="display:inline-block;transform:scaleX(.86)">NHẮN KHÁNH LINH</span></div>`,80.4,83.5,'pop');sfx(80.4,'pop',0);sfx(80.45,'sparkle',-4);
raw(`<div class="disc">Tuyến minh hoạ, chưa phải phương án được phê duyệt · Không phải lời khuyên đầu tư<br>Điều kiện vay theo chính sách từng thời điểm · Nguồn: Tạp chí Công Thương, VietnamPlus, Báo Văn Hóa, Regal Group</div>`,76.0,83.5);
// chuyển cảnh
[12.0,20.9,32.8,37.8,49.4,60.3,72.9].forEach(t=>sfx(t,'whoosh',-3));
sfx(0,'impact',-6);

FX.flash=[[0,0.5,1],[36.0,0.35,0.9],[37.8,0.2,0.35],[72.9,0.25,0.4]];
FX.glow=[[2.3,1.2],[36.0,1.6],[61.1,1.0],[74.5,1.0]];
FX.sweep=[[14.5],[23.5]];
