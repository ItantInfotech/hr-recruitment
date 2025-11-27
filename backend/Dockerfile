FROM python:3.12-slim

# Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project (we will mount source as volume in dev, but copy for safety)
COPY src /app/

EXPOSE 8000
