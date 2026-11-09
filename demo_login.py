"""
Demo: Login/Signup System
Run this to see the authentication in action!
"""
from src.auth.login_gui import show_login
from src.main import main as run_main_app


def on_login_success(user):
    """Called when user logs in successfully"""
    if user:
        print(f"\n✓ Logged in as: {user['username']} ({user['email']})")
        print(f"✓ User ID: {user['id']}")
        print("\nOpening Business Plan Generator...\n")
    else:
        print("\n✓ Continuing without login (Guest mode)")
        print("\nOpening Business Plan Generator...\n")
    
    # Now open the main app
    # run_main_app()  # Uncomment to auto-open main app


if __name__ == "__main__":
    print("=" * 60)
    print("  Business Plan Generator - Login Demo")
    print("=" * 60)
    print("\nShowing login window...\n")
    
    # Show login window
    user = show_login(on_success=on_login_success)
    
    print("\nLogin window closed")
    print("=" * 60)
