import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Initialize session state
if 'data' not in st.session_state:
    np.random.seed(42)
    st.session_state.data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'sales': np.random.randint(1000, 5000, 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'product': np.random.choice(['A', 'B', 'C'], 100)
    })

if 'settings' not in st.session_state:
    st.session_state.settings = {
        'theme': 'Light',
        'refresh_rate': 30,
        'show_raw_data': False
    }

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Analysis", "Settings"])

# Home Page
if page == "Home":
    st.title("Sales Dashboard - Home")
    
    df = st.session_state.data
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", f"${df['sales'].sum():,}")
    with col2:
        st.metric("Average Sale", f"${df['sales'].mean():.0f}")
    with col3:
        st.metric("Total Orders", len(df))
    with col4:
        st.metric("Regions", df['region'].nunique())
    
    # Quick charts
    col1, col2 = st.columns(2)
    with col1:
        monthly_sales = df.groupby(df['date'].dt.month)['sales'].sum()
        fig = px.line(x=monthly_sales.index, y=monthly_sales.values, title="Monthly Sales")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        region_sales = df.groupby('region')['sales'].sum()
        fig = px.pie(values=region_sales.values, names=region_sales.index, title="Sales by Region")
        st.plotly_chart(fig, use_container_width=True)

# Data Analysis Page
elif page == "Data Analysis":
    st.title("Data Analysis")
    
    df = st.session_state.data
    
    # Filters
    st.sidebar.subheader("Filters")
    selected_regions = st.sidebar.multiselect("Regions", df['region'].unique(), default=df['region'].unique())
    selected_products = st.sidebar.multiselect("Products", df['product'].unique(), default=df['product'].unique())
    
    # Filter data
    filtered_df = df[
        (df['region'].isin(selected_regions)) & 
        (df['product'].isin(selected_products))
    ]
    
    # Analysis
    st.subheader("Detailed Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(filtered_df, x='region', y='sales', title="Sales Distribution by Region")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(filtered_df, x='date', y='sales', color='product', title="Sales Trend by Product")
        st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data if enabled
    if st.session_state.settings['show_raw_data']:
        st.subheader("Raw Data")
        st.dataframe(filtered_df)

# Settings Page
elif page == "Settings":
    st.title("Settings")
    
    st.subheader("Dashboard Configuration")
    
    # Theme setting
    theme = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.settings['theme'] == 'Light' else 1)
    st.session_state.settings['theme'] = theme
    
    # Refresh rate
    refresh_rate = st.slider("Auto-refresh rate (seconds)", 10, 300, st.session_state.settings['refresh_rate'])
    st.session_state.settings['refresh_rate'] = refresh_rate
    
    # Show raw data toggle
    show_raw = st.checkbox("Show raw data in analysis", st.session_state.settings['show_raw_data'])
    st.session_state.settings['show_raw_data'] = show_raw
    
    st.subheader("Data Management")
    
    # Data upload
    uploaded_file = st.file_uploader("Upload new data", type="csv")
    if uploaded_file is not None:
        new_data = pd.read_csv(uploaded_file)
        if st.button("Replace current data"):
            st.session_state.data = new_data
            st.success("Data updated successfully!")
    
    # Reset data
    if st.button("Reset to sample data"):
        np.random.seed(42)
        st.session_state.data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'sales': np.random.randint(1000, 5000, 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
            'product': np.random.choice(['A', 'B', 'C'], 100)
        })
        st.success("Data reset to sample data!")