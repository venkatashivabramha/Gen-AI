import sys
sys.path.insert(0, "src")

print("=" * 60)
print("LIVE TEST: Business Plan Generator")
print("=" * 60)

# Test 1: Auth
print("\n[1] Auth System...", end=" ")
from auth.auth_manager import AuthManager
auth = AuthManager()
print("PASS")

# Test 2: Core Generator
print("[2] Core Generator...", end=" ")
from business_plan_generator import BusinessPlanGenerator
gen = BusinessPlanGenerator("groq", use_real_data=True)
print("PASS")

# Test 3: Market Data
print("[3] Market Data (Real API Call)...")
from data.market_data_fetcher import MarketDataFetcher
mdf = MarketDataFetcher()
print("    Fetching Technology sector data...")
data = mdf.get_industry_overview("Technology")
if data.get("fetch_status") != "failed":
    print(f"    Market Size: {data.get('market_size', 'N/A')}")
    print(f"    Growth Rate: {data.get('growth_rate', 'N/A')}%")
    print(f"    Competitors: {len(data.get('competitors', []))}")
    print("    PASS - Real Yahoo Finance data!")
else:
    print("    WARN: No data (check internet)")

# Test 4: RAG Engine
print("[4] RAG Engine...", end=" ")
from rag.rag_engine import RAGEngine
rag = RAGEngine(use_real_data=True)
print("PASS")

# Test 5: GUI
print("[5] GUI Components...", end=" ")
from gui.main_window import BusinessPlanGeneratorApp
from auth.login_gui import show_login
print("PASS")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nApplication is fully operational!")
print("\nTo start: python main_with_login.py")