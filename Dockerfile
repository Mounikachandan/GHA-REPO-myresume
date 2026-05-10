# ── Stage 1: base image ───────────────────────────────────────────────────────
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY myresume.py .

# Expose the port Flask runs on
EXPOSE 5000

# Run with gunicorn for production (falls back to Flask dev server if not installed)
CMD ["python", "myresume.py"]
