# FILE: app_03_interactive.py
# Interactive Widgets - The Heart of Streamlit!

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("🎛️ Interactive Housing Dashboard")

# SIDEBAR - Put controls here to keep main area clean
st.sidebar.header("Controls")

# 1. SLIDER - For numeric ranges
price_range = st.sidebar.slider(
    "Price Range ($K)",
    min_value=200,
    max_value=2000,
    value=(500, 1200),  # Default range
    step=50
)

# 2. SELECTBOX - For single choice
selected_city = st.sidebar.selectbox(
    "Select City",
    options=['All', 'Sydney', 'Melbourne', 'Brisbane', 'Perth']
)

# 3. MULTISELECT - For multiple choices
property_types = st.sidebar.multiselect(
    "Property Types",
    options=['House', 'Apartment', 'Townhouse', 'Villa'],
    default=['House', 'Apartment']  # Pre-selected
)

# 4. RADIO BUTTONS - For exclusive choices
chart_type = st.sidebar.radio(
    "Chart Type",
    options=['Bar', 'Line', 'Scatter']
)

# 5. CHECKBOX - For on/off
show_data = st.sidebar.checkbox("Show raw data", value=False)

# 6. NUMBER INPUT - For precise values
min_bedrooms = st.sidebar.number_input(
    "Minimum Bedrooms",
    min_value=1,
    max_value=5,
    value=2
)

# Now use these values!
st.header("Your Selections:")
st.write(f"**Price Range:** ${price_range[0]}K - ${price_range[1]}K")
st.write(f"**City:** {selected_city}")
st.write(f"**Property Types:** {', '.join(property_types)}")
st.write(f"**Min Bedrooms:** {min_bedrooms}")
st.write(f"**Chart Type:** {chart_type}")

# Create filtered data based on selections
# (In real app, you'd filter actual data here)
st.header("Filtered Results")
st.info(f"Showing {len(property_types)} property types in {selected_city} "
        f"between ${price_range[0]}K-${price_range[1]}K")

if show_data:
    st.write("Raw data would appear here...")