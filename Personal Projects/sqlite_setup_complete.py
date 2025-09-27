# sqlite_setup_complete.py - Step-by-step SQLite setup for beginners

"""
BEGINNER'S SQLITE SETUP GUIDE
==============================

This file shows you EXACTLY how to set up SQLite for your wellness tracker.
Follow each step and run the code to understand what's happening.
"""

import sqlite3
import datetime
import pandas as pd
import os

print("🚀 SQLITE SETUP GUIDE FOR WELLNESS TRACKER")
print("=" * 50)

# ===============================
# STEP 1: CREATE DATABASE CONNECTION
# ===============================

print("\n📁 STEP 1: Creating Database Connection")
print("-" * 40)

# Create database file (this creates the file if it doesn't exist)
database_name = "wellness_tracker.db"
connection = sqlite3.connect(database_name)
cursor = connection.cursor()

print(f"✅ Database file created: {database_name}")
print(f"📍 Location: {os.path.abspath(database_name)}")
print(f"💾 File size: {os.path.getsize(database_name)} bytes")

# ===============================
# STEP 2: CREATE YOUR TABLES
# ===============================

print("\n🏗️ STEP 2: Creating Database Tables")
print("-" * 40)

# Create the main wellness entries table
create_table_sql = """
CREATE TABLE IF NOT EXISTS wellness_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    tracking_reason TEXT,
    mood_rating INTEGER CHECK (mood_rating >= 1 AND mood_rating <= 10),
    safety_level INTEGER CHECK (safety_level >= 1 AND safety_level <= 10),
    energy_level INTEGER CHECK (energy_level >= 1 AND energy_level <= 10),
    sleep_hours REAL CHECK (sleep_hours >= 0 AND sleep_hours <= 24),
    water_intake REAL CHECK (water_intake >= 0),
    social_connection TEXT,
    daily_win TEXT,
    quick_mode BOOLEAN DEFAULT FALSE,
    exercise_today TEXT,
    sleep_quality INTEGER CHECK (sleep_quality >= 1 AND sleep_quality <= 10),
    stress_level INTEGER CHECK (stress_level >= 1 AND stress_level <= 10),
    triggers_encountered TEXT,
    physical_symptoms TEXT,
    coping_strategies TEXT,
    notes TEXT,
    created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

cursor.execute(create_table_sql)
connection.commit()

print("✅ Table 'wellness_entries' created successfully!")

# Show table structure
cursor.execute("PRAGMA table_info(wellness_entries)")
columns = cursor.fetchall()

print("\n📋 Table Structure:")
for col in columns:
    print(f"   {col[1]} ({col[2]}) - {'Required' if col[3] else 'Optional'}")

# ===============================
# STEP 3: INSERT SAMPLE DATA
# ===============================

print("\n📝 STEP 3: Adding Sample Data")
print("-" * 40)

# Sample data to test your database
sample_entries = [
    {
        'date': '2024-01-15',
        'tracking_reason': '🧠 Trauma recovery & PTSD healing',
        'mood_rating': 7,
        'safety_level': 6,
        'energy_level': 5,
        'sleep_hours': 7.5,
        'water_intake': 2.0,
        'social_connection': 'Good interactions - felt heard',
        'daily_win': 'Had a productive therapy session',
        'quick_mode': False,
        'exercise_today': 'Yes',
        'sleep_quality': 6,
        'stress_level': 4,
        'triggers_encountered': 'Maybe',
        'physical_symptoms': 'None',
        'coping_strategies': 'Deep breathing, Journaling',
        'notes': 'Feeling more grounded today'
    },
    {
        'date': '2024-01-16',
        'tracking_reason': '😰 Anxiety & stress management', 
        'mood_rating': 5,
        'safety_level': 7,
        'energy_level': 4,
        'sleep_hours': 6.0,
        'water_intake': 1.5,
        'social_connection': 'Minimal social contact',
        'daily_win': 'Made breakfast and tidied room',
        'quick_mode': True,
        'notes': 'Anxious morning but better afternoon'
    },
    {
        'date': '2024-01-17',
        'tracking_reason': '🌱 General wellness & self-care',
        'mood_rating': 8,
        'safety_level': 8,
        'energy_level': 7,
        'sleep_hours': 8.0,
        'water_intake': 2.5,
        'social_connection': 'Deep, meaningful connections',
        'daily_win': 'Had coffee with a good friend',
        'quick_mode': False,
        'exercise_today': 'Yes',
        'sleep_quality': 8,
        'stress_level': 3,
        'triggers_encountered': 'No',
        'physical_symptoms': 'None',
        'coping_strategies': 'Time in nature, Meditation',
        'notes': 'Great day overall, feeling positive'
    }
]

# Insert sample data
insert_sql = """
INSERT INTO wellness_entries (
    date, tracking_reason, mood_rating, safety_level, energy_level,
    sleep_hours, water_intake, social_connection, daily_win, quick_mode,
    exercise_today, sleep_quality, stress_level, triggers_encountered,
    physical_symptoms, coping_strategies, notes
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for entry in sample_entries:
    cursor.execute(insert_sql, (
        entry['date'],
        entry['tracking_reason'],
        entry['mood_rating'],
        entry['safety_level'],
        entry['energy_level'],
        entry['sleep_hours'],
        entry['water_intake'],
        entry['social_connection'],
        entry['daily_win'],
        entry['quick_mode'],
        entry.get('exercise_today'),
        entry.get('sleep_quality'),
        entry.get('stress_level'),
        entry.get('triggers_encountered'),
        entry.get('physical_symptoms'),
        entry.get('coping_strategies'),
        entry['notes']
    ))

connection.commit()
print(f"✅ Added {len(sample_entries)} sample entries")

# ===============================
# STEP 4: QUERY YOUR DATA
# ===============================

print("\n🔍 STEP 4: Testing Database Queries")
print("-" * 40)

# Count total entries
cursor.execute("SELECT COUNT(*) FROM wellness_entries")
total_count = cursor.fetchone()[0]
print(f"📊 Total entries in database: {total_count}")

# Get recent entries
print("\n📋 Recent Entries:")
cursor.execute("""
    SELECT date, mood_rating, energy_level, daily_win 
    FROM wellness_entries 
    ORDER BY date DESC 
    LIMIT 3
""")

recent_entries = cursor.fetchall()
for entry in recent_entries:
    print(f"   {entry[0]} | Mood: {entry[1]}/10 | Energy: {entry[2]}/10 | Win: {entry[3]}")

# Calculate averages
cursor.execute("""
    SELECT 
        AVG(mood_rating) as avg_mood,
        AVG(energy_level) as avg_energy,
        AVG(sleep_hours) as avg_sleep
    FROM wellness_entries
""")

averages = cursor.fetchone()
print(f"\n📈 Your Averages:")
print(f"   Mood: {averages[0]:.1f}/10")
print(f"   Energy: {averages[1]:.1f}/10") 
print(f"   Sleep: {averages[2]:.1f} hours")

# ===============================
# STEP 5: PANDAS INTEGRATION
# ===============================

print("\n🐼 STEP 5: Loading Data with Pandas")
print("-" * 40)

# Load all data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM wellness_entries", connection)

print(f"✅ Loaded {len(df)} rows into DataFrame")
print(f"📊 Columns: {list(df.columns)}")
print(f"💾 Memory usage: {df.memory_usage().sum()} bytes")

# Show first few rows
print("\n📋 Sample Data (first 2 rows):")
print(df[['date', 'mood_rating', 'energy_level', 'daily_win']].head(2))

# ===============================
# STEP 6: BACKUP AND EXPORT
# ===============================

print("\n💾 STEP 6: Creating Backup")
print("-" * 40)

# Export to CSV (backup)
backup_filename = f"wellness_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(backup_filename, index=False)

print(f"✅ Backup created: {backup_filename}")
print(f"📁 File size: {os.path.getsize(backup_filename)} bytes")

# ===============================
# STEP 7: UTILITY FUNCTIONS
# ===============================

print("\n🛠️ STEP 7: Useful Functions")
print("-" * 40)

def add_wellness_entry(connection, entry_data):
    """Add a new wellness entry to the database"""
    cursor = connection.cursor()
    
    insert_sql = """
    INSERT INTO wellness_entries (
        date, tracking_reason, mood_rating, safety_level, energy_level,
        sleep_hours, water_intake, social_connection, daily_win, quick_mode,
        exercise_today, sleep_quality, stress_level, triggers_encountered,
        physical_symptoms, coping_strategies, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_sql, (
        entry_data.get('date'),
        entry_data.get('tracking_reason'),
        entry_data.get('mood_rating'),
        entry_data.get('safety_level'),
        entry_data.get('energy_level'),
        entry_data.get('sleep_hours'),
        entry_data.get('water_intake'),
        entry_data.get('social_connection'),
        entry_data.get('daily_win'),
        entry_data.get('quick_mode', False),
        entry_data.get('exercise_today'),
        entry_data.get('sleep_quality'),
        entry_data.get('stress_level'),
        entry_data.get('triggers_encountered'),
        entry_data.get('physical_symptoms'),
        entry_data.get('coping_strategies'),
        entry_data.get('notes')
    ))
    
    connection.commit()
    return cursor.lastrowid

def get_mood_trend(connection, days=7):
    """Get mood trend for last N days"""
    query = """
    SELECT date, mood_rating 
    FROM wellness_entries 
    ORDER BY date DESC 
    LIMIT ?
    """
    return pd.read_sql_query(query, connection, params=[days])

def check_entry_exists(connection, date):
    """Check if entry exists for a specific date"""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM wellness_entries WHERE date = ?", (date,))
    return cursor.fetchone()[0] > 0

# Test the functions
print("✅ Utility functions defined:")
print("   - add_wellness_entry()")
print("   - get_mood_trend()")
print("   - check_entry_exists()")

# Test entry existence check
today = datetime.date.today().strftime('%Y-%m-%d')
exists = check_entry_exists(connection, today)
print(f"   Entry exists for today ({today}): {exists}")

# ===============================
# STEP 8: DATABASE MAINTENANCE
# ===============================

print("\n🔧 STEP 8: Database Maintenance")
print("-" * 40)

# Get database size
db_size = os.path.getsize(database_name)
print(f"💾 Database size: {db_size} bytes ({db_size/1024:.1f} KB)")

# Optimize database (removes unused space)
cursor.execute("VACUUM")
connection.commit()
print("✅ Database optimized (VACUUM completed)")

# Get updated size
new_size = os.path.getsize(database_name)
print(f"💾 Optimized size: {new_size} bytes ({new_size/1024:.1f} KB)")

# ===============================
# STEP 9: ERROR HANDLING EXAMPLE
# ===============================

print("\n⚠️ STEP 9: Error Handling Example")
print("-" * 40)

def safe_add_entry(connection, entry_data):
    """Safely add entry with error handling"""
    try:
        entry_id = add_wellness_entry(connection, entry_data)
        print(f"✅ Entry added successfully with ID: {entry_id}")
        return entry_id
    except sqlite3.IntegrityError as e:
        print(f"❌ Data validation error: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Test error handling with invalid data
print("Testing with invalid mood rating (15)...")
invalid_entry = {
    'date': '2024-01-18',
    'mood_rating': 15,  # Invalid - should be 1-10
    'safety_level': 5,
    'energy_level': 5,
    'sleep_hours': 8.0,
    'water_intake': 2.0,
    'social_connection': 'Good',
    'daily_win': 'Test entry'
}

safe_add_entry(connection, invalid_entry)

# ===============================
# FINAL SUMMARY
# ===============================

print("\n🎉 SETUP COMPLETE!")
print("=" * 50)

final_count = pd.read_sql_query("SELECT COUNT(*) as count FROM wellness_entries", connection)['count'][0]

print(f"""
✅ YOUR SQLITE DATABASE IS READY!

📊 Database Stats:
   - File: {database_name}
   - Total entries: {final_count}
   - Size: {os.path.getsize(database_name)} bytes
   - Location: {os.path.abspath(database_name)}

🛠️ What You Can Do Now:
   1. Run your Streamlit app with this database
   2. Add new wellness entries
   3. Query your data with SQL
   4. Create backups with pandas
   5. View trends and analytics

🚀 Next Steps:
   1. Copy this database file to your Streamlit app folder
   2. Update your Streamlit code to use these functions
   3. Start tracking your wellness data!

📚 Key Files Created:
   - {database_name} (your main database)
   - {backup_filename} (backup file)
""")

# Close connection properly
connection.close()
print("\n🔒 Database connection closed safely")

print("\n" + "=" * 50)
print("🎯 You're ready to build amazing wellness tracking apps!")