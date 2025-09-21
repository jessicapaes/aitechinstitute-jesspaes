import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def data_explorer():
    st.title("Data Explorer")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Show basic info
        st.subheader("Dataset Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns))
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        
        # Column filtering
        st.subheader("Column Selection")
        selected_columns = st.multiselect("Select columns to analyze", df.columns, default=df.columns[:5])
        
        if selected_columns:
            filtered_df = df[selected_columns]
            
            # Data preview
            st.subheader("Data Preview")
            st.dataframe(filtered_df.head())
            
            # Statistics
            st.subheader("Statistics")
            st.dataframe(filtered_df.describe())
            
            # Automatic visualizations
            st.subheader("Visualizations")
            numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) > 0:
                # Histogram
                hist_col = st.selectbox("Select column for histogram", numeric_cols)
                fig_hist = px.histogram(filtered_df, x=hist_col)
                st.plotly_chart(fig_hist)
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    st.write("Correlation Heatmap")
                    corr = filtered_df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, text_auto=True, aspect="auto")
                    st.plotly_chart(fig_corr)

data_explorer()