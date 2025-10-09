FROM python:3.12-slim

# Install system dependencies for tesseract, Pillow, and cron
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy default crontab (can be overridden by docker-compose volume)
COPY crontab /etc/cron.d/chronique-cron
RUN chmod 0644 /etc/cron.d/chronique-cron && \
    crontab /etc/cron.d/chronique-cron

# Ensure the script is executable
RUN chmod +x /app/main.py

# Expose port (optional, for logs or debug)
EXPOSE 8000

# Start cron in the foreground
CMD ["cron", "-f"]
