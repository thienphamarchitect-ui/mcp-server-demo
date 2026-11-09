import sys
sys.path.insert(0, '/home/user/mcp-server-demo/.claude/skills/dung-ban-do/scripts')
from explainer_kit import *
SCENE = {'pins': [{'id': 1, 'lat': 16.0439, 'lon': 108.1994, 'label': '', 'dot': True}], 'route': [], 'places': [], 'rings': [], 'train': None, 'ov': {'scale': 0.62, 'center': [16.05, 108.24]}}
BRAND = dict(BRAND)
LABELS = {}
SENT = [
  h1('Hỗ trợ lãi suất không phần trăm: vay thế nào cho an toàn?', 'DỰ ÁN REGAL COMPLEX', '0%', 'HỖ TRỢ LÃI SUẤT', 'VAY THẾ NÀO CHO AN TOÀN?', hero_cap=230, bg='DARK'),
  h2('Mình là Khánh Linh, và mình nghĩ: vay vừa sức, hiểu lúc hết ưu đãi.', 'VAY VỪA SỨC', bg='DARK'),
  evid('Dự án Regal Complex có chính sách vốn tự có mười phần trăm, ân hạn nợ gốc hai mươi bốn tháng.', 'CHÍNH SÁCH VAY', [('VỐN TỰ CÓ', '10%', 170, {'anim': 'count', 'count': [0, 10, '%'], 'sfx': 'impact', 'g': -3}), ('ÂN HẠN NỢ GỐC', '24 THÁNG', 150, {'anim': 'count', 'count': [0, 24, ' THÁNG'], 'sfx': 'impact', 'g': -3})], 'Nguồn: Regal Group · tài liệu hội thảo', k='ctx'),
  evid('Hỗ trợ lãi không phần trăm đến tháng ba năm hai nghìn không trăm hai mươi tám, qua ngân hàng Quân đội, chi nhánh Đà Nẵng. Điều kiện áp dụng theo từng thời điểm.', 'HỖ TRỢ LÃI SUẤT', [('ĐẾN 03/2028', '0%', 190, None)], 'Điều kiện áp dụng theo chính sách từng thời điểm · Nguồn: Regal Group', k='ev', extra=[('C', '◆', 'MBBANK · CN ĐÀ NẴNG', 1300, 0.6, 1.0)]),
  bridge('Ưu đãi hấp dẫn, nhưng cần tính kỹ.', 'ƯU ĐÃI HẤP DẪN', 'NHƯNG CẦN', 'TÍNH KỸ'),
  b2('Ba tiêu chí.', 'DÒNG TIỀN'),
  crit('c1', 1, 'Một, vị trí: căn tốt mới có người thuê trả lãi, đừng vay vì ưu đãi.', 'VỊ TRÍ', 'CĂN TỐT MỚI CÓ NGƯỜI THUÊ', [('C', '◆', 'ĐỪNG VAY VÌ ƯU ĐÃI', 900, 0.4, 1.0)], bg='DARK'),
  crit('c2', 2, 'Hai, vận hành: ba năm làm lưu trú, mình biết dòng tiền phải đủ trả lãi ngay cả tháng vắng.', 'VẬN HÀNH', 'DÒNG TIỀN ĐỦ TRẢ LÃI', [('C', '◆', '3 NĂM LƯU TRÚ', 900, 0.3, 1.0), ('C', '▣', 'CẢ THÁNG VẮNG', 1050, 0.55, 1.0)], bg='DARK'),
  crit('c3', 3, 'Ba, vốn vay: tính lãi sau khi hết ưu đãi và so với tiền thuê thực nhận, không chỉ nhìn con số không phần trăm.', 'VỐN VAY', 'LÃI SAU ƯU ĐÃI · SO VỚI THUÊ RÒNG', [('C', '◆', 'KHÔNG CHỈ NHÌN 0%', 900, 0.5, 1.0)], bg='DARK', title_cap=150),
  moc('Mình chờ ba mốc: lãi sau hỗ trợ, điều kiện giải ngân, ngày hết ưu đãi.', [('①', 'LÃI SAU HỖ TRỢ'), ('②', 'ĐIỀU KIỆN GIẢI NGÂN'), ('③', 'NGÀY HẾT ƯU ĐÃI')], bg='DARK'),
  cta('Cần tính theo căn cụ thể, nhắn Linh nhé.', 'TÍNH THEO CĂN CỤ THỂ', DISC_BASE + '<br>Nguồn: Regal Group · Quan hệ lợi ích: chờ Linh xác nhận', bg='DARK'),
]
CAM = []
