FROM python:3.10-slim

# Install system dependencies for OpenCV, Tesseract and FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tesseract-ocr \
    libopencv-dev \
    libsm6 \
    libxext6 \
    libzmq3-dev \
    mgba-sdl \
    python3-numpy \
    python3-pil \
    xdotool \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main"]
