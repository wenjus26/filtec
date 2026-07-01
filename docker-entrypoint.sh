#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "Waiting for MySQL database at $DB_HOST:$DB_PORT..."

python -c "
import socket
import time
import sys

port = int('$DB_PORT')
host = '$DB_HOST'
start = time.time()
while time.time() - start < 60:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
        print('MySQL is online and responding!')
        sys.exit(0)
    except Exception:
        time.sleep(1.5)
print('Error: MySQL wait timeout reached!')
sys.exit(1)
"

echo "Applying Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding the FILTEC database with initial B2B products and events..."
python seed_db.py

echo "Starting FILTEC Polyplast web server..."
exec python manage.py runserver 0.0.0.0:8000
