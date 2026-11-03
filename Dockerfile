# ---------- STAGE 1: Build dependencies ----------
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- STAGE 2: Runtime image ----------
FROM python:3.12-slim AS runtime

# Buat user non-root untuk keamanan
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy dependencies dari builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
COPY templates/ ./templates/

# Set PATH dan Environment Variables
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Ganti ke user non-root
USER appuser

EXPOSE 5000

# Healthcheck untuk Docker
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Jalankan dengan gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "app:app"]