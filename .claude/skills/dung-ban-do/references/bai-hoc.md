# Bài học và lỗi đã gặp khi dựng video bản đồ Metro Đà Nẵng – Chu Lai

## Hình ảnh
- **Số có dấu chấm ngàn**: `count` định dạng kiểu Đức → năm 2027 thành "2.027". Năm và số không cần đếm thì dùng `line` tĩnh (anim `hero`). Chỉ dùng `count` cho số nhỏ (103, 95%, 24).
- **Dấu mũ chạm nhãn phía trên**: số cap 150 có dấu (Á, Ố) vươn lên ~45px. Khoảng cách tâm nhãn → tâm số ≥ ~155px; tiêu đề nhỏ phía trên chữ hero lớn cách ≥ 0,9×cap.
- **Ghi chú dài bị cắt mép**: `note`/`src` không tự thu nhỏ. ≤ 28px và ≤ ~60 ký tự; chia hai dòng nếu dài.
- **Nhãn ghim đè chữ**: ở cảnh có nhiều chữ (kết video), bỏ nhãn ghim (`labwin` rỗng), chỉ để chấm. Vòng xung nằm sau chữ thì bỏ hoặc dời tâm.
- **Dòng ghi nguồn ảnh vệ tinh đè dòng nguồn khác**: để credit ở `bottom:44px`, dòng `src` ở y ≤ 1745.
- **Bản đồ tối, mờ**: ảnh vệ tinh vốn tối; engine đã tăng brightness 1,12 và giảm gradient. Đừng cộng thêm lớp phủ tối; dùng `dim` chỉ khi có thẻ đè.
- **Mép biển có mảng sáng/răng cưa**: dùng `seafix.py` bản mới; kiểm tra thumbnail trước khi dựng.
- **Tuyến chạy chéo làm lộ mép ảnh nền**: dùng `plan_map.py` để chọn bbox.
- **Cảnh nhiều chữ nên tối bản đồ (`dim`) và dùng nền DARK xen kẽ** để người xem nghỉ mắt; mỗi 10–15s đổi nền một lần.

## Giọng đọc (Speko)
- Mỗi câu/cụm một file. Số viết bằng chữ ("hai trăm sáu mươi sáu nghìn tỷ", "năm hai nghìn không trăm hai mươi bảy").
- Viết lại từ khó đọc: "DIFF" → "lễ hội pháo hoa", "MBBank" → "MB Bank"; giữ nguyên chữ gốc trên màn hình.
- **Luôn `audio_transcribe` lại** các đoạn có số/tên riêng. (STT đôi khi sai chữ thường như "Tiến" thay "Tuyến" — nghe lại bằng khoảng thời gian, đừng sửa lời vội.)
- Giọng nữ Việt đã dùng: Cartesia "Linh – Soft Presence" (`935a9060-373c-49e4-b078-f4ea6326987a`, `sonic-3.5`), ổn định giữa các lần gọi, ~173 từ/phút nên dùng `vo_prep.sh <project> 1.0`. Tìm giọng khác bằng `voices_search`, không đoán id.
- Kết quả `audio_synthesize` quá lớn nên bị lưu file → `scripts/tts_decode.py`. Link ký chỉ sống 15 phút: transcribe ngay.
- **Không nhân bản giọng một người thật nếu chưa có đồng ý của họ.** Dùng giọng stock, gắn nhãn "BẢN DEMO · GIỌNG ĐỌC AI MẪU", và nói rõ với người dùng. Bản đăng nên để người thật thu giọng.
- Chi phí: ~1.100 ký tự ≈ vài cent với Cartesia. Báo người dùng.

## Dữ liệu và pháp lý
- Mọi con số trên màn hình phải đối chiếu bài gốc (`capture_news.js` + xem ảnh cắt). Số lấy từ tóm tắt tìm kiếm mà chưa mở bài gốc phải được nói rõ là chưa kiểm.
- Tuyến vẽ tự do là **minh hoạ**: ghi trên màn hình + trong khung cuối.
- Ảnh vệ tinh Esri chỉ hợp cho demo; bản thương mại dùng nguồn có giấy phép hoặc flycam. Ảnh bài báo cũng chỉ cho demo.
- Nội dung có điều kiện tài chính/chính sách vay: chỉ nêu đúng các con số có trong tài liệu gốc, thêm "điều kiện áp dụng theo chính sách từng thời điểm", ghi nguồn, nêu mối quan hệ lợi ích nếu có. Không cam kết lợi nhuận.
- `capture_news.js`: ảnh head thường dính tên chuyên mục/menu ở trên → cắt lại bằng PIL (`crop`). Thẻ báo rộng 900px thì chữ tiêu đề ~30px là đọc được.

## Quy trình làm việc
- Giao từng bước: kịch bản → bản đồ/preview → video. Xem preview các mốc chính (contact sheet) và **xem 1–2 khung đầy đủ độ phân giải** trước khi render đủ; lỗi chồng chữ thường chỉ lộ ở khung lớn.
- Render đầy đủ chạy nền (`run_in_background`), không poll.
- Sau render: `ffprobe` (thời lượng/độ phân giải), `ebur128` (loudness), trích ~12 khung từ MP4 để xem lại.
- Nói rõ phần đã kiểm (khung hình, STT) và phần người dùng phải tự nghe (nhạc, SFX).
