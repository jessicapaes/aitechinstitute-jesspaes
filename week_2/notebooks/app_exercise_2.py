import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import plotly.express as px

def ml_app():
    st.title("Machine Learning App")
    
    uploaded_file = st.file_uploader("Upload training data", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        # Model configuration
        st.subheader("Model Configuration")
        target_col = st.selectbox("Select target column", df.columns)
        feature_cols = st.multiselect("Select feature columns", 
                                    [col for col in df.columns if col != target_col])
        
        model_type = st.radio("Model Type", ["Regression", "Classification"])
        
        if st.button("Train Model"):
            X = df[feature_cols]
            y = df[target_col]
            
            # Handle categorical variables
            X_encoded = pd.get_dummies(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_encoded, y, test_size=0.2, random_state=42)
            
            # Train model
            if model_type == "Regression":
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                
                # Metrics
                mse = mean_squared_error(y_test, predictions)
                st.metric("Mean Squared Error", f"{mse:.4f}")
                
                # Visualization
                fig = px.scatter(x=y_test, y=predictions, labels={'x': 'Actual', 'y': 'Predicted'})
                st.plotly_chart(fig)
                
            else:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                
                # Metrics
                accuracy = accuracy_score(y_test, predictions)
                st.metric("Accuracy", f"{accuracy:.4f}")
                
                # Feature importance
                importance_df = pd.DataFrame({
                    'feature': X_encoded.columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                fig = px.bar(importance_df.head(10), x='importance', y='feature', orientation='h')
                st.plotly_chart(fig)
            
            # Store model in session state
            st.session_state.model = model
            st.session_state.feature_cols = X_encoded.columns
        
        # Prediction section
        if 'model' in st.session_state:
            st.subheader("Make Predictions")
            
            # Input fields for new data
            new_data = {}
            for col in feature_cols:
                if df[col].dtype in ['int64', 'float64']:
                    new_data[col] = st.number_input(f"{col}", value=float(df[col].mean()))
                else:
                    new_data[col] = st.selectbox(f"{col}", df[col].unique())
            
            if st.button("Predict"):
                new_df = pd.DataFrame([new_data])
                new_df_encoded = pd.get_dummies(new_df)
                
                # Align columns
                for col in st.session_state.feature_cols:
                    if col not in new_df_encoded.columns:
                        new_df_encoded[col] = 0
                new_df_encoded = new_df_encoded[st.session_state.feature_cols]
                
                prediction = st.session_state.model.predict(new_df_encoded)[0]
                st.success(f"Prediction: {prediction:.4f}")

ml_app()