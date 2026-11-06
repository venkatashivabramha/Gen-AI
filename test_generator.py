"""
Test script for Business Plan Generator
Tests the generation without GUI
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from business_plan_generator import BusinessPlanGenerator
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

def test_form_generation():
    """Test generation from form data"""
    print("=" * 60)
    print("Testing Form-Based Generation")
    print("=" * 60)
    
    # Sample business data
    business_data = {
        "business_name": "TechFlow Solutions",
        "industry": "Technology / SaaS",
        "business_type": "Technology Startup",
        "location": "San Francisco, CA",
        "description": "TechFlow Solutions provides an AI-powered project management platform that helps remote teams collaborate more effectively. Our platform uses machine learning to predict project bottlenecks and suggest optimal task allocations.",
        "target_market": "Remote teams in technology companies, ranging from 10-500 employees, particularly in software development, marketing agencies, and consulting firms.",
        "products_services": "Cloud-based project management SaaS platform with AI-powered insights, real-time collaboration tools, and integration with popular development tools.",
        "revenue_model": "Monthly subscription with tiered pricing: Basic ($10/user), Professional ($25/user), Enterprise (custom pricing)",
        "initial_investment": "$500,000 for initial development, marketing, and 12-month runway",
        "innovation_focus": "AI-powered predictive analytics for project management, automated task prioritization, intelligent resource allocation"
    }
    
    try:
        # Initialize generator
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        print(f"\nUsing LLM Provider: {provider}")
        
        generator = BusinessPlanGenerator(provider)
        print("✓ Generator initialized")
        
        # Generate business plan
        print("\n🚀 Starting generation...\n")
        result = generator.generate_from_form(business_data, output_formats=['html', 'pdf'])
        
        # Display results
        print("\n" + "=" * 60)
        print("✅ Generation Complete!")
        print("=" * 60)
        print(f"\nStatus: {result['status']}")
        print("\nGenerated Files:")
        for fmt, path in result['files'].items():
            print(f"  • {fmt.upper()}: {path}")
        
        print("\nGenerated Sections:")
        for section_name in result['sections'].keys():
            print(f"  • {section_name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_generation():
    """Test generation from natural language"""
    print("\n" + "=" * 60)
    print("Testing AI Description Generation")
    print("=" * 60)
    
    description = """
    I want to start an e-commerce business selling eco-friendly home products.
    We'll focus on sustainable, biodegradable alternatives to common household items
    like cleaning supplies, kitchen products, and personal care items.
    
    Our target market is environmentally conscious consumers aged 25-45 with 
    middle to upper-middle income, primarily in urban areas. We'll start with
    a direct-to-consumer model through our website, then expand to marketplace
    platforms like Amazon and Etsy.
    
    Initial investment needed is around $100,000 for inventory, website development,
    and initial marketing. Revenue will come from product sales with a 40-50% margin.
    """
    
    try:
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        generator = BusinessPlanGenerator(provider)
        
        print("\n🤖 Generating from natural language...\n")
        result = generator.generate_from_natural_language(description, output_formats=['html'])
        
        print("\n✅ Generation Complete!")
        print(f"Status: {result['status']}")
        print("\nGenerated Files:")
        for fmt, path in result['files'].items():
            print(f"  • {fmt.upper()}: {path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_environment():
    """Check if environment is properly configured"""
    print("Checking environment configuration...")
    
    issues = []
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        issues.append("No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    elif openai_key:
        print("✓ OpenAI API key found")
    elif anthropic_key:
        print("✓ Anthropic API key found")
    
    # Check output directory
    output_dir = Path("output")
    if output_dir.exists():
        print(f"✓ Output directory exists: {output_dir}")
    else:
        print(f"⚠ Output directory will be created: {output_dir}")
    
    if issues:
        print("\n❌ Configuration issues:")
        for issue in issues:
            print(f"  • {issue}")
        return False
    
    print("\n✓ Environment configured correctly\n")
    return True

def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  Business Plan Generator - Test Suite")
    print("=" * 60 + "\n")
    
    # Check environment
    if not check_environment():
        print("\nPlease configure your environment and try again.")
        print("Create a .env file with your API keys.")
        return
    
    # Choose test
    print("Select test to run:")
    print("1. Form-based generation (recommended)")
    print("2. AI description generation")
    print("3. Run both tests")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        test_form_generation()
    elif choice == "2":
        test_ai_generation()
    elif choice == "3":
        test_form_generation()
        test_ai_generation()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
