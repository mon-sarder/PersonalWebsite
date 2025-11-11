# Portfolio Website Backend API

Flask-based REST API for a personal portfolio website with MongoDB database.

## Features

- ✉️ **Contact Form** - Submit messages with email notifications
- 🚀 **Project Showcase** - CRUD operations for projects
- 🛠️ **Skills Management** - Organize skills by category and proficiency
- 📊 **Analytics Dashboard** - Track page views and project clicks

## Tech Stack

- **Flask** - Python web framework
- **MongoDB** - NoSQL database
- **Flask-Mail** - Email notifications
- **Flask-CORS** - Cross-origin resource sharing

## Setup Instructions

### 1. Clone the Repository

```bash
cd portfolio-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB

1. Create a free MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster
3. Create a database user
4. Get your connection string

### 5. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# MongoDB - Replace with your connection string
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/portfolio?retryWrites=true&w=majority

# Flask
FLASK_ENV=development
SECRET_KEY=your-random-secret-key-here

# Gmail Configuration (for contact form emails)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Use App Password, not regular password
MAIL_DEFAULT_SENDER=your-email@gmail.com
ADMIN_EMAIL=your-email@gmail.com

# Frontend URL (update when deploying)
FRONTEND_URL=http://localhost:3000
```

**For Gmail App Password:**
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new app password
4. Use this password in MAIL_PASSWORD

### 6. Run the Application

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Check if API is running

### Contact Form
- `POST /api/contact` - Submit contact form
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello!"
  }
  ```
- `GET /api/contacts` - Get all contact submissions (admin)
- `PATCH /api/contacts/<id>/read` - Mark contact as read

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create new project
  ```json
  {
    "title": "My Awesome Project",
    "description": "A detailed description",
    "tech_stack": ["React", "Python", "MongoDB"],
    "github_link": "https://github.com/username/project",
    "live_link": "https://project.com",
    "image_url": "https://example.com/image.jpg"
  }
  ```
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Skills
- `GET /api/skills` - Get all skills
- `GET /api/skills?grouped=true` - Get skills grouped by category
- `GET /api/skills/<id>` - Get single skill
- `POST /api/skills` - Create new skill
  ```json
  {
    "name": "React",
    "category": "Frontend",
    "proficiency": "Advanced"
  }
  ```
- `PUT /api/skills/<id>` - Update skill
- `DELETE /api/skills/<id>` - Delete skill
- `POST /api/skills/batch` - Create multiple skills at once

### Analytics
- `POST /api/analytics/track` - Track an event
  ```json
  {
    "type": "page_view",
    "page": "/about"
  }
  ```
  or
  ```json
  {
    "type": "project_click",
    "project_id": "abc123",
    "project_title": "My Project"
  }
  ```
- `GET /api/analytics/dashboard?days=30` - Get dashboard statistics
- `GET /api/analytics/events?limit=50` - Get recent events

## Project Structure

```
portfolio-backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
│
├── config/
│   └── config.py         # Configuration settings
│
├── models/
│   └── models.py         # MongoDB document models
│
├── routes/
│   ├── contact.py        # Contact form routes
│   ├── projects.py       # Project CRUD routes
│   ├── skills.py         # Skills CRUD routes
│   └── analytics.py      # Analytics routes
│
└── utils/
    ├── database.py       # MongoDB connection
    └── email.py          # Email utilities
```

## Testing the API

You can test the API using:

1. **cURL**:
```bash
curl http://localhost:5000/health
```

2. **Postman** or **Insomnia** - Import the endpoints

3. **Python requests**:
```python
import requests

response = requests.get('http://localhost:5000/api/projects')
print(response.json())
```

## Deployment

### Option 1: Render.com (Recommended)
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect your repository
4. Add environment variables
5. Deploy

### Option 2: Railway.app
1. Install Railway CLI
2. Run `railway init`
3. Add environment variables
4. Run `railway up`

### Option 3: Heroku
1. Install Heroku CLI
2. Create new app
3. Add environment variables
4. Deploy with Git

## Next Steps

1. **Add Authentication** - JWT tokens for admin routes
2. **Add Image Upload** - For project images
3. **Add Rate Limiting** - Prevent abuse
4. **Add Logging** - Better error tracking
5. **Add Tests** - Unit and integration tests

## Troubleshooting

**MongoDB Connection Error:**
- Check your connection string
- Ensure IP address is whitelisted in MongoDB Atlas
- Verify database user credentials

**Email Not Sending:**
- Enable "Less secure app access" or use App Password for Gmail
- Check SMTP settings
- Verify firewall isn't blocking port 587

**CORS Errors:**
- Update FRONTEND_URL in .env
- Check Flask-CORS configuration

## License

MIT License - Feel free to use this for your own portfolio!