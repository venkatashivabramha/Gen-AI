"""
Simple Authentication System - No Firebase/Supabase needed!
Uses local SQLite database with secure password hashing
"""
import sqlite3
import hashlib
import secrets
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class AuthManager:
    """Manages user authentication with local SQLite database"""
    
    def __init__(self, db_path: str = "data/users.db"):
        """Initialize authentication manager"""
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        # Create data directory if needed
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Add status column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'pending'")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Create sessions table for "Remember Me" functionality
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Add business_plans_created column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN business_plans_created INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Add last_plan_date column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_plan_date TIMESTAMP")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        conn.commit()
        conn.close()
        print("✓ Authentication database initialized")
    
    def _hash_password(self, password: str, salt: str = None) -> tuple:
        """Hash password with salt for security"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Use SHA-256 with salt
        password_hash = hashlib.sha256(
            (password + salt).encode('utf-8')
        ).hexdigest()
        
        return password_hash, salt
    
    def signup(self, email: str, username: str, password: str, 
               full_name: str = "") -> Dict[str, Any]:
        """
        Create new user account
        
        Returns:
            {'success': bool, 'message': str, 'user_id': int}
        """
        # Validate input
        if not email or not username or not password:
            return {
                'success': False,
                'message': 'Email, username, and password are required'
            }
        
        if len(password) < 6:
            return {
                'success': False,
                'message': 'Password must be at least 6 characters'
            }
        
        if '@' not in email:
            return {
                'success': False,
                'message': 'Please enter a valid email address'
            }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email or username already exists
            cursor.execute(
                'SELECT id FROM users WHERE email = ? OR username = ?',
                (email, username)
            )
            if cursor.fetchone():
                conn.close()
                return {
                    'success': False,
                    'message': 'Email or username already exists'
                }
            
            # Hash password
            password_hash, salt = self._hash_password(password)
            
            # Insert new user
            cursor.execute('''
                INSERT INTO users (email, username, password_hash, salt, full_name, status)
                VALUES (?, ?, ?, ?, ?, 'pending')
            ''', (email, username, password_hash, salt, full_name))
            
            user_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            print(f"✓ New user created: {username} ({email})")
            
            return {
                'success': True,
                'message': 'Account created successfully!',
                'user_id': user_id
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error creating account: {str(e)}'
            }
    
    def login(self, username_or_email: str, password: str, 
              remember_me: bool = False) -> Dict[str, Any]:
        """
        Authenticate user
        
        Returns:
            {'success': bool, 'message': str, 'user': dict, 'session_token': str}
        """
        if not username_or_email or not password:
            return {
                'success': False,
                'message': 'Username/email and password are required'
            }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find user by email or username
            cursor.execute('''
                SELECT id, email, username, password_hash, salt, full_name, is_active, status
                FROM users
                WHERE email = ? OR username = ?
            ''', (username_or_email, username_or_email))
            
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return {
                    'success': False,
                    'message': 'Invalid username/email or password'
                }
            
            user_id, email, username, stored_hash, salt, full_name, is_active, status = user
            
            # Check if user is blocked
            if status == 'blocked':
                conn.close()
                return {
                    'success': False,
                    'message': '🚫 Your account has been blocked. Please contact the administrator.'
                }
            
            # Check if user is pending approval
            if status == 'pending':
                conn.close()
                return {
                    'success': False,
                    'message': '⏳ Your account is pending approval. Please wait for admin approval.'
                }
            
            if not is_active:
                conn.close()
                return {
                    'success': False,
                    'message': 'Account is disabled'
                }
            
            # Verify password
            password_hash, _ = self._hash_password(password, salt)
            
            if password_hash != stored_hash:
                conn.close()
                return {
                    'success': False,
                    'message': 'Invalid username/email or password'
                }
            
            # Update last login
            cursor.execute('''
                UPDATE users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))
            
            conn.commit()
            
            # Create session token if remember_me
            session_token = None
            if remember_me:
                session_token = secrets.token_urlsafe(32)
                expires_at = datetime.now() + timedelta(days=30)
                
                cursor.execute('''
                    INSERT INTO sessions (user_id, session_token, expires_at)
                    VALUES (?, ?, ?)
                ''', (user_id, session_token, expires_at))
                
                conn.commit()
            
            conn.close()
            
            print(f"✓ User logged in: {username}")
            
            return {
                'success': True,
                'message': 'Login successful!',
                'user': {
                    'id': user_id,
                    'email': email,
                    'username': username,
                    'full_name': full_name
                },
                'session_token': session_token
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Login error: {str(e)}'
            }
    
    def verify_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Verify session token (for Remember Me feature)"""
        if not session_token:
            return None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.user_id, u.email, u.username, u.full_name
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP
            ''', (session_token,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                user_id, email, username, full_name = result
                return {
                    'id': user_id,
                    'email': email,
                    'username': username,
                    'full_name': full_name
                }
            
            return None
            
        except Exception as e:
            print(f"Session verification error: {e}")
            return None
    
    def logout(self, session_token: str = None):
        """Logout user (clear session)"""
        if session_token:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Logout error: {e}")
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT plans_generated, last_plan_date
                FROM user_stats
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                plans_generated, last_plan_date = result
                return {
                    'plans_generated': plans_generated,
                    'last_plan_date': last_plan_date
                }
            
            return {'plans_generated': 0, 'last_plan_date': None}
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {'plans_generated': 0, 'last_plan_date': None}
    
    def increment_plan_count(self, user_id: int):
        """Increment user's plan generation count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_stats
                SET plans_generated = plans_generated + 1,
                    last_plan_date = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating stats: {e}")


# Singleton instance
_auth_manager = None

def get_auth_manager() -> AuthManager:
    """Get or create AuthManager singleton"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
