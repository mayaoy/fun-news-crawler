FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV CRAWL_INTERVAL=10
ENV DB_PATH=/app/data/news.db

# 移除 CMD，讓 docker-compose 的 command 來控制啟動流程 