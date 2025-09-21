import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="Database Dashboard",
    layout="wide"
)

st.title("Database Integration Dashboard")

# Create or connect to SQLite database
@st.cache_resource
def init_database():
    conn = sqlite3.connect("dashboard.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            product TEXT,
            region TEXT,
            amount REAL,
            quantity INTEGER
        )
    """)

    # Check if table is empty and add sample data
    cursor.execute("SELECT COUNT(*) FROM sales")
    if cursor.fetchone()[0] == 0:
        # Add sample data
        from datetime import timedelta

        products = ["Product A", "Product B", "Product C"]
        regions = ["North", "South", "East", "West"]

        for i in range(100):
            date = datetime.now() - timedelta(days=100-i)
            product = np.random.choice(products)
            region = np.random.choice(regions)
            amount = np.random.uniform(100, 1000)
            quantity = np.random.randint(1, 20)

            cursor.execute(
                "INSERT INTO sales (date, product, region, amount, quantity) VALUES (?, ?, ?, ?, ?)",
                (date.date(), product, region, amount, quantity)
            )

        conn.commit()

    return conn

# Initialize database
conn = init_database()

# Sidebar for database operations
st.sidebar.header("Database Operations")

operation = st.sidebar.selectbox(
    "Select Operation",
    ["View Data", "Add Record", "Query Builder"]
)

if operation == "View Data":
    st.header("View Database Tables")

    # Fetch data from database
    query = "SELECT * FROM sales ORDER BY id DESC LIMIT 100"
    df = pd.read_sql_query(query, conn)

    # Display metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Sales", f"${df['amount'].sum():,.2f}")
    with col3:
        st.metric("Avg Order", f"${df['amount'].mean():,.2f}")

    # Display data
    st.dataframe(df, use_container_width=True)

elif operation == "Add Record":
    st.header("Add New Record")

    with st.form("add_sale"):
        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date")
            product = st.selectbox("Product", ["Product A", "Product B", "Product C"])
            region = st.selectbox("Region", ["North", "South", "East", "West"])

        with col2:
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
            quantity = st.number_input("Quantity", min_value=1, step=1)

        if st.form_submit_button("Add Sale", type="primary"):
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sales (date, product, region, amount, quantity) VALUES (?, ?, ?, ?, ?)",
                (date, product, region, amount, quantity)
            )
            conn.commit()
            st.success("Sale record added successfully!")

elif operation == "Query Builder":
    st.header("SQL Query Builder")

    query = st.text_area(
        "Enter SQL Query",
        value="SELECT * FROM sales WHERE amount > 500 LIMIT 10",
        height=100
    )

    if st.button("Execute Query", type="primary"):
        try:
            result_df = pd.read_sql_query(query, conn)
            st.success(f"Query executed successfully! {len(result_df)} rows returned.")
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")