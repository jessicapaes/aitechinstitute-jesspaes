import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(
    page_title="API Integration Dashboard",
    layout="wide"
)

st.title("API Integration Dashboard")
st.markdown("Connect to external data sources via APIs")

# Cache API calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_api_data(url, params=None):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Weather API Example
st.header("Weather Data Dashboard")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input("Latitude", value=40.7128, format="%.4f")
with col2:
    longitude = st.number_input("Longitude", value=-74.0060, format="%.4f")

if st.button("Fetch Weather Data", type="primary"):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "forecast_days": 3
    }

    with st.spinner("Fetching weather data..."):
        data = fetch_api_data("https://api.open-meteo.com/v1/forecast", params)

    if data:
        # Process weather data
        hourly_data = data.get("hourly", {})

        df = pd.DataFrame({
            "time": pd.to_datetime(hourly_data.get("time", [])),
            "temperature": hourly_data.get("temperature_2m", []),
            "precipitation": hourly_data.get("precipitation", [])
        })

        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Temp", f"{df['temperature'].iloc[0]:.1f}°C")
        with col2:
            st.metric("Max Temp", f"{df['temperature'].max():.1f}°C")
        with col3:
            st.metric("Total Precipitation", f"{df['precipitation'].sum():.1f} mm")

        # Create chart
        fig = px.line(df, x="time", y="temperature", title="Temperature Forecast")
        st.plotly_chart(fig, use_container_width=True)