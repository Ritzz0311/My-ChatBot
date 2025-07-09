# Use stable Python base image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (for packages like opencv, pyproj, rasterio, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libffi-dev \
    libpq-dev \
    python3-dev \
    python3-pip \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file first for caching
COPY requirements.txt .

# Remove audioop-lts (Python 3.13+ only)
RUN sed -i '/audioop-lts/d' requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run with Gunicorn for production (you can change app:app if your file is named differently)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
