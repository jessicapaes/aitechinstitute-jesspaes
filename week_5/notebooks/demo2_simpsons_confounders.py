"""
Streamlit Demo 2: Simpson's Paradox & Confounders
Save as: demo2_simpsons_confounders.py
Run with: streamlit run demo2_simpsons_confounders.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="Simpson's Paradox & Confounders", page_icon="🎭", layout="wide")

st.title("🎭 Simpson's Paradox & Confounders Demo")
st.markdown("### See how aggregated data can lie and how hidden variables affect relationships!")

# Tabs
tab1, tab2, tab3 = st.tabs(["🎓 Simpson's Paradox", "🌡️ Ice Cream & Crime", "🎯 Matching Demo"])

# Tab 1: Simpson's Paradox
with tab1:
    st.header("University Admissions Paradox")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📚 The Setup")
        st.info("""
        **Scenario:** University with 2 departments
        - Department A: Easy to get into
        - Department B: Hard to get into
        
        Let's see who applies where and what happens!
        """)
        
        # Controls
        st.markdown("### Adjust the Applications:")
        
        men_to_easy = st.slider("Men applying to Easy Dept", 0, 500, 450, 10)
        men_to_hard = st.slider("Men applying to Hard Dept", 0, 500, 50, 10)
        women_to_easy = st.slider("Women applying to Easy Dept", 0, 500, 50, 10)
        women_to_hard = st.slider("Women applying to Hard Dept", 0, 500, 450, 10)
        
        # Admission rates
        st.markdown("### Admission Rates by Department:")
        easy_rate_men = st.slider("Easy Dept - Men Accept Rate", 0.0, 1.0, 0.60, 0.01)
        easy_rate_women = st.slider("Easy Dept - Women Accept Rate", 0.0, 1.0, 0.80, 0.01)
        hard_rate_men = st.slider("Hard Dept - Men Accept Rate", 0.0, 1.0, 0.30, 0.01)
        hard_rate_women = st.slider("Hard Dept - Women Accept Rate", 0.0, 1.0, 0.35, 0.01)
        
    with col2:
        st.subheader("📊 Results")
        
        # Calculate admissions
        easy_men_admitted = int(men_to_easy * easy_rate_men)
        easy_women_admitted = int(women_to_easy * easy_rate_women)
        hard_men_admitted = int(men_to_hard * hard_rate_men)
        hard_women_admitted = int(women_to_hard * hard_rate_women)
        
        # Total admissions
        total_men_applied = men_to_easy + men_to_hard
        total_women_applied = women_to_easy + women_to_hard
        total_men_admitted = easy_men_admitted + hard_men_admitted
        total_women_admitted = easy_women_admitted + hard_women_admitted
        
        # Overall rates
        overall_rate_men = total_men_admitted / total_men_applied if total_men_applied > 0 else 0
        overall_rate_women = total_women_admitted / total_women_applied if total_women_applied > 0 else 0
        
        # Create visualization
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("By Department", "Overall"),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Department-specific rates
        departments = ['Easy-Men', 'Easy-Women', 'Hard-Men', 'Hard-Women']
        rates = [easy_rate_men, easy_rate_women, hard_rate_men, hard_rate_women]
        colors = ['lightblue', 'pink', 'lightblue', 'pink']
        
        fig.add_trace(
            go.Bar(x=departments, y=[r*100 for r in rates], 
                   marker_color=colors, name='By Dept'),
            row=1, col=1
        )
        
        # Overall rates
        fig.add_trace(
            go.Bar(x=['Men Overall', 'Women Overall'], 
                   y=[overall_rate_men*100, overall_rate_women*100],
                   marker_color=['lightblue', 'pink'], name='Overall'),
            row=1, col=2
        )
        
        fig.update_yaxes(title_text="Admission Rate (%)", row=1, col=1)
        fig.update_yaxes(title_text="Admission Rate (%)", row=1, col=2)
        fig.update_layout(height=400, showlegend=False)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show the paradox
        dept_winner = "Women" if (easy_rate_women > easy_rate_men and hard_rate_women > hard_rate_men) else "Mixed"
        overall_winner = "Men" if overall_rate_men > overall_rate_women else "Women"
        
        if dept_winner == "Women" and overall_winner == "Men":
            st.error("""
            🎭 **SIMPSON'S PARADOX DETECTED!**
            
            - Women have higher admission rates in BOTH departments
            - But men have higher OVERALL admission rate!
            
            **Why?** More women applied to the harder department!
            """)
        else:
            st.info("""
            No paradox currently. Try the original settings:
            - Many men → Easy dept
            - Many women → Hard dept
            - Women better rates in each dept
            """)
        
        # Show the numbers
        with st.expander("📋 See the Details"):
            st.markdown(f"""
            **Department A (Easy):**
            - Men: {easy_men_admitted}/{men_to_easy} = {easy_rate_men:.1%}
            - Women: {easy_women_admitted}/{women_to_easy} = {easy_rate_women:.1%}
            
            **Department B (Hard):**
            - Men: {hard_men_admitted}/{men_to_hard} = {hard_rate_men:.1%}
            - Women: {hard_women_admitted}/{women_to_hard} = {hard_rate_women:.1%}
            
            **Overall:**
            - Men: {total_men_admitted}/{total_men_applied} = {overall_rate_men:.1%}
            - Women: {total_women_admitted}/{total_women_applied} = {overall_rate_women:.1%}
            """)

# Tab 2: Ice Cream & Crime Confounder
with tab2:
    st.header("The Ice Cream Crime Mystery 🍦🚔")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Generate Data")
        
        # Controls
        n_days = st.slider("Number of days to simulate", 30, 365, 100)
        temp_effect_ice = st.slider("How much temperature affects ice cream sales", 0.0, 5.0, 3.0, 0.1)
        temp_effect_crime = st.slider("How much temperature affects crime", 0.0, 3.0, 1.5, 0.1)
        
        if st.button("🌞 Generate Summer Data", key="gen_ice"):
            np.random.seed(42)
            
            # Generate temperature (the confounder)
            temperature = np.random.normal(25, 8, n_days)
            
            # Ice cream sales increase with temperature
            ice_cream = 50 + temp_effect_ice * temperature + np.random.normal(0, 10, n_days)
            
            # Crime also increases with temperature
            crime = 20 + temp_effect_crime * temperature + np.random.normal(0, 5, n_days)
            
            # Create dataframe
            df = pd.DataFrame({
                'Day': range(1, n_days + 1),
                'Temperature': temperature,
                'Ice_Cream_Sales': ice_cream,
                'Crime_Rate': crime
            })
            
            st.session_state['ice_crime_df'] = df
    
    with col2:
        if 'ice_crime_df' in st.session_state:
            df = st.session_state['ice_crime_df']
            
            st.subheader("📊 Analysis Results")
            
            # Calculate correlations
            corr_ice_crime = df['Ice_Cream_Sales'].corr(df['Crime_Rate'])
            corr_temp_ice = df['Temperature'].corr(df['Ice_Cream_Sales'])
            corr_temp_crime = df['Temperature'].corr(df['Crime_Rate'])
            
            # Display correlations
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Ice Cream ↔ Crime", f"{corr_ice_crime:.3f}")
            with col_b:
                st.metric("Temp → Ice Cream", f"{corr_temp_ice:.3f}")
            with col_c:
                st.metric("Temp → Crime", f"{corr_temp_crime:.3f}")
            
            # Scatter plots
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Spurious Correlation", "True Relationships")
            )
            
            # Spurious correlation
            fig.add_trace(
                go.Scatter(x=df['Ice_Cream_Sales'], y=df['Crime_Rate'],
                          mode='markers', marker=dict(color='red', size=8),
                          name='Ice Cream vs Crime'),
                row=1, col=1
            )
            
            # True relationships
            fig.add_trace(
                go.Scatter(x=df['Temperature'], y=df['Ice_Cream_Sales'],
                          mode='markers', marker=dict(color='lightblue', size=6),
                          name='Temp vs Ice Cream'),
                row=1, col=2
            )
            fig.add_trace(
                go.Scatter(x=df['Temperature'], y=df['Crime_Rate'],
                          mode='markers', marker=dict(color='orange', size=6),
                          name='Temp vs Crime'),
                row=1, col=2
            )
            
            fig.update_xaxes(title_text="Ice Cream Sales", row=1, col=1)
            fig.update_yaxes(title_text="Crime Rate", row=1, col=1)
            fig.update_xaxes(title_text="Temperature (°C)", row=1, col=2)
            fig.update_layout(height=400, showlegend=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Explanation
            if corr_ice_crime > 0.5:
                st.warning(f"""
                ⚠️ **Strong correlation ({corr_ice_crime:.3f}) between ice cream and crime!**
                
                Should we ban ice cream to reduce crime? **NO!**
                
                🌡️ **Temperature is the confounder:**
                - Hot days → More ice cream sales
                - Hot days → More crime
                - Ice cream doesn't cause crime!
                
                This is why **correlation ≠ causation**!
                """)

# Tab 3: Matching Demo
with tab3:
    st.header("Matching: Finding Your Data Twin 👥")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 The Problem")
        st.info("""
        **Question:** Does premium membership increase spending?
        
        **Challenge:** Older, wealthier customers more likely to be premium.
        
        **Solution:** Match similar customers and compare!
        """)
        
        if st.button("Generate Customer Data", key="gen_match"):
            np.random.seed(42)
            n_customers = 200
            
            # Generate customer features
            age = np.random.uniform(20, 60, n_customers)
            income = np.random.uniform(20000, 100000, n_customers)
            
            # Premium membership depends on age and income
            premium_prob = (age - 20) / 40 * 0.5 + (income - 20000) / 80000 * 0.5
            is_premium = np.random.binomial(1, premium_prob)
            
            # Spending depends on age, income, AND premium status
            true_premium_effect = 50
            spending = (
                100 + 
                2 * age + 
                0.001 * income + 
                true_premium_effect * is_premium + 
                np.random.normal(0, 20, n_customers)
            )
            
            df = pd.DataFrame({
                'Customer': range(1, n_customers + 1),
                'Age': age,
                'Income': income,
                'Premium': is_premium,
                'Spending': spending,
                'Group': ['Premium' if p else 'Regular' for p in is_premium]
            })
            
            st.session_state['match_df'] = df
    
    with col2:
        if 'match_df' in st.session_state:
            df = st.session_state['match_df']
            
            st.subheader("📊 Analysis Methods")
            
            # Naive comparison
            premium_spend = df[df['Premium'] == 1]['Spending'].mean()
            regular_spend = df[df['Premium'] == 0]['Spending'].mean()
            naive_effect = premium_spend - regular_spend
            
            st.metric("Naive Comparison", f"${naive_effect:.2f}", 
                     "⚠️ Biased - includes age/income effects")
            
            # Matching
            st.markdown("### 🎯 Matching Analysis")
            
            # For each premium customer, find closest regular customer
            matched_pairs = []
            premium_customers = df[df['Premium'] == 1].sample(min(20, len(df[df['Premium'] == 1])))
            
            for _, premium_cust in premium_customers.iterrows():
                # Find regular customers with similar age and income
                regular_customers = df[df['Premium'] == 0].copy()
                regular_customers['distance'] = (
                    abs(regular_customers['Age'] - premium_cust['Age'])/10 +
                    abs(regular_customers['Income'] - premium_cust['Income'])/10000
                )
                
                closest_match = regular_customers.nsmallest(1, 'distance').iloc[0]
                
                matched_pairs.append({
                    'Premium_Spend': premium_cust['Spending'],
                    'Regular_Spend': closest_match['Spending'],
                    'Age_Diff': abs(premium_cust['Age'] - closest_match['Age']),
                    'Income_Diff': abs(premium_cust['Income'] - closest_match['Income'])
                })
            
            matched_df = pd.DataFrame(matched_pairs)
            matched_effect = matched_df['Premium_Spend'].mean() - matched_df['Regular_Spend'].mean()
            
            st.metric("Matched Comparison", f"${matched_effect:.2f}", 
                     "✅ Controls for age/income")
            
            # Statistical Adjustment (simplified linear regression concept)
            st.markdown("### 📈 Statistical Adjustment")
            
            # Group by age brackets and calculate within-group effects
            df['Age_Group'] = pd.cut(df['Age'], bins=4, labels=['20-30', '30-40', '40-50', '50-60'])
            
            adjusted_effects = []
            for age_group in df['Age_Group'].unique():
                group_data = df[df['Age_Group'] == age_group]
                if len(group_data[group_data['Premium'] == 1]) > 0 and len(group_data[group_data['Premium'] == 0]) > 0:
                    group_premium = group_data[group_data['Premium'] == 1]['Spending'].mean()
                    group_regular = group_data[group_data['Premium'] == 0]['Spending'].mean()
                    adjusted_effects.append(group_premium - group_regular)
            
            if adjusted_effects:
                adjusted_effect = np.mean(adjusted_effects)
                st.metric("Adjusted (within age groups)", f"${adjusted_effect:.2f}", 
                         "✅ Controls for age")
            
            # True effect
            st.success(f"""
            **True Premium Effect: $50**
            
            - Naive estimate: ${naive_effect:.2f} (biased high)
            - Matched estimate: ${matched_effect:.2f} (close!)
            - Adjusted estimate: ${adjusted_effect:.2f} (close!)
            
            **Lesson:** Controlling for confounders reveals true effects!
            """)
            
            # Visualization
            fig = px.scatter(df, x='Age', y='Spending', color='Group',
                           title="Why We Need Matching",
                           labels={'Age': 'Customer Age', 'Spending': 'Monthly Spending ($)'},
                           color_discrete_map={'Premium': 'red', 'Regular': 'blue'})
            
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("### 🎯 Key Takeaways")
st.success("""
1. **Simpson's Paradox:** Always check subgroups - aggregated data can reverse the truth!
2. **Confounders:** Hidden variables (like temperature) create fake correlations
3. **Matching:** Compare apples to apples by finding similar units
4. **Statistical Adjustment:** Math can "control for" confounding variables
""")