"""Quick script to approve a user"""
import sqlite3
import sys

def approve_user(username):
    """Approve a user by username"""
    try:
        conn = sqlite3.connect('data/users.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT username, status FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ User '{username}' not found!")
            conn.close()
            return False
        
        current_status = user[1]
        print(f"Current status: {current_status}")
        
        # Approve user
        cursor.execute("UPDATE users SET status = 'approved' WHERE username = ?", (username,))
        conn.commit()
        
        # Verify
        cursor.execute("SELECT username, email, status FROM users WHERE username = ?", (username,))
        updated_user = cursor.fetchone()
        
        print(f"\n✅ User '{updated_user[0]}' has been APPROVED!")
        print(f"   Email: {updated_user[1]}")
        print(f"   Status: {updated_user[2]}")
        print(f"\n✅ User can now login!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Get all pending users
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, status FROM users")
    users = cursor.fetchall()
    
    print("=" * 60)
    print("CURRENT USERS IN DATABASE")
    print("=" * 60)
    
    for username, email, status in users:
        print(f"\nUsername: {username}")
        print(f"Email: {email}")
        print(f"Status: {status}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("APPROVING ALL PENDING USERS...")
    print("=" * 60)
    
    # Approve all pending users
    for username, email, status in users:
        if status == 'pending':
            print(f"\nApproving: {username}...")
            approve_user(username)
