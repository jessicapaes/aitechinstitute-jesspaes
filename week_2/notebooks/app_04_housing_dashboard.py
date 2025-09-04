# FILE: app_04_housing_dashboard.py
# Complete Housing Market Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Australian Housing Dashboard",
    page_icon="🏠",
    layout="wide"  # Use full screen width
)

# Title and description
st.title("🏠 Australian Housing Market Dashboard")
st.markdown("Interactive analysis of property prices across major cities")

# Generate our housing data (from notebook 1)
@st.cache_data  # This decorator caches the data - SUPER IMPORTANT!
def load_data():
    np.random.seed(42)
    n_properties = 5000
    
    cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Hobart', 'Darwin', 'Canberra']
    city_weights = [0.25, 0.22, 0.15, 0.12, 0.10, 0.06, 0.04, 0.06]
    
    housing_data = pd.DataFrame({
        'property_id': range(1, n_properties + 1),
        'city': np.random.choice(cities, n_properties, p=city_weights),
        'property_type': np.random.choice(['House', 'Apartment', 'Townhouse', 'Villa'], 
                                         n_properties, p=[0.45, 0.35, 0.15, 0.05]),
        'bedrooms': np.random.choice([1, 2, 3, 4, 5], n_properties, p=[0.1, 0.25, 0.35, 0.25, 0.05]),
        'bathrooms': np.random.choice([1, 2, 3], n_properties, p=[0.4, 0.45, 0.15]),
        'car_spaces': np.random.choice([0, 1, 2, 3], n_properties, p=[0.15, 0.35, 0.40, 0.10]),
        'land_size': np.random.lognormal(6, 0.8, n_properties),
        'building_size': np.random.lognormal(5, 0.6, n_properties),
        'year_built': np.random.normal(1995, 20, n_properties).astype(int).clip(1950, 2024),
        'distance_cbd': np.random.exponential(15, n_properties),
    })
    
    # Add realistic prices
    base_price = {
        'Sydney': 1200000, 'Melbourne': 950000, 'Brisbane': 750000, 'Perth': 650000,
        'Adelaide': 600000, 'Hobart': 550000, 'Darwin': 600000, 'Canberra': 850000
    }
    
    housing_data['price'] = housing_data.apply(lambda row: 
        base_price[row['city']] * 
        (1 + 0.15 * row['bedrooms']) * 
        (1 + 0.1 * row['bathrooms']) *
        (1 - 0.01 * row['distance_cbd']) *
        (1 + np.random.normal(0, 0.15)), axis=1
    )
    
    housing_data['price_per_sqm'] = housing_data['price'] / housing_data['building_size']
    housing_data['age'] = 2024 - housing_data['year_built']
    
    return housing_data

# Load the data
df = load_data()

# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")

# City filter
selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=df['city'].unique(),
    default=df['city'].unique()
)

# Property type filter
selected_types = st.sidebar.multiselect(
    "Property Types",
    options=df['property_type'].unique(),
    default=df['property_type'].unique()
)

# Bedroom filter
bedroom_range = st.sidebar.slider(
    "Number of Bedrooms",
    min_value=int(df['bedrooms'].min()),
    max_value=int(df['bedrooms'].max()),
    value=(2, 4)
)

# Price filter
price_range = st.sidebar.slider(
    "Price Range ($K)",
    min_value=int(df['price'].min()/1000),
    max_value=int(df['price'].max()/1000),
    value=(500, 1500),
    step=50
)

# Filter the data
filtered_df = df[
    (df['city'].isin(selected_cities)) &
    (df['property_type'].isin(selected_types)) &
    (df['bedrooms'] >= bedroom_range[0]) &
    (df['bedrooms'] <= bedroom_range[1]) &
    (df['price'] >= price_range[0] * 1000) &
    (df['price'] <= price_range[1] * 1000)
]

# MAIN DASHBOARD
# Row 1: Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Properties",
        f"{len(filtered_df):,}",
        f"{len(filtered_df)/len(df)*100:.1f}% of total"
    )

with col2:
    avg_price = filtered_df['price'].mean()
    st.metric(
        "Average Price",
        f"${avg_price/1e6:.2f}M",
        f"${avg_price - df['price'].mean():+,.0f} vs all"
    )

with col3:
    avg_size = filtered_df['building_size'].mean()
    st.metric(
        "Avg Building Size",
        f"{avg_size:.0f} sqm",
        f"{avg_size - df['building_size'].mean():+.0f} vs all"
    )

with col4:
    avg_age = filtered_df['age'].mean()
    st.metric(
        "Average Age",
        f"{avg_age:.0f} years",
        f"{avg_age - df['age'].mean():+.1f} vs all"
    )

# Row 2: Charts
st.markdown("---")  # Horizontal line
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Average Price by City")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    city_avg = filtered_df.groupby('city')['price'].mean().sort_values(ascending=False)
    
    bars = ax.bar(city_avg.index, city_avg.values/1e6, color='steelblue')
    ax.set_xlabel('City')
    ax.set_ylabel('Average Price ($M)')
    ax.set_title('Average Property Prices')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.1f}M',
                ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("🏠 Property Type Distribution")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    type_counts = filtered_df['property_type'].value_counts()
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    wedges, texts, autotexts = ax.pie(
        type_counts.values,
        labels=type_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    ax.set_title('Property Types')
    plt.tight_layout()
    st.pyplot(fig)

# Row 3: Price Distribution
st.markdown("---")
st.subheader("📈 Price Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(filtered_df['price']/1e6, bins=30, color='skyblue', edgecolor='navy', alpha=0.7)
    ax.set_xlabel('Price ($M)')
    ax.set_ylabel('Number of Properties')
    ax.set_title('Price Distribution')
    ax.axvline(filtered_df['price'].mean()/1e6, color='red', linestyle='--', label=f'Mean: ${filtered_df["price"].mean()/1e6:.1f}M')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scatter plot: Price vs Distance from CBD
    scatter = ax.scatter(
        filtered_df['distance_cbd'],
        filtered_df['price']/1e6,
        c=filtered_df['bedrooms'],
        cmap='viridis',
        alpha=0.6,
        s=30
    )
    
    ax.set_xlabel('Distance from CBD (km)')
    ax.set_ylabel('Price ($M)')
    ax.set_title('Price vs Distance from CBD')
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Bedrooms')
    
    plt.tight_layout()
    st.pyplot(fig)

# Row 4: Data Table (Optional)
st.markdown("---")
if st.checkbox("📋 Show Raw Data"):
    st.subheader("Filtered Property Data")
    
    # Show only relevant columns
    display_cols = ['city', 'property_type', 'bedrooms', 'bathrooms', 'price', 'building_size', 'distance_cbd', 'age']
    
    # Format the dataframe for display
    display_df = filtered_df[display_cols].copy()
    display_df['price'] = display_df['price'].apply(lambda x: f'${x/1e6:.2f}M')
    display_df['building_size'] = display_df['building_size'].apply(lambda x: f'{x:.0f} sqm')
    display_df['distance_cbd'] = display_df['distance_cbd'].apply(lambda x: f'{x:.1f} km')
    display_df['age'] = display_df['age'].apply(lambda x: f'{x:.0f} years')
    
    st.dataframe(display_df.head(100), use_container_width=True)

# Footer
st.markdown("---")
st.caption("Dashboard created with Streamlit • Data is synthetic for demonstration purposes")

# Save this as app_04_housing_dashboard.py and run it!