"""
User Session Manager - Access logged-in user from anywhere
Works as a wrapper - NO changes to existing code needed!
"""
import builtins
from typing import Optional, Dict, Any


class UserSession:
    """Manages current user session across the app"""
    
    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        """
        Get currently logged-in user
        
        Returns:
            User dict if logged in, None if guest mode
            User dict contains: id, email, username, full_name
        """
        return getattr(builtins, 'CURRENT_USER', None)
    
    @staticmethod
    def is_logged_in() -> bool:
        """Check if user is logged in"""
        return UserSession.get_current_user() is not None
    
    @staticmethod
    def get_username() -> str:
        """Get username or 'Guest' if not logged in"""
        user = UserSession.get_current_user()
        return user['username'] if user else 'Guest'
    
    @staticmethod
    def get_user_id() -> Optional[int]:
        """Get user ID or None if guest"""
        user = UserSession.get_current_user()
        return user['id'] if user else None
    
    @staticmethod
    def update_user_activity():
        """Update user statistics (if logged in)"""
        user = UserSession.get_current_user()
        if user:
            try:
                from auth.auth_manager import get_auth_manager
                auth = get_auth_manager()
                auth.increment_plan_count(user['id'])
            except Exception as e:
                print(f"Could not update user stats: {e}")


# Convenience functions
def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current user (shorthand)"""
    return UserSession.get_current_user()


def is_logged_in() -> bool:
    """Check if logged in (shorthand)"""
    return UserSession.is_logged_in()


def get_username() -> str:
    """Get username or 'Guest' (shorthand)"""
    return UserSession.get_username()
