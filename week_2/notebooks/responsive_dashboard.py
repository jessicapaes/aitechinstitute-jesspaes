import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Responsive Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .row-widget.stHorizontal {
            flex-direction: column;
        }

        h1 {
            font-size: 1.5rem;
        }

        h2 {
            font-size: 1.25rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("Responsive Dashboard")
st.caption("Optimized for all screen sizes")

# Mobile-friendly tabs instead of sidebar on small screens
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Analytics", "Data", "Settings"])

with tab1:
    st.header("Overview")

    # Responsive metrics grid
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Revenue", "$45.2K", "+12%")
        st.metric("Users", "1,234", "+5%")
    with col2:
        st.metric("Orders", "342", "+8%")
        st.metric("Avg. Value", "$132", "-2%")

    # Responsive chart
    st.subheader("Trend")

    # Generate sample data
    dates = pd.date_range(start="2024-01-01", periods=30)
    data = pd.DataFrame({
        "Date": dates,
        "Value": np.random.randn(30).cumsum() + 100
    })

    fig = px.line(data, x="Date", y="Value", title="30-Day Trend")
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Analytics")

    analysis_type = st.selectbox(
        "Select Analysis",
        ["Sales by Region", "Product Performance", "Customer Segments"]
    )

    if analysis_type == "Sales by Region":
        region_data = pd.DataFrame({
            "Region": ["North", "South", "East", "West"],
            "Sales": [45000, 38000, 52000, 41000]
        })

        fig = px.bar(
            region_data,
            x="Sales",
            y="Region",
            orientation="h",
            title="Sales by Region"
        )
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Data Table")

    # Generate sample data
    df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=10),
        "Sales": np.random.randint(1000, 5000, 10),
        "Orders": np.random.randint(10, 50, 10),
        "Region": np.random.choice(["North", "South", "East", "West"], 10)
    })

    # Mobile-optimized table display
    display_columns = st.multiselect(
        "Select columns to display",
        options=df.columns.tolist(),
        default=["Date", "Sales"]
    )

    if display_columns:
        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True
        )

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
        use_container_width=True
    )

with tab4:
    st.header("Settings")

    with st.form("settings_form"):
        st.subheader("Display Preferences")

        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        notifications = st.checkbox("Enable notifications")

        submitted = st.form_submit_button(
            "Save Settings",
            type="primary",
            use_container_width=True
        )

        if submitted:
            st.success("Settings saved successfully!")