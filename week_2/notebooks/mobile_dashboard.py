import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# Custom CSS for mobile responsiveness
mobile_css = """
<style>
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .metric-container {
            background: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1.2rem;
        }
    }
    
    .metric-container {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        text-align: center;
    }
</style>
"""

st.set_page_config(
    page_title="Mobile Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(mobile_css, unsafe_allow_html=True)

# Detect screen size (approximate)
if 'mobile_view' not in st.session_state:
    st.session_state.mobile_view = False

view_toggle = st.sidebar.radio("View Mode", ["Auto", "Mobile", "Desktop"])

if view_toggle == "Mobile":
    mobile_view = True
elif view_toggle == "Desktop":
    mobile_view = False
else:
    mobile_view = st.session_state.mobile_view

st.title("📱 Mobile Dashboard")

# Sample data
np.random.seed(42)
data = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'sales': np.random.randint(1000, 5000, 30),
    'users': np.random.randint(100, 500, 30)
})

# Responsive layout
if mobile_view:
    # Mobile layout - single column
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Total Sales", f"${data['sales'].sum():,}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Total Users", f"{data['users'].sum():,}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Avg Daily Sales", f"${data['sales'].mean():.0f}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Touch-friendly controls
    st.subheader("Quick Actions")
    if st.button("📊 View Report", key="mobile_report"):
        st.success("Report generated!")
    
    if st.button("📈 Analyze Trends", key="mobile_trends"):
        fig = px.line(data, x='date', y='sales', title="Sales Trend")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

else:
    # Desktop layout - multiple columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sales", f"${data['sales'].sum():,}")
    with col2:
        st.metric("Total Users", f"{data['users'].sum():,}")
    with col3:
        st.metric("Avg Daily Sales", f"${data['sales'].mean():.0f}")
    
    # Charts side by side
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(data, x='date', y='sales', title="Sales Trend")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(data.tail(7), x='date', y='users', title="Recent Users")
        st.plotly_chart(fig2, use_container_width=True)