FROM python:3.10-slim

# Install system dependencies for OpenCV, Tesseract and FFmpeg
RUN apt-get update && apt-get install -y \
    mgba-sdl \
    ffmpeg \
    tesseract-ocr \
    libopencv-dev \
    libsm6 \
    libxext6 \
    libzmq3-dev \
    python3-numpy \
    python3-pil \
    xdotool \
    xvfb \
    x11-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PROFILE=release
ENV PYTHONPATH=/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5555
EXPOSE 5000

COPY . .

CMD ["bash", "-c", "Xvfb :1 -screen 0 1280x1024x24 & export DISPLAY=:1 && python -m src.main"]
