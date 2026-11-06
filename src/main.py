"""
Main entry point for Business Plan Generator
"""
import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Check for required environment variables
from dotenv import load_dotenv
load_dotenv()

def check_requirements():
    """Check if all requirements are met"""
    errors = []
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        errors.append("No AI API key found. Please set either OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
    
    return errors

def main():
    """Main application entry point"""
    
    print("=" * 60)
    print("  Business Plan Generator - AI Powered")
    print("=" * 60)
    print()
    
    # Check requirements
    errors = check_requirements()
    if errors:
        print("⚠️  Configuration Issues:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("Please create a .env file based on .env.example")
        print("and add your API keys.")
        print()
        
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Launch GUI
    try:
        from gui.main_window import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print()
        print("Please install required dependencies:")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
