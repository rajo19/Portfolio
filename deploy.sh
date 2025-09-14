#!/bin/bash

# Update system packages
sudo yum update -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    sudo amazon-linux-extras install docker -y
    sudo service docker start
    sudo usermod -a -G docker ec2-user
    sudo systemctl enable docker
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    sudo amazon-linux-extras install nginx1 -y
    sudo systemctl enable nginx
    sudo systemctl start nginx
fi

# Install certbot for SSL
if ! command -v certbot &> /dev/null; then
    sudo amazon-linux-extras install epel -y
    sudo yum install -y certbot python3-certbot-nginx
fi

# Create directory for the application
APP_DIR="/opt/portfolio"
sudo mkdir -p $APP_DIR
sudo chown -R ec2-user:ec2-user $APP_DIR

# Create directory for MongoDB data
MONGO_DIR="/data/db"
sudo mkdir -p $MONGO_DIR
sudo chown -R 1000:1000 $MONGO_DIR

# Create production docker-compose file
cat << 'EOF' > $APP_DIR/docker-compose.prod.yml
version: '3.8'

services:
  backend:
    image: ghcr.io/your-github-username/your-repo-name:main-backend
    restart: always
    env_file:
      - .env
    environment:
      - FLASK_ENV=production
      - MONGO_URI=mongodb://mongo:27017/portfolio
    depends_on:
      - mongo
    networks:
      - portfolio-network

  frontend:
    image: ghcr.io/your-github-username/your-repo-name:main-frontend
    restart: always
    depends_on:
      - backend
    networks:
      - portfolio-network

  mongo:
    image: mongo:6.0
    restart: always
    volumes:
      - mongodb_data:/data/db
    networks:
      - portfolio-network

networks:
  portfolio-network:
    driver: bridge

volumes:
  mongodb_data:
EOF

# Create .env file with sensitive data
# Note: In a real production environment, use AWS Secrets Manager or Parameter Store
cat << 'EOF' > $APP_DIR/.env
# MongoDB
MONGO_URI=mongodb://mongo:27017/portfolio

# Flask
SECRET_KEY=your-secret-key
FLASK_ENV=production

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Groq API
GROQ_API_KEY=your-groq-api-key

# Frontend
VITE_API_BASE_URL=/api
EOF

# Create Nginx configuration for production
cat << 'EOF' > /etc/nginx/conf.d/portfolio.conf
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
EOF

# Restart Nginx
sudo systemctl restart nginx

# Set up SSL with Let's Encrypt
sudo certbot --nginx -d your-domain.com -d www.your-domain.com --non-interactive --agree-tos -m your-email@example.com --redirect

# Create a systemd service for the application
cat << 'EOF' | sudo tee /etc/systemd/system/portfolio.service
[Unit]
Description=Portfolio Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/portfolio
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start the service
sudo systemctl daemon-reload
sudo systemctl enable portfolio.service
sudo systemctl start portfolio.service

# Set up log rotation for Docker containers
cat << 'EOF' | sudo tee /etc/logrotate.d/docker-containers
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
EOF

# Set up firewall rules
sudo yum install -y iptables-services
sudo systemctl enable iptables
sudo systemctl start iptables

# Allow HTTP, HTTPS, and SSH
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Save iptables rules
sudo service iptables save

# Print completion message
echo "Deployment completed successfully!"
