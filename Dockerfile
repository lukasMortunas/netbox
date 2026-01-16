FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt base_requirements.txt ./

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application
COPY netbox/ ./netbox/
COPY manage.py ./

# Create media directory
RUN mkdir -p /app/media /app/static

# Expose port
EXPOSE 8000

# Run startup script
CMD ["/app/netbox/startup.sh"]
