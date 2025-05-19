FROM python:3.10-slim

# Install system dependencies for OpenCV, Tesseract and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main"]
