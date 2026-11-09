"""
Main Entry Point with Authentication
Wrapper that adds login BEFORE your existing app - NO code changes needed!

Usage: python main_with_login.py
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from auth.login_gui import show_login


def main():
    """Show login, then launch existing app"""
    
    print("=" * 60)
    print("  Business Plan Generator")
    print("  Please login or sign up to continue")
    print("=" * 60)
    print()
    
    # Show login window - blocks until user logs in or skips
    user = show_login(on_success=handle_login_success)
    
    # If window was closed without action, exit
    if user is None and not hasattr(show_login, 'closed'):
        print("\nLogin cancelled. Exiting...")
        return


def handle_login_success(user):
    """Called when user logs in - launch main app"""
    
    if user:
        print("\n" + "=" * 60)
        print(f"  ✓ Welcome, {user['username']}!")
        print(f"  ✓ Email: {user['email']}")
        print("=" * 60)
        print("\nLaunching Business Plan Generator...")
    else:
        print("\n" + "=" * 60)
        print("  ✓ Continuing as Guest")
        print("=" * 60)
        print("\nLaunching Business Plan Generator...")
    
    print()
    
    # Import and run your EXISTING main.py without any changes!
    try:
        # Store user info globally so app can access it if needed
        import builtins
        builtins.CURRENT_USER = user
        
        # Import your existing main app (FIXED: correct path to src/)
        from src.main import main as run_original_app
        
        print("✓ Successfully imported main application")
        
        # Run it!
        run_original_app()
        
    except ImportError as e:
        print(f"\n❌ Error: Could not import main application")
        print(f"   Details: {e}")
        print(f"\nTrying alternative launch method...")
        
        # Fallback: run main.py directly
        try:
            import subprocess
            subprocess.run([sys.executable, "src/main.py"])
        except Exception as e2:
            print(f"\n❌ Alternative launch also failed: {e2}")
            print(f"\nPlease try running directly:")
            print(f"   python src/main.py")
            input("\nPress Enter to exit...")
    
    except Exception as e:
        print(f"\n❌ Unexpected error launching application:")
        print(f"   {e}")
        print(f"\nPlease try running directly:")
        print(f"   python src/main.py")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()