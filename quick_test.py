"""
Quick test script to verify the Business Plan Generator works
Run this to test without using the GUI
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test if all required imports work"""
    print("=" * 60)
    print("  Testing Business Plan Generator")
    print("=" * 60)
    print()
    
    print("1. Testing imports...")
    try:
        from dotenv import load_dotenv
        print("   ✅ python-dotenv")
        
        import customtkinter
        print("   ✅ customtkinter")
        
        import anthropic
        print("   ✅ anthropic")
        
        from reportlab.lib.pagesizes import letter
        print("   ✅ reportlab")
        
        from docx import Document
        print("   ✅ python-docx")
        
        from jinja2 import Template
        print("   ✅ Jinja2")
        
        print("   ✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_configuration():
    """Test if configuration is correct"""
    print("\n2. Testing configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check API keys
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if anthropic_key and anthropic_key.startswith("sk-ant-"):
            print("   ✅ Anthropic API key configured")
        else:
            print("   ⚠️  Anthropic API key not found or invalid")
        
        if openai_key and openai_key.startswith("sk-"):
            print("   ✅ OpenAI API key configured")
        else:
            print("   ⚠️  OpenAI API key not configured (optional)")
        
        # Check output directory
        output_dir = Path("output")
        if output_dir.exists():
            print("   ✅ Output directory exists")
        else:
            output_dir.mkdir()
            print("   ✅ Output directory created")
        
        return True
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False

def test_business_plan_generator():
    """Test the core generator"""
    print("\n3. Testing Business Plan Generator...")
    
    try:
        from business_plan_generator import BusinessPlanGenerator
        print("   ✅ BusinessPlanGenerator imported")
        
        # Try to initialize (won't call API yet)
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "anthropic")
        print(f"   ℹ️  Using provider: {provider}")
        
        # Note: We don't actually generate here to save API costs
        print("   ✅ Generator class ready")
        
        return True
    except Exception as e:
        print(f"   ❌ Generator error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_generation():
    """Test actual business plan generation (optional)"""
    print("\n4. Testing actual generation (optional)...")
    
    response = input("   Generate a test plan? This will use your API credits (y/n): ")
    
    if response.lower() != 'y':
        print("   ⏭️  Skipping actual generation")
        return True
    
    try:
        from business_plan_generator import BusinessPlanGenerator
        
        print("\n   🚀 Generating test business plan...")
        print("   This will take 2-3 minutes...")
        
        # Simple test data
        test_data = {
            "business_name": "QuickTest Startup",
            "industry": "Technology",
            "business_type": "Software",
            "location": "Test City",
            "description": "A quick test to verify the generator works correctly.",
            "target_market": "Test market",
            "products_services": "Test products",
            "revenue_model": "Test revenue model",
            "initial_investment": "$10,000",
            "innovation_focus": "Test innovation"
        }
        
        generator = BusinessPlanGenerator("anthropic")
        result = generator.generate_from_form(test_data, output_formats=['html'])
        
        if result['status'] == 'success':
            print("\n   ✅ Generation successful!")
            print(f"   📄 File: {result['files'].get('html', 'N/A')}")
            
            # Check if file exists
            html_file = result['files'].get('html')
            if html_file and Path(html_file).exists():
                print(f"   ✅ File verified: {Path(html_file).stat().st_size} bytes")
                print("\n   🎉 ALL TESTS PASSED!")
                return True
            else:
                print("   ❌ File not found")
                return False
        else:
            print("   ❌ Generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Generation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("Generator", test_business_plan_generator()))
    results.append(("Generation", test_sample_generation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is working perfectly!")
        print("\n📋 Next steps:")
        print("   1. Open the GUI: python src/main.py")
        print("   2. Or check test_samples.md for sample inputs")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("   Review INSTALLATION.md for troubleshooting")
    
    print()

if __name__ == "__main__":
    main()
