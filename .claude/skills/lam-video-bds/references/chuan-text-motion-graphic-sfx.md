# Chuẩn Text · Motion · Graphic · Sound effect

Mọi thông số dưới đây lấy từ engine đã dùng dựng video Metro Đà Nẵng – Chu Lai (`engine.js`, `render.html`, `audio.py`), không phải số ước chừng.
Khung 1080×1920, 30 fps. Đơn vị px trừ khi ghi khác.

## 1. TEXT (chữ)

### Font và kiểu chữ
- **Source Sans 3** (giấy phép OFL), bộ ký tự latin + vietnamese đóng gói sẵn. Hiển thị: weight **900**; chip/ghi chú: 700; nguồn/miễn trừ: 600.
- `line()`: IN HOA, weight 900, co ngang `scaleX(.86)` (chữ gọn, không mất dấu tiếng Việt). Phụ đề: chữ thường, weight 900, không co ngang.
- Bóng chữ trắng: `0 0 18px rgba(0,0,0,.75), 0 0 4px rgba(0,0,0,.9), 0 6px 30px rgba(0,0,0,.6)`. Chữ cyan thêm quầng `0 0 22px rgba(5,244,232,.55)`.

### Cỡ chữ (cap = chiều cao chữ hoa; font-size = cap / 0,66)
| Vai trò | cap | Ví dụ trong video |
|---|---|---|
| Số hero | 190–230 | "266.000 TỶ" (210), "3 TIÊU CHÍ" (230) |
| Giá trị / tiêu đề chính | 100–150 | "95%" (150), "VỐN VAY" (150), "KHÁNH LINH" (150) |
| Tiêu đề phụ / nhãn | 40–66 | "TIÊU CHÍ 1" (62), "VỐN TỰ CÓ" (40) |
| Chip | font 58 | "3 NĂM LƯU TRÚ" |
| Phụ đề | font 50 | cụm ≤ 5 từ |
| Nguồn `src` / ghi chú `note` / miễn trừ `disc` | 30 / 28 / 25 | — |
| Brand | tên 44, dòng phụ 26; nhãn địa điểm 28; nhãn demo 26 (`BẢN DEMO · GIỌNG ĐỌC AI MẪU`) | góc trên |

**Chính sách cỡ chữ:** chữ mang thông tin (hero, nhãn, chip, `note`, `src`) ≥ 28 px; chỉ **câu miễn trừ** (25 px) và nhãn phụ ở góc được nhỏ hơn 30. Nhãn AI/demo ≥ 26 px để đọc được trên điện thoại.

### Màu chữ
Trắng `#FFFFFF` = nhãn, mô tả. Cyan `#05F4E8` = giá trị, điểm nhấn. Đỏ `#FF4D5E` = cảnh báo/giảm (không dùng cho số tăng). Vàng `#FFE600` = vòng bán kính, nhãn "20 KM", tô nhấn.

### Vùng an toàn
- y 0–230: brand (trái), nhãn địa điểm + nhãn demo (phải), thanh tiến trình 8px trên cùng.
- y 230–1560: nội dung chính (tiêu đề, số, thẻ báo, chip).
- y 1560–1670: **phụ đề**.
- y > 1670: dành cho giao diện nền tảng (nút, caption); chỉ để dòng nguồn/miễn trừ nhỏ.

**Bản đồ vùng y (chọn y cho từng thành phần):**
| y | Thành phần |
|---|---|
| 0–230 | brand, nhãn địa điểm, nhãn demo, thanh tiến trình |
| 230–1400 | hero, nhãn, chip, thẻ số, thẻ báo |
| 1400–1610 | nút CTA, chip mốc (cuối video; ở khối CTA không bật phụ đề) |
| 1434–1630 | thanh km (khi bật `kmbar`: không để chữ lớn ở đây) |
| 1560–1670 | phụ đề (chỉ bật khi không có thẻ nào ở y ≥ 1560) |
| ~1700 | dòng `src` 30 px, gồm chữ "minh hoạ"/"đo đường chim bay, minh hoạ" |
| ≥ 1760 | câu miễn trừ 25 px, cách đáy ~100 |

CTA là thẻ của người dẫn nên đặt trong 1400–1610, **không** để dưới y 1670 (bị giao diện nền tảng che).
- Lề ngang 70–90; dòng rộng > 950 tự co (`fit()`).

### Quy tắc nội dung
1. **Một ý một con số.** Số phụ đưa thành chữ nhỏ trên màn hình, đừng bắt người đọc đọc.
2. Hero ≤ ~24 ký tự; nhãn ≤ ~32 ký tự; chip ≤ ~22 ký tự; `note` ≤ ~60 ký tự (không tự co).
3. Mỗi cảnh ≤ 3 khối chữ **cùng lúc** (không tính phụ đề). Hook có thể có 4 dòng chữ nhưng phải **vào so le và ra dần** (0,25–0,6 s giữa các dòng; dòng trước ra/mờ khi dòng thứ tư vào) để tại mỗi thời điểm không quá 3 khối.
4. Số kiểu Việt: 1.234,5 (`count` có `decimals`); **năm viết tĩnh** (count sẽ ra "2.027").
5. Mọi số liệu có dòng nguồn + ngày; cuối video có câu miễn trừ (mẫu: `tuan-thu-noi-dung.md`). Chữ "minh hoạ" dùng `src` 30 px, y ≈ 1700, hiện cùng lúc với tuyến/vòng và ở lại đến hết cảnh đó.
6. Từ khoá giọng đọc nên có mặt bằng chữ trên màn hình (người xem tắt tiếng vẫn hiểu).

### Thời gian hiển thị
- ≤ 3 từ: tối thiểu 1,2 s; mỗi từ thêm +0,25 s; số liệu ≥ 2 s; thẻ báo ≥ 3 s; chip ≥ 1,5 s.
- `tin` = lúc giọng bắt đầu từ khoá (lấy từ khoảng lặng của `vo_prep.sh`) trừ ~0,05 s; `tout` = đầu cảnh sau.

### Khoảng cách (tránh dấu mũ chạm nhau)
Nhãn → số cap 150: tâm cách ≥ 155. Tiêu đề nhỏ → chữ hero: cách ≥ 0,9 × cap. Các chip: bước 150.

### Phụ đề (`captions()`)
Cụm ≤ 5 từ / ≤ 30 ký tự, tối đa 2 dòng, viền đen 10px, nhấn `*từ*` bằng cyan, vào bằng nảy nhẹ 0,14 s (scale .92→1). Tạo tự động từ lời đọc bằng `scripts/make_captions.py` (±0,2 s). Chỉ bật phụ đề ở cảnh không có thẻ nào ở y ≥ 1560.

## 2. MOTION (chuyển động)

### Hoạt ảnh chữ và thẻ
| Phần tử | Chuyển động | Thời lượng | Easing |
|---|---|---|---|
| `line` mặc định `track` | giãn chữ 0,55em → 0, mờ 10px → 0, hiện dần | 0,45 s (hiện 0,15 s) | expo-out |
| `line` `hero` | phóng 1,7 → 1, mờ 8px → 0 | 0,35 s | expo-out |
| `line` `count` | như hero + số đếm từ → đến | 0,35 s + 0,7 s | expo-out + cubic-out |
| `line` `pulse` | nhấp nhô ±6% | liên tục (9 rad/s) | sin |
| `paper` (thẻ báo) | trượt lên 700px, xoay +10° → góc, scale .88 → 1, đẩy chậm +3%/4 s; ra: trượt trái 1100px | vào 0,55 s | back (nảy) |
| `chip` | trượt từ trái 500px | 0,45 s | back |
| `raw` `pop` (CTA) | scale .3 → 1 rồi nhún | 0,5 s | back |
| `caption` | scale .92 → 1 | 0,14 s | back |
| Thoát chung | mờ dần | 0,12 s trước `tout` | tuyến tính |
| Kết video | tối dần | 0,6 s cuối | tuyến tính |

### Camera bản đồ
Toàn cảnh đẩy chậm +10% → bám tàu (trượt vào 1,4 s, giữ theo tàu) → keyframe: vị trí easeInOut (cubic), scale nội suy mũ (zoom đều mắt). Nhịp: zoom vào 1,5–3 s → giữ/đẩy chậm 1–3 s (lúc hiện số) → zoom ra 1,5–2 s. Ghim: xanh xám trước khi tàu qua, cyan + xung 1,3 s khi tàu qua. Vòng xung 3 sóng, chu kỳ ~1,8 s.

### Chuyển cảnh và hiệu ứng toàn khung
- Giao nhau MAP ↔ DARK: crossfade 0,3–0,35 s + whoosh.
- Flash trắng: đầu video (0,5 s, 100%), tại `drop` (0,35 s, 90%), chuyển cảnh mạnh (0,2–0,25 s, 35–40%).
- Glow cyan: 1–1,6 s (sin) ở khoảnh khắc nhấn. Sweep: vệt sáng quét qua thẻ báo 0,8 s sau khi thẻ vào 0,4 s.
- Tối bản đồ (`dim`) 38% khi có thẻ/số đè lên.

### Nhịp và đồng bộ
- 3 giây đầu phải có chữ lớn + chuyển động (hook). Hook ≤ 13 s.
- Có sự kiện hình mới mỗi 1,5–3 s; cảnh dài 8–16 s; đổi nền (MAP/DARK) 10–15 s một lần để nghỉ mắt.
- Các khối trong một cảnh vào so le 0,25–0,6 s; không hai hero cùng lúc.
- **Tiết tấu theo thông tin, không theo quãng đường**: chậm ở nơi có số liệu, lướt nhanh ở chỗ trống.

## 3. GRAPHIC (đồ hoạ)

### Hệ màu (token)
`--navy #06121C` nền · `--cy #05F4E8` nhấn chính · `--y #FFE600` vòng/nhấn phụ · đỏ `#FF4D5E`/`#E3172F` cảnh báo + nhãn nguồn · trắng chữ. Tối đa 4 màu; đừng thêm màu mới ngoài bảng mã nghĩa (ví dụ đỏ/vàng/cyan cho loại nút giao).

### Lớp từ dưới lên
Ảnh nền (MAP vệ tinh hoặc DARK: gradient navy + lưới cyan 90px 7% + 40 hạt) → tuyến/ghim/vòng → làm tối (dim) → **clip** (quay/B-roll) → chữ, thẻ, chip, phụ đề → flash/glow/sweep → vignette → brand/nhãn/thanh tiến trình.

### Xử lý bản đồ
Ảnh vệ tinh: `saturate 1.08, brightness 1.12, contrast 1.08`; gradient phủ trên 78% → 15% (ở 28%) → 0 (ở 50%) → 25% (75%) → 85% (đáy); thêm lớp xanh navy `multiply` 12%. Ghi nguồn ảnh góc dưới phải 22px.

### Thành phần
| Thành phần | Quy cách |
|---|---|
| Tuyến | nét mờ trắng có dash chạy (teaser) + nét neon vẽ dần: 4 lớp rộng 26/14/6/2,5 px (màn hình), cyan; lớp lõi trắng |
| Tàu | viên nang 148×40, trắng, viền cyan 3, 4 cửa sổ, sọc đỏ; kích thước cố định theo màn hình, xoay theo đường |
| Ghim | chấm cyan r=20 (r=30 khi xung), số trong chấm; nhãn nền navy 88%, viền cyan 3, chữ trắng 34; `dot` r×0,55 |
| Vòng | vàng, nét 4–5 px màn hình; `static`: đứt nét 26/16, nền 6%, đường bán kính, nhãn vàng chữ navy |
| Thẻ báo | nền trắng, bo 22, đệm 18, nhãn đỏ góc trên trái ("TÊN BÁO · NGÀY"); biến thể `dark` viền cyan cho "nguồn chủ đầu tư" |
| Chip | cao 116, nền navy 78%, viền cyan 3, icon tròn cyan 70 |
| CTA | 820×170, bo 90, nền cyan, chữ navy 66 |
| Miễn trừ | 25px, trắng 78%, cách đáy 100 |
| Brand | thanh cyan 12×64 + tên 44 + dòng phụ 24 cyan |
| Thẻ khu vực (`zones`) | thẻ trắng bo 10, sọc màu trái 9, dòng nhỏ "KHU VỰC" 15 (màu loại) + tên 30 đậm; đường dẫn 3 + chấm 7; viền polygon 4 (quầng 11), nền 13%; màu theo loại: vàng cam KCN, đỏ khu đô thị, tím cảng, cam sân bay, xanh lá ranh đô thị/du lịch, xanh dương ranh hành chính |
| Thanh km (`kmbar`) | dòng nhỏ cyan 26 (giãn 4) + tiêu đề trắng 56; thanh 900px, chấm ga 16 đặt đúng tỷ lệ km, đầu thanh 22 + số km 28; chiếm y 1434–1630 |
| Logo | thẻ trắng bo 22, đệm 10, 120×120, góc trên phải (cách mép 54) |

### Clip (người dẫn / cảnh trám)
`clip()` ghép chuỗi ảnh tách từ video quay: toàn khung (`cover`) hoặc khung nhỏ bo góc (viền cyan, đổ bóng). Thêm lớp tối phía sau chữ. Vào/ra mờ 0,2 s. Tách khung: `ffmpeg -i in.mp4 -vf "fps=30,scale=1080:-2" clips/a/%05d.jpg`; tiếng của clip thêm vào `timeline.vo`.

### Nguyên tắc nhất quán
Một bộ màu cho cả loạt video; cùng vị trí brand/nhãn; mã màu nhãn cố định; không che quá ~50% bản đồ; chữ luôn có bóng/viền để đọc được trên mọi nền.

## 4. SOUND EFFECT và nhạc

### Bộ SFX tổng hợp (không dính bản quyền)
| Tên | Âm | Dài | Dùng khi | Gain mặc định |
|---|---|---|---|---|
| `whoosh` | nhiễu băng 2,5 kHz + quét 300→1700 Hz | 0,55 s | chuyển cảnh, thẻ báo vào, zoom ra | −2…−3 dB |
| `pop` | sin 900→250 Hz tắt nhanh | 0,12 s | chữ trắng vào, CTA | 0 |
| `ting` | 4 bội âm 1568/2352/3136/4704 Hz | 0,9 s | giá trị cyan | 0 |
| `impact` | sin 110→42 Hz + nhiễu 60–3000 Hz | 1,6 s | số hero, drop | −3…−6 dB (drop 0) |
| `riser` | nhiễu 0,8–9 kHz tăng dần + sin 200→1100 Hz | 2,3 s | 1,5–2 s trước drop | −4 |
| `shutter` | 2 tiếng click cách 0,07 s | 0,16 s | thẻ báo vào (+0,32 s) | −3 |
| `heartbeat` | 2 nhịp 60→40 Hz | 0,7 s | hồi hộp trước drop | −2 |
| `notify` | 2 nốt 1318/1976 Hz | 0,45 s | chip vào | −1 |
| `cash` | ting + 6 nhiễu cao | 0,9 s | số tiền | −2 |
| `sparkle` | 9 nốt ngẫu nhiên 2,5–6 kHz | 1,0 s | tên dự án/người, CTA | −4 |

### Quy tắc gắn
Chữ trắng → `pop`; giá trị cyan → `ting`; số hero → `impact`; thẻ báo → `whoosh` + `shutter`; chip → `notify`; chuyển cảnh/zoom ra → `whoosh`; trước drop → `riser` (+ `heartbeat`); tên/CTA → `sparkle`; số tiền → `cash`. Mỗi SFX đặt đúng `tin` của phần tử.
Giới hạn: ≤ 3 SFX mỗi giây; `impact` cách nhau ≥ 3–4 s; không đặt SFX lớn đè lên từ khoá của giọng.
**Ngoại lệ riser:** `riser` bắt đầu 1,5–2 s trước `drop`, tức nằm dưới câu cuối của khối trước. Chấp nhận được vì riser là tiếng nền tăng dần (−4 dB, 0,8–9 kHz), không phải âm tức thời; đặt nó **sau** từ khoá của câu đó (từ khoá đã được đọc) và không để `impact`/`pop` nào trong cùng khoảng.

### Nhạc nền
Tổng hợp Am–F–C–G, 100 BPM (nhịp 0,6 s). Cấu trúc: vào nhạc (`start`) → kick nhẹ (`beatsFrom`) → mỏng dần và im (`breakdown`) → **drop** full beat + impact + flash → chỉ còn pad (`outro`) → tắt dần 2 s. Đặt `drop` vào thẻ/câu chốt (khoảng 40% độ dài nếu không có khoảnh khắc nào nổi bật).

### Mix (từ audio.py)
- Giọng: chuẩn RMS 0,12, nén mềm `tanh`, ưu tiên cao nhất.
- Nhạc ×0,9, **hạ 55% khi có giọng** (cửa sổ 150 ms). SFX ×0,55 và (gain − 6 dB).
- Master: `loudnorm` **−14 LUFS**, đỉnh thật −1,0 dBTP, LRA 9, 48 kHz.
- Kiểm: `ffmpeg -i out.mp4 -af ebur128 -vn -f null -`; nghe bằng tai (Claude không nghe được âm thanh).

### Giới hạn hiện tại (cần cải tiến nếu muốn chuyên nghiệp hơn)
SFX và nhạc là tổng hợp đơn giản, mono-ra-stereo; chưa EQ/khử ồn cho giọng; chưa sidechain SFX. Bản đăng thương mại nên thay nhạc bằng bản có giấy phép (căn `drop` của bài vào `TL.drop`).
