# Checklist QC và đăng bài

## Nội dung
- [ ] Mọi con số khớp bài gốc; số chưa kiểm được ghi rõ trong ghi chú giao.
- [ ] Có dòng nguồn trên màn hình cho từng nhóm số liệu; có câu miễn trừ "không phải lời khuyên đầu tư".
- [ ] Không hứa lợi nhuận; điều kiện vay/ưu đãi chỉ nêu đúng tài liệu gốc kèm "áp dụng theo chính sách từng thời điểm"; nêu quan hệ lợi ích.
- [ ] Tuyến/ranh giới tự vẽ có chữ "minh hoạ".
- [ ] Thông tin cá nhân của người dẫn đúng và đã được xác nhận.

## Hình
- [ ] Xem khung đầu + khung cuối + 1 khung giữa mỗi cảnh ở độ phân giải đầy đủ: không chồng chữ, không tràn mép, bản đồ phủ kín khung (không lộ mép navy).
- [ ] Chữ nhỏ nhất ≥ 30px (trừ câu miễn trừ); thẻ/CTA không nằm dưới y = 1670.
- [ ] Khi bật thanh km: không có chữ lớn ở y 1434–1630. Khi bật phụ đề: không có thẻ ở y ≥ 1560.
- [ ] B-roll: người rõ mặt có đồng ý; không logo bên thứ ba; có `nguon-b-roll.md`.

## Âm thanh
- [ ] Giọng không sai số/tên riêng (đã nhận dạng ngược); phụ đề khớp giọng.
- [ ] `ffmpeg -i out.mp4 -af ebur128 -vn -f null -`: −14 ± 1 LUFS, đỉnh ≤ −1 dBTP.
- [ ] Không SFX lớn đè lên từ khoá của giọng; người duyệt tự nghe giọng/nhạc/SFX.

## Kỹ thuật
- [ ] `ffprobe`: 1080×1920, 30 fps, đúng thời lượng; file ≤ ~100 MB (nén `-crf 26`).

## Đăng bài
- [ ] Ảnh bìa: khung hook (số lớn + câu hỏi): `ffmpeg -ss 3.5 -i out.mp4 -frames:v 1 bia.jpg`.
- [ ] Caption: 1 câu hook + 1 dòng nguồn + 3–5 hashtag; không nêu lợi nhuận chắc chắn.
- [ ] Bật nhãn "nội dung do AI tạo" nếu dùng giọng AI; ghi nguồn ảnh Esri; nhớ ảnh Esri/ảnh báo chỉ cho demo.
- [ ] Kiểm giới hạn độ dài/dung lượng hiện hành của nền tảng.

## Đóng gói
- [ ] Lời đọc (.txt), `scene.js`, `timeline.js`, ảnh báo chứng, ghi chú nguồn + trạng thái kiểm, MP4 → commit vào nhánh riêng.
- [ ] Cập nhật bài học mới vào `bai-hoc.md` của skill `dung-ban-do`.
