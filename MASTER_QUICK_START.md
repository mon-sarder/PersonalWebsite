# 🎯 MASTER QUICK START GUIDE

## Complete Setup in 3 Steps

Follow these guides in order to get your portfolio running:

---

## ✅ Step 1: Create .env File (10 minutes)

**Guide:** [STEP_BY_STEP_ENV_SETUP.md](computer:///mnt/user-data/outputs/STEP_BY_STEP_ENV_SETUP.md)

**Terminal commands:**
```bash
# 1. Generate keys
python generate_keys.py

# 2. Create .env file
cd portfolio-backend
nano .env

# 3. Paste template and fill in your values
# (See guide for template)

# 4. Save: Ctrl+X, Y, Enter
```

**What you need:**
- Generated SECRET_KEY and SETUP_KEY
- Gmail address (optional - for email features)
- Gmail App Password (optional - get from https://myaccount.google.com/apppasswords)

---

## ✅ Step 2: Deploy Locally (5 minutes)

**Guide:** [DEPLOYMENT_GUIDE.md](computer:///mnt/user-data/outputs/DEPLOYMENT_GUIDE.md)

**Terminal commands:**
```bash
# Build and start with Docker
docker-compose build
docker-compose up -d

# Create admin user
docker exec -it portfolio-backend flask create-admin

# Access your site
open http://localhost
```

**What you'll see:**
- ✅ Frontend at http://localhost
- ✅ Backend API at http://localhost:5000
- ✅ Health check at http://localhost:5000/health

---

## ✅ Step 3: Set Up GitHub Secrets (5 minutes)

**Guide:** [GITHUB_SECRETS_GUIDE.md](computer:///mnt/user-data/outputs/GITHUB_SECRETS_GUIDE.md)

**Steps:**
1. Go to GitHub repository → Settings → Secrets → Actions
2. Add these secrets:
   - `DOCKER_USERNAME` (from Docker Hub)
   - `DOCKER_PASSWORD` (Docker Hub access token)
   - `MONGODB_URI` (for testing: `mongodb://admin:password@localhost:27017/test?authSource=admin`)
   - `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)

3. Push code to test:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 📋 Complete Terminal Session Example

Here's what a complete setup looks like:

```bash
# Navigate to your project
cd /path/to/portfolio

# ==========================================
# STEP 1: Create .env
# ==========================================

# Generate keys
python generate_keys.py
# Copy the SECRET_KEY and SETUP_KEY

# Create .env file
cd portfolio-backend
nano .env

# Paste this template:
# ------------------
# MONGODB_URI=mongodb://admin:mypassword@mongodb:27017/portfolio?authSource=admin
# FLASK_ENV=development
# SECRET_KEY=<paste SECRET_KEY from generate_keys.py>
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your_email@gmail.com
# MAIL_PASSWORD=your_gmail_app_password
# MAIL_DEFAULT_SENDER=your_email@gmail.com
# ADMIN_EMAIL=your_email@gmail.com
# FRONTEND_URL=http://localhost:3000
# SETUP_KEY=<paste SETUP_KEY from generate_keys.py>
# MONGO_USERNAME=admin
# MONGO_PASSWORD=mypassword
# ------------------

# Save: Ctrl+X, Y, Enter

# Verify
cat .env

# Go back to project root
cd ..


# ==========================================
# STEP 2: Deploy with Docker
# ==========================================

# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Create admin user
docker exec -it portfolio-backend flask create-admin
# Enter username: admin
# Enter password: YourSecurePassword123

# (Optional) Add sample data
docker exec -it portfolio-backend python seed_data.py
# Type: yes

# View logs
docker-compose logs -f

# Test the site
# Open browser to http://localhost


# ==========================================
# STEP 3: Set Up GitHub
# ==========================================

# First, set up secrets on GitHub.com:
# 1. Go to your repo → Settings → Secrets → Actions
# 2. Add: DOCKER_USERNAME, DOCKER_PASSWORD, MONGODB_URI, SECRET_KEY

# Then push your code
git init
git add .
git commit -m "Initial commit: Full-stack portfolio"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main

# Check GitHub Actions
# Go to: https://github.com/yourusername/your-repo/actions
```

---

## 🎓 Understanding Your Setup

### What's Running After Step 2?

**4 Docker Containers:**
1. **frontend** - React app (http://localhost)
2. **backend** - Flask API (http://localhost:5000)
3. **mongodb** - Database (localhost:27017)
4. **redis** - Caching (localhost:6379)

**Services:**
- Frontend serves the React app
- Nginx routes `/api` requests to backend
- Backend connects to MongoDB
- All containers communicate via Docker network

### File Structure You Need

```
your-portfolio/
├── .env                              ❌ Don't create (for frontend)
├── .gitignore                        ✅ Already have
├── docker-compose.yml                ✅ Already have
├── Dockerfile                        ✅ Already have (frontend)
├── nginx.conf                        ✅ Already have
├── mongo-init.js                     ✅ Already have
├── generate_keys.py                  ✅ Already have
│
├── frontend/
│   ├── src/                          ✅ Already have
│   ├── package.json                  ✅ Already have
│   └── vite.config.js                ✅ Already have
│
├── portfolio-backend/
│   ├── .env                          ✅ YOU CREATE THIS
│   ├── Dockerfile                    ✅ Already have (backend)
│   ├── requirements.txt              ✅ Already have
│   ├── app_enhanced.py               ✅ Already have
│   ├── routes/                       ✅ Already have
│   ├── utils/                        ✅ Already have
│   └── models/                       ✅ Already have
│
└── .github/
    └── workflows/
        └── ci-cd.yml                 ✅ Already have
```

---

## 🐛 Common Issues & Quick Fixes

### Issue: "Can't find generate_keys.py"
```bash
# Make sure you're in project root
ls generate_keys.py

# If not found, download it from outputs folder
```

### Issue: "Port 80 already in use"
```bash
# Check what's using port 80
sudo lsof -i :80

# Stop it (example for nginx)
sudo systemctl stop nginx

# Or change port in docker-compose.yml:
# ports:
#   - "8080:80"  # Changed from "80:80"
```

### Issue: "MongoDB connection failed"
```bash
# Check MongoDB is running
docker-compose ps

# Check logs
docker-compose logs mongodb

# Restart MongoDB
docker-compose restart mongodb

# Check .env file
docker exec -it portfolio-backend cat /app/.env | grep MONGODB_URI
```

### Issue: "Frontend can't reach backend"
```bash
# Check backend is running
curl http://localhost:5000/health

# Check nginx logs
docker-compose logs frontend

# Verify proxy settings in nginx.conf
```

### Issue: "GitHub Actions failing"
```bash
# Check GitHub Secrets are set correctly
# Go to: Settings → Secrets → Actions

# Check spelling (case-sensitive):
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - MONGODB_URI
# - SECRET_KEY

# Check Actions logs on GitHub
# Actions tab → Click failed run → View logs
```

---

## 📊 Verification Checklist

### After Step 1 (Creating .env):
- [ ] `.env` file exists in `portfolio-backend/`
- [ ] SECRET_KEY is 64+ characters
- [ ] SETUP_KEY is random string
- [ ] No placeholder text (no "YOUR_", "PASTE_", etc.)
- [ ] File is not in Git (`git status` shouldn't show it)

### After Step 2 (Local Deployment):
- [ ] 4 containers running (`docker-compose ps`)
- [ ] Frontend loads at http://localhost
- [ ] Backend health check works: http://localhost:5000/health
- [ ] Can create admin user
- [ ] No errors in logs (`docker-compose logs`)

### After Step 3 (GitHub Setup):
- [ ] 4 secrets added to GitHub
- [ ] Code pushed to repository
- [ ] GitHub Actions workflow triggered
- [ ] Tests passing (green checkmark)
- [ ] Docker images built (if on main branch)

---

## 🚀 Next Steps

### Customize Your Portfolio

**Frontend:**
```bash
# Edit these files:
frontend/src/components/Hero.jsx       # Change name and title
frontend/src/components/About.jsx      # Update bio
frontend/src/components/Contact.jsx    # Update contact info
frontend/src/components/Footer.jsx     # Update social links
```

**Add Your Projects:**
```bash
# Option 1: Use seed script
docker exec -it portfolio-backend python seed_data.py

# Option 2: Use admin API
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Project",
    "description": "Description here",
    "tech_stack": ["React", "Python"],
    "github_link": "https://github.com/..."
  }'
```

### Deploy to Production

**Option 1: Render.com (Free)**
- See DEPLOYMENT_GUIDE.md → "Option A: Deploy to Render.com"

**Option 2: Your Own Server**
- See DEPLOYMENT_GUIDE.md → "Option C: Deploy to Your Own Server"

### Monitor Your App

```bash
# View real-time logs
docker-compose logs -f

# Check resource usage
docker stats

# Backup database
docker exec portfolio-mongodb mongodump --out /backup

# Update after code changes
git pull
docker-compose up -d --build
```

---

## 📞 Getting Help

### Check Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Common Commands
```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# Restart a service
docker-compose restart backend

# Rebuild after code changes
docker-compose up -d --build

# Enter a container
docker exec -it portfolio-backend bash

# Check status
docker-compose ps
```

### Resources
- **Documentation:** All guides in `/outputs/` folder
- **Backend logs:** `portfolio-backend/logs/portfolio_api.log`
- **Test API:** `cd portfolio-backend && python test_api.py`
- **GitHub Actions:** Repository → Actions tab

---

## ✅ Success Criteria

You're done when:

1. ✅ Local site loads at http://localhost
2. ✅ API responds at http://localhost:5000/health
3. ✅ Admin user created successfully
4. ✅ GitHub Actions passing (green checkmark)
5. ✅ No errors in Docker logs

**Congratulations! Your portfolio is ready!** 🎉

---

## 📚 Complete Guide Index

1. **[STEP_BY_STEP_ENV_SETUP.md](computer:///mnt/user-data/outputs/STEP_BY_STEP_ENV_SETUP.md)** - Creating .env file
2. **[DEPLOYMENT_GUIDE.md](computer:///mnt/user-data/outputs/DEPLOYMENT_GUIDE.md)** - Deployment options
3. **[GITHUB_SECRETS_GUIDE.md](computer:///mnt/user-data/outputs/GITHUB_SECRETS_GUIDE.md)** - CI/CD setup
4. **This file** - Quick reference and commands

Start with Step 1 and follow in order! 🚀