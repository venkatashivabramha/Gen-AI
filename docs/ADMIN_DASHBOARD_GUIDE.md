# 🔐 Admin Dashboard Guide

## Complete guide to managing users and controlling access

---

## 🚀 Quick Start

### Running the Admin Dashboard

```bash
# Windows - Double-click
.\run_admin.bat

# Or manually
python admin_dashboard.py
```

**Requirements:**
- Virtual environment activated
- `data/users.db` exists (created automatically on first signup)

---

## 📊 Dashboard Overview

### Main Features

1. **User Statistics** (Top right)
   ```
   Total: 25 | Pending: 3 | Approved: 20 | Blocked: 2
   ```

2. **Filter Buttons**
   - 🔵 All Users - Show everyone
   - 🟠 Pending Approval - New signups waiting
   - 🟢 Approved - Active users
   - 🔴 Blocked - Blocked accounts

3. **User Table**
   | Username | Email | Status | Registered | Last Login | Plans Created |
   |----------|-------|--------|------------|------------|---------------|
   | john_doe | john@example.com | ✅ Approved | 2026-11-01 | 2026-11-06 | 5 |

4. **Action Buttons**
   - ✅ Approve User
   - 🚫 Block User
   - 🔓 Unblock User
   - 🗑️ Delete User
   - 📊 View Details

---

## 🔄 User Lifecycle

### 1. New User Signs Up

**What happens:**
1. User fills signup form
2. Account created with status: `pending` ⏳
3. User CANNOT login yet
4. You get notified (in admin dashboard)

**User sees:**
```
"⏳ Your account is pending approval. Please wait for admin approval."
```

### 2. You Review the User

**In admin dashboard:**
1. Click "Pending Approval" filter
2. See the new user in the list
3. Click their row to select
4. Click "📊 View Details" to see info

**Details shown:**
```
╔══════════════════════════════════════════╗
║          USER DETAILS                     ║
╚══════════════════════════════════════════╝

👤 Username:        john_doe
📧 Email:           john@example.com
🔐 Status:          PENDING

📅 Registered:      2026-11-06 14:30:00
🕐 Last Login:      Never

📊 Business Plans:  0
📝 Last Plan:       N/A
```

### 3. You Approve or Deny

**Option A: Approve**
1. Select user
2. Click "✅ Approve User"
3. Status changes to: `approved` ✅
4. User can now login!

**Option B: Deny (Block)**
1. Select user
2. Click "🚫 Block User"
3. Status changes to: `blocked` 🚫
4. User CANNOT login

### 4. User Logs In

**If approved:**
```
✅ Login successful!
→ Opens Business Plan Generator
```

**If blocked:**
```
🚫 Your account has been blocked. 
   Please contact the administrator.
```

---

## 🎯 Common Tasks

### Task 1: Approve Multiple Users

```
1. Click "Pending Approval" filter
2. See all pending users
3. For each user:
   - Click their row
   - Click "✅ Approve User"
   - Confirmation: "User 'john_doe' has been approved!"
4. Click "🔄 Refresh" to update counts
```

### Task 2: Block Suspicious User

```
1. Find the user (search or filter)
2. Click their row
3. Click "🚫 Block User"
4. Confirm: "Are you sure you want to block 'username'?"
5. User immediately cannot login
```

### Task 3: Unblock User

```
1. Click "Blocked" filter
2. Select blocked user
3. Click "🔓 Unblock User"
4. Status changes to: approved
5. User can login again
```

### Task 4: View User Activity

```
1. Select any user
2. Click "📊 View Details"
3. See complete history:
   - Registration date
   - Last login time
   - Business plans created
   - Last plan date
```

### Task 5: Delete User Permanently

```
1. Select user
2. Click "🗑️ Delete User"
3. Confirm: "Are you sure you want to PERMANENTLY delete 'username'?"
4. ⚠️ WARNING: Cannot be undone!
5. User and all data deleted
```

---

## 🔔 Notification System

### Current Setup: Manual Check

You need to manually:
1. Open admin dashboard
2. Click "Pending Approval"
3. See new signups

### Future Options (Can be added):

#### Option 1: Email Notification
```python
# When user signs up, you receive:
Subject: 🔔 New Signup - john_doe
Body: 
  Username: john_doe
  Email: john@example.com
  Registered: 2026-11-06 14:30
  
  [Approve] [Block] [View Details]
```

#### Option 2: Desktop Notification
```
Windows notification when admin dashboard is running:
"🔔 New signup: john_doe"
Click to approve/deny
```

#### Option 3: SMS Alert
```
Text message when user signs up:
"New signup: john_doe (john@example.com)"
```

**Want any of these? Just ask!**

---

## 🛡️ Security Features

### 1. Status-Based Access Control

**3 Status Levels:**
- `pending` - Waiting for approval (default)
- `approved` - Full access
- `blocked` - No access

### 2. Secure Password Storage

Users' passwords are:
- ✅ Hashed with SHA-256
- ✅ Salted (unique per user)
- ✅ Never stored as plain text
- ✅ You CANNOT see users' passwords

### 3. Activity Tracking

**Tracked automatically:**
- Registration date
- Last login time
- Business plans created
- Last plan date

### 4. Instant Blocking

- Block user → immediate effect
- User session terminated
- Cannot login until unblocked

---

## 📈 User Statistics

### Dashboard Stats (Top Right)

```
Total: 25        - All users in system
Pending: 3       - Waiting for approval
Approved: 20     - Active users
Blocked: 2       - Blocked accounts
```

### Individual User Stats

**Click "📊 View Details" to see:**
- Total business plans created
- Last plan generation date
- Account age (days since registration)
- Activity level (last login)

---

## 🎨 Dashboard Interface

### Color Coding

- 🔵 **Blue** - All users filter
- 🟠 **Orange** - Pending approval filter
- 🟢 **Green** - Approved users / Approve button
- 🔴 **Red** - Blocked users / Block button
- 🟣 **Purple** - Refresh button

### Status Indicators

- ⏳ Pending - Yellow, waiting
- ✅ Approved - Green, active
- 🚫 Blocked - Red, denied

---

## 🔧 Troubleshooting

### Problem: Admin dashboard won't open

**Solution:**
```bash
# Check if database exists
dir data\users.db

# If not found, create test user:
python main_with_login.py
# Sign up with test account
# Database will be created
```

### Problem: Can't see any users

**Solution:**
```bash
# Check database file
sqlite3 data/users.db
SELECT * FROM users;

# If empty, no users have signed up yet
# Create test account first
```

### Problem: Approval button doesn't work

**Solution:**
```bash
# Make sure you selected a user first
# Click a row in the table
# Then click "✅ Approve User"
```

### Problem: User still can't login after approval

**Solution:**
```bash
# 1. Click "🔄 Refresh" in admin dashboard
# 2. Check user status is "✅ Approved"
# 3. Ask user to try login again
# 4. Check error message
```

---

## 🚀 Advanced Features

### Bulk Operations (Can be added)

**Approve all pending:**
```python
# New button: "Approve All Pending"
# One click to approve all waiting users
```

**Export user list:**
```python
# Export to CSV
# users_export_2026-11-06.csv
```

**Import users:**
```python
# Import from CSV
# Bulk user creation
```

### Integration Options (Can be added)

**Email verification:**
- User signs up
- Receives verification email
- You get notified after verification

**Two-factor authentication:**
- SMS code on login
- Google Authenticator
- Email code

**Role-based permissions:**
- Admin (full access)
- Manager (limited access)
- User (generate only)

**Want any of these? Just ask!**

---

## 📋 Best Practices

### Daily Routine

```
Morning:
1. Open admin dashboard
2. Click "Pending Approval"
3. Review and approve/block new users
4. Click "🔄 Refresh"

Weekly:
1. Review "Approved" users
2. Check for inactive accounts
3. Review user activity stats

Monthly:
1. Export user list (backup)
2. Clean up old blocked accounts
3. Review system usage
```

### Approval Guidelines

**Consider approving if:**
- ✅ Email looks legitimate
- ✅ Username is professional
- ✅ Registration time is normal

**Consider blocking if:**
- ❌ Suspicious email (fake domains)
- ❌ Random username (qwerty123)
- ❌ Multiple signups from same IP
- ❌ Unusual registration time (bot-like)

---

## 🆘 Getting Help

### Need Additional Features?

I can add:

1. **Email notifications** when users sign up
2. **SMS alerts** for new registrations
3. **Automated approval** based on rules
4. **IP blocking** for spam prevention
5. **Rate limiting** to prevent abuse
6. **Export/Import** user data
7. **Audit log** of all admin actions
8. **Multi-admin** support (multiple admins)

**Just tell me what you need!**

---

## 📊 Database Structure

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    status TEXT DEFAULT 'pending',
    business_plans_created INTEGER DEFAULT 0,
    last_plan_date TIMESTAMP
);
```

### Status Values

- `pending` - New signup, waiting for approval
- `approved` - Admin approved, can login
- `blocked` - Admin blocked, cannot login

---

## 🎯 Quick Reference

### Keyboard Shortcuts (Future)

```
Ctrl+R  - Refresh user list
Ctrl+F  - Search users
Ctrl+A  - Approve selected user
Ctrl+B  - Block selected user
Ctrl+D  - View user details
Delete  - Delete selected user
```

### Status Flow

```
[Sign Up] → pending
              ↓
         [Admin Reviews]
         ↙          ↘
    approved      blocked
         ↓            ↓
    [Can Login]  [Cannot Login]
         ↓
    [Unblock] ← blocked
```

---

## 📝 Next Steps

### After Setting Up Admin Dashboard:

1. **Test the flow:**
   - Create test user account
   - Open admin dashboard
   - Approve test user
   - Login with test user

2. **Customize (optional):**
   - Add email notifications
   - Add custom approval rules
   - Add more user fields

3. **Deploy (when ready):**
   - See `DEPLOYMENT_GUIDE.md`
   - Choose deployment option
   - Set up remote admin access

---

*Need help? Just ask: "How do I [task]?"*

---

*Last updated: November 6, 2026*
