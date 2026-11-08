# demo-mcp-server

Một MCP (Model Context Protocol) server mẫu viết bằng Python, cung cấp cho
Claude 9 công cụ chia làm 4 nhóm:

| Nhóm | Tool | Mô tả |
|---|---|---|
| Gọi API ngoài | `http_get` | Gửi HTTP GET tới một URL bất kỳ |
| Cơ sở dữ liệu | `db_tables` | Liệt kê bảng trong DB demo (SQLite) |
| | `db_query` | Chạy câu lệnh `SELECT` trên DB demo |
| Thao tác file | `list_files` | Liệt kê file/thư mục trong `files/` |
| | `read_file` | Đọc nội dung file trong `files/` |
| | `write_file` | Ghi file trong `files/` |
| Voice Studio (TTS) | `voice_list` | Liệt kê giọng đọc (lọc theo ngôn ngữ, mặc định `vi`) |
| | `voice_tts` | Đọc văn bản thành file MP3 (+ phụ đề `.srt`) trong `files/` |
| | `voice_dialogue` | Ghép nhiều câu thoại, nhiều giọng thành 1 file MP3 |

Nhóm 1–3 chỉ dùng thư viện chuẩn của Python (`sqlite3`, `urllib`) + SDK `mcp`.
Voice Studio dùng thêm gói [`edge-tts`](https://pypi.org/project/edge-tts/)
(đã có trong `requirements.txt`).

## Cài đặt

```bash
cd mcp-server-demo
pip install -r requirements.txt
```

## Chạy thử nhanh (không cần Claude)

```bash
python3 server.py
```

Lệnh này sẽ khởi động server ở chế độ `stdio` và chờ một MCP client kết nối
vào qua stdin/stdout (đây là cách Claude Desktop/Claude Code sẽ gọi nó —
bạn không cần tự chạy lệnh này khi đã khai báo trong config bên dưới).

## Đăng ký với Claude Desktop

Mở file config của Claude Desktop:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Thêm vào mục `mcpServers` (đổi `/duong/dan/toi` cho đúng máy bạn):

```json
{
  "mcpServers": {
    "demo-mcp-server": {
      "command": "python3",
      "args": ["/duong/dan/toi/mcp-server-demo/server.py"]
    }
  }
}
```

Khởi động lại Claude Desktop. Server sẽ xuất hiện trong danh sách công cụ
(biểu tượng cái búa 🔨) và các tool `http_get`, `db_query`, `read_file`...
sẽ có thể dùng trong hội thoại.

## Đăng ký với Claude Code

Trong thư mục project (hoặc global), chạy:

```bash
claude mcp add demo-mcp-server -- python3 /duong/dan/toi/mcp-server-demo/server.py
```

hoặc thêm trực tiếp vào `.mcp.json` của project:

```json
{
  "mcpServers": {
    "demo-mcp-server": {
      "command": "python3",
      "args": ["/duong/dan/toi/mcp-server-demo/server.py"]
    }
  }
}
```

## Voice Studio (chuyển văn bản thành giọng nói)

Voice Studio dùng giọng neural của Microsoft Edge qua thư viện `edge-tts`:
miễn phí, **không cần API key**, chất lượng tốt cho tiếng Việt.

Cài đặt: đã nằm trong `pip install -r requirements.txt` ở trên (hoặc riêng lẻ
`pip install edge-tts`). Server cần truy cập Internet tới
`speech.platform.bing.com` khi tạo giọng.

| Giọng tiếng Việt | Giới tính |
|---|---|
| `vi-VN-HoaiMyNeural` (mặc định) | Nữ |
| `vi-VN-NamMinhNeural` | Nam |

Gọi `voice_list` với `language=""` để xem toàn bộ giọng đa ngôn ngữ (vài trăm giọng).

Ví dụ yêu cầu với Claude:

- *"Đọc đoạn này bằng giọng nam, nhanh hơn 10%, lưu vào voice/intro.mp3"* →
  `voice_tts(text=..., voice="vi-VN-NamMinhNeural", rate="+10%", output="voice/intro.mp3")`
  — tạo `files/voice/intro.mp3` và `files/voice/intro.srt` (phụ đề có mốc thời gian,
  dùng thẳng cho CapCut/Premiere).
- *"Làm đoạn hội thoại 2 người giới thiệu dự án"* →
  `voice_dialogue(lines=[{"voice": "vi-VN-NamMinhNeural", "text": "..."}, {"voice": "vi-VN-HoaiMyNeural", "text": "..."}])`.

Tham số chỉnh giọng: `rate` (`"+15%"`, `"-10%"`), `pitch` (`"+5Hz"`),
`volume` (`"+20%"`). File chỉ được ghi trong `files/` và mặc định không ghi đè
(truyền `overwrite=True`).

Biến môi trường tùy chọn:

| Biến | Ý nghĩa |
|---|---|
| `VOICE_DEFAULT` | Giọng mặc định (mặc định `vi-VN-HoaiMyNeural`) |
| `VOICE_CA_BUNDLE` | File CA bundle khi chạy sau proxy có chứng chỉ riêng (báo lỗi `CERTIFICATE_VERIFY_FAILED`). Cũng đọc `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE` nếu có. |

## Mở rộng thêm tool

Thêm tool mới chỉ cần viết một hàm Python và gắn decorator `@server.tool()`
trong `server.py`:

```python
@server.tool()
def my_tool(x: int) -> str:
    """Docstring này sẽ hiển thị cho Claude như mô tả của tool."""
    return str(x * 2)
```

- Type hint của tham số quyết định schema mà Claude thấy — hãy khai báo rõ
  (`str`, `int`, `dict`, `list`, hoặc `Optional[...]`).
- Docstring chính là mô tả tool mà Claude dùng để quyết định khi nào gọi —
  viết rõ, có ví dụ nếu cần.
- Ném exception (`raise ValueError(...)`) khi input không hợp lệ; MCP sẽ
  trả lỗi đó lại cho Claude để nó tự sửa và gọi lại.

## An toàn

- `db_query` chỉ cho phép câu `SELECT`, chặn `INSERT/UPDATE/DELETE/DROP`.
- `read_file`/`write_file`/`list_files` bị giới hạn trong thư mục `files/`
  của project — không thể đọc/ghi ra ngoài (`../`, đường dẫn tuyệt đối đều
  bị chặn).
- `http_get` không có whitelist domain — nếu dùng với API có khóa bí mật,
  nên sửa code để đọc token từ biến môi trường (`os environ`) thay vì để
  Claude tự truyền token trong câu lệnh.

## Chạy remote (nhiều người/máy dùng chung một server)

Server hỗ trợ 2 transport, chọn bằng biến môi trường `MCP_TRANSPORT`:

| `MCP_TRANSPORT` | Khi nào dùng |
|---|---|
| `stdio` (mặc định) | Dùng một mình trên máy cá nhân — Claude Desktop/Code tự khởi chạy server như tiến trình con. Không cần auth. |
| `http` | Server chạy như một web service độc lập (streamable-http), nhiều người/máy kết nối chung qua mạng tới cùng 1 instance. |

### 1. Chạy trực tiếp bằng Python (mode http)

```bash
export MCP_TRANSPORT=http
export MCP_API_KEY=$(openssl rand -hex 32)   # bắt buộc nên đặt khi public ra internet
python3 server.py
```

Server lắng nghe ở `http://0.0.0.0:8000/mcp` (đổi bằng `MCP_HTTP_HOST`/`MCP_HTTP_PORT`).
Mọi request phải có header `Authorization: Bearer <MCP_API_KEY>`, thiếu hoặc
sai sẽ nhận `401`. Nếu không đặt `MCP_API_KEY`, server chạy **không auth** —
chỉ nên làm vậy khi server đã bị cách ly sau VPN/mạng nội bộ.

### 2. Chạy bằng Docker (đã có Dockerfile + docker-compose.yml)

```bash
export MCP_API_KEY=$(openssl rand -hex 32)
docker compose up --build -d
```

Mặc định publish port `8000`, mount 2 volume `./data` và `./files` ra ngoài
container để dữ liệu (DB demo, file người dùng tạo) không mất khi container
bị xoá/build lại. Image build từ `python:3.12-slim`, không cần gì thêm ngoài
Docker.

*Lưu ý: container này chưa được build/test thật trong môi trường có Docker
daemon (sandbox hiện tại không có `dockerd`) — Dockerfile dùng cấu trúc
chuẩn (pip install từ requirements.txt rồi copy code) nên về lý thuyết chạy
được ngay, nhưng bạn nên tự `docker compose up --build` một lần để xác nhận
trên máy/server thật trước khi dùng production.*

### 3. Deploy lên một VPS/cloud bất kỳ

Vì đã đóng gói bằng Docker, cách deploy giống nhau trên hầu hết nền tảng:

- **VPS tự quản (Ubuntu, Debian...)**: cài Docker, copy project lên, chạy
  `docker compose up -d`, rồi đặt Caddy hoặc nginx làm reverse proxy có TLS
  (Caddy tự lấy cert Let's Encrypt chỉ với vài dòng Caddyfile).
- **Fly.io / Render / Railway**: các nền tảng này build trực tiếp từ
  `Dockerfile` trong repo, chỉ cần khai báo biến môi trường `MCP_API_KEY`
  và port `8000` trong dashboard/CLI của họ.
- **Cloud Run (GCP)**: `gcloud run deploy --source .` — Cloud Run tự cấp
  HTTPS, chỉ cần set env `MCP_API_KEY`, `MCP_TRANSPORT=http`,
  `MCP_HTTP_PORT=8080` (Cloud Run quy định PORT qua biến `PORT`, nên map
  thêm `MCP_HTTP_PORT=$PORT` trong lệnh start).

Dù chọn nền tảng nào, luôn đặt HTTPS ở lớp ngoài (hầu hết PaaS tự làm; với
VPS tự quản thì cần Caddy/nginx) — token API không nên đi qua HTTP thường.

### 4. Kết nối Claude tới server remote

- **Claude Code**: `claude mcp add demo-mcp-server --transport http https://<host>/mcp --header "Authorization: Bearer <MCP_API_KEY>"`
- **Claude Desktop**: hiện cấu hình desktop chủ yếu hỗ trợ `command`/`args`
  (stdio) hoặc một mục `url` cho server HTTP tùy phiên bản — kiểm tra lại
  tài liệu Claude Desktop hiện hành vì phần này thay đổi khá nhanh.
- **Claude.ai**: thêm server qua mục "Connectors" / "Custom connector" của
  tổ chức, dán URL `https://<host>/mcp` — phần xác thực bằng API key tĩnh
  (như ở đây) phù hợp cho dùng nội bộ/cá nhân; nếu cần nhiều người dùng
  trong tổ chức với quyền riêng từng người, nên nâng cấp sang OAuth
  (SDK `mcp` hỗ trợ qua `auth`/`token_verifier` trong `MCPServer(...)`).
