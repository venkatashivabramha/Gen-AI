# 🔗 Login Integration Guide

## How to Use Login with Your App

Your existing project code **doesn't need ANY changes**! Just use the new entry point.

---

## 🚀 Quick Start

### Option 1: With Login (Recommended)

**Windows:**
```powershell
# Double-click this file:
run_with_login.bat

# Or run manually:
python main_with_login.py
```

This will:
1. ✅ Show login window
2. ✅ Let user login/signup or skip
3. ✅ Launch your existing app unchanged

### Option 2: Without Login (Original)

**Windows:**
```powershell
# Double-click this file:
run_app.bat

# Or run manually:
python src/main.py
```

This works **exactly as before** - no login required.

---

## 🔧 How It Works (No Code Changes!)

### The Wrapper Approach

```
User starts app
     ↓
main_with_login.py (NEW!)
     ↓
Show login window
     ↓
User logs in / signs up / skips
     ↓
Store user in global variable
     ↓
Import and run your EXISTING main.py
     ↓
Your app runs UNCHANGED!
```

**Key Point:** Your existing `src/main.py` and all other files are **NOT modified**!

---

## 📊 Accessing User Info (Optional)

If you **want** to use user info in your app (optional!), you can access it anywhere:

### Anywhere in Your Code:

```python
from utils.user_session import get_current_user, is_logged_in, get_username

# Check if user is logged in
if is_logged_in():
    print(f"User is logged in as: {get_username()}")
else:
    print("Running in guest mode")

# Get full user info
user = get_current_user()
if user:
    print(f"User ID: {user['id']}")
    print(f"Email: {user['email']}")
    print(f"Username: {user['username']}")
    print(f"Full Name: {user['full_name']}")
```

### Track User Activity:

```python
from utils.user_session import UserSession

# When user generates a business plan
UserSession.update_user_activity()
```

---

## 🎯 Integration Examples

### Example 1: Show Welcome Message

**In your GUI (`src/gui/main_window.py`):**

```python
# Add this at the top
from utils.user_session import get_username

# In your __init__ or _create_ui method
username = get_username()
welcome_label = ctk.CTkLabel(
    self,
    text=f"Welcome, {username}!",
    font=ctk.CTkFont(size=14)
)
welcome_label.pack()
```

### Example 2: Limit Guest Users

**In your generation logic:**

```python
from utils.user_session import is_logged_in

def generate_business_plan(self):
    # Check if user is logged in
    if not is_logged_in():
        response = messagebox.askyesno(
            "Guest Mode",
            "You're using guest mode. Plans won't be saved to your account.\n\n"
            "Continue anyway?"
        )
        if not response:
            return
    
    # Rest of your existing code...
```

### Example 3: Track Generation Count

**In your `business_plan_generator.py`:**

```python
from utils.user_session import UserSession

def generate_from_form(self, form_data, output_formats):
    # Your existing code...
    
    # At the end, track activity
    UserSession.update_user_activity()
    
    return result
```

### Example 4: Show User Stats

**In your GUI:**

```python
from auth.auth_manager import get_auth_manager
from utils.user_session import get_current_user

user = get_current_user()
if user:
    auth = get_auth_manager()
    stats = auth.get_user_stats(user['id'])
    
    stats_label.configure(
        text=f"Plans Generated: {stats['plans_generated']}"
    )
```

---

## 📁 New Files Added

```
✅ main_with_login.py          - Wrapper entry point
✅ run_with_login.bat           - Easy launcher
✅ src/utils/user_session.py    - User access helper
✅ src/utils/__init__.py        - Module setup
✅ docs/LOGIN_INTEGRATION_GUIDE.md - This file
```

**Your existing files:** ✅ UNCHANGED!

---

## 🔄 Two Ways to Run

### 1. With Login:
```
run_with_login.bat  →  Login Window  →  Your App
```

### 2. Without Login (Original):
```
run_app.bat  →  Your App (no login)
```

**Both work!** User can choose.

---

## 🎨 User Experience Flow

### First Time User:

1. **Runs:** `run_with_login.bat`
2. **Sees:** Login window with 2 tabs (Login / Sign Up)
3. **Clicks:** "Sign Up" tab
4. **Enters:** Name, email, username, password
5. **Clicks:** "Create Account"
6. **Switches to:** Login tab (auto-filled username)
7. **Enters:** Password
8. **Clicks:** "Login"
9. **Sees:** "Welcome, [username]!" message
10. **App opens:** Your existing GUI, unchanged!

### Returning User:

1. **Runs:** `run_with_login.bat`
2. **Sees:** Login window
3. **Enters:** Username + password
4. **Checks:** "Remember me" (optional)
5. **Clicks:** "Login"
6. **App opens:** Instantly!

### Guest User:

1. **Runs:** `run_with_login.bat`
2. **Sees:** Login window
3. **Clicks:** "Continue Without Login"
4. **App opens:** Works exactly as before!

---

## 🔒 Security Notes

### What's Stored:

**With Login:**
- User credentials in `data/users.db` (encrypted passwords)
- Session tokens if "Remember Me" is checked

**Guest Mode:**
- Nothing stored
- Works exactly like your original app

### Where Data Lives:

```
data/
├── users.db              - User accounts (SQLite)
├── business_templates/   - Your existing templates
└── (no user data in guest mode)
```

---

## 💡 Optional Enhancements

Want to go further? Here are easy additions (all optional!):

### 1. Auto-Login with Saved Session

**In `main_with_login.py`:**

```python
from auth.auth_manager import get_auth_manager
import json

# Try to load saved session
try:
    with open('data/session.json', 'r') as f:
        session_token = json.load(f)['token']
    
    auth = get_auth_manager()
    user = auth.verify_session(session_token)
    
    if user:
        print(f"Auto-logged in as {user['username']}")
        # Skip login window, launch app directly
        handle_login_success(user)
        return
except:
    pass

# Show login window if auto-login failed
user = show_login(on_success=handle_login_success)
```

### 2. Show User in Title Bar

**Access from anywhere:**

```python
from utils.user_session import get_username

self.title(f"Business Plan Generator - {get_username()}")
```

### 3. User Preferences

**Store per-user settings:**

```python
from utils.user_session import get_user_id

user_id = get_user_id()
if user_id:
    # Load user's preferences
    prefs = load_preferences(user_id)
    # Apply them...
```

---

## 🐛 Troubleshooting

### Login Window Doesn't Show

**Solution:** Make sure you're running the right file:
```powershell
python main_with_login.py  # NOT main.py
```

### "CURRENT_USER not defined" Error

**Solution:** This means you ran `main.py` directly without the wrapper. Run:
```powershell
python main_with_login.py
```

### Guest Mode Not Working

**Solution:** Click "Continue Without Login" button in login window. The app works exactly as before.

### Changes to main.py Not Reflected

**Solution:** The wrapper imports your `main.py`, so changes ARE reflected automatically. No need to modify the wrapper.

---

## 🎯 Summary

### What You Get:

✅ **Login/Signup System** - Beautiful GUI
✅ **Zero Code Changes** - Your app works as-is
✅ **Two Entry Points:**
  - `main_with_login.py` - With authentication
  - `src/main.py` - Original (no auth)
✅ **Optional Integration** - Use user info if you want
✅ **Guest Mode** - App works without login
✅ **Session Tracking** - Remember Me for 30 days
✅ **User Statistics** - Track usage per user

### How It Works:

```
main_with_login.py (wrapper)
    ↓
Show login window
    ↓
Store user globally
    ↓
Import your main.py
    ↓
Your app runs UNCHANGED!
```

---

## 🚀 Start Using It

**With Login:**
```powershell
python main_with_login.py
```

**Without Login (Original):**
```powershell
python src/main.py
```

**Both work!** Choose what you prefer. Your existing code is **untouched**! 🎉

---

## 📚 Related Docs

- `docs/AUTHENTICATION_GUIDE.md` - Complete auth system guide
- `QUICK_START.md` - Basic usage
- `USAGE_GUIDE.md` - Full manual

**Everything is ready!** Just use `main_with_login.py` instead of `main.py`!
