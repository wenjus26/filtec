# Use official lightweight Python image
FROM python:3.12-slim

# Ensure dos2unix is available to fix Windows line endings

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
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root group and user with UID/GID 1000 (matches 'ubuntu' user on VPS host)
RUN groupadd -r -g 1000 django && useradd -r -u 1000 -g django -d /app -s /sbin/nologin django

# Install python packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and assign ownership to the non-root user
COPY --chown=django:django . /app/

# Fix Windows CRLF line endings on entrypoint (performed while still root)
RUN dos2unix /app/docker-entrypoint.sh && chmod 755 /app/docker-entrypoint.sh

# Switch to the non-root user
USER django

# Expose port 8000
EXPOSE 8000

# Run entrypoint script via sh explicitly (avoids execute permission issues)
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
