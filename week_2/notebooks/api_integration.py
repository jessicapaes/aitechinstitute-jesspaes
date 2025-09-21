import streamlit as st
import pandas as pd
import requests
import sqlite3
import plotly.express as px
from datetime import datetime
import time

def init_cache_db():
    conn = sqlite3.connect('api_cache.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS api_cache (
            url TEXT PRIMARY KEY,
            data TEXT,
            timestamp REAL,
            ttl INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_cached_data(url, ttl=300):
    conn = sqlite3.connect('api_cache.db')
    cursor = conn.execute('SELECT data, timestamp FROM api_cache WHERE url = ?', (url,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        data, timestamp = result
        if time.time() - timestamp < ttl:
            return data
    return None

def cache_data(url, data, ttl=300):
    conn = sqlite3.connect('api_cache.db')
    conn.execute('INSERT OR REPLACE INTO api_cache VALUES (?, ?, ?, ?)',
                (url, data, time.time(), ttl))
    conn.commit()
    conn.close()

def fetch_api_data(url, params=None, use_cache=True):
    cache_key = f"{url}?{str(params)}"
    
    if use_cache:
        cached = get_cached_data(cache_key)
        if cached:
            st.info("Using cached data")
            return eval(cached)  # Note: In production, use json.loads
    
    try:
        with st.spinner("Fetching data from API..."):
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if use_cache:
                cache_data(cache_key, str(data))
            
            return data
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("Connection error. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    
    return None

st.set_page_config(page_title="API Integration Dashboard", layout="wide")

init_cache_db()

st.title("API Integration Dashboard")

# API selection
api_choice = st.selectbox("Choose API", ["Weather", "News", "Cryptocurrency"])

if api_choice == "Weather":
    st.subheader("Weather Data")
    
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=40.7128, format="%.4f")
    with col2:
        lon = st.number_input("Longitude", value=-74.0060, format="%.4f")
    
    if st.button("Get Weather"):
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,precipitation",
            "forecast_days": 3
        }
        
        data = fetch_api_data("https://api.open-meteo.com/v1/forecast", params)
        
        if data:
            hourly = data.get("hourly", {})
            df = pd.DataFrame({
                "time": pd.to_datetime(hourly.get("time", [])),
                "temperature": hourly.get("temperature_2m", []),
                "precipitation": hourly.get("precipitation", [])
            })
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Temp", f"{df['temperature'].iloc[0]:.1f}°C")
            with col2:
                st.metric("Max Temp", f"{df['temperature'].max():.1f}°C")
            with col3:
                st.metric("Total Rain", f"{df['precipitation'].sum():.1f} mm")
            
            fig = px.line(df, x="time", y="temperature", title="Temperature Forecast")
            st.plotly_chart(fig, use_container_width=True)

elif api_choice == "Cryptocurrency":
    st.subheader("Cryptocurrency Prices")
    
    if st.button("Get Crypto Prices"):
        data = fetch_api_data("https://api.coingecko.com/api/v3/simple/price", {
            "ids": "bitcoin,ethereum,cardano",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        })
        
        if data:
            for coin, info in data.items():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        coin.title(),
                        f"${info['usd']:,.2f}",
                        f"{info.get('usd_24h_change', 0):.2f}%"
                    )

# Cache management
st.sidebar.subheader("Cache Management")
if st.sidebar.button("Clear Cache"):
    conn = sqlite3.connect('api_cache.db')
    conn.execute('DELETE FROM api_cache')
    conn.commit()
    conn.close()
    st.sidebar.success("Cache cleared!")

# Error logging
if st.sidebar.checkbox("Show Error Log"):
    st.sidebar.text("Error logging would be implemented here")