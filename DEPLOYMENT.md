# Portfolio Deployment Guide

This guide provides instructions for deploying the portfolio application to an AWS EC2 instance using Docker and GitHub Actions.

## Prerequisites

1. AWS account with EC2 access
2. Domain name (recommended)
3. GitHub repository for the project
4. Docker Hub or GitHub Container Registry (GHCR) account

## Infrastructure Setup

### 1. Create an EC2 Instance

- Launch an EC2 instance with Amazon Linux 2 AMI
- Recommended instance type: t3.medium or larger
- Storage: At least 20GB of EBS storage
- Security Group: Open ports 22 (SSH), 80 (HTTP), and 443 (HTTPS)
- IAM Role: Attach a role with permissions for ECR (if using) and other AWS services

### 2. Set Up DNS (Optional but Recommended)

- Create an A record in your DNS provider pointing to your EC2 instance's public IP
- Example: `portfolio.yourdomain.com` → `YOUR_EC2_IP`

## GitHub Repository Setup

### 1. Add Required Secrets

Go to your GitHub repository → Settings → Secrets → Actions → New repository secret

Add the following secrets:

- `AWS_ACCESS_KEY_ID`: AWS access key with EC2 permissions
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_REGION`: AWS region (e.g., `us-east-1`)
- `EC2_PUBLIC_IP`: Public IP of your EC2 instance
- `SSH_PRIVATE_KEY`: Private key to access the EC2 instance
- `DOMAIN`: Your domain name (e.g., portfolio.yourdomain.com)
- `EMAIL`: Your email for Let's Encrypt SSL certificates

### 2. Update GitHub Actions Workflow

Update the following in `.github/workflows/docker-deploy.yml`:

- Replace `your-github-username/your-repo-name` with your actual GitHub username and repository name
- Update any other environment-specific variables

## Deployment Process

### 1. Initial Server Setup

SSH into your EC2 instance and run the following commands:

```bash
# Make the deploy script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

### 2. Configure Environment Variables

Edit the `.env` file in the `/opt/portfolio` directory with your production environment variables:

```bash
nano /opt/portfolio/.env
```

### 3. Start the Application

```bash
cd /opt/portfolio
sudo systemctl start portfolio
```

## Post-Deployment

### 1. Verify the Application

- Visit `http://your-domain.com` in your browser
- The application should be accessible via HTTPS

### 2. Set Up Monitoring (Optional)

- Configure CloudWatch for logs and monitoring
- Set up alerts for high CPU/memory usage
- Monitor application logs: `journalctl -u portfolio -f`

## Updating the Application

1. Push changes to the `main` branch
2. GitHub Actions will automatically build and deploy the new version
3. The deployment script will handle zero-downtime updates

## Backup and Recovery

### Database Backups

MongoDB data is stored in a Docker volume. To back up:

```bash
# Create a backup
docker run --rm -v mongodb_data:/data/db -v $(pwd):/backup mongo:6.0 bash -c "cd /data/db && tar czf /backup/mongodb_backup_$(date +%Y%m%d).tar.gz ."

# Restore from backup
docker run --rm -v mongodb_data:/data/db -v $(pwd):/backup mongo:6.0 bash -c "cd /data/db && tar xzf /backup/backup_file.tar.gz --strip 1"
```

### Application Data

Back up the `/opt/portfolio` directory:

```bash
tar czf portfolio_backup_$(date +%Y%m%d).tar.gz /opt/portfolio
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 80 and 443 are not in use by other services
2. **Docker Permissions**: If you get permission errors, add your user to the docker group: `sudo usermod -aG docker $USER`
3. **SSL Certificate Issues**: Check Let's Encrypt logs: `journalctl -xe | grep certbot`

### Checking Logs

- Application logs: `journalctl -u portfolio -f`
- Docker logs: `docker-compose -f /opt/portfolio/docker-compose.prod.yml logs -f`
- Nginx logs: `sudo tail -f /var/log/nginx/error.log`

## Security Considerations

1. **Keep Software Updated**: Regularly update Docker, Nginx, and the underlying OS
2. **Firewall**: Ensure only necessary ports are open
3. **Backups**: Regularly back up your database and application data
4. **Monitoring**: Set up monitoring and alerts for security events
5. **Secrets Management**: Use AWS Secrets Manager or Parameter Store for sensitive data in production
