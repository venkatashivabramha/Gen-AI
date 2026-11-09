"""
Test Streamlit Web Version
Quick test to ensure all imports work
"""
import sys
import os

print("Testing Streamlit Web Version...")
print("=" * 60)

# Test 1: Streamlit
try:
    import streamlit as st
    print("✓ Streamlit imported successfully")
except ImportError as e:
    print(f"✗ Streamlit import failed: {e}")
    print("  Install with: pip install streamlit")

# Test 2: MongoDB
try:
    from pymongo import MongoClient
    print("✓ PyMongo imported successfully")
except ImportError as e:
    print(f"✗ PyMongo import failed: {e}")
    print("  Install with: pip install pymongo")

# Test 3: Bcrypt
try:
    import bcrypt
    print("✓ Bcrypt imported successfully")
except ImportError as e:
    print(f"✗ Bcrypt import failed: {e}")
    print("  Install with: pip install bcrypt")

# Test 4: Backend modules
sys.path.insert(0, 'src')
try:
    from business_plan_generator import BusinessPlanGenerator
    print("✓ Business Plan Generator imported")
except ImportError as e:
    print(f"✗ Generator import failed: {e}")

# Test 5: Data modules
try:
    from data.market_data_fetcher import MarketDataFetcher
    print("✓ Market Data Fetcher imported")
except ImportError as e:
    print(f"✗ Market Data import failed: {e}")

print("=" * 60)
print("\nIf all tests passed, run:")
print("  streamlit run streamlit_app.py")
print("\nFor deployment guide, see:")
print("  STREAMLIT_DEPLOYMENT.md")
