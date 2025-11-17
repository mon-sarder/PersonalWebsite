# 🚀 Deployment Guide - Terminal Commands

## Choose Your Deployment Method:

1. **Docker (Recommended)** - Easiest, works everywhere
2. **Manual Setup** - More control, good for development
3. **Production Deployment** - For hosting on servers

---

## Method 1: Docker Deployment (Recommended ⭐)

### Prerequisites
- Docker installed
- Docker Compose installed
- .env file created (see STEP_BY_STEP_ENV_SETUP.md)

### Step 1: Verify Your Setup

```bash
# Check Docker is installed
docker --version
docker-compose --version

# Check .env exists
ls portfolio-backend/.env

# Check all required files
ls Dockerfile
ls portfolio-backend/Dockerfile
ls docker-compose.yml
ls nginx.conf
ls mongo-init.js
```

### Step 2: Build and Start All Services

```bash
# Build images
docker-compose build

# Start all containers
docker-compose up -d

# Check status
docker-compose ps
```

**Expected Output:**
```
NAME                    STATUS
portfolio-backend       Up (healthy)
portfolio-frontend      Up
portfolio-mongodb       Up (healthy)
portfolio-redis         Up (healthy)
```

### Step 3: Create Admin User

```bash
# Enter the backend container
docker exec -it portfolio-backend bash

# Inside container, create admin
flask create-admin

# Enter username and password when prompted
# Exit container
exit
```

### Step 4: Seed Sample Data (Optional)

```bash
# Enter backend container
docker exec -it portfolio-backend bash

# Run seed script
python seed_data.py

# Type 'yes' when prompted
# Exit container
exit
```

### Step 5: Access Your Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/health
- **MongoDB:** localhost:27017

### Common Docker Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Restart a service
docker-compose restart backend

# Rebuild after code changes
docker-compose up -d --build

# Check resource usage
docker stats
```

### Troubleshooting Docker

**Problem: Port already in use**
```bash
# Find what's using port 80
sudo lsof -i :80

# Stop the service
sudo systemctl stop nginx  # or apache2

# Or change port in docker-compose.yml
```

**Problem: Permission denied**
```bash
# Add yourself to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

**Problem: Container keeps restarting**
```bash
# Check logs
docker-compose logs backend

# Check .env file
docker exec -it portfolio-backend cat /app/.env

# Verify MongoDB connection
docker exec -it portfolio-mongodb mongosh
```

---

## Method 2: Manual Setup (Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup

```bash
# Navigate to backend
cd portfolio-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (if not done)
# See STEP_BY_STEP_ENV_SETUP.md

# Initialize database
flask init-db

# Create admin user
flask create-admin

# Seed sample data (optional)
python seed_data.py

# Run backend
python app_enhanced.py
```

**Backend should start at:** http://localhost:5000

### Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local (optional)
echo "VITE_API_BASE_URL=http://localhost:5000/api" > .env.local

# Run frontend
npm run dev
```

**Frontend should start at:** http://localhost:3000

### Test the API

```bash
# In another terminal
cd portfolio-backend
python test_api.py
```

---

## Method 3: Production Deployment

### Option A: Deploy to Render.com (Free Tier Available)

#### Backend Deployment

1. **Push code to GitHub** (make sure .env is in .gitignore)

2. **Go to Render.com** → Sign up/Login

3. **Create New Web Service:**
   - Connect GitHub repository
   - **Name:** portfolio-backend
   - **Root Directory:** portfolio-backend
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT --workers 4 app_enhanced:app`

4. **Add Environment Variables:**
   ```
   MONGODB_URI=your_mongodb_atlas_uri
   SECRET_KEY=your_secret_key
   FLASK_ENV=production
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_DEFAULT_SENDER=your_email@gmail.com
   ADMIN_EMAIL=your_email@gmail.com
   SETUP_KEY=your_setup_key
   FRONTEND_URL=https://your-frontend.onrender.com
   ```

5. **Deploy** → Wait for build to complete

#### Frontend Deployment

1. **Create New Static Site:**
   - Connect same GitHub repository
   - **Name:** portfolio-frontend
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`

2. **Add Environment Variable:**
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api
   ```

3. **Deploy** → Wait for build

4. **Update Backend FRONTEND_URL:**
   - Go back to backend service
   - Update `FRONTEND_URL` to your frontend URL
   - Redeploy backend

#### Database (MongoDB Atlas)

1. **Go to** https://mongodb.com/cloud/atlas
2. **Create Free Cluster**
3. **Database Access:** Create user
4. **Network Access:** Add IP `0.0.0.0/0` (allow all)
5. **Connect:** Get connection string
6. **Update** backend MONGODB_URI

---

### Option B: Deploy to Railway.app

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add MongoDB
railway add

# Set environment variables
railway variables set MONGODB_URI=your_uri
railway variables set SECRET_KEY=your_key
# ... (set all variables from .env)

# Deploy
railway up
```

---

### Option C: Deploy to Your Own Server (VPS)

#### Using Docker on Server

```bash
# SSH into your server
ssh user@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# Create .env file
nano portfolio-backend/.env
# Paste your configuration

# Build and start
docker-compose up -d

# Set up reverse proxy (optional - for custom domain)
# Install nginx
sudo apt update
sudo apt install nginx

# Configure nginx
sudo nano /etc/nginx/sites-available/portfolio
```

**Nginx config for custom domain:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up SSL (free with Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Post-Deployment Checklist

### After deploying, test these:

- [ ] Frontend loads: https://your-site.com
- [ ] API health check: https://your-api.com/health
- [ ] Can create admin user
- [ ] Contact form works
- [ ] Projects display correctly
- [ ] Skills display correctly
- [ ] No console errors
- [ ] Email notifications work (if configured)

### Commands to Run After Deployment

```bash
# Create admin user
# If Docker:
docker exec -it portfolio-backend flask create-admin

# If manual/VPS:
cd portfolio-backend
source venv/bin/activate
flask create-admin

# Seed data (optional)
python seed_data.py

# Check logs
# Docker:
docker-compose logs -f

# Manual:
tail -f portfolio-backend/logs/portfolio_api.log
```

---

## Monitoring Your Application

### Health Check Endpoint

```bash
# Check if API is running
curl https://your-api.com/health

# Should return:
# {"status": "healthy", "database": "healthy", "message": "Portfolio API is running"}
```

### View Logs

```bash
# Docker:
docker-compose logs -f backend

# Manual:
tail -f portfolio-backend/logs/portfolio_api.log

# Production server:
journalctl -u your-service-name -f
```

### Database Backup (Important!)

```bash
# Docker MongoDB backup
docker exec portfolio-mongodb mongodump --out /data/backup

# Copy backup from container
docker cp portfolio-mongodb:/data/backup ./mongodb-backup

# Restore from backup
docker exec -i portfolio-mongodb mongorestore /data/backup
```

---

## Updating Your Application

### With Docker

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose down
docker-compose up -d --build

# Check status
docker-compose ps
```

### Manual Deployment

```bash
# Backend
cd portfolio-backend
git pull
source venv/bin/activate
pip install -r requirements.txt
# Restart your process manager (systemd, supervisor, etc.)

# Frontend
cd frontend
git pull
npm install
npm run build
# Copy build files to web server
```

---

## Environment-Specific .env Files

### Development (.env)
```env
FLASK_ENV=development
MONGODB_URI=mongodb://admin:password@localhost:27017/portfolio?authSource=admin
FRONTEND_URL=http://localhost:3000
```

### Production (.env.production)
```env
FLASK_ENV=production
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/portfolio
FRONTEND_URL=https://yourdomain.com
```

**Switch between environments:**
```bash
# Copy appropriate env file
cp .env.production .env

# Or use environment variables
export $(cat .env.production | xargs)
```

---

## Quick Reference Commands

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after changes
docker-compose up -d --build

# Create admin
docker exec -it portfolio-backend flask create-admin

# Enter backend container
docker exec -it portfolio-backend bash

# Enter MongoDB container
docker exec -it portfolio-mongodb mongosh

# Check disk space
df -h

# Check container resources
docker stats

# Backup database
docker exec portfolio-mongodb mongodump --out /backup
```

---

## Need Help?

- ✅ Backend not starting? Check `.env` file and logs
- ✅ Frontend not connecting? Check `VITE_API_BASE_URL`
- ✅ Database errors? Verify MongoDB connection string
- ✅ Email not working? Check Gmail App Password
- ✅ Port conflicts? Change ports in `docker-compose.yml`

**Check logs for specific errors:**
```bash
docker-compose logs backend | grep ERROR
```