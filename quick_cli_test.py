"""
Quick CLI test to verify the generation works
"""
import sys
from pathlib import Path

# Add src to path correctly
sys.path.insert(0, str(Path(__file__).parent / "src"))

from business_plan_generator import BusinessPlanGenerator
from dotenv import load_dotenv

load_dotenv()

print("Testing business plan generation...")
print()

# Simple test data
test_data = {
    "business_name": "TechFlow AI Solutions",
    "industry": "Technology",
    "business_type": "Technology Startup",
    "location": "San Francisco, CA",
    "description": "AI-powered project management tools for remote teams",
    "target_market": "Remote teams and distributed organizations",
    "products_services": "Cloud-based collaboration platform with AI features",
    "revenue_model": "Monthly subscription",
    "initial_investment": "$500,000",
    "innovation_focus": "AI-powered automation and smart scheduling"
}

print("Initializing generator...")
try:
    generator = BusinessPlanGenerator("anthropic")
    print("✅ Generator initialized")
    print()
    print("🚀 Starting generation... (this will take 2-5 minutes)")
    print("   Please wait...")
    print()
    
    result = generator.generate_from_form(test_data, output_formats=['html'])
    
    print()
    print("="*60)
    if result['status'] == 'success':
        print("✅ SUCCESS!")
        print()
        print("Generated files:")
        for fmt, path in result['files'].items():
            print(f"  {fmt.upper()}: {path}")
            if Path(path).exists():
                size = Path(path).stat().st_size
                print(f"         Size: {size:,} bytes")
    else:
        print("❌ FAILED")
        print(result)
    print("="*60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
