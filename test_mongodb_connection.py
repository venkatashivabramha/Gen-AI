"""
Test MongoDB Connection
"""
import os
import sys

print("Testing MongoDB Connection...")
print("=" * 60)

# Try to load from secrets
try:
    import streamlit as st
    mongodb_uri = st.secrets.get("MONGODB_URI", "")
    print(f"✓ Loaded from Streamlit secrets")
except:
    # Fallback to environment variable
    mongodb_uri = os.getenv("MONGODB_URI", "")
    print(f"✓ Loaded from environment variable")

if not mongodb_uri:
    print("❌ MONGODB_URI not found!")
    print("\nPlease add to .streamlit/secrets.toml:")
    print('MONGODB_URI = "mongodb+srv://..."')
    sys.exit(1)

# Hide password in output
safe_uri = mongodb_uri.replace(mongodb_uri.split('@')[0].split(':')[-1], "****")
print(f"✓ Connection string found: {safe_uri}")

# Test connection
try:
    from pymongo import MongoClient
    print("\n✓ PyMongo imported")
    
    client = MongoClient(mongodb_uri)
    client.admin.command('ping')
    print("✓ Connected to MongoDB successfully!")
    
    # List databases
    dbs = client.list_database_names()
    print(f"✓ Available databases: {dbs}")
    
    print("\n" + "=" * 60)
    print("SUCCESS! MongoDB is ready to use.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check username/password in connection string")
    print("2. Verify Network Access includes 0.0.0.0/0")
    print("3. Ensure database user has correct permissions")
