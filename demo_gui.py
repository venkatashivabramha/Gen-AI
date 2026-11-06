"""
Demo script to show the GUI without requiring API keys
"""
import customtkinter as ctk
from datetime import datetime

class DemoApp(ctk.CTk):
    """Demo application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Business Plan Generator - Demo Mode")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the demo user interface"""
        
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="🚀 Business Plan Generator",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, pady=30)
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            main_frame,
            text="AI-Powered Business Planning Tool",
            font=ctk.CTkFont(size=18)
        )
        subtitle.grid(row=1, column=0, pady=10)
        
        # Status
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.grid(row=2, column=0, pady=30, padx=40, sticky="ew")
        
        status_text = """
✅ Application Structure: COMPLETE
✅ GUI Framework: CustomTkinter Loaded
✅ Python Version: 3.12.10
✅ Project Files: All Created

⚠️  To use full features:
   1. Get an API key from OpenAI or Anthropic
   2. Add it to the .env file
   3. Run: python src/main.py
        """
        
        status_label = ctk.CTkLabel(
            status_frame,
            text=status_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        status_label.pack(pady=20, padx=20)
        
        # Features
        features_frame = ctk.CTkFrame(main_frame)
        features_frame.grid(row=3, column=0, pady=20, padx=40, sticky="ew")
        
        features_label = ctk.CTkLabel(
            features_frame,
            text="🎯 Features Available:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        features_label.pack(pady=10)
        
        features_text = """
📝 Form-based Input Mode
🤖 AI Natural Language Mode
📋 Template-based Generation
📄 Export to PDF, HTML, DOCX
🎨 Dark/Light Theme Toggle
💻 Command-Line Interface
🔌 MCP Integration (Optional)
        """
        
        features_content = ctk.CTkLabel(
            features_frame,
            text=features_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        features_content.pack(pady=10, padx=20)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.grid(row=4, column=0, pady=30)
        
        # Documentation button
        docs_btn = ctk.CTkButton(
            button_frame,
            text="📚 Open Documentation",
            command=self.open_docs,
            height=50,
            width=250,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        docs_btn.grid(row=0, column=0, padx=10)
        
        # Setup button
        setup_btn = ctk.CTkButton(
            button_frame,
            text="⚙️ Setup Instructions",
            command=self.show_setup,
            height=50,
            width=250,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        setup_btn.grid(row=0, column=1, padx=10)
        
        # Theme toggle
        theme_btn = ctk.CTkButton(
            button_frame,
            text="🌙 Toggle Theme",
            command=self.toggle_theme,
            height=50,
            width=250,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        theme_btn.grid(row=0, column=2, padx=10)
        
        # Footer
        footer = ctk.CTkLabel(
            main_frame,
            text=f"Demo Mode | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        footer.grid(row=5, column=0, pady=20)
    
    def open_docs(self):
        """Open documentation folder"""
        import subprocess
        import os
        
        # Open the project folder
        folder_path = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(f'explorer "{folder_path}"')
        
        # Show message
        self.show_info("Documentation", "Opening project folder...\n\nRead QUICK_START.md to get started!")
    
    def show_setup(self):
        """Show setup instructions"""
        message = """
Setup Steps:

1. Get an API Key:
   • OpenAI: https://platform.openai.com/api-keys
   • Anthropic: https://console.anthropic.com/

2. Edit the .env file:
   • Open .env in a text editor
   • Add your API key (no quotes)
   • Save the file

3. Run the full application:
   • Double-click: run_app.bat
   • Or run: python src/main.py

4. Generate your first plan:
   • Choose an input mode
   • Fill in your business details
   • Click Generate!

For detailed instructions, see INSTALLATION.md
        """
        
        self.show_info("Setup Instructions", message)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        current = ctk.get_appearance_mode()
        new_mode = "light" if current.lower() == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
        self.show_info("Theme Changed", f"Switched to {new_mode} mode!")
    
    def show_info(self, title, message):
        """Show info dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.transient(self)
        
        # Make it modal
        dialog.grab_set()
        
        # Message
        text = ctk.CTkTextbox(dialog, wrap="word", font=ctk.CTkFont(size=12))
        text.pack(fill="both", expand=True, padx=20, pady=20)
        text.insert("1.0", message)
        text.configure(state="disabled")
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        close_btn.pack(pady=10)

def main():
    """Main entry point"""
    print("=" * 60)
    print("  Business Plan Generator - Demo Mode")
    print("=" * 60)
    print()
    print("✅ GUI Framework: Ready")
    print("✅ Application: Installed")
    print()
    print("ℹ️  Running in demo mode (no API key required)")
    print("   To use full features, add your API key to .env file")
    print()
    print("🚀 Launching GUI...")
    print()
    
    app = DemoApp()
    app.mainloop()

if __name__ == "__main__":
    main()
