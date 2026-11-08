# Năm biến thể MAP EXPLAINER

Chọn biến thể theo **đối tượng của tin**. Cấu trúc 6 khối, nhịp và thành phần bắt buộc giữ nguyên (xem `dang-video-map-explainer.md`); khác nhau ở hình bản đồ và loại bằng chứng.

| | Khi dùng | Hình bản đồ | Mẫu |
|---|---|---|---|
| **A. Tuyến hạ tầng** | metro, cao tốc, vành đai, đường ven biển | tuyến phát sáng + tàu bám + ghim ga (+ thanh km) | `assets/kich-ban-mau-metro-linh.md` |
| **B. Bán kính tiện ích** | sân bay, khu công nghiệp, trung tâm tài chính, bệnh viện | ghim + vòng bán kính km cố định (+ B-roll) | `assets/kich-ban-mau-b-san-bay-60s.md`; scene mẫu: skill `dung-ban-do`, `assets/example-ring/` |
| **C. So sánh hai khu** | "khu nào đáng mua hơn" | hai vòng/hai màu, thẻ so sánh 2 cột | — |
| **D. Tin chính sách / thị trường** | lãi suất, bảng giá đất, nguồn cung | nền tối + thẻ số liệu; bản đồ chỉ 1–2 cảnh | — |
| **E. Dòng thời gian dự án** | khởi công → vận hành | tuyến + mốc năm hiện lần lượt trên bản đồ | — |

## Biến thể B (bán kính) — hướng dẫn chi tiết
- **Vòng:** tối đa 3 vòng cố định (ví dụ 5/10/20 km), vàng, nhãn "5 KM"… Mỗi vòng phải có lý do với người thuê/mua (ví dụ ≤ 10 km là vùng đi làm hằng ngày). Dùng `rings:[{km,static:true,label}]` (đổi km sang px tự động).
- **Chim bay hay thời gian di chuyển:** vòng km là **đường chim bay**, luôn ghi "đo đường chim bay, minh hoạ" (dòng `src` 30px, y≈1700, hiện cùng lúc với vòng và ở lại). Nếu muốn nói thời gian di chuyển ("dưới 25 phút") phải có nguồn đo (bản đồ số, giờ cao điểm hay không) và ghi nguồn; không suy ra từ vòng km.
- **Khối 2 (bối cảnh) khi không có tàu:** zoom vào đối tượng, vòng hiện, 1–2 ghim phụ (thành phố, nút giao) kèm chip khoảng cách; không dùng thanh km.
- **Camera:** toàn cảnh → zoom vào đối tượng (scale 1,9–2,3) → zoom ra. Vùng ảnh nền: `plan_map.py --follow-scale 0 --extra "<đối tượng>" --extra-scale 2.2 --ring "lat,lon,km"`.
- **Tiêu chí gợi ý cho "căn hộ cho thuê gần tiện ích lớn"** (người dẫn duyệt/thay): ① vị trí (thời gian tới tiện ích có nguồn) ② người thuê thật (ai thuê, hợp đồng dài hạn) ③ giá vào và dòng tiền (thuê ròng/năm so với lãi vay).
- **Hai chiều:** *lý do kỳ vọng* (cầu thuê từ lao động/chuyển bay, hạ tầng nối) so với *lý do chờ* (nguồn cung mới, thời gian lấp đầy, hạ tầng nối chưa xong, lãi vay thả nổi). Không kết luận "chắc chắn tăng".
- **B-roll:** quay từ nơi công cộng; công trình đang vận hành (sân bay) có khu vực hạn chế/flycam cần giấy phép — dùng tư liệu có phép (xem `tuan-thu-noi-dung.md`).

## Biến thể khác (ghi chú nhanh)
- **C:** hai ghim/hai vòng hai màu; cùng 3 tiêu chí áp cho cả hai, một thẻ so sánh 2 cột ở khối 4; kết luận theo tiêu chí, không "khu nào hơn tuyệt đối".
- **D:** nền DARK + thẻ số + thẻ báo là chính; bản đồ chỉ ở bối cảnh (khu vực bị ảnh hưởng) và mốc theo dõi.
- **E:** các mốc năm là `line` hiện lần lượt dọc tuyến; tàu chạy theo thời gian thay vì theo km; luôn có cột "dự kiến".
