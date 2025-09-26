FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/err
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies (if any needed for building wheels)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port Railway will map to $PORT
EXPOSE 8000

# Start the app (Railway sets $PORT). Default to 8000 if not set.
CMD ["sh", "-c", "uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-8000}"]