#!/bin/bash

# Exit on error
set -e

# Update and upgrade packages
echo "Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    nginx \
    nodejs \
    npm \
    certbot \
    python3-certbot-nginx

# Install PM2 globally
echo "Installing PM2..."
sudo npm install -g pm2

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt gunicorn

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd frontend
npm install
npm run build
cd ..

# Set up Nginx
echo "Configuring Nginx..."
sudo cp nginx-config /etc/nginx/sites-available/portfolio
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Create systemd service for Gunicorn
echo "Creating systemd service..."
sudo bash -c 'cat > /etc/systemd/system/portfolio.service << EOL
[Unit]
Description=Gunicorn instance to serve portfolio
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/portfolio/backend
Environment="PATH=/home/ubuntu/portfolio/venv/bin"
ExecStart=/home/ubuntu/portfolio/venv/bin/gunicorn --workers 3 --bind unix:portfolio.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
EOL'

# Reload systemd and start the service
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl start portfolio
sudo systemctl enable portfolio

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
echo "y" | sudo ufw --force enable

# Restart services
echo "Restarting services..."
sudo systemctl restart nginx
sudo systemctl restart portfolio

# Set proper permissions
echo "Setting file permissions..."
sudo chown -R ubuntu:www-data /home/ubuntu/portfolio
sudo chmod -R 755 /home/ubuntu/portfolio

# Set up log rotation
echo "Configuring log rotation..."
sudo bash -c 'cat > /etc/logrotate.d/portfolio << EOL
/home/ubuntu/portfolio/backend/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 ubuntu www-data
    sharedscripts
    postrotate
        systemctl restart portfolio >/dev/null 2>&1 || true
    endscript
}
EOL'

echo ""
echo "=========================================="
echo "Production setup completed successfully!"
echo "Next steps:"
echo "1. Set up your domain name in the nginx-config file"
echo "2. Run 'sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com' to set up SSL"
echo "3. Configure your domain's DNS to point to this server's IP address"
echo "4. Set up environment variables in /home/ubuntu/portfolio/backend/.env"
echo "5. Restart the service: sudo systemctl restart portfolio"
echo "=========================================="
