# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure app.log file exists for logging
RUN touch /app/app.log /app/celery_worker.log /app/celery_beat.log

# Set environment variables for logging (optional)
ENV LOG_FILE=/app/app.log
ENV LOG_LEVEL=INFO

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app using Uvicorn with log forwarding
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.ini"]
