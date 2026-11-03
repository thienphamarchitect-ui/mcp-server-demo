FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# Dữ liệu demo sẽ được tạo lại tự động nếu không tồn tại (xem _seed_demo_db
# trong server.py), nhưng khai báo volume để dữ liệu + file người dùng tạo ra
# không mất khi container bị thay/khởi động lại.
RUN mkdir -p /app/data /app/files
VOLUME ["/app/data", "/app/files"]

ENV MCP_TRANSPORT=http \
    MCP_HTTP_HOST=0.0.0.0 \
    MCP_HTTP_PORT=8000

EXPOSE 8000

CMD ["python3", "server.py"]
