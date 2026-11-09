"""
Main GUI Window using CustomTkinter
Modern, user-friendly interface for business plan generation
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
from typing import Dict, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from business_plan_generator import BusinessPlanGenerator
from config.config import BUSINESS_TYPES


class BusinessPlanGeneratorApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Business Plan Generator - AI Powered")
        self.geometry("1200x800")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize generator (will be created when needed)
        self.generator = None
        
        # Create UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface"""
        
        # Create main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self._create_sidebar()
        
        # Main content area
        self._create_main_content()
    
    def _create_sidebar(self):
        """Create sidebar with mode selection"""
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        title = ctk.CTkLabel(
            self.sidebar,
            text="Business Plan\nGenerator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)
        
        # Mode selection
        mode_label = ctk.CTkLabel(
            self.sidebar,
            text="Input Mode:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        mode_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        
        # Form Mode Button
        self.form_btn = ctk.CTkButton(
            self.sidebar,
            text="📝 Form Input",
            command=lambda: self._switch_mode("form"),
            font=ctk.CTkFont(size=13)
        )
        self.form_btn.grid(row=2, column=0, padx=20, pady=10)
        
        # AI Mode Button
        self.ai_btn = ctk.CTkButton(
            self.sidebar,
            text="🤖 AI Description",
            command=lambda: self._switch_mode("ai"),
            font=ctk.CTkFont(size=13)
        )
        self.ai_btn.grid(row=3, column=0, padx=20, pady=10)
        
        # Template Mode Button
        self.template_btn = ctk.CTkButton(
            self.sidebar,
            text="📋 Template",
            command=lambda: self._switch_mode("template"),
            font=ctk.CTkFont(size=13)
        )
        self.template_btn.grid(row=4, column=0, padx=20, pady=10)
        
        # Settings
        settings_label = ctk.CTkLabel(
            self.sidebar,
            text="Settings:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_label.grid(row=7, column=0, padx=20, pady=(20, 10))
        
        # LLM Provider selection
        self.llm_var = ctk.StringVar(value="groq")
        llm_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["groq", "openrouter", "anthropic", "openai", "huggingface"],
            variable=self.llm_var,
            font=ctk.CTkFont(size=12),
            width=180
        )
        llm_menu.grid(row=8, column=0, padx=20, pady=10)
        
        # Theme toggle
        self.theme_btn = ctk.CTkButton(
            self.sidebar,
            text="🌙 Dark/Light",
            command=self._toggle_theme,
            font=ctk.CTkFont(size=12)
        )
        self.theme_btn.grid(row=9, column=0, padx=20, pady=10)
    
    def _create_main_content(self):
        """Create main content area"""
        
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self.main_frame,
            text="Create Your Comprehensive Business Plan",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Content frame (will be replaced based on mode)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Start with form mode
        self._switch_mode("form")
    
    def _switch_mode(self, mode: str):
        """Switch between different input modes"""
        
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create appropriate mode UI
        if mode == "form":
            self._create_form_mode()
        elif mode == "ai":
            self._create_ai_mode()
        elif mode == "template":
            self._create_template_mode()
    
    def _create_form_mode(self):
        """Create form input mode UI"""
        
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.content_frame)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Form fields
        self.form_data = {}
        
        fields = [
            ("Business Name", "business_name", "Enter your business name"),
            ("Industry", "industry", "e.g., Technology, Retail, Healthcare"),
            ("Business Type", "business_type", "e.g., Startup, E-commerce, Services"),
            ("Location", "location", "City, State/Country"),
            ("Target Market", "target_market", "Describe your target customers"),
            ("Products/Services", "products_services", "What do you offer?"),
            ("Revenue Model", "revenue_model", "How will you make money?"),
            ("Initial Investment", "initial_investment", "Estimated startup costs"),
            ("Innovation Focus", "innovation_focus", "Key innovations or differentiators"),
        ]
        
        for i, (label, key, placeholder) in enumerate(fields):
            # Label
            lbl = ctk.CTkLabel(
                scroll_frame,
                text=label + ":",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            lbl.grid(row=i*2, column=0, padx=10, pady=(10, 5), sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(
                scroll_frame,
                placeholder_text=placeholder,
                width=600,
                font=ctk.CTkFont(size=12)
            )
            entry.grid(row=i*2+1, column=0, padx=10, pady=(0, 10), sticky="ew")
            self.form_data[key] = entry
        
        # Description (larger text box)
        desc_label = ctk.CTkLabel(
            scroll_frame,
            text="Business Description:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        desc_label.grid(row=len(fields)*2, column=0, padx=10, pady=(10, 5), sticky="w")
        
        desc_text = ctk.CTkTextbox(
            scroll_frame,
            width=600,
            height=100,
            font=ctk.CTkFont(size=12)
        )
        desc_text.grid(row=len(fields)*2+1, column=0, padx=10, pady=(0, 20), sticky="ew")
        self.form_data["description"] = desc_text
        
        # Output format selection
        format_label = ctk.CTkLabel(
            scroll_frame,
            text="Output Formats:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        format_label.grid(row=len(fields)*2+2, column=0, padx=10, pady=(10, 5), sticky="w")
        
        format_frame = ctk.CTkFrame(scroll_frame)
        format_frame.grid(row=len(fields)*2+3, column=0, padx=10, pady=(0, 20), sticky="w")
        
        self.format_vars = {}
        formats = ["PDF", "HTML", "DOCX"]
        for i, fmt in enumerate(formats):
            var = ctk.BooleanVar(value=(fmt == "PDF"))
            cb = ctk.CTkCheckBox(
                format_frame,
                text=fmt,
                variable=var,
                font=ctk.CTkFont(size=12)
            )
            cb.grid(row=0, column=i, padx=10)
            self.format_vars[fmt.lower()] = var
        
        # Real Market Data Toggle (NEW!)
        data_label = ctk.CTkLabel(
            scroll_frame,
            text="📊 Market Data Enhancement:",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        data_label.grid(row=len(fields)*2+4, column=0, padx=10, pady=(20, 5), sticky="w")
        
        data_info_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        data_info_frame.grid(row=len(fields)*2+5, column=0, padx=10, pady=(0, 10), sticky="w")
        
        self.use_real_data_var = ctk.BooleanVar(value=True)  # Default: enabled
        real_data_cb = ctk.CTkCheckBox(
            data_info_frame,
            text="Use Real Market Data (FREE from Yahoo Finance)",
            variable=self.use_real_data_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2ecc71",  # Green
            hover_color="#27ae60"
        )
        real_data_cb.grid(row=0, column=0, padx=5)
        
        data_info = ctk.CTkLabel(
            data_info_frame,
            text="✨ Fetches verified market sizes, competitor data, and growth rates",
            font=ctk.CTkFont(size=11),
            text_color="#7f8c8d"
        )
        data_info.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="w")
        
        # Generate button - LARGE, RED, VISIBLE
        generate_btn = ctk.CTkButton(
            scroll_frame,
            text="🚀 GENERATE BUSINESS PLAN 🚀",
            command=self._generate_from_form,
            height=80,
            width=700,
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#DC143C",  # Crimson red
            hover_color="#8B0000",  # Dark red
            corner_radius=15
        )
        generate_btn.grid(row=len(fields)*2+6, column=0, padx=10, pady=20)
        
        scroll_frame.grid_columnconfigure(0, weight=1)
    
    def _create_ai_mode(self):
        """Create AI natural language mode UI"""
        
        # Create scrollable frame
        scroll_container = ctk.CTkScrollableFrame(self.content_frame)
        scroll_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Instructions - BIGGER AND CLEARER
        instructions = ctk.CTkLabel(
            scroll_container,
            text="📝 Describe your business idea in natural language.\nThe AI will create a comprehensive business plan from your description.",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=700
        )
        instructions.pack(pady=30)
        
        # Text area
        self.ai_text = ctk.CTkTextbox(
            scroll_container,
            width=700,
            height=300,
            font=ctk.CTkFont(size=13)
        )
        self.ai_text.pack(pady=20, padx=20)
        self.ai_text.insert("1.0", "Example: I want to start a technology startup that uses AI to help small businesses automate their customer service. We'll target small to medium businesses in the retail sector...")
        
        # Output formats
        format_label = ctk.CTkLabel(
            scroll_container,
            text="Output Formats:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        format_label.pack(pady=(20, 10))
        
        format_frame = ctk.CTkFrame(scroll_container)
        format_frame.pack(pady=10)
        
        self.ai_format_vars = {}
        formats = ["PDF", "HTML", "DOCX"]
        for i, fmt in enumerate(formats):
            var = ctk.BooleanVar(value=(fmt == "PDF"))
            cb = ctk.CTkCheckBox(
                format_frame,
                text=fmt,
                variable=var,
                font=ctk.CTkFont(size=14)
            )
            cb.grid(row=0, column=i, padx=20)
            self.ai_format_vars[fmt.lower()] = var
        
        # Generate button - LARGE, RED, VISIBLE
        generate_btn = ctk.CTkButton(
            scroll_container,
            text="🤖 GENERATE WITH AI 🤖",
            command=self._generate_from_ai,
            height=80,
            width=700,
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#DC143C",  # Crimson red
            hover_color="#8B0000",  # Dark red
            corner_radius=15
        )
        generate_btn.pack(pady=40)
    
    def _create_template_mode(self):
        """Create template selection mode UI"""
        
        # Create scrollable frame
        scroll_container = ctk.CTkScrollableFrame(self.content_frame)
        scroll_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Instructions - BIGGER AND CLEARER
        instructions = ctk.CTkLabel(
            scroll_container,
            text="📋 Select a business type template and provide basic information.\nQuickest way to generate a business plan!",
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=700
        )
        instructions.pack(pady=30)
        
        # Template selection
        template_label = ctk.CTkLabel(
            scroll_container,
            text="Select Business Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        template_label.pack(pady=(20, 10))
        
        self.template_var = ctk.StringVar(value=BUSINESS_TYPES[0])
        template_menu = ctk.CTkOptionMenu(
            scroll_container,
            values=BUSINESS_TYPES,
            variable=self.template_var,
            width=500,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=12)
        )
        template_menu.pack(pady=10)
        
        # Basic info frame
        info_frame = ctk.CTkFrame(scroll_container)
        info_frame.pack(pady=30, padx=20, fill="x")
        
        self.template_data = {}
        
        basic_fields = [
            ("Business Name", "business_name"),
            ("Location", "location"),
            ("Specific Focus", "specific_focus")
        ]
        
        for label, key in basic_fields:
            lbl = ctk.CTkLabel(
                info_frame,
                text=label + ":",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            lbl.pack(pady=(15, 5), anchor="w")
            
            entry = ctk.CTkEntry(
                info_frame,
                width=600,
                height=40,
                font=ctk.CTkFont(size=13)
            )
            entry.pack(pady=(0, 10), fill="x")
            self.template_data[key] = entry
        
        # Output formats
        format_label = ctk.CTkLabel(
            scroll_container,
            text="Output Formats:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        format_label.pack(pady=(30, 10))
        
        format_frame = ctk.CTkFrame(scroll_container)
        format_frame.pack(pady=10)
        
        self.template_format_vars = {}
        formats = ["PDF", "HTML", "DOCX"]
        for i, fmt in enumerate(formats):
            var = ctk.BooleanVar(value=(fmt == "PDF"))
            cb = ctk.CTkCheckBox(
                format_frame,
                text=fmt,
                variable=var,
                font=ctk.CTkFont(size=14)
            )
            cb.grid(row=0, column=i, padx=20)
            self.template_format_vars[fmt.lower()] = var
        
        # Generate button - LARGE, RED, VISIBLE
        generate_btn = ctk.CTkButton(
            scroll_container,
            text="📋 GENERATE FROM TEMPLATE 📋",
            command=self._generate_from_template,
            height=80,
            width=700,
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#DC143C",  # Crimson red
            hover_color="#8B0000",  # Dark red
            corner_radius=15
        )
        generate_btn.pack(pady=40)
    
    def _generate_from_form(self):
        """Generate business plan from form data"""
        
        # Collect form data
        data = {}
        for key, widget in self.form_data.items():
            if isinstance(widget, ctk.CTkTextbox):
                data[key] = widget.get("1.0", "end-1c")
            else:
                data[key] = widget.get()
        
        # Get output formats
        formats = [fmt for fmt, var in self.format_vars.items() if var.get()]
        
        if not formats:
            messagebox.showerror("Error", "Please select at least one output format")
            return
        
        # Validate required fields
        if not data.get("business_name"):
            messagebox.showerror("Error", "Business name is required")
            return
        
        # Generate in background thread
        self._run_generation(
            lambda: self._get_generator().generate_from_form(data, formats)
        )
    
    def _generate_from_ai(self):
        """Generate business plan from AI description"""
        
        description = self.ai_text.get("1.0", "end-1c").strip()
        
        if not description or description.startswith("Example:"):
            messagebox.showerror("Error", "Please provide a business description")
            return
        
        # Get output formats
        formats = [fmt for fmt, var in self.ai_format_vars.items() if var.get()]
        
        if not formats:
            messagebox.showerror("Error", "Please select at least one output format")
            return
        
        # Generate in background thread
        self._run_generation(
            lambda: self._get_generator().generate_from_natural_language(description, formats)
        )
    
    def _generate_from_template(self):
        """Generate business plan from template"""
        
        business_type = self.template_var.get()
        
        # Collect template data
        basic_info = {}
        for key, widget in self.template_data.items():
            basic_info[key] = widget.get()
        
        if not basic_info.get("business_name"):
            messagebox.showerror("Error", "Business name is required")
            return
        
        # Get output formats
        formats = [fmt for fmt, var in self.template_format_vars.items() if var.get()]
        
        if not formats:
            messagebox.showerror("Error", "Please select at least one output format")
            return
        
        # Generate in background thread
        self._run_generation(
            lambda: self._get_generator().generate_from_template(business_type, basic_info, formats)
        )
    
    def _run_generation(self, generation_func):
        """Run generation in background thread"""
        
        # Show progress dialog
        progress = self._show_progress_dialog()
        
        def worker():
            try:
                result = generation_func()
                self.after(0, lambda r=result, p=progress: self._on_generation_complete(r, p))
            except Exception as e:
                error_msg = str(e)
                self.after(0, lambda err=error_msg, p=progress: self._on_generation_error(err, p))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def _show_progress_dialog(self):
        """Show progress dialog"""
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Generating Business Plan")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text="Generating your business plan...\nThis may take a few moments.",
            font=ctk.CTkFont(size=14)
        )
        label.pack(pady=30)
        
        progress = ctk.CTkProgressBar(dialog, width=300, mode="indeterminate")
        progress.pack(pady=20)
        progress.start()
        
        dialog.progress = progress
        
        return dialog
    
    def _on_generation_complete(self, result, progress_dialog):
        """Handle generation completion"""
        
        progress_dialog.destroy()
        
        if result['status'] == 'success':
            # Show success dialog with file links
            message = "Business plan generated successfully!\n\nFiles created:\n"
            for fmt, path in result['files'].items():
                message += f"\n{fmt.upper()}: {path}"
            
            messagebox.showinfo("Success", message)
            
            # Ask if user wants to open the files
            if messagebox.askyesno("Open Files", "Would you like to open the output folder?"):
                import subprocess
                from config.config import OUTPUT_DIR
                subprocess.Popen(f'explorer "{OUTPUT_DIR}"')
        else:
            messagebox.showerror("Error", "Generation failed. Please check console for details.")
    
    def _on_generation_error(self, error, progress_dialog):
        """Handle generation error"""
        
        progress_dialog.destroy()
        messagebox.showerror("Error", f"An error occurred:\n\n{error}")
    
    def _get_generator(self):
        """Get or create generator instance"""
        
        if self.generator is None:
            provider = self.llm_var.get()
            # Get real data preference from checkbox
            use_real_data = getattr(self, 'use_real_data_var', None)
            use_real_data_enabled = use_real_data.get() if use_real_data else True
            
            self.generator = BusinessPlanGenerator(
                provider, 
                use_real_data=use_real_data_enabled
            )
        
        return self.generator
    
    def _toggle_theme(self):
        """Toggle between dark and light theme"""
        
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)


def main():
    """Main entry point"""
    app = BusinessPlanGeneratorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
