"""
Streamlit Demo 3: Causal Inference Techniques
Save as: demo3_causal_techniques.py
Run with: streamlit run demo3_causal_techniques.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# Page config
st.set_page_config(page_title="Causal Inference Techniques", page_icon="🔬", layout="wide")

st.title("🔬 Causal Inference Techniques Demo")
st.markdown("### Interactive demonstrations of DiD, RDD, IV, and Propensity Score methods")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Difference-in-Differences", "📊 Regression Discontinuity", 
                                   "🎯 Instrumental Variables", "⚖️ Propensity Scores"])

# Tab 1: Difference-in-Differences
with tab1:
    st.header("Difference-in-Differences (DiD)")
    st.info("""
    **Scenario:** A retail chain implements a loyalty program in some stores but not others.
    We'll compare the CHANGE in sales between treated and control stores.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Setup")
        
        n_stores = st.slider("Number of stores per group", 5, 20, 10)
        true_effect = st.slider("True treatment effect (%)", 0, 30, 15)
        trend = st.slider("General market trend (% per month)", -5, 5, 1)
        
        if st.button("🏪 Generate Store Data", key="did_gen"):
            np.random.seed(42)
            
            months = 12
            treatment_start = 6
            
            # Generate data for treatment and control stores
            data = []
            
            for store_group in ['Treatment', 'Control']:
                for store in range(n_stores):
                    base_sales = np.random.uniform(80000, 120000)
                    
                    for month in range(months):
                        # Base sales with trend
                        sales = base_sales * (1 + trend/100 * month)
                        
                        # Add treatment effect after month 6
                        if store_group == 'Treatment' and month >= treatment_start:
                            sales *= (1 + true_effect/100)
                        
                        # Add noise
                        sales += np.random.normal(0, 5000)
                        
                        data.append({
                            'Store': f"{store_group[0]}{store}",
                            'Group': store_group,
                            'Month': month,
                            'Sales': sales,
                            'Period': 'Before' if month < treatment_start else 'After'
                        })
            
            df = pd.DataFrame(data)
            st.session_state['did_df'] = df
    
    with col2:
        if 'did_df' in st.session_state:
            df = st.session_state['did_df']
            
            st.subheader("📊 DiD Analysis")
            
            # Calculate DiD
            avg_sales = df.groupby(['Group', 'Period'])['Sales'].mean().reset_index()
            
            # Get the four values
            control_before = avg_sales[(avg_sales['Group'] == 'Control') & 
                                      (avg_sales['Period'] == 'Before')]['Sales'].values[0]
            control_after = avg_sales[(avg_sales['Group'] == 'Control') & 
                                     (avg_sales['Period'] == 'After')]['Sales'].values[0]
            treatment_before = avg_sales[(avg_sales['Group'] == 'Treatment') & 
                                        (avg_sales['Period'] == 'Before')]['Sales'].values[0]
            treatment_after = avg_sales[(avg_sales['Group'] == 'Treatment') & 
                                       (avg_sales['Period'] == 'After')]['Sales'].values[0]
            
            # Calculate differences
            control_change = control_after - control_before
            treatment_change = treatment_after - treatment_before
            did_effect = treatment_change - control_change
            did_percent = (did_effect / treatment_before) * 100
            
            # Visualization
            fig = go.Figure()
            
            # Plot average lines
            months = df['Month'].unique()
            for group in ['Control', 'Treatment']:
                group_data = df[df['Group'] == group].groupby('Month')['Sales'].mean()
                color = 'blue' if group == 'Control' else 'red'
                fig.add_trace(go.Scatter(
                    x=months, y=group_data,
                    mode='lines+markers',
                    name=group,
                    line=dict(color=color, width=2),
                    marker=dict(size=8)
                ))
            
            # Add vertical line for treatment start
            fig.add_vline(x=5.5, line_dash="dash", line_color="gray",
                         annotation_text="Program Starts")
            
            fig.update_layout(
                title="Sales Over Time: Parallel Trends & Treatment Effect",
                xaxis_title="Month",
                yaxis_title="Sales ($)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # DiD Table
            st.markdown("### DiD Calculation Table")
            
            did_table = pd.DataFrame({
                'Group': ['Control', 'Treatment', 'Difference'],
                'Before': [f"${control_before:,.0f}", f"${treatment_before:,.0f}", ""],
                'After': [f"${control_after:,.0f}", f"${treatment_after:,.0f}", ""],
                'Change': [f"${control_change:,.0f}", f"${treatment_change:,.0f}", 
                          f"**${did_effect:,.0f}**"]
            })
            
            st.dataframe(did_table, use_container_width=True, hide_index=True)
            
            # Results
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("DiD Effect", f"{did_percent:.1f}%")
            with col_b:
                st.metric("True Effect", f"{true_effect}%")
            
            st.success(f"""
            **Interpretation:**
            - Control stores changed by ${control_change:,.0f} (market trend)
            - Treatment stores changed by ${treatment_change:,.0f} (trend + program)
            - DiD isolates program effect: ${did_effect:,.0f} ({did_percent:.1f}%)
            
            The parallel trends assumption appears valid - groups moved similarly before treatment!
            """)

# Tab 2: Regression Discontinuity Design
with tab2:
    st.header("Regression Discontinuity Design (RDD)")
    st.info("""
    **Scenario:** Customers get a 20% discount if they spend ≥$100.
    We'll see how this threshold creates a jump in future spending.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Setup")
        
        n_customers = st.slider("Number of customers", 100, 500, 200)
        threshold = st.slider("Discount threshold ($)", 50, 150, 100)
        discount_effect = st.slider("True discount effect on future spending ($)", 0, 50, 20)
        
        if st.button("🛍️ Generate Customer Data", key="rdd_gen"):
            np.random.seed(42)
            
            # Generate customer spending (running variable)
            current_spending = np.random.uniform(threshold - 50, threshold + 50, n_customers)
            
            # Treatment: discount if spending >= threshold
            got_discount = (current_spending >= threshold).astype(int)
            
            # Future spending: continuous relationship + jump at threshold
            future_spending = (
                0.8 * current_spending +  # Natural relationship
                discount_effect * got_discount +  # Treatment effect
                np.random.normal(0, 10, n_customers)  # Noise
            )
            
            df = pd.DataFrame({
                'Customer': range(n_customers),
                'Current_Spending': current_spending,
                'Got_Discount': got_discount,
                'Future_Spending': future_spending,
                'Group': ['Discount' if d else 'No Discount' for d in got_discount]
            })
            
            st.session_state['rdd_df'] = df
    
    with col2:
        if 'rdd_df' in st.session_state:
            df = st.session_state['rdd_df']
            
            st.subheader("📊 RDD Analysis")
            
            # Create RDD plot
            fig = go.Figure()
            
            # Scatter plot
            for group, color in [('No Discount', 'blue'), ('Discount', 'red')]:
                group_data = df[df['Group'] == group]
                fig.add_trace(go.Scatter(
                    x=group_data['Current_Spending'],
                    y=group_data['Future_Spending'],
                    mode='markers',
                    name=group,
                    marker=dict(color=color, size=5, opacity=0.5)
                ))
            
            # Fit lines on each side of threshold
            bandwidth = 20
            left_data = df[df['Current_Spending'] < threshold]
            right_data = df[df['Current_Spending'] >= threshold]
            
            # Local linear regression
            left_near = left_data[left_data['Current_Spending'] > threshold - bandwidth]
            right_near = right_data[right_data['Current_Spending'] < threshold + bandwidth]
            
            if len(left_near) > 5 and len(right_near) > 5:
                # Fit polynomials
                z_left = np.polyfit(left_near['Current_Spending'], 
                                   left_near['Future_Spending'], 1)
                z_right = np.polyfit(right_near['Current_Spending'],
                                    right_near['Future_Spending'], 1)
                
                # Create smooth lines
                x_left = np.linspace(threshold - bandwidth, threshold, 50)
                x_right = np.linspace(threshold, threshold + bandwidth, 50)
                
                y_left = np.polyval(z_left, x_left)
                y_right = np.polyval(z_right, x_right)
                
                fig.add_trace(go.Scatter(
                    x=x_left, y=y_left,
                    mode='lines',
                    name='Left fit',
                    line=dict(color='blue', width=3)
                ))
                
                fig.add_trace(go.Scatter(
                    x=x_right, y=y_right,
                    mode='lines',
                    name='Right fit',
                    line=dict(color='red', width=3)
                ))
                
                # Calculate discontinuity
                left_at_threshold = np.polyval(z_left, threshold)
                right_at_threshold = np.polyval(z_right, threshold)
                discontinuity = right_at_threshold - left_at_threshold
                
                # Add discontinuity line
                fig.add_trace(go.Scatter(
                    x=[threshold, threshold],
                    y=[left_at_threshold, right_at_threshold],
                    mode='lines+markers',
                    name=f'Effect: ${discontinuity:.2f}',
                    line=dict(color='green', width=4),
                    marker=dict(size=10)
                ))
            
            # Add threshold line
            fig.add_vline(x=threshold, line_dash="dash", line_color="gray",
                         annotation_text=f"Threshold: ${threshold}")
            
            fig.update_layout(
                title="RDD: Sharp Discontinuity at Threshold",
                xaxis_title="Current Spending ($)",
                yaxis_title="Future Spending ($)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Results
            if 'discontinuity' in locals():
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("RDD Estimate", f"${discontinuity:.2f}")
                with col_b:
                    st.metric("True Effect", f"${discount_effect}")
                
                st.success(f"""
                **Interpretation:**
                - Customers just below ${threshold} are very similar to those just above
                - The only difference: getting the discount
                - The jump at the threshold ({discontinuity:.2f}) estimates the causal effect
                
                This works because being just above/below the threshold is essentially random!
                """)

# Tab 3: Instrumental Variables
with tab3:
    st.header("Instrumental Variables (IV)")
    st.info("""
    **Scenario:** Does education increase income? Problem: Ability affects both!
    Solution: Use distance to college as an "instrument" - it affects education but not income directly.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Setup")
        
        n_people = st.slider("Number of people", 100, 500, 300)
        true_education_effect = st.slider("True effect of education on income ($/year)", 
                                         0, 10000, 5000)
        
        if st.button("🎓 Generate Population Data", key="iv_gen"):
            np.random.seed(42)
            
            # Hidden confounder: ability
            ability = np.random.normal(50, 15, n_people)
            
            # Instrument: distance to college (random, like lottery)
            distance_to_college = np.random.uniform(0, 100, n_people)
            
            # Distance affects education (farther = less education)
            years_education = (
                12 +  # Base
                ability / 20 +  # Ability increases education
                - distance_to_college / 25 +  # Distance decreases education
                np.random.normal(0, 2, n_people)
            )
            years_education = np.clip(years_education, 8, 20)
            
            # Income affected by ability AND education
            income = (
                20000 +  # Base
                ability * 500 +  # Ability directly affects income (confounding!)
                true_education_effect * years_education +  # True causal effect
                np.random.normal(0, 5000, n_people)
            )
            
            df = pd.DataFrame({
                'Person': range(n_people),
                'Distance_to_College': distance_to_college,
                'Years_Education': years_education,
                'Income': income,
                'Ability': ability  # Hidden in real life!
            })
            
            st.session_state['iv_df'] = df
    
    with col2:
        if 'iv_df' in st.session_state:
            df = st.session_state['iv_df']
            
            st.subheader("📊 IV Analysis")
            
            # Naive OLS estimate (biased)
            corr_edu_income = df['Years_Education'].corr(df['Income'])
            slope_naive = np.polyfit(df['Years_Education'], df['Income'], 1)[0]
            
            # IV estimate
            # First stage: Distance → Education
            first_stage = np.polyfit(df['Distance_to_College'], df['Years_Education'], 1)[0]
            
            # Reduced form: Distance → Income
            reduced_form = np.polyfit(df['Distance_to_College'], df['Income'], 1)[0]
            
            # IV estimate = Reduced form / First stage
            iv_estimate = reduced_form / first_stage if first_stage != 0 else 0
            
            # Display results
            st.markdown("### Three Estimation Methods")
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Naive OLS", f"${slope_naive:.0f}/year",
                         "❌ Biased by ability")
            with col_b:
                st.metric("IV Estimate", f"${abs(iv_estimate):.0f}/year",
                         "✅ Controls for ability")
            with col_c:
                st.metric("True Effect", f"${true_education_effect}/year",
                         "🎯 Target")
            
            # Visualizations
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=("Naive: Education → Income",
                              "First Stage: Distance → Education",
                              "Reduced Form: Distance → Income")
            )
            
            # Naive regression
            fig.add_trace(
                go.Scatter(x=df['Years_Education'], y=df['Income'],
                          mode='markers', marker=dict(color='lightblue', size=5),
                          name='Data'),
                row=1, col=1
            )
            
            # First stage
            fig.add_trace(
                go.Scatter(x=df['Distance_to_College'], y=df['Years_Education'],
                          mode='markers', marker=dict(color='lightgreen', size=5),
                          name='First Stage'),
                row=1, col=2
            )
            
            # Reduced form
            fig.add_trace(
                go.Scatter(x=df['Distance_to_College'], y=df['Income'],
                          mode='markers', marker=dict(color='lightcoral', size=5),
                          name='Reduced Form'),
                row=1, col=3
            )
            
            fig.update_xaxes(title_text="Years Education", row=1, col=1)
            fig.update_xaxes(title_text="Distance (miles)", row=1, col=2)
            fig.update_xaxes(title_text="Distance (miles)", row=1, col=3)
            fig.update_yaxes(title_text="Income ($)", row=1, col=1)
            fig.update_yaxes(title_text="Years Education", row=1, col=2)
            fig.update_yaxes(title_text="Income ($)", row=1, col=3)
            
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"""
            **How IV Works:**
            1. **Distance affects education** (people far from college get less education)
            2. **Distance doesn't directly affect income** (only through education)
            3. **So:** The income change from distance ÷ education change from distance = true effect!
            
            The naive estimate (${slope_naive:.0f}) is biased because high-ability people get more 
            education AND earn more. The IV estimate (${abs(iv_estimate):.0f}) isolates the true 
            causal effect by using random variation in distance!
            """)

# Tab 4: Propensity Score
with tab4:
    st.header("Propensity Score Methods")
    st.info("""
    **Scenario:** Does a wellness program reduce sick days? 
    Problem: Healthier employees more likely to join!
    Solution: Use propensity scores to balance groups.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("⚙️ Setup")
        
        n_employees = st.slider("Number of employees", 100, 500, 300, key="ps_n")
        true_program_effect = st.slider("True program effect (fewer sick days)", 
                                       -5, 0, -2, key="ps_effect")
        
        if st.button("👥 Generate Employee Data", key="ps_gen"):
            np.random.seed(42)
            
            # Employee characteristics
            age = np.random.uniform(25, 60, n_employees)
            fitness_level = np.random.uniform(0, 10, n_employees)
            stress_level = np.random.uniform(0, 10, n_employees)
            
            # Propensity to join program (healthier people more likely)
            propensity_score = 1 / (1 + np.exp(-(
                -2 + 
                0.05 * age + 
                0.3 * fitness_level - 
                0.2 * stress_level
            )))
            
            # Actual program participation
            joined_program = np.random.binomial(1, propensity_score)
            
            # Sick days (affected by characteristics AND program)
            sick_days = (
                10 - 
                0.1 * age - 
                0.5 * fitness_level + 
                0.3 * stress_level + 
                true_program_effect * joined_program +
                np.random.normal(0, 2, n_employees)
            )
            sick_days = np.clip(sick_days, 0, 20)
            
            df = pd.DataFrame({
                'Employee': range(n_employees),
                'Age': age,
                'Fitness': fitness_level,
                'Stress': stress_level,
                'Propensity_Score': propensity_score,
                'Joined_Program': joined_program,
                'Sick_Days': sick_days
            })
            
            st.session_state['ps_df'] = df
    
    with col2:
        if 'ps_df' in st.session_state:
            df = st.session_state['ps_df']
            
            st.subheader("📊 Propensity Score Analysis")
            
            # Naive comparison
            program_sick = df[df['Joined_Program'] == 1]['Sick_Days'].mean()
            no_program_sick = df[df['Joined_Program'] == 0]['Sick_Days'].mean()
            naive_effect = program_sick - no_program_sick
            
            # Propensity score matching
            # For each treated person, find control with closest propensity score
            matched_effects = []
            treated = df[df['Joined_Program'] == 1].sample(min(30, len(df[df['Joined_Program'] == 1])))
            
            for _, treated_emp in treated.iterrows():
                # Find untreated with similar propensity score
                untreated = df[df['Joined_Program'] == 0].copy()
                untreated['ps_diff'] = abs(untreated['Propensity_Score'] - 
                                          treated_emp['Propensity_Score'])
                
                if len(untreated) > 0:
                    closest_match = untreated.nsmallest(1, 'ps_diff').iloc[0]
                    effect = treated_emp['Sick_Days'] - closest_match['Sick_Days']
                    matched_effects.append(effect)
            
            ps_effect = np.mean(matched_effects) if matched_effects else 0
            
            # Display results
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Naive Effect", f"{naive_effect:.2f} days",
                         "❌ Biased")
            with col_b:
                st.metric("PS Matched", f"{ps_effect:.2f} days",
                         "✅ Balanced")
            with col_c:
                st.metric("True Effect", f"{true_program_effect} days",
                         "🎯 Target")
            
            # Visualize propensity score overlap
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Propensity Score Distribution", "Sick Days by Group")
            )
            
            # Propensity scores by group
            for joined, color, name in [(0, 'blue', 'No Program'), 
                                        (1, 'red', 'Joined Program')]:
                group_data = df[df['Joined_Program'] == joined]
                fig.add_trace(
                    go.Histogram(x=group_data['Propensity_Score'],
                                name=name,
                                marker_color=color,
                                opacity=0.6,
                                nbinsx=20),
                    row=1, col=1
                )
            
            # Sick days
            fig.add_trace(
                go.Box(y=df[df['Joined_Program'] == 0]['Sick_Days'],
                      name='No Program',
                      marker_color='blue'),
                row=1, col=2
            )
            fig.add_trace(
                go.Box(y=df[df['Joined_Program'] == 1]['Sick_Days'],
                      name='Joined',
                      marker_color='red'),
                row=1, col=2
            )
            
            fig.update_xaxes(title_text="Propensity Score", row=1, col=1)
            fig.update_yaxes(title_text="Count", row=1, col=1)
            fig.update_yaxes(title_text="Sick Days", row=1, col=2)
            
            fig.update_layout(height=350, showlegend=True, barmode='overlay')
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"""
            **How Propensity Scores Work:**
            1. **Calculate probability** of getting treatment based on characteristics
            2. **Match people** with similar probabilities but different treatment
            3. **Compare outcomes** between matched pairs
            
            The naive comparison ({naive_effect:.2f}) is biased because healthier people joined.
            Propensity score matching ({ps_effect:.2f}) creates balanced comparison groups!
            """)

st.markdown("---")
st.markdown("### 🎯 Method Selection Guide")

st.info("""
| Method | When to Use | Key Assumption | What Makes It Work |
|--------|------------|----------------|-------------------|
| **DiD** | Policy changes over time | Parallel trends | Removes time-invariant confounders |
| **RDD** | Treatment has threshold | Continuity at cutoff | Near-threshold is random |
| **IV** | Hidden confounders exist | Valid instrument | Random variation in treatment |
| **Propensity Score** | Many observed confounders | No hidden confounders | Balances observed characteristics |
""")

st.success("""
**Remember:** Each method makes different assumptions. The key is:
1. Understanding what assumption you're making
2. Checking if it's reasonable in your context
3. Being honest about limitations
""")