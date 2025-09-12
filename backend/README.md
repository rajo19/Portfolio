# Portfolio Backend

This is the backend server for Rajorshi Tah's portfolio website, built with Python Flask and MongoDB.

## Features

- RESTful API endpoints for portfolio data
- JWT-based authentication
- File upload/download for CV
- Blog post management
- AI-powered Q&A using Groq API
- Contact form with email notifications

## Prerequisites

- Python 3.8+
- MongoDB 4.4+
- pip (Python package manager)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Portfolio/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with the following variables:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   MONGO_URI=mongodb://localhost:27017/portfolio
   JWT_SECRET=your_jwt_secret_key
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   GROQ_API_KEY=your_groq_api_key
   ```

## Running the Application

1. Start MongoDB service if it's not already running.

2. Run the Flask development server:
   ```bash
   flask run
   ```
   The server will start at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with username and password

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get a specific project
- `POST /api/projects` - Create a new project (admin only)
- `PUT /api/projects/<id>` - Update a project (admin only)
- `DELETE /api/projects/<id>` - Delete a project (admin only)

### CV
- `GET /api/cv/download` - Download the latest CV
- `POST /api/cv/upload` - Upload a new CV (admin only)

### Blog
- `GET /api/blog` - Get all blog posts
- `GET /api/blog/<id>` - Get a specific blog post
- `POST /api/blog` - Create a new blog post (admin only)
- `PUT /api/blog/<id>` - Update a blog post (admin only)
- `DELETE /api/blog/<id>` - Delete a blog post (admin only)

### AI
- `POST /api/ai/ask` - Ask a question to the AI assistant

### Contact
- `POST /api/contact` - Send a contact form message

## Default Admin Credentials
- Username: admin
- Password: password123

## Deployment

For production deployment, consider using:
- Gunicorn or uWSGI as the WSGI server
- Nginx as a reverse proxy
- Environment variables for configuration
- Proper SSL/TLS setup
