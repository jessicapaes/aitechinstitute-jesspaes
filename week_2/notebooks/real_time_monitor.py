import streamlit as st
import pandas as pd
import time
import psutil
import sqlite3
import plotly.express as px
from datetime import datetime

def init_db():
    conn = sqlite3.connect('system_metrics.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            timestamp TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_metrics(cpu, memory, disk):
    conn = sqlite3.connect('system_metrics.db')
    conn.execute(
        'INSERT INTO metrics VALUES (?, ?, ?, ?)',
        (datetime.now().isoformat(), cpu, memory, disk)
    )
    conn.commit()
    conn.close()

def get_system_metrics():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk

st.set_page_config(page_title="System Monitor", layout="wide")
st.title("Real-Time System Monitor")

init_db()

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90

# Auto-refresh every 5 seconds
time.sleep(5)
st.rerun()

cpu, memory, disk = get_system_metrics()
log_metrics(cpu, memory, disk)

# Metrics display
col1, col2, col3 = st.columns(3)

with col1:
    if cpu > CPU_THRESHOLD:
        st.error(f"CPU: {cpu:.1f}% - HIGH!")
    else:
        st.metric("CPU Usage", f"{cpu:.1f}%")

with col2:
    if memory > MEMORY_THRESHOLD:
        st.error(f"Memory: {memory:.1f}% - HIGH!")
    else:
        st.metric("Memory Usage", f"{memory:.1f}%")

with col3:
    if disk > DISK_THRESHOLD:
        st.error(f"Disk: {disk:.1f}% - HIGH!")
    else:
        st.metric("Disk Usage", f"{disk:.1f}%")

# Historical data chart
conn = sqlite3.connect('system_metrics.db')
df = pd.read_sql_query('SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 50', conn)
conn.close()

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig = px.line(df, x='timestamp', y=['cpu_percent', 'memory_percent', 'disk_percent'])
    st.plotly_chart(fig, use_container_width=True)