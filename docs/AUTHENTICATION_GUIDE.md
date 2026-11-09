# 🔐 Authentication System Guide

## Overview

Your Business Plan Generator now has a **FREE, simple, secure** authentication system!

**No Firebase, Supabase, or paid services needed!**

---

## ✨ Features

✅ **User Registration** (Signup)
✅ **User Login** with password verification
✅ **Remember Me** (30-day sessions)
✅ **Guest Mode** (use without login)
✅ **Password Hashing** (SHA-256 with salt)
✅ **User Statistics** (track plans generated)
✅ **SQLite Database** (local, no server needed)
✅ **Modern GUI** (CustomTkinter interface)

---

## 🚀 How to Use

### Option 1: With Login System

```powershell
# Run the login demo
python demo_login.py
```

You'll see a beautiful login window with two tabs:
- **Login** - For existing users
- **Sign Up** - Create new account

### Option 2: Integrate with Main App

Update `src/main.py` to show login first:

```python
from src.auth.login_gui import show_login

def main():
    # Show login window first
    user = show_login()
    
    if user:
        print(f"Welcome, {user['username']}!")
    
    # Then show main app
    # ... rest of your code
```

---

## 📊 Database Structure

All user data is stored in `data/users.db` (SQLite):

### Tables

**users**
- id (Primary Key)
- email (Unique)
- username (Unique)
- password_hash (SHA-256)
- salt (Random 32-byte hex)
- full_name
- created_at
- last_login
- is_active

**sessions**
- id
- user_id
- session_token (for Remember Me)
- created_at
- expires_at (30 days)

**user_stats**
- user_id
- plans_generated
- last_plan_date

---

## 🔒 Security Features

### Password Hashing
```python
# Password is NEVER stored in plain text!
password -> SHA-256(password + random_salt) -> stored_hash
```

### Salt (32 bytes random)
Each user gets a unique salt, so even identical passwords have different hashes.

### Session Tokens
"Remember Me" uses secure random tokens (256-bit) that expire after 30 days.

---

## 💻 Code Examples

### Check if User is Logged In

```python
from src.auth.auth_manager import get_auth_manager

auth = get_auth_manager()

# Verify session token
user = auth.verify_session(session_token)
if user:
    print(f"User {user['username']} is logged in")
```

### Track User Activity

```python
from src.auth.auth_manager import get_auth_manager

auth = get_auth_manager()

# When user generates a business plan
auth.increment_plan_count(user_id)

# Get user statistics
stats = auth.get_user_stats(user_id)
print(f"Plans generated: {stats['plans_generated']}")
```

### Manual Login/Signup (Programmatic)

```python
from src.auth.auth_manager import get_auth_manager

auth = get_auth_manager()

# Create account
result = auth.signup(
    email="user@example.com",
    username="johndoe",
    password="secure123",
    full_name="John Doe"
)

if result['success']:
    print("Account created!")

# Login
result = auth.login(
    username_or_email="johndoe",
    password="secure123",
    remember_me=True
)

if result['success']:
    user = result['user']
    session_token = result['session_token']
    print(f"Logged in as {user['username']}")
```

---

## 🎨 GUI Features

### Login Tab
- Username/Email input
- Password input (hidden with ●)
- "Remember me" checkbox
- Login button
- "Continue Without Login" button

### Signup Tab
- Full Name (optional)
- Email (required, validated)
- Username (required, unique)
- Password (min 6 characters)
- Create Account button

### Auto-Fill
After signup, automatically switches to Login tab and pre-fills username!

---

## 🔧 Configuration

### Change Database Location

```python
from src.auth.auth_manager import AuthManager

# Custom database path
auth = AuthManager(db_path="custom/path/users.db")
```

### Change Session Duration

In `auth_manager.py`, find:
```python
expires_at = datetime.now() + timedelta(days=30)  # Change 30 to your value
```

### Minimum Password Length

In `auth_manager.py`, find:
```python
if len(password) < 6:  # Change 6 to your requirement
```

---

## 📱 Integration Ideas

### 1. Show User Stats in GUI

```python
# In your main window
stats = auth.get_user_stats(current_user['id'])
stats_label.configure(
    text=f"Plans Generated: {stats['plans_generated']}"
)
```

### 2. Limit Free Users

```python
if current_user is None:  # Guest
    if plan_count >= 3:
        show_message("Create an account for unlimited plans!")
        return
```

### 3. Save User Preferences

Add a preferences table:
```sql
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    default_format TEXT,
    theme TEXT,
    auto_save INTEGER
)
```

### 4. Multi-User on Same Computer

Each user has their own account and generated plans can be linked to them!

---

## 🐛 Troubleshooting

### Database Locked Error
Make sure only one app instance accesses the database at a time.

### "Table already exists" Error
This is normal on first run - tables are created if they don't exist.

### Password Not Working
Passwords are case-sensitive! Make sure Caps Lock is off.

### Session Expired
Sessions last 30 days. After that, user needs to log in again.

---

## 🎯 Comparison with Other Solutions

| Feature | This Solution | Firebase | Supabase |
|---------|--------------|----------|----------|
| **Cost** | FREE ✅ | $25+/month | $25+/month |
| **Setup Time** | 5 minutes | 30 minutes | 30 minutes |
| **Internet Required** | No ✅ | Yes | Yes |
| **User Limit** | Unlimited ✅ | 50k free | 50k free |
| **Email Verification** | Optional | Yes | Yes |
| **OAuth (Google, etc.)** | No | Yes | Yes |
| **Data Privacy** | 100% local ✅ | Cloud | Cloud |

---

## 🚀 Next Steps

### Easy Enhancements:

1. **Email Verification**
   - Add email verification using `smtplib`
   - Free with Gmail SMTP

2. **Password Reset**
   - Generate reset tokens
   - Send via email

3. **Profile Pictures**
   - Store avatar path in database
   - Display in GUI

4. **Social Login** (Google, GitHub)
   - Use `authlib` library
   - Free OAuth implementation

5. **Two-Factor Authentication**
   - Use `pyotp` library
   - TOTP codes (like Google Authenticator)

---

## 📦 Dependencies

Already included in your project:
- ✅ sqlite3 (Python built-in)
- ✅ hashlib (Python built-in)
- ✅ secrets (Python built-in)
- ✅ customtkinter (already installed)

**No additional packages needed!** 🎉

---

## ✨ Summary

You now have a **complete, secure, FREE authentication system** that:
- ✅ Works completely offline
- ✅ No API limits or costs
- ✅ Secure password hashing
- ✅ Beautiful modern UI
- ✅ Easy to use and extend
- ✅ 100% Python, no JavaScript needed

**Perfect for your Business Plan Generator!** 🚀
