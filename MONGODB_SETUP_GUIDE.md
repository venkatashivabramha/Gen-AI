# MongoDB Atlas Connection Guide

## Step 1: Create FREE MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Click "Try Free" or "Sign Up"
3. Create account (use your email)

## Step 2: Create FREE Cluster

1. After login, click "Build a Database"
2. Choose **M0 FREE** tier:
   - ✅ 512 MB storage
   - ✅ No credit card required
   - ✅ Forever FREE
3. Choose cloud provider: **AWS** (recommended)
4. Choose region: **Closest to your users**
5. Cluster Name: **Cluster0** (default is fine)
6. Click "Create"

## Step 3: Create Database User

1. Security Quickstart will appear
2. **Authentication Method:** Username and Password
3. **Username:** `businessplanapp` (or your choice)
4. **Password:** Click "Autogenerate Secure Password" and COPY IT!
   - Example: `xY9mK2nP4qR7sT1v`
   - **SAVE THIS PASSWORD!** You'll need it
5. Click "Create User"

## Step 4: Configure Network Access

1. Click "Add My Current IP Address" (for testing)
2. For Streamlit Cloud, click "Add IP Address"
   - IP: `0.0.0.0/0` (allow from anywhere)
   - Description: "Streamlit Cloud"
   - ⚠️ Note: This allows all IPs (needed for Streamlit Cloud)
3. Click "Finish and Close"

## Step 5: Get Connection String

1. Click "Database" in left sidebar
2. Click "Connect" button on your cluster
3. Choose "Connect your application"
4. **Driver:** Python
5. **Version:** 3.11 or later
6. **Copy the connection string:**
   ```
   mongodb+srv://businessplanapp:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
7. **Replace `<password>` with your actual password!**
   - Example: `mongodb+srv://businessplanapp:xY9mK2nP4qR7sT1v@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority`

## Step 6: Add to Streamlit Cloud Secrets

1. Go to https://share.streamlit.io/
2. Find your app: **gen-ai-businessplan-generator**
3. Click ⚙️ (Settings)
4. Click "Secrets"
5. Add this:
   ```toml
   MONGODB_URI = "mongodb+srv://businessplanapp:YOUR_PASSWORD_HERE@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
6. **Replace**:
   - `YOUR_PASSWORD_HERE` with your database password
   - `cluster0.xxxxx.mongodb.net` with your actual cluster address
7. Click "Save"

## Step 7: Restart Your App

1. In Streamlit Cloud, click "Reboot app"
2. Wait 1-2 minutes
3. Your app will now use MongoDB!

## Testing

1. Visit your app: https://gen-ai-businessplan-generator.streamlit.app
2. Go to Login page
3. **Create Account:**
   - Full Name: Test User
   - Email: test@example.com
   - Password: test123456
4. Click "Create Account"
5. **You should see:** "Account created successfully! You can now login."
6. **Login** with those credentials
7. ✅ You're logged in with real MongoDB!

## Troubleshooting

### "SSL handshake failed" error
- Already fixed! App falls back to Demo Mode silently

### "Database connection error"
- Check your connection string format
- Make sure password is correct (no < > brackets)
- Verify IP whitelist includes 0.0.0.0/0

### "User not found" after creating account
- MongoDB not connected, running in Demo Mode
- Check Streamlit secrets have correct MONGODB_URI

## Current Status

**Without MongoDB:** 
- ✅ App works in Demo Mode
- ✅ Any email/password works
- ❌ No data persistence

**With MongoDB:**
- ✅ Real user authentication
- ✅ Data persistence
- ✅ User management via Admin page
- ✅ Secure password hashing (bcrypt)

## Example Connection String

```
mongodb+srv://businessplanapp:MyS3cur3P@ssw0rd@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

**Components:**
- `businessplanapp` = username
- `MyS3cur3P@ssw0rd` = password
- `cluster0.abc123.mongodb.net` = your cluster address
- `retryWrites=true&w=majority` = connection options

## Security Notes

- ✅ Passwords are hashed with bcrypt (never stored plain text)
- ✅ SSL/TLS encryption for all connections
- ✅ MongoDB Atlas is SOC 2 Type 2 certified
- ⚠️ 0.0.0.0/0 IP whitelist is needed for Streamlit Cloud (they use dynamic IPs)

## Need Help?

If you get stuck, check:
1. MongoDB Atlas Dashboard → Database → Browse Collections
2. Should see `business_plan_generator` database
3. Should see `users` collection with your test user

---

**Ready to connect MongoDB? Follow the steps above!** 🚀
