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
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app/src"
ENV ENABLE_GUI="true"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5555
EXPOSE 5000

COPY . .

CMD ["xvfb-run", "--server-args=-screen 0 640x480x24", "python", "-m", "src.main"]
