"""
Admin Dashboard for Business Plan Generator
Manage users, approve signups, view activity, block/unblock users
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from auth.auth_manager import AuthManager


class AdminDashboard:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔐 Admin Dashboard - Business Plan Generator")
        self.root.geometry("1200x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.auth_manager = AuthManager()
        self.current_filter = "all"  # all, pending, approved, blocked
        
        self.setup_ui()
        self.load_users()
        
    def setup_ui(self):
        """Setup the admin dashboard UI"""
        
        # Header
        header_frame = ctk.CTkFrame(self.root, fg_color="#1a1a2e", height=80)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header_frame,
            text="🔐 Admin Dashboard",
            font=("Arial", 28, "bold"),
            text_color="#00ff88"
        )
        title.pack(side="left", padx=20)
        
        # Stats
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="Loading stats...",
            font=("Arial", 14),
            text_color="#ffffff"
        )
        self.stats_label.pack(side="right", padx=20)
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        filters = [
            ("All Users", "all", "#3498db"),
            ("Pending Approval", "pending", "#f39c12"),
            ("Approved", "approved", "#2ecc71"),
            ("Blocked", "blocked", "#e74c3c")
        ]
        
        for text, filter_val, color in filters:
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                width=150,
                height=40,
                fg_color=color,
                hover_color=self._darken_color(color),
                command=lambda f=filter_val: self.filter_users(f)
            )
            btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Refresh",
            width=120,
            height=40,
            fg_color="#9b59b6",
            hover_color="#8e44ad",
            command=self.load_users
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Quick approve all button
        approve_all_btn = ctk.CTkButton(
            filter_frame,
            text="✅ Approve All Pending",
            width=180,
            height=40,
            fg_color="#27ae60",
            hover_color="#229954",
            command=self.approve_all_pending
        )
        approve_all_btn.pack(side="right", padx=5)
        
        # User list frame
        list_frame = ctk.CTkFrame(self.root)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview for user list
        columns = ("Username", "Email", "Status", "Registered", "Last Login", "Plans Created")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=20)
        
        # Configure columns
        self.tree.column("#0", width=0, stretch=False)
        self.tree.column("Username", width=150, anchor="w")
        self.tree.column("Email", width=200, anchor="w")
        self.tree.column("Status", width=120, anchor="center")
        self.tree.column("Registered", width=150, anchor="center")
        self.tree.column("Last Login", width=150, anchor="center")
        self.tree.column("Plans Created", width=120, anchor="center")
        
        # Headings
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
        
        # Double-click to approve
        self.tree.bind("<Double-Button-1>", self._on_double_click)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Style the treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0,
                       font=("Arial", 11))
        style.configure("Treeview.Heading",
                       background="#1a1a2e",
                       foreground="white",
                       borderwidth=1,
                       font=("Arial", 12, "bold"))
        style.map("Treeview",
                 background=[("selected", "#0066cc")])
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=10)
        
        approve_btn = ctk.CTkButton(
            action_frame,
            text="✅ Approve User",
            width=150,
            height=50,
            fg_color="#2ecc71",
            hover_color="#27ae60",
            font=("Arial", 14, "bold"),
            command=self.approve_user
        )
        approve_btn.pack(side="left", padx=5)
        
        block_btn = ctk.CTkButton(
            action_frame,
            text="🚫 Block User",
            width=150,
            height=50,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Arial", 14, "bold"),
            command=self.block_user
        )
        block_btn.pack(side="left", padx=5)
        
        unblock_btn = ctk.CTkButton(
            action_frame,
            text="🔓 Unblock User",
            width=150,
            height=50,
            fg_color="#f39c12",
            hover_color="#e67e22",
            font=("Arial", 14, "bold"),
            command=self.unblock_user
        )
        unblock_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ Delete User",
            width=150,
            height=50,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            font=("Arial", 14, "bold"),
            command=self.delete_user
        )
        delete_btn.pack(side="left", padx=5)
        
        view_details_btn = ctk.CTkButton(
            action_frame,
            text="📊 View Details",
            width=150,
            height=50,
            fg_color="#3498db",
            hover_color="#2980b9",
            font=("Arial", 14, "bold"),
            command=self.view_user_details
        )
        view_details_btn.pack(side="right", padx=5)
    
    def _darken_color(self, hex_color):
        """Darken a hex color by 20%"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = int(r * 0.8), int(g * 0.8), int(b * 0.8)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _on_double_click(self, event):
        """Handle double-click on user row"""
        username = self.get_selected_username()
        if username:
            # Get current status
            selection = self.tree.selection()
            if selection:
                item = self.tree.item(selection[0])
                status = item['values'][2]
                
                if '⏳ Pending' in status:
                    # Auto-approve pending users on double-click
                    self.approve_user()
                else:
                    # Show details for other users
                    self.view_user_details()
    
    def load_users(self):
        """Load all users from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            # Get all users
            cursor.execute("""
                SELECT username, email, status, created_at, last_login, business_plans_created
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = cursor.fetchall()
            
            # Count stats
            total = len(users)
            pending = sum(1 for u in users if u[2] == 'pending')
            approved = sum(1 for u in users if u[2] == 'approved')
            blocked = sum(1 for u in users if u[2] == 'blocked')
            
            self.stats_label.configure(
                text=f"Total: {total} | Pending: {pending} | Approved: {approved} | Blocked: {blocked}"
            )
            
            # Add users to treeview
            for user in users:
                username, email, status, created_at, last_login, plans = user
                
                # Format dates
                created = created_at.split()[0] if created_at else "N/A"
                last_login_fmt = last_login.split()[0] if last_login else "Never"
                
                # Status emoji
                status_emoji = {
                    'pending': '⏳ Pending',
                    'approved': '✅ Approved',
                    'blocked': '🚫 Blocked'
                }.get(status, status)
                
                # Filter by current filter
                if self.current_filter == "all" or status == self.current_filter:
                    self.tree.insert("", "end", values=(
                        username,
                        email,
                        status_emoji,
                        created,
                        last_login_fmt,
                        plans or 0
                    ))
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def filter_users(self, filter_type):
        """Filter users by status"""
        self.current_filter = filter_type
        self.load_users()
    
    def get_selected_username(self):
        """Get the selected username"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a user first")
            return None
        
        item = self.tree.item(selection[0])
        username = item['values'][0]
        return username
    
    def approve_user(self):
        """Approve a pending user"""
        username = self.get_selected_username()
        if not username:
            return
        
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            # Check current status
            cursor.execute("SELECT status FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if not result:
                messagebox.showerror("Error", f"User '{username}' not found!")
                conn.close()
                return
            
            current_status = result[0]
            
            if current_status == 'approved':
                messagebox.showinfo("Info", f"User '{username}' is already approved!")
                conn.close()
                return
            
            # Update to approved
            cursor.execute("UPDATE users SET status = 'approved' WHERE username = ?", (username,))
            conn.commit()
            
            rows_affected = cursor.rowcount
            conn.close()
            
            if rows_affected > 0:
                messagebox.showinfo("✅ Success", f"User '{username}' has been approved!\n\nThey can now login to the application.")
                print(f"✅ Approved user: {username}")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to update user status")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve user:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def approve_all_pending(self):
        """Approve all pending users at once"""
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            # Get count of pending users
            cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'pending'")
            pending_count = cursor.fetchone()[0]
            
            if pending_count == 0:
                messagebox.showinfo("Info", "No pending users to approve!")
                conn.close()
                return
            
            # Confirm
            if not messagebox.askyesno("Confirm Approve All", 
                                      f"Approve all {pending_count} pending user(s)?"):
                conn.close()
                return
            
            # Approve all
            cursor.execute("UPDATE users SET status = 'approved' WHERE status = 'pending'")
            conn.commit()
            rows_affected = cursor.rowcount
            conn.close()
            
            messagebox.showinfo("✅ Success", f"Approved {rows_affected} user(s)!\n\nAll pending users can now login.")
            print(f"✅ Approved {rows_affected} pending users")
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve users:\n{str(e)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve user: {str(e)}")
    
    def block_user(self):
        """Block a user"""
        username = self.get_selected_username()
        if not username:
            return
        
        if not messagebox.askyesno("Confirm Block", f"Are you sure you want to block '{username}'?\n\nThey will not be able to login."):
            return
        
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET status = 'blocked' WHERE username = ?", (username,))
            conn.commit()
            
            rows_affected = cursor.rowcount
            conn.close()
            
            if rows_affected > 0:
                messagebox.showinfo("🚫 Success", f"User '{username}' has been blocked!")
                print(f"🚫 Blocked user: {username}")
                self.load_users()
            else:
                messagebox.showerror("Error", "Failed to update user status")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to block user:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def unblock_user(self):
        """Unblock a user"""
        username = self.get_selected_username()
        if not username:
            return
        
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            cursor.execute("UPDATE users SET status = 'approved' WHERE username = ?", (username,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"User '{username}' has been unblocked!")
            self.load_users()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unblock user: {str(e)}")
    
    def delete_user(self):
        """Delete a user permanently"""
        username = self.get_selected_username()
        if not username:
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to PERMANENTLY delete '{username}'?\n\nThis cannot be undone!"):
            try:
                conn = sqlite3.connect('data/users.db')
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"User '{username}' has been deleted!")
                self.load_users()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
    
    def view_user_details(self):
        """View detailed user information"""
        username = self.get_selected_username()
        if not username:
            return
        
        try:
            conn = sqlite3.connect('data/users.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT username, email, status, created_at, last_login, 
                       business_plans_created, last_plan_date
                FROM users
                WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                username, email, status, created, last_login, plans, last_plan = user
                
                details = f"""
╔══════════════════════════════════════════╗
║          USER DETAILS                     ║
╚══════════════════════════════════════════╝

👤 Username:        {username}
📧 Email:           {email}
🔐 Status:          {status.upper()}

📅 Registered:      {created or 'N/A'}
🕐 Last Login:      {last_login or 'Never'}

📊 Business Plans:  {plans or 0}
📝 Last Plan:       {last_plan or 'N/A'}

═══════════════════════════════════════════
                """
                
                messagebox.showinfo("User Details", details)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user details: {str(e)}")
    
    def run(self):
        """Run the admin dashboard"""
        self.root.mainloop()


if __name__ == "__main__":
    # Check if users.db exists
    if not Path("data/users.db").exists():
        print("❌ Error: data/users.db not found!")
        print("Please make sure the authentication system is set up.")
        sys.exit(1)
    
    app = AdminDashboard()
    app.run()
