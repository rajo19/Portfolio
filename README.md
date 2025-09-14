# Portfolio

Personal portfolio website built with Vue.js, Flask, and MongoDB.

## Features
- Modern, responsive UI built with Vuetify
- AI-powered Q&A section using Groq API
- Blog functionality
- Resume/CV section
- Contact form
- Admin dashboard for content management

## Prerequisites
- Python 3.10+
- Node.js 16+
- MongoDB (local or Atlas)
- AWS EC2 instance (for production)
- Domain name (optional but recommended)

## Local Development

### Backend Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   MONGODB_URI=mongodb://localhost:27017/portfolio
   GROQ_API_KEY=your-groq-api-key
   ```

4. Run the backend server:
   ```bash
   cd backend
   flask run
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Production Deployment

### AWS EC2 Setup
1. Launch an EC2 instance (Ubuntu 22.04 LTS recommended)
2. Configure security groups to allow:
   - SSH (port 22)
   - HTTP (port 80)
   - HTTPS (port 443)
3. Associate an Elastic IP with your instance
4. Point your domain to the Elastic IP (optional)

### GitHub Secrets
Add the following secrets to your GitHub repository:
- `EC2_HOST`: Your EC2 public IP or domain
- `EC2_USERNAME`: Usually 'ubuntu' for Ubuntu AMIs
- `SSH_PRIVATE_KEY`: Your private SSH key for the EC2 instance

### First-time Deployment
1. SSH into your EC2 instance
2. Clone the repository
3. Run the deployment script:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

### CI/CD
This project includes a GitHub Actions workflow that will automatically deploy changes to the `main` branch to your EC2 instance.

## Environment Variables

### Backend
- `FLASK_APP`: Main application file (app.py)
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Flask secret key for session security
- `MONGODB_URI`: MongoDB connection string
- `GROQ_API_KEY`: API key for Groq AI services

## License
MIT