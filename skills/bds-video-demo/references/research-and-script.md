# Nghiên cứu số liệu & viết kịch bản

## Mục lục
1. Nguồn tin uy tín và cách tìm
2. Quy tắc trung thực (bắt buộc đọc)
3. Chụp ảnh báo làm "báo chứng"
4. Ba cấp kịch bản: đầy đủ dài, video ngắn 75s, kịch bản sản xuất
5. Công thức hook, giữ chân, CTA

---

## 1. Nguồn tin uy tín và cách tìm

Ưu tiên theo thứ tự:
1. **Báo cáo thị trường**: DKRA, CBRE, Savills, Avison Young, JLL, Batdongsan.com.vn (báo cáo quý), Bộ Xây dựng / Sở Xây dựng.
2. **Văn bản nhà nước**: Nghị quyết HĐND về bảng giá đất, Quyết định Thủ tướng (quy hoạch, khu thương mại tự do, trung tâm tài chính), danh mục kêu gọi đầu tư.
3. **Báo chính thống**: Tuổi Trẻ, VnExpress, Thanh Niên, Dân Trí, Báo Đầu Tư, CafeF, VietnamFinance, Báo Xây dựng, Người Lao Động, Báo Chính phủ, cổng thông tin tỉnh/thành.
4. **Trang chủ đầu tư**: chỉ dùng cho thông tin sản phẩm (vật liệu, tiện ích, mốc cất nóc). Luôn ghi "Nguồn: chủ đầu tư" trên video.

Tránh làm "báo chứng": trang môi giới, blog dự án, bài có nhãn **"Nội dung được tài trợ" / "Thông tin doanh nghiệp"** (VnExpress, CafeF hay có). Có thể đọc để lấy ý nhưng không cắt ảnh làm bằng chứng.

Cách tìm (WebSearch `mode: extended` cho tin mới): chạy song song 3–4 truy vấn, ví dụ:
- `bất động sản <TP> <năm> khu vực tăng giá giá đất số liệu`
- `DKRA <TP> quý <N> <năm> căn hộ giá sơ cấp`
- `<TP> bảng giá đất <năm> tăng bao nhiêu phần trăm`
- `<chủ đầu tư> dự án <năm>` + `<dự án> Sở Xây dựng đủ điều kiện bán`
Sau đó WebFetch từng bài để **trích nguyên văn số liệu + ngày đăng**. Không dùng số từ tóm tắt tìm kiếm khi chưa mở bài.

Ghi cho mỗi số liệu: con số · đơn vị · khu vực · kỳ (quý/năm) · tên báo · ngày đăng · URL.

## 2. Quy tắc trung thực

Người xem là nhà đầu tư thật; một con số sai làm mất uy tín kênh và có thể bị khiếu nại.

- **Nếu thị trường đang giảm, nói thẳng.** Biến nó thành luận điểm ("dòng tiền chọn lọc", "tiền đổi chỗ") thay vì giả vờ "sốt giá". Ví dụ đã dùng: DKRA Q3/2026 tiêu thụ căn hộ Đà Nẵng −25% → hook "Thị trường đang giảm, nhưng 4 vùng vẫn tăng".
- **Bảng giá đất ≠ giá giao dịch.** Bảng giá là giá Nhà nước dùng tính nghĩa vụ tài chính. Luôn có dòng chú thích trên màn hình.
- **Không nói "chứng nhận xanh / công trình bền vững được chứng nhận"** (LOTUS, EDGE, LEED) trừ khi tìm thấy chứng nhận. Thay bằng mô tả vật liệu cụ thể (kính Low-E, đá tự nhiên, sơn nhiều lớp) — đó mới là "bằng chứng độ hoàn thiện".
- **Số liệu lệch giữa các nguồn** (vốn 1.500 hay 1.520 tỷ; 260 hay 265 căn): dùng con số an toàn ("hơn 1.500 tỷ", tổng số căn đã được xác nhận) và ghi chú trong kịch bản.
- **Không hứa lợi nhuận**: tránh "chắc chắn tăng", "lãi x%", "cam kết". Kết video bằng "Nội dung tham khảo, không phải khuyến nghị đầu tư".
- Nếu video là hợp tác/được trả tiền bởi chủ đầu tư → nhắc người dùng bật nhãn "Paid partnership".
- Kiểm tra lại mọi con số trong lời đọc TTS (đã từng viết nhầm 3.525 thành "ba nghìn năm trăm").

## 3. Chụp ảnh báo làm "báo chứng"

`scripts/capture_news.js` (xem đầu file). Tạo `news.json` liệt kê bài + từ khoá cần tô vàng:
```bash
node scripts/capture_news.js news.json <project>/assets
```
Mỗi bài cho `_head.png` (tiêu đề + ngày + sapo), `_quote.png` (đoạn có từ khoá, tô vàng), `_imgN.png`.
Luôn ghép thumbnail và nhìn lại: lỗi hay gặp
- h1 là logo → `_head.png` chỉ vài chục px. Cách sửa: chụp toàn trang viewport rồi crop vùng tiêu đề bằng PIL.
- Quảng cáo nổi ("Build a New Christmas Toy…") đè lên ảnh/đoạn → crop bỏ phần đó.
- Đoạn tô vàng dính ảnh bên cạnh → crop chiều rộng.
Ngoài ra nên chụp bộ ảnh "toàn trang" (tiêu đề + đoạn số liệu, khung 1080x1350 @2x) để người dùng tự dựng: đặt tên `NN-<báo>-<chủ đề>-A-tieude.png` / `-B-solieu.png`.

**Bản quyền**: ảnh chụp tiêu đề báo dùng để trích dẫn nguồn là hợp lý; **ảnh minh hoạ trong bài là của báo** — chỉ dùng cho bản demo, bản đăng công khai thay bằng B-roll tự quay / ảnh chủ đầu tư cung cấp.

## 4. Ba cấp kịch bản

Người dùng thường đi lần lượt: kịch bản tổng → "như chuyên gia video ngắn" → "đầy đủ". Có thể làm cả ba, lưu `.md` trong repo.

### 4.1 Kịch bản tổng (2–4 phút)
Bảng `Hình ảnh | Lời thoại` theo phần: Hook → Bức tranh thật → Các khu vực (mỗi khu: số liệu + ảnh báo) → Chủ đầu tư & sản phẩm đón đầu xu hướng → Độ hoàn thiện/chất lượng (vật liệu, công trình đã vận hành) → Kết + CTA. Cuối file: bảng danh sách ảnh báo + nguồn, mục "Lưu ý trước khi đăng".

### 4.2 Video ngắn ~60–75s (chuẩn short-form)
- Bảng 0–3s, 3–8s… với cột: Hình ảnh/Dựng · Lời thoại · Text on-screen · SFX.
- 3 phương án hook để A/B test, khuyến nghị 1.
- Nhịp đổi khung 2–3s, "pattern interrupt" mỗi 5–7s, ảnh báo mỗi 7–8s.
- Mục kỹ thuật giữ chân (open loop "số 4 mới đáng tiền nhất", giữ thứ hay nhất cuối danh sách, nối số liệu → sản phẩm để không lộ quảng cáo, CTA từ khoá, loop liền mạch).
- Cover, caption, hashtag, comment ghim nguồn.

### 4.3 Kịch bản sản xuất đầy đủ (~2:45)
- Tổng quan (persona, thông số, khán giả, mục tiêu KPI), cấu trúc 7 phần.
- Shot-by-shot: CẢNH n · thời gian · góc máy (MCU/CU/WS) · lời thoại nguyên văn · text · ảnh báo [BÁO-xx-A/B] · B-roll · SFX/nhạc · ghi chú dựng.
- **Lời đọc liền mạch cho teleprompter** (/ = ngắt ngắn, // = ngắt dài, in đậm = nhấn).
- Shot list người dẫn, B-roll (đánh dấu cái nào xin chủ đầu tư), motion graphic, nhạc/SFX theo đoạn.
- Đăng bài + bản cắt 60s (map cảnh nào giữ) + checklist pháp lý + nguồn.

## 5. Công thức

- **Hook đối lập**: "Thị trường X đang giảm — nhưng có N vùng giá vẫn tăng." (đúng số liệu + tò mò)
- **Hook số sốc**: "Có nơi giá đất vừa tăng 70%. Nhưng đừng vội mua."
- **Hook nỗi sợ**: "Mua sai khu năm nay là kẹp hàng."
- **Open loop**: "Vùng thứ 4 mới là vùng tôi thấy đáng tiền nhất" → dừng nhạc 0,5s → drop khi lộ tên.
- **Cầu nối sang chủ đầu tư**: "Cùng một vùng, có dự án giữ giá, có dự án cắt lỗ. Khác nhau ở chủ đầu tư." (dẫn lại câu của báo: thanh khoản tập trung ở dự án quy mô lớn, chủ đầu tư uy tín).
- **CTA từ khoá**: "Bình luận '<TÊN>' để nhận bảng so sánh" → lọc lead.
