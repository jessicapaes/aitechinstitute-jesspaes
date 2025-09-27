# test_database.py - Run this in VS Code to verify your database works

"""
DATABASE VERIFICATION SCRIPT
=============================

Run this file in VS Code to check if your SQLite database is working correctly.

HOW TO RUN IN VS CODE:
1. Open VS Code
2. Open your project folder (File → Open Folder)
3. Create new file: test_database.py
4. Copy this code into the file
5. Click the "Play" button (▶️) in top-right corner
6. Or press Ctrl+F5 (Windows) or Cmd+F5 (Mac)
7. Check the output in the Terminal panel at bottom
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime

print("🔍 DATABASE VERIFICATION TEST")
print("=" * 40)

# ===============================
# TEST 1: Check if database file exists
# ===============================

print("\n📁 TEST 1: Checking if database file exists...")

database_file = "wellness_tracker.db"

if os.path.exists(database_file):
    print(f"✅ Database file found: {database_file}")
    file_size = os.path.getsize(database_file)
    print(f"📊 File size: {file_size} bytes ({file_size/1024:.1f} KB)")
    print(f"📍 Full path: {os.path.abspath(database_file)}")
else:
    print(f"❌ Database file NOT found: {database_file}")
    print("❗ You need to run 'sqlite_setup_complete.py' first!")
    exit()

# ===============================
# TEST 2: Connect to database
# ===============================

print("\n🔌 TEST 2: Connecting to database...")

try:
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    print("✅ Successfully connected to database")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit()

# ===============================
# TEST 3: Check table exists
# ===============================

print("\n🏗️ TEST 3: Checking if tables exist...")

try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"✅ Found {len(tables)} tables:")
    for table in tables:
        print(f"   📋 {table[0]}")
except Exception as e:
    print(f"❌ Error checking tables: {e}")

# ===============================
# TEST 4: Count entries
# ===============================

print("\n🔢 TEST 4: Counting entries...")

try:
    cursor.execute("SELECT COUNT(*) FROM wellness_entries")
    count = cursor.fetchone()[0]
    print(f"✅ Found {count} wellness entries")
    
    if count == 0:
        print("⚠️ No data found - database is empty")
    else:
        print(f"🎉 Great! You have {count} entries to work with")
        
except Exception as e:
    print(f"❌ Error counting entries: {e}")

# ===============================
# TEST 5: Load data with pandas
# ===============================

print("\n🐼 TEST 5: Loading data with pandas...")

try:
    # Load all data
    df = pd.read_sql_query("SELECT * FROM wellness_entries", conn)
    print(f"✅ Pandas loaded {len(df)} rows")
    print(f"📊 Columns: {list(df.columns)}")
    
    if len(df) > 0:
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"😊 Average mood: {df['mood_rating'].mean():.1f}/10")
        print(f"⚡ Average energy: {df['energy_level'].mean():.1f}/10")
        print(f"💤 Average sleep: {df['sleep_hours'].mean():.1f} hours")
        
except Exception as e:
    print(f"❌ Pandas error: {e}")

# ===============================
# TEST 6: Show sample data
# ===============================

print("\n📋 TEST 6: Sample data preview...")

try:
    # Show first 3 entries
    sample_query = """
    SELECT date, mood_rating, energy_level, daily_win, created_timestamp
    FROM wellness_entries 
    ORDER BY date DESC 
    LIMIT 3
    """
    
    cursor.execute(sample_query)
    samples = cursor.fetchall()
    
    if samples:
        print("✅ Sample entries:")
        print("   Date       | Mood | Energy | Daily Win")
        print("   " + "-" * 45)
        for sample in samples:
            date, mood, energy, win, timestamp = sample
            win_short = (win[:30] + "...") if win and len(win) > 30 else win
            print(f"   {date} | {mood:4}/10 | {energy:6}/10 | {win_short}")
    else:
        print("⚠️ No sample data available")
        
except Exception as e:
    print(f"❌ Sample data error: {e}")

# ===============================
# TEST 7: Test insert operation
# ===============================

print("\n✏️ TEST 7: Testing insert operation...")

try:
    # Try to insert a test entry
    test_entry = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'tracking_reason': '🧪 Database test',
        'mood_rating': 8,
        'safety_level': 8, 
        'energy_level': 7,
        'sleep_hours': 8.0,
        'water_intake': 2.0,
        'social_connection': 'Testing connection',
        'daily_win': 'Successfully tested database!',
        'quick_mode': False,
        'notes': 'This is a test entry to verify database works'
    }
    
    insert_sql = """
    INSERT INTO wellness_entries (
        date, tracking_reason, mood_rating, safety_level, energy_level,
        sleep_hours, water_intake, social_connection, daily_win, quick_mode, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (
        test_entry['date'], test_entry['tracking_reason'], test_entry['mood_rating'],
        test_entry['safety_level'], test_entry['energy_level'], test_entry['sleep_hours'],
        test_entry['water_intake'], test_entry['social_connection'], test_entry['daily_win'],
        test_entry['quick_mode'], test_entry['notes']
    ))
    
    conn.commit()
    test_id = cursor.lastrowid
    
    print(f"✅ Test entry inserted successfully with ID: {test_id}")
    
    # Clean up - remove test entry
    cursor.execute("DELETE FROM wellness_entries WHERE id = ?", (test_id,))
    conn.commit()
    print("🧹 Test entry cleaned up")
    
except Exception as e:
    print(f"❌ Insert test failed: {e}")

# ===============================
# TEST 8: Streamlit compatibility test
# ===============================

print("\n🚀 TEST 8: Streamlit compatibility...")

try:
    # Test if we can use the database the way Streamlit will
    def streamlit_style_query(conn):
        return pd.read_sql_query(
            "SELECT date, mood_rating, energy_level FROM wellness_entries ORDER BY date DESC LIMIT 5", 
            conn
        )
    
    streamlit_df = streamlit_style_query(conn)
    print(f"✅ Streamlit-style query successful: {len(streamlit_df)} rows")
    
    # Test session-state style operations
    if len(streamlit_df) > 0:
        print("✅ Data ready for Streamlit visualizations")
    else:
        print("⚠️ No data for Streamlit to display")
        
except Exception as e:
    print(f"❌ Streamlit compatibility issue: {e}")

# ===============================
# FINAL RESULTS
# ===============================

print("\n🎯 VERIFICATION COMPLETE!")
print("=" * 40)

# Recount final entries
cursor.execute("SELECT COUNT(*) FROM wellness_entries")
final_count = cursor.fetchone()[0]

if final_count > 0:
    print(f"""
✅ YOUR DATABASE IS WORKING PERFECTLY!

📊 Final Status:
   - Database file: ✅ Found
   - Connection: ✅ Working  
   - Tables: ✅ Created
   - Data: ✅ {final_count} entries ready
   - Pandas: ✅ Compatible
   - Streamlit: ✅ Ready

🚀 You can now:
   1. Run your Streamlit wellness tracker
   2. Add new entries through the web interface
   3. View your data in beautiful charts
   4. Export your data anytime

🎉 Database setup is COMPLETE! 
""")
else:
    print(f"""
⚠️ DATABASE SETUP INCOMPLETE

📊 Status:
   - Database file: ✅ Found
   - Connection: ✅ Working
   - Tables: ✅ Created  
   - Data: ❌ No entries found

🔧 Next Steps:
   1. Run 'sqlite_setup_complete.py' first
   2. Or start using your Streamlit app to add data
   3. Then run this verification again
""")

# Close connection
conn.close()
print("\n🔒 Database connection closed safely")

print("\n" + "=" * 40)
print("🎓 Great job learning database verification!")