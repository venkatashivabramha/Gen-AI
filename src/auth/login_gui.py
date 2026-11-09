"""
Login/Signup GUI using CustomTkinter
Beautiful, modern authentication interface
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Callable
from .auth_manager import get_auth_manager


class LoginWindow(ctk.CTk):
    """Login/Signup window with modern UI"""
    
    def __init__(self, on_login_success: Callable = None):
        super().__init__()
        
        self.auth_manager = get_auth_manager()
        self.on_login_success = on_login_success
        self.current_user = None
        
        # Configure window
        self.title("Business Plan Generator - Login")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Center window
        self._center_window()
        
        # Create UI
        self._create_ui()
    
    def _center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        """Create login/signup interface"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Title
        title = ctk.CTkLabel(
            main_frame,
            text="🚀 Business Plan Generator",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            main_frame,
            text="AI-Powered Professional Business Plans",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))
        
        # Tab view for Login/Signup
        self.tabview = ctk.CTkTabview(main_frame, width=400, height=400)
        self.tabview.pack(fill="both", expand=True)
        
        # Add tabs
        self.tabview.add("Login")
        self.tabview.add("Sign Up")
        
        # Create login tab
        self._create_login_tab()
        
        # Create signup tab
        self._create_signup_tab()
    
    def _create_login_tab(self):
        """Create login form"""
        tab = self.tabview.tab("Login")
        
        # Username/Email
        username_label = ctk.CTkLabel(tab, text="Username or Email:")
        username_label.pack(pady=(20, 5))
        
        self.login_username = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="Enter username or email"
        )
        self.login_username.pack(pady=(0, 15))
        
        # Password
        password_label = ctk.CTkLabel(tab, text="Password:")
        password_label.pack(pady=(0, 5))
        
        self.login_password = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="Enter password",
            show="●"
        )
        self.login_password.pack(pady=(0, 15))
        
        # Remember me
        self.remember_me = ctk.CTkCheckBox(
            tab,
            text="Remember me for 30 days"
        )
        self.remember_me.pack(pady=(0, 20))
        
        # Login button
        login_btn = ctk.CTkButton(
            tab,
            text="Login",
            command=self._handle_login,
            width=300,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        login_btn.pack(pady=(0, 10))
        
        # Or continue without login
        skip_btn = ctk.CTkButton(
            tab,
            text="Continue Without Login",
            command=self._skip_login,
            width=300,
            fg_color="transparent",
            border_width=2
        )
        skip_btn.pack(pady=(10, 0))
        
        # Bind Enter key
        self.login_password.bind('<Return>', lambda e: self._handle_login())
    
    def _create_signup_tab(self):
        """Create signup form"""
        tab = self.tabview.tab("Sign Up")
        
        # Full Name
        name_label = ctk.CTkLabel(tab, text="Full Name (Optional):")
        name_label.pack(pady=(20, 5))
        
        self.signup_name = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="John Doe"
        )
        self.signup_name.pack(pady=(0, 10))
        
        # Email
        email_label = ctk.CTkLabel(tab, text="Email:")
        email_label.pack(pady=(0, 5))
        
        self.signup_email = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="your@email.com"
        )
        self.signup_email.pack(pady=(0, 10))
        
        # Username
        username_label = ctk.CTkLabel(tab, text="Username:")
        username_label.pack(pady=(0, 5))
        
        self.signup_username = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="Choose a username"
        )
        self.signup_username.pack(pady=(0, 10))
        
        # Password
        password_label = ctk.CTkLabel(tab, text="Password (min 6 characters):")
        password_label.pack(pady=(0, 5))
        
        self.signup_password = ctk.CTkEntry(
            tab,
            width=300,
            placeholder_text="Choose a strong password",
            show="●"
        )
        self.signup_password.pack(pady=(0, 15))
        
        # Signup button
        signup_btn = ctk.CTkButton(
            tab,
            text="Create Account",
            command=self._handle_signup,
            width=300,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#28a745"
        )
        signup_btn.pack(pady=(0, 10))
        
        # Bind Enter key
        self.signup_password.bind('<Return>', lambda e: self._handle_signup())
    
    def _handle_login(self):
        """Handle login button click"""
        username = self.login_username.get().strip()
        password = self.login_password.get()
        remember = self.remember_me.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Attempt login
        result = self.auth_manager.login(username, password, remember)
        
        if result['success']:
            self.current_user = result['user']
            messagebox.showinfo("Success", f"Welcome back, {result['user']['username']}!")
            
            # Close login window and open main app
            self.destroy()
            if self.on_login_success:
                self.on_login_success(result['user'])
        else:
            messagebox.showerror("Login Failed", result['message'])
    
    def _handle_signup(self):
        """Handle signup button click"""
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        
        # Attempt signup
        result = self.auth_manager.signup(email, username, password, name)
        
        if result['success']:
            messagebox.showinfo("Success", "Account created! Please login.")
            # Switch to login tab
            self.tabview.set("Login")
            # Pre-fill username
            self.login_username.delete(0, 'end')
            self.login_username.insert(0, username)
            self.login_password.focus()
        else:
            messagebox.showerror("Signup Failed", result['message'])
    
    def _skip_login(self):
        """Continue without logging in"""
        response = messagebox.askyesno(
            "Continue Without Login",
            "You can use the app without an account, but your business plans won't be saved.\n\nContinue anyway?"
        )
        if response:
            self.current_user = None
            self.destroy()
            if self.on_login_success:
                self.on_login_success(None)


def show_login(on_success: Callable = None) -> Optional[dict]:
    """
    Show login window and return user info
    
    Args:
        on_success: Callback function when login succeeds
    
    Returns:
        User dict if successful, None if skipped
    """
    app = LoginWindow(on_success)
    app.mainloop()
    return app.current_user
