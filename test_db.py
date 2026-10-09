import os
import sys
from dotenv import load_dotenv

# Ensure we're in the right directory
sys.path.insert(0, os.path.dirname(__file__))
load_dotenv()

from database import engine
from database import engine, Base
from sqlalchemy import text

print("========================================")
print("🔍 TESTING SUPABASE POSTGRES CONNECTION")
print("========================================")

try:
    # 1. Test raw connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();")).fetchone()
        print(f"✅ Connection Successful!")
        print(f"   PostgreSQL Version: {result[0][:30]}...")

    # 2. Automatically generate the schema/tables in Supabase
    print("⏳ Synchronizing Database Tables (Creating if not exist)...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully in Supabase.")

    # 3. Fetch table list to prove it works
    print("📋 Current Tables in Database:")
    with engine.connect() as conn:
        tables = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")).fetchall()
        for t in tables:
            print(f"   - {t[0]}")
    
    print("========================================")
    print("🚀 DATABASE READY FOR PRODUCTION!")
    print("========================================")

except Exception as e:
    print("❌ CONNECTION FAILED!")
    print(str(e))
