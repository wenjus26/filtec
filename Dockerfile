# Use official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (needed for mysqlclient, psycopg2, pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    default-libmysqlclient-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root group and user
RUN groupadd -r django && useradd -r -g django -d /app -s /sbin/nologin django

# Install python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and assign ownership to the non-root user
COPY --chown=django:django . /app/

# Make entrypoint script executable (performed while still root)
RUN chmod +x /app/docker-entrypoint.sh

# Switch to the non-root user
USER django

# Expose port 8000
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]
