import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
from datetime import datetime
import json

st.set_page_config(
    page_title="Export Dashboard",
    layout="wide"
)

st.title("Data Export Dashboard")
st.markdown("Export your data in multiple formats")

# Generate sample data
@st.cache_data
def generate_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")

    data = pd.DataFrame({
        "date": dates,
        "sales": np.random.uniform(1000, 5000, 100),
        "costs": np.random.uniform(500, 2500, 100),
        "customers": np.random.randint(50, 200, 100),
        "region": np.random.choice(["North", "South", "East", "West"], 100),
        "product": np.random.choice(["A", "B", "C"], 100)
    })

    data["profit"] = data["sales"] - data["costs"]
    data["margin"] = (data["profit"] / data["sales"]) * 100

    return data

df = generate_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=df["region"].unique(),
    default=df["region"].unique()
)

selected_products = st.sidebar.multiselect(
    "Select Products",
    options=df["product"].unique(),
    default=df["product"].unique()
)

# Apply filters
filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["product"].isin(selected_products))
]

# Display metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${filtered_df['sales'].sum():,.0f}")
with col2:
    st.metric("Total Profit", f"${filtered_df['profit'].sum():,.0f}")
with col3:
    st.metric("Avg Margin", f"{filtered_df['margin'].mean():.1f}%")
with col4:
    st.metric("Total Customers", f"{filtered_df['customers'].sum():,}")

# Display chart
st.subheader("Sales Trend")
fig = px.line(filtered_df, x="date", y="sales", color="region")
st.plotly_chart(fig, use_container_width=True)

# Download section
st.markdown("---")
st.subheader("Export Data")

col1, col2, col3 = st.columns(3)

# CSV Download
with col1:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# Excel Download
with col2:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        filtered_df.to_excel(writer, sheet_name="Data", index=False)

    st.download_button(
        label="Download Excel",
        data=buffer.getvalue(),
        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# JSON Download
with col3:
    json_data = filtered_df.to_json(orient="records", date_format="iso")
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# Display data table
st.markdown("---")
st.subheader("Data Preview")
st.dataframe(filtered_df, use_container_width=True)