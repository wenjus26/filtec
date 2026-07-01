# FILTEC Polyplast — B2B Deployment Guide

This guide outlines instructions to build, configure, and deploy the containerized **FILTEC Polyplast** Django application using Docker and MySQL.

---

## Architecture Overview

The application is fully containerized and runs on a dedicated bridge network containing:
1. **Web Service (`filtec-web`)**: Running Django inside a Python 3.12-slim container under a secure non-root `django` user account.
2. **Database Service (`filtec-mysql`)**: Running a MySQL 8.0 server with volume-persisted storage.
3. **Network (`filtec-network`)**: A private virtual network bridge separating B2B service communication.

---

## Prerequisites

Ensure you have the following installed on your machine:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)
* Git

---

## Getting Started (Quick Run)

### 1. Configure the Environment
Check the environment variables defined in the `.env` file at the root of the project. For the local docker environment, the database values are automatically overridden by the `docker-compose.yml` variables to ensure plug-and-play operations.

### 2. Build and Start Containers
Run the following command in your terminal at the project root:
```bash
docker-compose up --build -d
```
*The `-d` flag runs the containers in detached (background) mode.*

### 3. Automated Entrypoint Pipeline
During startup, the container entrypoint script automatically handles the database pipeline:
1. Waits for the MySQL database container port to become online and accepting TCP sockets.
2. Generates initial database migrations.
3. Runs DB schema migrations.
4. Seeds the MySQL database with initial B2B products and events.
5. Starts the Django web server binding to port `8000` (mapped to host port `8001`).

---

## Verification & URLs

Once the build is complete, you can access the application through the following endpoints:

* **Public Web Portal**: [http://127.0.0.1:8001/](http://127.0.0.1:8001/)
* **Admin Portal**: [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/)

---

## Post-Deployment Operations

### 1. Create a Django Superuser
To log into the Django Admin portal (`/admin/`), run the following command to create an administrator account:
```bash
docker-compose exec web python manage.py createsuperuser
```
Follow the prompts in your terminal to set the username, email, and password.

### 2. Re-seeding the Database
To reset and re-seed the products and events tables at any time, run:
```bash
docker-compose exec web python seed_db.py
```

---

## Helpful Commands Cheat Sheet

* **Stop the Services**:
  ```bash
  docker-compose down
  ```
* **Stop and Purge Database Volume (Fresh DB Start)**:
  ```bash
  docker-compose down -v
  ```
* **View Container Logs**:
  ```bash
  docker-compose logs -f web
  ```
* **Run a Django Shell inside the container**:
  ```bash
  docker-compose exec web python manage.py shell
  ```

---

## VPS / Ubuntu Server Deployment Guide

To deploy the application to your Ubuntu VPS at `ubuntu@vps-95353d2f:/var/www/customer/filtec/filtec`, follow these steps:

### 1. Transfer Project Files to VPS
You can transfer your project files to your VPS directory using `rsync` or by cloning from your repository:
```bash
# Example using rsync from your local machine:
rsync -avz --exclude 'db.sqlite3' --exclude '.git' --exclude '__pycache__' ./ ubuntu@vps-95353d2f:/var/www/customer/filtec/filtec/
```

### 2. Install Docker & Docker Compose on Ubuntu VPS
If Docker is not yet installed on your VPS, run the following commands on your Ubuntu terminal:
```bash
# Update package list
sudo apt-get update

# Install Docker dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine & Compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
sudo docker compose version
```

### 3. Build & Run on VPS
Navigate to the directory on your VPS and spin up the containers:
```bash
cd /var/www/customer/filtec/filtec
sudo docker compose up --build -d
```
*The entrypoint pipeline will automatically run migrations and pre-seed the MySQL database.*

### 4. Configure Nginx Reverse Proxy (Recommended)
To expose the site securely on ports `80` (HTTP) / `443` (HTTPS) with a domain name, configure Nginx as a reverse proxy:

1. Install Nginx:
   ```bash
   sudo apt-get install -y nginx
   ```
2. Create a configuration file `/etc/nginx/sites-available/filtec`:
   ```nginx
   server {
       listen 80;
       server_name filtec.in www.filtec.in;  # Replace with your domain / VPS IP

       location / {
           proxy_pass http://127.0.0.1:8001;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /var/www/customer/filtec/filtec/staticfiles/;
       }

       location /media/ {
           alias /var/www/customer/filtec/filtec/media/;
       }
   }
   ```
3. Enable the site and restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/filtec /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

