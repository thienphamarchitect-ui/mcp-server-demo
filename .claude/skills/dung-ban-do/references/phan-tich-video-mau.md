# Phân tích video bản đồ mẫu: "Mô phỏng hướng tuyến Metro Đà Nẵng – Chu Lai"

Video mẫu: 61 giây, 576x1024 (9:16), 30fps, có logo L&D (Invest & Develop) góc trên phải, watermark Google Earth dưới đáy.
Tài liệu này ghi lại cách video đó được làm để áp dụng cho video khác. Phần "công cụ" là suy luận từ hình ảnh, chưa xác nhận.

## 1. Cấu trúc theo thời gian
| Giây | Nội dung |
|---|---|
| 0–5 | **Teaser toàn tuyến**: camera bay lướt dọc bờ biển, các nhãn điểm chính hiện dần để người xem thấy cả tuyến, rồi lia về điểm đầu. |
| 6–46 | **Chạy tàu dọc tuyến**: camera nghiêng ~60°, bám tàu. Sau tàu là vệt neon cyan, phía trước là đường mờ. Nhãn hiện khi tàu tới gần, biến mất khi đã qua. |
| 46–53 | **Cao trào**: camera orbit quanh điểm cuối (Chu Lai), vòng tròn vàng đồng tâm phát xung, polygon khu vực tô viền (cảng, khu kinh tế, khu đô thị, sân bay). |
| 54–61 | **Pull-back** lùi ra toàn cảnh, giữ 4–5s với mọi nhãn cùng hiện — khung "chốt" để nhớ. |

**Tiết tấu không đều (quan trọng)**: đoạn dày điểm quan trọng tàu chạy ~1,8 km/s; đoạn thưa dân cư ~3 km/s. Thời gian dừng nhiều ở chỗ có thông tin, lướt nhanh ở chỗ trống, nên 104 km vẫn gọn trong ~40s.

## 2. Các lớp hình ảnh (từ dưới lên)
1. Ảnh vệ tinh 3D kiểu Google Earth, camera nghiêng, hướng nhìn bám theo tuyến.
2. Vệt tuyến cyan phát sáng, vẽ dần sau tàu.
3. Đoàn tàu 3D 4 toa trắng đỏ, đúng phối cảnh.
4. Polygon khu vực vẽ dính mặt đất: vàng = KCN, cyan = ranh hành chính, tím = cảng, cam = sân bay, xanh lá = khu đô thị, đỏ = điểm nhấn.
5. Nhãn 2 kiểu: (a) nút giao/nhà ga — pill nền navy, viền + chấm màu, chữ trắng; (b) khu vực — thẻ trắng, sọc màu bên trái, dòng nhỏ "KHU VỰC" phía trên, tên đậm phía dưới. Mọi nhãn có đường dẫn mảnh xuống đúng điểm.
6. HUD đáy: gradient tối; dòng nhỏ cyan "MÔ PHỎNG HƯỚNG TUYẾN"; tiêu đề trắng đậm; **thanh tiến độ km** với các chấm ga đặt **theo tỷ lệ km thật**, thanh tô cyan dần, số km chạy theo đầu thanh.
7. Logo cố định góc trên phải. Giữ dòng ghi nguồn ảnh (Google Earth).

## 3. Mã màu nhãn nút giao (suy đoán)
Xanh dương = nút giao thông thường; đỏ = nút giao nối KCN/cảng/sân bay (đầu mối kinh tế); vàng/cam = đô thị, du lịch (Tam Kỳ, Hội An). Chọn mã màu cố định cho từng loại và giữ xuyên suốt video.

## 4. Kỹ thuật cần giữ khi làm video khác
- Mở bằng teaser toàn tuyến → đi theo tuyến → một cao trào có vòng xung → pull-back chốt.
- Tốc độ theo thông tin, không theo quãng đường.
- Nhãn hiện khi tàu tới gần, mất khi qua: mỗi lúc 3–5 nhãn.
- Thanh km tỷ lệ thật giúp người xem biết "đã đi được bao xa".
- Vòng tròn xung = "bán kính X km quanh dự án".

## 5. Cách phân tích một video mẫu mới
```bash
V=video.mov; mkdir -p frames sheets
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 $V
ffmpeg -v error -i $V -vf "fps=1,scale=288:-1" frames/f_%03d.jpg
# contact sheet 12 khung (6x2) mỗi tấm: start_number = i*12+1
ffmpeg -v error -y -start_number 1 -framerate 1 -i frames/f_%03d.jpg -frames:v 12 -vf tile=6x2 sheets/sheet_0.jpg
ffmpeg -i $V -vf "select='gt(scene,0.25)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*"   # điểm cắt cảnh
ffmpeg -ss 15 -i $V -frames:v 1 full15.png      # khung đủ độ phân giải để xem chi tiết HUD/nhãn
ffmpeg -i $V -af volumedetect -vn -f null -     # có âm thanh không (không nghe được nội dung)
```
Xem từng sheet (Read ảnh), ghi lại: mốc thời gian từng giai đoạn, số km theo giây (để suy ra tốc độ), kiểu nhãn, màu, HUD. Không nghe được audio thì nói rõ.
