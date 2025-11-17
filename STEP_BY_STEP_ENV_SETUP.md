# 🔧 Step-by-Step: Creating Your .env File

## Step 1: Generate Secret Keys

Open your terminal and run:

```bash
python generate_keys.py
```

**Output will look like:**
```
🔐 Secure Key Generator for .env File
════════════════════════════════════════════════════

SECRET_KEY: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
SETUP_KEY: xYz123Abc456_DefGhi789-JklMno
```

**✅ COPY THESE VALUES** - You'll need them in Step 3

---

## Step 2: Get Gmail App Password (Optional - for email features)

### If you want contact form emails to work:

1. **Go to Google Account Security:**
   - Visit: https://myaccount.google.com/security
   - Make sure 2-Factor Authentication is enabled

2. **Generate App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Click "Select app" → Choose "Mail"
   - Click "Select device" → Choose "Other" → Type "Portfolio"
   - Click "Generate"
   - **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)
   - Remove all spaces: `abcdefghijklmnop`

### If you DON'T want emails (just testing):
Skip this step and use placeholder values in Step 3.

---

## Step 3: Create the .env File

```bash
cd portfolio-backend
nano .env
```

**Paste this template and fill in YOUR values:**

```env
# ============================================
# MONGODB - Database Connection
# ============================================
# For Docker (easiest):
MONGODB_URI=mongodb://admin:secure_password_123@mongodb:27017/portfolio?authSource=admin

# For MongoDB Atlas (cloud):
# MONGODB_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@cluster.mongodb.net/portfolio?retryWrites=true&w=majority


# ============================================
# FLASK - Application Settings
# ============================================
FLASK_ENV=development
SECRET_KEY=PASTE_YOUR_SECRET_KEY_FROM_STEP_1_HERE


# ============================================
# EMAIL - Contact Form Notifications
# ============================================
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Replace with YOUR Gmail:
MAIL_USERNAME=YOUR_GMAIL_ADDRESS@gmail.com
MAIL_PASSWORD=PASTE_YOUR_16_CHAR_APP_PASSWORD_FROM_STEP_2_HERE
MAIL_DEFAULT_SENDER=YOUR_GMAIL_ADDRESS@gmail.com
ADMIN_EMAIL=YOUR_GMAIL_ADDRESS@gmail.com


# ============================================
# FRONTEND - CORS Configuration
# ============================================
# Development:
FRONTEND_URL=http://localhost:3000

# Production (after deployment):
# FRONTEND_URL=https://your-deployed-site.com


# ============================================
# ADMIN - User Creation
# ============================================
SETUP_KEY=PASTE_YOUR_SETUP_KEY_FROM_STEP_1_HERE


# ============================================
# DOCKER - MongoDB Credentials
# ============================================
MONGO_USERNAME=admin
MONGO_PASSWORD=secure_password_123
```

**Save the file:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 4: Verify Your .env File

```bash
cat portfolio-backend/.env
```

**Check that:**
- ✅ No placeholder text (no "YOUR_", "PASTE_", etc.)
- ✅ SECRET_KEY is 64+ characters long
- ✅ SETUP_KEY has random letters/numbers
- ✅ Email addresses are real (if using email features)
- ✅ No spaces in the Gmail app password

---

## 🎯 Quick Examples

### Example 1: Testing Without Email (Easiest)
```env
MONGODB_URI=mongodb://admin:mypassword123@mongodb:27017/portfolio?authSource=admin
FLASK_ENV=development
SECRET_KEY=a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=test@example.com
MAIL_PASSWORD=test-placeholder
MAIL_DEFAULT_SENDER=test@example.com
ADMIN_EMAIL=test@example.com
FRONTEND_URL=http://localhost:3000
SETUP_KEY=xYz123Abc456_DefGhi789-JklMno
MONGO_USERNAME=admin
MONGO_PASSWORD=mypassword123
```

### Example 2: Production With Real Email
```env
MONGODB_URI=mongodb://admin:SecurePass456!@mongodb:27017/portfolio?authSource=admin
FLASK_ENV=production
SECRET_KEY=f9e8d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=john.smith@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
MAIL_DEFAULT_SENDER=john.smith@gmail.com
ADMIN_EMAIL=john.smith@gmail.com
FRONTEND_URL=https://myportfolio.com
SETUP_KEY=Abc123Def456_Ghi789-Jkl012
MONGO_USERNAME=admin
MONGO_PASSWORD=SecurePass456!
```

---

## ✅ You're Done!

Your .env file is ready. Next steps:
1. **Test locally:** See DEPLOYMENT_GUIDE.md
2. **Deploy to production:** See DEPLOYMENT_GUIDE.md
3. **Set up GitHub secrets:** See GITHUB_SECRETS_GUIDE.md

---

## 🐛 Troubleshooting

**"Can't find generate_keys.py"**
```bash
# Make sure you're in the project root
cd /path/to/your/portfolio
python generate_keys.py
```

**"Permission denied" when creating .env**
```bash
# Make sure portfolio-backend folder exists
mkdir -p portfolio-backend
nano portfolio-backend/.env
```

**"Email not working"**
- Use the Gmail App Password, NOT your regular password
- Make sure 2FA is enabled first
- Remove ALL spaces from the 16-character code

**"MongoDB connection failed"**
- Check that MONGODB_URI doesn't have any line breaks
- If using Docker, make sure MONGO_PASSWORD matches in both places
- If using Atlas, make sure IP 0.0.0.0/0 is whitelisted