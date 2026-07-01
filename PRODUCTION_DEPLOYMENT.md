# End-to-End Production Deployment Guide for web.filtec.in

This guide details the complete setup to deploy the **FILTEC Polyplast** Django & MySQL application on your Ubuntu VPS under the domain **`web.filtec.in`** with full SSL encryption.

---

## Deployment Architecture

```
[Internet] ---> [Ports 80/443] ---> [Host Nginx (SSL / Certbot)]
                                          |
                                    [Port 8040]
                                          |
                                          v
                              [Docker Nginx (Port 80)]
                                          |
                                    (filtec-network)
                                          |
                                          v
                               [Django Web (Port 8000)]
                                          |
                                          v
                                [MySQL DB (Port 3306)]
```

* **No direct exposure**: Neither Gunicorn/Django nor MySQL expose ports to the public internet. They run securely inside the virtual Docker network.
* **Host Nginx**: Serves as the primary entry point, handling Let's Encrypt SSL certificates, and proxies traffic to the internal container on port `8040`.

---

## Phase 1: DNS Configuration

Before starting, point your subdomain to your VPS IP:
1. Log into your domain registrar (e.g., GoDaddy, Cloudflare, Namecheap).
2. Go to the **DNS Management Panel** for `filtec.in`.
3. Add a new **A Record**:
   * **Host/Name**: `web`
   * **Value/IP**: `YOUR_VPS_IP_ADDRESS` (The public IP of `vps-95353d2f`)
   * **TTL**: Auto or 3600 seconds.

---

## Phase 2: Host VPS Initial Setup

Connect to your VPS:
```bash
ssh ubuntu@web.filtec.in
```

### 1. Update Packages & Install Nginx + Certbot
Run these commands to install the required system tools:
```bash
sudo apt-get update
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

### 2. Install Docker & Docker Compose
If Docker is not yet installed on the VPS, run:
```bash
# Install Docker dependencies
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's GPG Key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```


---

## Phase 2.5: Environment Variables Configuration (.env)

At the root of the project directory `/var/www/customer/filtec/filtec`, you must create a `.env` file containing the environment configurations. This keeps passwords and security credentials secure.

Create the file:
```bash
nano /var/www/customer/filtec/filtec/.env
```

Paste the following configuration:
```ini
# Django Configuration
SECRET_KEY=generate-a-secure-random-secret-key-for-production-here
DEBUG=False
ALLOWED_HOSTS=web.filtec.in,localhost,127.0.0.1

# Database Configuration
DB_ENGINE=mysql
DB_NAME=filtec_db
DB_USER=filtec_user
DB_PASSWORD=filtec_password
DB_HOST=filtec-mysql
DB_PORT=3306
```

---

## Phase 3: Transfer & Build the Code

### 1. Synchronize Project Files
Ensure your project files are synced to `/var/www/customer/filtec/filtec`.

### 2. Launch the Docker Stack
Build and launch the isolated containers in background mode:
```bash
cd /var/www/customer/filtec/filtec
sudo docker compose up --build -d
```
* **What happens now?**: The entrypoint script waits for the database, runs migrations, aggregates static files into a shared volume, seeds the products/events content, and starts the Django server internally.

---

## Phase 4: Configure Host Nginx & Let's Encrypt SSL

### 1. Configure the Nginx Proxy Server Block
Create a new configuration file for Nginx:
```bash
sudo nano /etc/nginx/sites-available/filtec
```

Paste the following configuration:
```nginx
server {
    listen 80;
    server_name web.filtec.in;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8040;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration and reload Nginx:
```bash
# Link the site configuration
sudo ln -s /etc/nginx/sites-available/filtec /etc/nginx/sites-enabled/

# Remove the default default site if active to avoid conflicts
sudo rm /etc/nginx/sites-enabled/default || echo "Default already removed"

# Test configuration syntax
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 2. Request SSL Certificate (HTTPS)
Use Certbot to request a free SSL certificate from Let's Encrypt and automatically configure HTTPS redirection:
```bash
sudo certbot --nginx -d web.filtec.in
```
Follow the interactive prompts:
* Provide your email address for renewal reminders.
* Agree to terms of service.
* **Choose Redirect**: Select Option `2` to redirect all HTTP traffic to secure HTTPS.

---

## Phase 5: Post-Deployment Administration

### 1. Create a Django Superuser
Create an administrator credentials account inside the running Django web container:
```bash
sudo docker compose exec web python manage.py createsuperuser
```

### 2. Check Service Logs
If you encounter issues, inspect active container processes:
```bash
sudo docker compose logs -f web
sudo docker compose logs -f nginx
```

### 3. Renewal of SSL Certificates
Let's Encrypt certificates are valid for 90 days. Certbot automatically adds a system cron job to handle renewal. Test it with:
```bash
sudo certbot renew --dry-run
```
