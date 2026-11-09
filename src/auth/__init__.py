"""
Authentication module - Simple, secure, FREE!
No Firebase, Supabase, or external services needed
"""

from .auth_manager import AuthManager, get_auth_manager

__all__ = ['AuthManager', 'get_auth_manager']
