import sys
sys.path.insert(0, '/home/user/mcp-server-demo/.claude/skills/dung-ban-do/scripts')
from explainer_kit import *
AP = (16.0439, 108.1994)
SCENE = {
  'pins': [{'id': 1, 'lat': AP[0], 'lon': AP[1], 'label': 'SÂN BAY ĐÀ NẴNG', 'side': 'R', 'dy': 60},
           {'id': 2, 'lat': 16.0680, 'lon': 108.2220, 'label': 'SÔNG HÀN', 'side': 'R', 'dy': -70},
           {'id': 3, 'lat': 16.0495, 'lon': 108.2480, 'label': 'MỸ KHÊ', 'side': 'L', 'dy': 50}],
  'route': [], 'places': [['SƠN TRÀ', 16.115, 108.285, 0, 1.2]],
  'rings': [{'lat': AP[0], 'lon': AP[1], 'km': k, 'static': True, 'label': '%d KM' % k, 'labAng': a, 'ks': ('ctx', 'ctx')} for k, a in ((3, 100), (5, 160), (10, -100))],
  'ov': {'scale': 0.62, 'center': [16.05, 108.24]}}
BRAND = dict(BRAND)
LABELS = {'1': [('ctx', 'ctx'), ('c1', 'c1')], '2': [('c1', 'c1')], '3': [('c1', 'c1')]}
SENT = [
  h1('Căn hộ gần sân bay Đà Nẵng: dòng tiền thật hay chỉ tiện?', 'GẦN SÂN BAY ĐÀ NẴNG', 'DÒNG TIỀN', 'THẬT HAY', 'CHỈ TIỆN?', hero_cap=190),
  h2('Mình là Khánh Linh, và mình nghĩ: dòng tiền thật, nếu chọn đúng khách.', 'DÒNG TIỀN THẬT'),
  ctx('Sân bay nằm sát trung tâm, chỉ vài cây số tới sông Hàn và biển Mỹ Khê.', 'SÁT TRUNG TÂM', '3 · 5 · 10 KM', 140, 'QUANH SÂN BAY', note='Vòng bán kính đo đường chim bay, chỉ mang tính minh hoạ', dim=False, big_opt={'anim': 'hero'}, ys=(330, 470, 1560)),
  evid('Nhà ga quốc tế đang được mở rộng từ bốn lên sáu triệu khách một năm. Năm hai nghìn không trăm hai mươi lăm, nhà ga đón sáu phẩy tám mốt triệu lượt khách.', 'NHÀ GA QUỐC TẾ ĐÀ NẴNG',
       [('CÔNG SUẤT MỞ RỘNG', '4 → 6 TRIỆU', 150, None), ('LƯỢT KHÁCH NĂM 2025', '6,81 TRIỆU', 150, None)], 'Nguồn: Báo Đại biểu Nhân dân · 19/05/2026'),
  {'k': 'story', 'say': 'Có khách của mình đã mua hai căn để làm căn hộ dòng tiền, vì căn hộ ở Đà Nẵng đang thiếu vào mùa du lịch.', 'bg': 'DARK', 'els': [
     ('L', 'KHÁCH CỦA LINH', 'w', 62, 520, 0.0, 1.0, {'sfx': 'whoosh'}), ('L', 'MUA 2 CĂN', 'c', 200, 700, 0.15, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -3}),
     ('L', 'LÀM CĂN HỘ DÒNG TIỀN', 'w', 56, 900, 0.4, 1.0), ('L', 'CĂN HỘ ĐANG THIẾU MÙA DU LỊCH', 'c', 44, 1020, 0.65, 1.0),
     ('S', 'Câu chuyện thật của khách Linh · theo quan sát của Linh', 1700, 0.3, 1.0)]},
  bridge('Nhưng gần sân bay chưa chắc có lãi.', 'NHƯNG GẦN SÂN BAY', 'CHƯA CHẮC', 'CÓ LÃI'),
  b2('Ba tiêu chí.', 'DÒNG TIỀN'),
  crit('c1', 1, 'Một, vị trí: gần cả sân bay lẫn biển, đi lại nhanh cho khách.', 'VỊ TRÍ', 'GẦN SÂN BAY · GẦN BIỂN', [('C', '◆', 'ĐI LẠI NHANH', 1480, 0.4, 1.0)]),
  crit('c2', 2, 'Hai, vận hành: khách bay thường đến muộn, đi sớm, nên tự check-in và dọn phòng nhanh là chỗ giữ lại lợi nhuận.', 'VẬN HÀNH', 'KHÁCH ĐẾN MUỘN · ĐI SỚM', [('C', '◆', 'TỰ CHECK-IN', 900, 0.35, 1.0), ('C', '▣', 'DỌN PHÒNG NHANH', 1050, 0.55, 1.0)], bg='DARK'),
  crit('c3', 3, 'Ba, vốn vay: chọn dự án có chủ đầu tư hỗ trợ lãi, điều kiện áp dụng theo từng thời điểm.', 'VỐN VAY', 'CHỦ ĐẦU TƯ HỖ TRỢ LÃI', [('C', '◆', 'ÁP DỤNG THEO TỪNG THỜI ĐIỂM', 900, 0.5, 1.0)], bg='DARK', title_cap=150),
  moc('Mình chờ ba mốc: đường bay mới, kết nối sân bay, nguồn cung căn hộ quanh khu.', [('①', 'ĐƯỜNG BAY MỚI'), ('②', 'KẾT NỐI SÂN BAY'), ('③', 'NGUỒN CUNG QUANH KHU')]),
  cta('Cần xem căn gần sân bay, nhắn Linh nhé.', 'XEM CĂN GẦN SÂN BAY', DISC_BASE + '<br>Nguồn: Báo Đại biểu Nhân dân · Quan hệ lợi ích: chờ Linh xác nhận'),
]
CAM = [('ctx', 0.1, 1, 0.8), ('ctx', 0.9, 1, 0.85), ('c1', 0.0, [16.052, 108.225, -330], 1.25), ('c1', 0.95, [16.052, 108.225, -330], 1.4), ('moc', 0.0, 'OV', 0.62)]
