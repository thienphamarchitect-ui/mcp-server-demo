"""
MCP server mẫu cho Claude.

Cung cấp 4 nhóm công cụ (tool) đại diện cho các use-case phổ biến:
  1. Gọi API ngoài qua HTTP   -> http_get
  2. Truy vấn cơ sở dữ liệu   -> db_query / db_tables (SQLite demo)
  3. Thao tác file hệ thống   -> list_files / read_file / write_file
     (bị giới hạn trong thư mục WORKSPACE_DIR để an toàn)
  4. Voice Studio (TTS)       -> voice_list / voice_tts / voice_dialogue

Chạy qua stdio (mặc định) để dùng ngay với Claude Desktop hoặc Claude Code.
Nhóm 1-3 chỉ dùng thư viện chuẩn của Python (sqlite3, urllib) + SDK "mcp";
nhóm 4 (Voice Studio) cần thêm gói "edge-tts" (có trong requirements.txt).
"""

from __future__ import annotations

import json
import os
import sqlite3
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

# --------------------------------------------------------------------------
# Cấu hình chung
# --------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.resolve()

# Thư mục "an toàn" mà tool file được phép đọc/ghi. Không cho ra ngoài thư mục này.
WORKSPACE_DIR = BASE_DIR / "files"
WORKSPACE_DIR.mkdir(exist_ok=True)

# File SQLite demo (sẽ tự tạo + seed dữ liệu mẫu nếu chưa có).
DB_PATH = BASE_DIR / "data" / "demo.db"
DB_PATH.parent.mkdir(exist_ok=True)


def _seed_demo_db() -> None:
    """Tạo bảng + dữ liệu mẫu nếu DB chưa tồn tại, để tool db_query có gì mà thử."""
    if DB_PATH.exists():
        return
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                city TEXT
            )
            """
        )
        conn.executemany(
            "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
            [
                ("Nguyen Van A", "a.nguyen@example.com", "Ha Noi"),
                ("Tran Thi B", "b.tran@example.com", "Ho Chi Minh"),
                ("Le Van C", "c.le@example.com", "Da Nang"),
            ],
        )
        conn.commit()
    finally:
        conn.close()


_seed_demo_db()


def _resolve_in_workspace(relative_path: str) -> Path:
    """Ghép relative_path vào WORKSPACE_DIR và chặn mọi cách thoát ra ngoài (../, path tuyệt đối)."""
    candidate = (WORKSPACE_DIR / relative_path).resolve()
    if WORKSPACE_DIR not in candidate.parents and candidate != WORKSPACE_DIR:
        raise ValueError(
            f"Đường dẫn '{relative_path}' nằm ngoài thư mục được phép ({WORKSPACE_DIR})."
        )
    return candidate


# --------------------------------------------------------------------------
# Khởi tạo server
# --------------------------------------------------------------------------

server = MCPServer(
    name="demo-mcp-server",
    version="0.1.0",
    instructions=(
        "Server mẫu cung cấp 3 nhóm công cụ: gọi HTTP API ngoài (http_get), "
        "truy vấn cơ sở dữ liệu SQLite demo (db_query, db_tables), và thao tác "
        "file trong thư mục 'files/' của project (list_files, read_file, write_file), "
        "và Voice Studio chuyển văn bản thành giọng nói tiếng Việt/đa ngôn ngữ, lưu MP3 "
        "trong 'files/' (voice_list, voice_tts, voice_dialogue)."
    ),
)


# --------------------------------------------------------------------------
# Nhóm 1: Gọi API ngoài qua HTTP
# --------------------------------------------------------------------------

@server.tool()
def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = 10) -> str:
    """Gửi HTTP GET tới một URL và trả về nội dung response (dạng text, cắt ở 10,000 ký tự).

    Args:
        url: URL đầy đủ, bắt đầu bằng http:// hoặc https://
        headers: Header tùy chọn, ví dụ {"Authorization": "Bearer ..."}
        timeout: Thời gian chờ tối đa (giây)
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError("url phải bắt đầu bằng http:// hoặc https://")

    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return f"Lỗi khi gọi {url}: {e.reason}"

    snippet = body[:10000]
    truncated = "" if len(body) <= 10000 else "\n...(đã cắt bớt, nội dung dài hơn 10.000 ký tự)"
    return f"HTTP {status}\n{snippet}{truncated}"


# --------------------------------------------------------------------------
# Nhóm 2: Truy vấn cơ sở dữ liệu (SQLite demo)
# --------------------------------------------------------------------------

@server.tool()
def db_tables() -> str:
    """Liệt kê các bảng hiện có trong cơ sở dữ liệu demo."""
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    finally:
        conn.close()
    return json.dumps([r[0] for r in rows], ensure_ascii=False)


@server.tool()
def db_query(sql: str) -> str:
    """Chạy một câu lệnh SQL SELECT trên cơ sở dữ liệu demo và trả kết quả dạng JSON.

    Chỉ cho phép câu lệnh SELECT (chặn INSERT/UPDATE/DELETE/DROP... để an toàn).

    Args:
        sql: Câu lệnh SQL, ví dụ "SELECT * FROM customers WHERE city = 'Ha Noi'"
    """
    normalized = sql.strip().lower()
    if not normalized.startswith("select"):
        raise ValueError("db_query chỉ cho phép câu lệnh SELECT.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()

    result = [dict(row) for row in rows]
    return json.dumps(result, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------
# Nhóm 3: Thao tác file (trong thư mục an toàn WORKSPACE_DIR)
# --------------------------------------------------------------------------

@server.tool()
def list_files(subpath: str = ".") -> str:
    """Liệt kê file/thư mục con trong thư mục làm việc (files/).

    Args:
        subpath: Thư mục con cần liệt kê, mặc định là gốc của thư mục làm việc.
    """
    target = _resolve_in_workspace(subpath)
    if not target.exists():
        return f"Thư mục '{subpath}' không tồn tại."
    if not target.is_dir():
        return f"'{subpath}' không phải là thư mục."

    entries = []
    for p in sorted(target.iterdir()):
        kind = "dir" if p.is_dir() else "file"
        size = p.stat().st_size if p.is_file() else ""
        entries.append(f"[{kind}] {p.relative_to(WORKSPACE_DIR)} {size}")
    return "\n".join(entries) if entries else "(thư mục rỗng)"


@server.tool()
def read_file(relative_path: str) -> str:
    """Đọc nội dung một file văn bản trong thư mục làm việc (files/).

    Args:
        relative_path: Đường dẫn tương đối tới file, ví dụ "notes/todo.txt"
    """
    target = _resolve_in_workspace(relative_path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Không tìm thấy file '{relative_path}' trong thư mục làm việc.")
    return target.read_text(encoding="utf-8", errors="replace")


@server.tool()
def write_file(relative_path: str, content: str, overwrite: bool = False) -> str:
    """Ghi nội dung vào một file văn bản trong thư mục làm việc (files/).

    Tự tạo thư mục con nếu cần. Mặc định KHÔNG cho ghi đè file đã tồn tại
    (phải truyền overwrite=True để ghi đè).

    Args:
        relative_path: Đường dẫn tương đối tới file cần ghi, ví dụ "notes/todo.txt"
        content: Nội dung cần ghi
        overwrite: Cho phép ghi đè nếu file đã tồn tại
    """
    target = _resolve_in_workspace(relative_path)
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"File '{relative_path}' đã tồn tại. Truyền overwrite=True nếu muốn ghi đè."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Đã ghi {len(content)} ký tự vào '{relative_path}'."


# --------------------------------------------------------------------------
# Nhóm 4: Voice Studio — chuyển văn bản thành giọng nói (TTS)
#
# Dùng thư viện edge-tts (giọng neural của Microsoft Edge, miễn phí, không cần
# API key, có giọng tiếng Việt vi-VN-HoaiMyNeural (nữ) và vi-VN-NamMinhNeural
# (nam)). File âm thanh MP3 (+ phụ đề .srt) được ghi vào thư mục files/ để
# dùng tiếp với list_files/read_file hoặc lấy ra dựng video.
# --------------------------------------------------------------------------

DEFAULT_VOICE = os.environ.get("VOICE_DEFAULT", "vi-VN-HoaiMyNeural")


def _edge_tts():
    """Import edge-tts khi cần (server vẫn chạy được nếu chưa cài gói này)."""
    try:
        import edge_tts  # type: ignore
        import edge_tts.communicate as communicate  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "Chưa cài Voice Studio. Chạy: pip install -r requirements.txt (cần gói edge-tts)."
        ) from e

    # edge-tts luôn dùng CA của certifi; khi chạy sau proxy công ty / proxy có
    # CA riêng thì cho phép chỉ định CA bundle qua biến môi trường.
    ca_file = (
        os.environ.get("VOICE_CA_BUNDLE")
        or os.environ.get("SSL_CERT_FILE")
        or os.environ.get("REQUESTS_CA_BUNDLE")
    )
    if ca_file and Path(ca_file).is_file():
        import ssl

        communicate._SSL_CTX = ssl.create_default_context(cafile=ca_file)
    return edge_tts


def _check_audio_output(output: str, overwrite: bool) -> Path:
    if not output.lower().endswith(".mp3"):
        raise ValueError("output phải là file .mp3, ví dụ 'voice/intro.mp3'.")
    target = _resolve_in_workspace(output)
    if target.exists() and not overwrite:
        raise FileExistsError(f"File '{output}' đã tồn tại. Truyền overwrite=True nếu muốn ghi đè.")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


async def _synthesize(text: str, voice: str, rate: str, pitch: str, volume: str):
    """Trả về (audio_bytes, danh sách boundary để làm phụ đề)."""
    if not text.strip():
        raise ValueError("text không được để trống.")
    edge_tts = _edge_tts()
    comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume)
    audio = bytearray()
    boundaries = []
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
            boundaries.append(chunk)
    if not audio:
        raise RuntimeError("Không nhận được dữ liệu âm thanh — kiểm tra lại tên giọng (voice) hoặc kết nối mạng.")
    return bytes(audio), boundaries


@server.tool()
async def voice_list(language: str = "vi") -> str:
    """Liệt kê các giọng đọc có sẵn trong Voice Studio.

    Args:
        language: Lọc theo mã ngôn ngữ/locale, ví dụ "vi" (tiếng Việt), "en-US",
            hoặc "" để lấy tất cả.
    """
    edge_tts = _edge_tts()
    voices = await edge_tts.list_voices()
    prefix = language.lower()
    result = [
        {"voice": v["ShortName"], "locale": v["Locale"], "gender": v["Gender"]}
        for v in voices
        if not prefix or v["Locale"].lower().startswith(prefix)
    ]
    return json.dumps(result, ensure_ascii=False, indent=2)


@server.tool()
async def voice_tts(
    text: str,
    output: str = "voice/output.mp3",
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "+0%",
    subtitles: bool = True,
    overwrite: bool = False,
) -> str:
    """Chuyển văn bản thành giọng nói và lưu file MP3 trong thư mục files/.

    Args:
        text: Văn bản cần đọc (tiếng Việt hoặc ngôn ngữ của giọng đã chọn).
        output: Đường dẫn file .mp3 tương đối trong files/, ví dụ "voice/intro.mp3".
        voice: Tên giọng, ví dụ "vi-VN-HoaiMyNeural" (nữ) hoặc "vi-VN-NamMinhNeural" (nam).
            Xem voice_list để biết thêm.
        rate: Tốc độ đọc, ví dụ "+15%" (nhanh hơn) hoặc "-10%" (chậm hơn).
        pitch: Cao độ, ví dụ "+5Hz" hoặc "-5Hz".
        volume: Âm lượng, ví dụ "+20%".
        subtitles: Có xuất kèm file phụ đề .srt cùng tên hay không.
        overwrite: Cho phép ghi đè nếu file đã tồn tại.
    """
    target = _check_audio_output(output, overwrite)
    audio, boundaries = await _synthesize(text, voice, rate, pitch, volume)
    target.write_bytes(audio)

    msg = f"Đã tạo '{target.relative_to(WORKSPACE_DIR)}' ({len(audio):,} bytes, giọng {voice})."
    if subtitles and boundaries:
        edge_tts = _edge_tts()
        sub = edge_tts.SubMaker()
        for b in boundaries:
            sub.feed(b)
        srt_path = target.with_suffix(".srt")
        srt_path.write_text(sub.get_srt(), encoding="utf-8")
        msg += f" Phụ đề: '{srt_path.relative_to(WORKSPACE_DIR)}'."
    return msg


@server.tool()
async def voice_dialogue(
    lines: list[dict[str, str]],
    output: str = "voice/dialogue.mp3",
    rate: str = "+0%",
    overwrite: bool = False,
) -> str:
    """Tạo một file MP3 nhiều giọng (hội thoại, podcast, quảng cáo nhiều vai).

    Mỗi phần tử trong lines là {"voice": "<tên giọng>", "text": "<câu thoại>"};
    nếu bỏ "voice" sẽ dùng giọng mặc định. Các đoạn được ghép liền theo thứ tự.

    Args:
        lines: Danh sách câu thoại, ví dụ
            [{"voice": "vi-VN-NamMinhNeural", "text": "Chào chị!"},
             {"voice": "vi-VN-HoaiMyNeural", "text": "Chào anh, hôm nay thế nào?"}]
        output: Đường dẫn file .mp3 tương đối trong files/.
        rate: Tốc độ đọc chung, ví dụ "+10%".
        overwrite: Cho phép ghi đè nếu file đã tồn tại.
    """
    if not lines:
        raise ValueError("lines không được rỗng.")
    target = _check_audio_output(output, overwrite)

    # edge-tts luôn trả cùng một định dạng MP3 (24 kHz, mono, 48 kbps) nên có
    # thể ghép trực tiếp các frame MP3 mà không cần ffmpeg.
    combined = bytearray()
    for i, line in enumerate(lines, 1):
        text = (line.get("text") or "").strip()
        if not text:
            raise ValueError(f"Dòng {i} thiếu 'text'.")
        voice = line.get("voice") or DEFAULT_VOICE
        audio, _ = await _synthesize(text, voice, rate, "+0Hz", "+0%")
        combined.extend(audio)

    target.write_bytes(combined)
    return (
        f"Đã tạo '{target.relative_to(WORKSPACE_DIR)}' gồm {len(lines)} đoạn "
        f"({len(combined):,} bytes)."
    )


# --------------------------------------------------------------------------
# Entry point
#
# Chọn transport bằng biến môi trường MCP_TRANSPORT:
#   - "stdio" (mặc định): Claude Desktop/Code tự khởi chạy server như tiến
#     trình con. Dùng cho máy cá nhân, không cần auth.
#   - "http": chạy như một web service độc lập (streamable-http), để nhiều
#     client/máy kết nối chung qua mạng. Có API-key auth đơn giản qua
#     MCP_API_KEY (xem README.md phần "Chạy remote").
# --------------------------------------------------------------------------


def _run_http() -> None:
    """Chạy server ở chế độ streamable-http, bọc thêm 1 lớp kiểm tra API key.

    Không dùng cơ chế OAuth đầy đủ của SDK (cần issuer URL, metadata...) vì
    quá nặng cho một demo/service nội bộ. Thay vào đó, bọc ASGI app bằng một
    middleware tối giản: so khớp header Authorization: Bearer <token> với
    biến môi trường MCP_API_KEY. Nếu không đặt MCP_API_KEY, server chạy mà
    KHÔNG có auth (chỉ nên dùng khi đã tự giới hạn mạng, ví dụ VPN nội bộ).
    """
    import uvicorn
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    from starlette.types import ASGIApp, Receive, Scope, Send

    api_key = os.environ.get("MCP_API_KEY")
    host = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_HTTP_PORT", "8000"))

    inner_app = server.streamable_http_app(host=host)

    class ApiKeyMiddleware:
        """Middleware ASGI thuần: chặn request thiếu/sai Bearer token."""

        def __init__(self, app: ASGIApp, expected_key: str | None) -> None:
            self.app = app
            self.expected_key = expected_key

        async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
            if self.expected_key is None or scope["type"] != "http":
                await self.app(scope, receive, send)
                return

            headers = dict(scope.get("headers") or [])
            auth_header = headers.get(b"authorization", b"").decode("latin-1")
            token = auth_header.removeprefix("Bearer ").strip()

            if token != self.expected_key:
                response = JSONResponse(
                    {"error": "unauthorized", "message": "Thiếu hoặc sai Authorization: Bearer <MCP_API_KEY>."},
                    status_code=401,
                )
                await response(scope, receive, send)
                return

            await self.app(scope, receive, send)

    app: ASGIApp = ApiKeyMiddleware(inner_app, api_key)

    if api_key is None:
        print("[CẢNH BÁO] MCP_API_KEY chưa được đặt — server HTTP đang chạy KHÔNG có xác thực.")
    print(f"MCP server (streamable-http) đang chạy tại http://{host}:{port}/mcp")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    transport = os.environ.get("MCP_TRANSPORT", "stdio").lower()
    if transport == "http":
        _run_http()
    else:
        server.run(transport="stdio")
