import sys, os
sys.path.insert(0, '/home/user/mcp-server-demo/.claude/skills/dung-ban-do/scripts')
from explainer_kit import *
SCENE = {
  'pins': [
    {'id': 1, 'lat': 16.0495, 'lon': 108.2480, 'label': 'MỸ KHÊ', 'side': 'L', 'dy': 40},
    {'id': 2, 'lat': 16.0680, 'lon': 108.2220, 'label': 'SÔNG HÀN', 'side': 'L', 'dy': -60},
    {'id': 3, 'lat': 16.0439, 'lon': 108.1994, 'label': 'SÂN BAY', 'side': 'R', 'dy': 40}],
  'route': [], 'places': [['SƠN TRÀ', 16.115, 108.285, 0, 1.2], ['BIỂN ĐÔNG', 16.06, 108.34, 0, 1.2]],
  'rings': [], 'train': None, 'ov': {'scale': 0.62, 'center': [16.05, 108.24]}}
BRAND = dict(BRAND)
LABELS = {'1': [('c1', 'c1')], '2': [('c1', 'c1')], '3': [('c1', 'c1')]}
SENT = [
  h1('Chín tháng đầu năm, Đà Nẵng đón mười lăm phẩy tám sáu triệu lượt khách lưu trú.', 'CHÍN THÁNG ĐẦU NĂM 2026', '15,86 TRIỆU', 'LƯỢT KHÁCH LƯU TRÚ', None, hero_cap=190),
  h2('Mình là Khánh Linh. Vậy đầu tư dòng tiền có đáng không?', 'ĐẦU TƯ DÒNG TIỀN CÓ ĐÁNG?'),
  ctx('Gần một nửa là khách quốc tế: bảy phẩy bảy ba triệu lượt.', 'KHÁCH QUỐC TẾ', '7,73 TRIỆU', 200, 'LƯỢT KHÁCH · 9 THÁNG 2026', bg='DARK', dim=False),
  evid('Doanh thu lưu trú và ăn uống đạt năm mươi hai nghìn chín trăm bốn mươi lăm tỷ đồng. Nguồn: VietnamPlus, ngày năm tháng mười năm hai nghìn không trăm hai mươi sáu.',
       'DOANH THU LƯU TRÚ · ĂN UỐNG', [('9 THÁNG ĐẦU NĂM', '52.945 TỶ', 170, None)], 'Nguồn: VietnamPlus · 05/10/2026'),
  {'k': 'story', 'say': 'Có khách của mình đã mua hai căn để làm căn hộ dòng tiền, vì căn hộ ở Đà Nẵng đang thiếu vào mùa du lịch.', 'bg': 'DARK', 'els': [
     ('L', 'KHÁCH CỦA LINH', 'w', 62, 520, 0.0, 1.0, {'sfx': 'whoosh'}), ('L', 'MUA 2 CĂN', 'c', 200, 700, 0.15, 1.0, {'anim': 'hero', 'sfx': 'impact', 'g': -3}),
     ('L', 'LÀM CĂN HỘ DÒNG TIỀN', 'w', 56, 900, 0.4, 1.0), ('L', 'CĂN HỘ ĐANG THIẾU MÙA DU LỊCH', 'c', 44, 1020, 0.65, 1.0),
     ('S', 'Câu chuyện thật của khách Linh · theo quan sát của Linh', 1700, 0.3, 1.0)]},
  bridge('Nhưng khách đông chưa chắc căn nào cũng lãi.', 'NHƯNG KHÁCH ĐÔNG', 'CHƯA CHẮC CĂN NÀO', 'CŨNG CÓ LÃI'),
  b2('Ba tiêu chí.', 'DÒNG TIỀN'),
  crit('c1', 1, 'Một, vị trí: nơi khách chọn ngủ, gần biển hoặc sông Hàn.', 'VỊ TRÍ', 'NƠI KHÁCH CHỌN NGỦ', [('C', '◆', 'GẦN BIỂN · SÔNG HÀN', 1480, 0.4, 1.0)]),
  crit('c2', 2, 'Hai, vận hành: ba năm làm lưu trú, bảy năm làm nội thất, mình biết lợi nhuận nằm ở chi phí.', 'VẬN HÀNH', 'LỢI NHUẬN NẰM Ở CHI PHÍ',
       [('C', '◆', '3 NĂM LƯU TRÚ', 900, 0.3, 1.0), ('C', '▣', '7 NĂM NỘI THẤT', 1050, 0.5, 1.0)], bg='DARK'),
  crit('c3', 3, 'Ba, vốn vay: ưu tiên dự án có hỗ trợ lãi và ân hạn gốc, áp dụng theo từng thời điểm.', 'VỐN VAY', 'HỖ TRỢ LÃI · ÂN HẠN GỐC',
       [('C', '◆', 'ÁP DỤNG THEO TỪNG THỜI ĐIỂM', 900, 0.4, 1.0)], bg='DARK', title_cap=150),
  moc('Mình theo dõi ba mốc: số liệu cả năm, đường bay mới, sự kiện lớn.', [('①', 'SỐ LIỆU CẢ NĂM'), ('②', 'ĐƯỜNG BAY MỚI'), ('③', 'SỰ KIỆN LỚN')]),
  cta('Cần phân tích khu bạn quan tâm, nhắn Linh nhé.', 'PHÂN TÍCH KHU BẠN QUAN TÂM',
      DISC_BASE + '<br>Nguồn: VietnamPlus · Quan hệ lợi ích: chờ Linh xác nhận'),
]
CAM = [('c1', 0.0, 1, 1.5), ('c1', 0.95, 2, 1.9), ('moc', 0.0, 'OV', 0.62)]
