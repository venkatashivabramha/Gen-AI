"""
Quick script to approve a specific user
"""
import sqlite3
import sys

def approve_user(username):
    """Approve a user by username"""
    try:
        conn = sqlite3.connect('data/users.db')
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT username, status FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            print(f"❌ User '{username}' not found!")
            conn.close()
            return False
        
        current_username, current_status = result
        print(f"Found user: {current_username}")
        print(f"Current status: {current_status}")
        
        if current_status == 'approved':
            print(f"✅ User '{username}' is already approved!")
            conn.close()
            return True
        
        # Update to approved
        cursor.execute("UPDATE users SET status = 'approved' WHERE username = ?", (username,))
        conn.commit()
        
        # Verify
        cursor.execute("SELECT status FROM users WHERE username = ?", (username,))
        new_status = cursor.fetchone()[0]
        
        conn.close()
        
        if new_status == 'approved':
            print(f"✅ SUCCESS! User '{username}' has been approved!")
            print(f"   They can now login to the application.")
            return True
        else:
            print(f"❌ Failed to approve user")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def approve_all_pending():
    """Approve all pending users"""
    try:
        conn = sqlite3.connect('data/users.db')
        cursor = conn.cursor()
        
        # Get pending users
        cursor.execute("SELECT username FROM users WHERE status = 'pending'")
        pending_users = cursor.fetchall()
        
        if not pending_users:
            print("ℹ️  No pending users to approve")
            conn.close()
            return
        
        print(f"Found {len(pending_users)} pending user(s):")
        for user in pending_users:
            print(f"  - {user[0]}")
        
        # Approve all
        cursor.execute("UPDATE users SET status = 'approved' WHERE status = 'pending'")
        conn.commit()
        
        rows_affected = cursor.rowcount
        conn.close()
        
        print(f"\n✅ SUCCESS! Approved {rows_affected} user(s)")
        print("   They can all now login to the application.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("QUICK USER APPROVAL TOOL")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Approve specific user
        username = sys.argv[1]
        print(f"\nApproving user: {username}")
        approve_user(username)
    else:
        # Approve all pending
        print("\nApproving ALL pending users:")
        approve_all_pending()
    
    print("=" * 60)
