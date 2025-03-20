# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p \
    config \
    utilities \
    bots \
    data/audiobackup

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DOCKER_CONTAINER=1

# Expose ports
EXPOSE 8000
EXPOSE 4455

# Command to run the application (default to GerryAI)
CMD ["python", "main.py", "--bot", "GerryAI"] 