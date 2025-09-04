# FILE: app_05_pro_tips.py
# Professional Streamlit Patterns

import streamlit as st
import pandas as pd
import time

st.title("🚀 Streamlit Pro Tips")

# TIP 1: Use Session State for persistence
st.header("1. Session State - Remember Things!")

# Initialize counter in session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Button increments counter
if st.button('Click me!'):
    st.session_state.counter += 1

st.write(f"Button clicked {st.session_state.counter} times")
st.caption("The count persists even when the app reruns!")

# TIP 2: Use columns for layout
st.header("2. Columns for Better Layout")

col1, col2, col3 = st.columns([2, 1, 1])  # Different widths!

with col1:
    st.write("Wide column (50%)")
    st.selectbox("Pick one", ["A", "B", "C"])

with col2:
    st.write("Medium (25%)")
    st.button("Action")

with col3:
    st.write("Medium (25%)")
    st.checkbox("Enable")

# TIP 3: Use containers for dynamic content
st.header("3. Containers for Dynamic Updates")

# Create empty container
placeholder = st.empty()

# Update it multiple times
for i in range(5):
    placeholder.write(f"Counting: {i+1}/5")
    time.sleep(0.5)

placeholder.success("✅ Done!")

# TIP 4: Use expander for optional content
st.header("4. Expanders Hide Complexity")

with st.expander("🔍 Advanced Options"):
    st.write("These settings are hidden by default!")
    advanced_mode = st.checkbox("Enable advanced mode")
    threshold = st.slider("Threshold", 0, 100, 50)
    st.write(f"Current settings: Mode={advanced_mode}, Threshold={threshold}")

# TIP 5: Use tabs for organization
st.header("5. Tabs for Multiple Views")

tab1, tab2, tab3 = st.tabs(["📊 Chart", "📋 Data", "ℹ️ Info"])

with tab1:
    st.write("Chart goes here")
    st.bar_chart(pd.DataFrame({'data': [1, 3, 2, 4]}))

with tab2:
    st.write("Data table goes here")
    st.dataframe(pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}))

with tab3:
    st.write("Information about the data")
    st.info("This data is synthetic")

# TIP 6: Use forms for batch input
st.header("6. Forms - Submit Everything at Once")

with st.form("my_form"):
    st.write("Fill out this form:")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    agree = st.checkbox("I agree")
    
    # Form submit button
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Submitted: {name}, {age} years old, Agreed: {agree}")

# TIP 7: Progress bars and spinners
st.header("7. Show Progress")

if st.button("Start long process"):
    # Show progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f'Processing... {i+1}%')
        time.sleep(0.01)
    
    status_text.text('Done!')
    st.balloons()

# Save as app_05_pro_tips.py and explore!