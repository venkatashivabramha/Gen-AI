"""Test Yahoo Finance market data fetching"""
import sys
sys.path.insert(0, 'src')

from data.market_data_fetcher import get_market_data_fetcher

print("=" * 60)
print("📊 TESTING YAHOO FINANCE INTEGRATION")
print("=" * 60)

fetcher = get_market_data_fetcher()

# Test HR Tech (for AI Resume Builder example)
print("\n" + "="*60)
print("TEST: HR Tech Industry (AI Resume Builder)")
print("="*60)

data = fetcher.get_industry_overview('HR Tech')

print(f"\n✅ RESULTS:")
print(f"   Industry: {data['industry']}")
print(f"   Market Size: {data['market_size']}")
print(f"   Growth Rate: {data['growth_rate']}")
print(f"   Data Source: {data['data_source']}")
print(f"   Confidence: {data['market_confidence']}")

print(f"\n📈 Top Competitors:")
for i, comp in enumerate(data['competitors'][:5], 1):
    print(f"   {i}. {comp['name']}")
    print(f"      Market Cap: {comp['market_cap']}")
    print(f"      Revenue: {comp['revenue']}")
    print(f"      Employees: {comp['employees']}")
    print()

print("="*60)
print("✅ TEST COMPLETE - Real market data fetched successfully!")
print("="*60)
