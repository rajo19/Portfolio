#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx nodejs npm

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend
npm install
npm run build
cd ..

# Set up Nginx
sudo cp nginx-config /etc/nginx/sites-available/portfolio
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# Set up PM2
sudo npm install -g pm2

# Start the application
cd backend
pm2 start app.py --name "portfolio" --interpreter python3
pm2 save
pm2 startup

# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw --force enable

echo "Deployment completed successfully!"
