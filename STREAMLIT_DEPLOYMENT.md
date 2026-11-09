# Streamlit Web Deployment Guide

## 🎉 Web Version Features

Your Business Plan Generator now has a **web version** that can be deployed to Streamlit Cloud for FREE!

### What's New:
- ✅ **Web-based UI** - Access from any browser
- ✅ **MongoDB Integration** - Cloud database (free tier)
- ✅ **User Authentication** - Secure login/signup
- ✅ **Admin Dashboard** - User management
- ✅ **Same AI Features** - All generation modes work
- ✅ **Real Market Data** - Yahoo Finance integration preserved
- ✅ **Multi-format Export** - Download generated files

---

## 🚀 Quick Start (Local Testing)

### 1. Install Dependencies
```bash
pip install streamlit pymongo bcrypt
```

### 2. Set Up MongoDB Atlas (FREE)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Create FREE account (no credit card)
3. Create FREE cluster (M0 Sandbox - 512MB)
4. Create database user:
   - Username: `bpg_user`
   - Password: (generate secure password)
5. Get connection string:
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

### 3. Configure Secrets

Create `.streamlit/secrets.toml`:
```toml
MONGODB_URI = "mongodb+srv://bpg_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
ANTHROPIC_API_KEY = "your-key-here"
GROQ_API_KEY = "your-groq-key-here"
```

### 4. Run Locally
```bash
streamlit run streamlit_app.py
```

Open browser to: http://localhost:8501

---

## ☁️ Deploy to Streamlit Cloud (FREE HOSTING!)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Add Streamlit web version"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "Sign in with GitHub"
3. Click "New app"
4. Select:
   - **Repository:** `venkatashivabramha/Gen-AI`
   - **Branch:** `main`
   - **Main file:** `streamlit_app.py`
5. Click "Advanced settings"
6. Add secrets:
   ```toml
   MONGODB_URI = "mongodb+srv://..."
   GROQ_API_KEY = "your-key"
   # ... other API keys
   ```
7. Click "Deploy!"

### Step 3: Your App is Live! 🎉

URL: `https://your-app-name.streamlit.app`

**Features:**
- ✅ Automatic HTTPS
- ✅ Auto-redeploy on git push
- ✅ FREE forever (community tier)
- ✅ No server management needed

---

## 📊 MongoDB Atlas Setup (Detailed)

### Create Database Structure:

Your app will automatically create collections, but here's the structure:

```javascript
// Database: business_plan_generator

// Collection: users
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "bcrypt_hash",
  "full_name": "John Doe",
  "created_at": ISODate,
  "approved": true,
  "is_admin": false,
  "last_login": ISODate
}

// Collection: settings
{
  "_id": "global",
  "require_approval": true,
  "allow_registration": true,
  "max_generations_per_day": 10,
  "updated_at": ISODate
}
```

### Create First Admin User:

1. Sign up through the web app
2. Go to MongoDB Atlas
3. Browse Collections → users
4. Find your user document
5. Edit: Set `is_admin: true` and `approved: true`
6. Now you can access Admin Dashboard!

---

## 🔧 Configuration Options

### Environment Variables (Alternative to secrets.toml):

```bash
# For local development
export MONGODB_URI="mongodb+srv://..."
export GROQ_API_KEY="your-key"
```

### Streamlit Cloud Secrets:

Go to app settings → Secrets → Add:
```toml
MONGODB_URI = "your-connection-string"
ANTHROPIC_API_KEY = "sk-ant-..."
GROQ_API_KEY = "gsk_..."
OPENROUTER_API_KEY = "sk-or-..."
```

---

## 📁 File Structure

```
Project_Kiro/
├── streamlit_app.py           # Main web app (home page)
├── pages/
│   ├── 1_📝_Generate.py       # Business plan generator
│   ├── 2_🔐_Login.py          # Authentication
│   └── 3_⚙️_Admin.py          # Admin dashboard
├── .streamlit/
│   ├── config.toml            # Streamlit config
│   └── secrets.toml           # API keys (DO NOT COMMIT!)
├── src/                       # Shared backend code
│   ├── business_plan_generator.py
│   ├── data/
│   ├── ai/
│   └── ...
├── main_with_login.py         # Desktop version (still works!)
└── requirements.txt           # Updated with Streamlit

```

---

## 🎯 Testing Checklist

### Local Testing:
- [ ] Run `streamlit run streamlit_app.py`
- [ ] Test home page loads
- [ ] Test signup/login
- [ ] Test business plan generation (all modes)
- [ ] Test file downloads
- [ ] Test admin dashboard

### Cloud Testing:
- [ ] App deploys successfully
- [ ] Secrets loaded correctly
- [ ] MongoDB connection works
- [ ] Authentication works
- [ ] File generation works
- [ ] Downloads work

---

## 🐛 Troubleshooting

### "Database connection error"
- Check MongoDB URI in secrets
- Ensure IP whitelist includes `0.0.0.0/0` (all IPs)
- Verify database user has read/write permissions

### "Module not found"
- Check `requirements.txt` has all dependencies
- Streamlit Cloud auto-installs from requirements.txt
- Local: `pip install -r requirements.txt`

### "API key not found"
- Add API keys to `.streamlit/secrets.toml` (local)
- Add secrets in Streamlit Cloud settings (cloud)

### Long generation times
- Normal: 2-5 minutes for comprehensive plans
- With market data: Add 30-60 seconds
- Groq provider is fastest

---

## 🔒 Security Best Practices

### ✅ DO:
- Use environment variables/secrets for API keys
- Enable MongoDB authentication
- Use strong passwords
- Keep secrets.toml in .gitignore

### ❌ DON'T:
- Commit API keys to Git
- Use weak passwords
- Expose MongoDB connection string publicly
- Share admin credentials

---

## 🌐 Custom Domain (Optional)

### Streamlit Cloud:
1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to add CNAME record
4. Example: `businessplan.yourdomain.com`

---

## 📈 Scaling Options

### Free Tier Limits:
- **Streamlit Cloud:** Unlimited apps, resource sharing
- **MongoDB Atlas:** 512MB storage (thousands of users)
- **Bandwidth:** Generous limits

### Upgrade When Needed:
- **Streamlit:** $20/month for dedicated resources
- **MongoDB:** $9/month for 2GB, more features
- **Both support millions of users at scale**

---

## 🎉 Success!

Your app is now:
- ✅ Accessible worldwide
- ✅ Hosted for FREE
- ✅ Auto-updating from Git
- ✅ Using cloud database
- ✅ Secure with authentication

**Share your URL with users:**
`https://your-app.streamlit.app`

---

## 📞 Support

- **Streamlit Docs:** https://docs.streamlit.io
- **MongoDB Docs:** https://www.mongodb.com/docs/atlas
- **Community:** https://discuss.streamlit.io

---

## 🔄 Maintenance

### Update your app:
```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main
# Streamlit Cloud auto-deploys!
```

### Monitor usage:
- Streamlit Cloud dashboard shows traffic
- MongoDB Atlas shows database usage
- Check admin dashboard for user stats

---

**Congratulations! Your Business Plan Generator is now deployed as a web app! 🎊**
