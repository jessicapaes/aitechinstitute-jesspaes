import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Real-Time Dashboard",
    layout="wide"
)

st.title("Real-Time Data Dashboard")
st.markdown("Dashboard updates automatically every few seconds")

# Sidebar controls
st.sidebar.header("Settings")
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 1, 10, 3)

# Placeholder for metrics
placeholder = st.empty()

# Function to generate random data
def get_current_data():
    return {
        "timestamp": datetime.now(),
        "users_online": np.random.randint(100, 500),
        "cpu_usage": np.random.uniform(20, 80),
        "memory_usage": np.random.uniform(30, 70),
        "requests_per_sec": np.random.randint(50, 200),
        "error_rate": np.random.uniform(0, 5)
    }

# Initialize session state for historical data
if "history" not in st.session_state:
    st.session_state.history = []

# Main update loop
if auto_refresh:
    for _ in range(10):
        with placeholder.container():
            # Get current data
            current_data = get_current_data()

            # Add to history
            st.session_state.history.append(current_data)

            # Keep only last 100 points
            if len(st.session_state.history) > 100:
                st.session_state.history = st.session_state.history[-100:]

            # Display metrics
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric(
                    "Users Online",
                    current_data["users_online"],
                    delta=np.random.randint(-10, 20)
                )

            with col2:
                st.metric(
                    "CPU Usage",
                    f"{current_data['cpu_usage']:.1f}%",
                    delta=f"{np.random.uniform(-5, 5):.1f}%"
                )

            with col3:
                st.metric(
                    "Memory",
                    f"{current_data['memory_usage']:.1f}%",
                    delta=f"{np.random.uniform(-3, 3):.1f}%"
                )

            with col4:
                st.metric(
                    "Requests/sec",
                    current_data["requests_per_sec"],
                    delta=np.random.randint(-20, 30)
                )

            with col5:
                st.metric(
                    "Error Rate",
                    f"{current_data['error_rate']:.2f}%",
                    delta=f"{np.random.uniform(-0.5, 0.5):.2f}%"
                )

            # Create real-time chart
            if len(st.session_state.history) > 1:
                df = pd.DataFrame(st.session_state.history)

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["cpu_usage"],
                    mode="lines",
                    name="CPU Usage",
                    line=dict(color="blue")
                ))

                fig.add_trace(go.Scatter(
                    x=df["timestamp"],
                    y=df["memory_usage"],
                    mode="lines",
                    name="Memory Usage",
                    line=dict(color="green")
                ))

                fig.update_layout(
                    title="System Metrics Over Time",
                    xaxis_title="Time",
                    yaxis_title="Usage (%)",
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

            # Display last update time
            st.caption(f"Last updated: {current_data['timestamp'].strftime('%H:%M:%S')}")

        time.sleep(refresh_interval)

        if not auto_refresh:
            break