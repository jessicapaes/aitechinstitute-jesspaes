# FILE: app_02_basics.py
# The Essential Streamlit Commands You'll Use 90% of the Time

import streamlit as st
import pandas as pd
import numpy as np

# 1. TEXT ELEMENTS
st.title("🎯 Streamlit Basics")
st.header("Text Elements")
st.subheader("Different sizes for different purposes")
st.write("This is regular text. You can write **markdown** too!")
st.caption("This is a small caption")

# 2. DISPLAY DATA
st.header("Displaying Data")

# Create sample data
df = pd.DataFrame({
    'City': ['Sydney', 'Melbourne', 'Brisbane'],
    'Avg Price': [1200000, 950000, 750000],
    'Properties': [250, 220, 150]
})

st.write("Here's our data:")
st.dataframe(df)  # Interactive table!

# 3. METRICS (Perfect for dashboards!)
st.header("Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Properties", "620", "+12%")
with col2:
    st.metric("Avg Price", "$950K", "-2.3%")
with col3:
    st.metric("Days on Market", "28", "+5")

# 4. STATUS MESSAGES
st.success("✅ Data loaded successfully!")
st.info("ℹ️ Tip: Try changing the values above")
st.warning("⚠️ Some data might be outdated")

# Save this as app_02_basics.py and run it!