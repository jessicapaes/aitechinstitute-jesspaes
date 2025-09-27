"""
Streamlit Demo 1: Random Assignment & P-values
Save as: demo1_randomization.py
Run with: streamlit run demo1_randomization.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Page config
st.set_page_config(page_title="Random Assignment & P-values Demo", page_icon="🎲", layout="wide")

st.title("🎲 Random Assignment & P-values Demo")
st.markdown("### See randomization in action and understand what p-values really mean!")

# Sidebar for controls
st.sidebar.header("⚙️ Controls")

# Tab layout
tab1, tab2, tab3 = st.tabs(["🎯 Random Assignment", "📊 P-Value Meaning", "🔬 Proof vs Evidence"])

# Tab 1: Random Assignment
with tab1:
    st.header("Why Random Assignment Matters")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎓 The Scenario")
        st.info("""
        **Imagine:** We're testing if a new study method improves test scores.
        
        We have 100 students with different abilities (shown as their baseline scores).
        
        **Question:** How should we assign who gets the new method?
        """)
        
        # Generate student data
        np.random.seed(42)
        n_students = 100
        baseline_ability = np.random.normal(70, 15, n_students)
        
        assignment_method = st.radio(
            "How should we assign students?",
            ["Let students volunteer (Biased)", "Random assignment (Fair)"],
            key="assignment"
        )
        
        if st.button("🎲 Assign Students & Run Experiment", key="run_exp"):
            
            if assignment_method == "Let students volunteer (Biased)":
                # Biased: Better students more likely to volunteer
                volunteer_prob = (baseline_ability - 40) / 60
                volunteer_prob = np.clip(volunteer_prob, 0.1, 0.9)
                treatment = np.random.binomial(1, volunteer_prob)
                st.warning("⚠️ Better students were more likely to volunteer!")
            else:
                # Random assignment
                treatment = np.random.binomial(1, 0.5, n_students)
                st.success("✅ Students randomly assigned - groups are balanced!")
            
            # Generate outcomes
            true_effect = 5  # True treatment effect
            noise = np.random.normal(0, 10, n_students)
            final_score = baseline_ability + treatment * true_effect + noise
            
            # Create dataframe
            df = pd.DataFrame({
                'Student': range(1, n_students + 1),
                'Baseline': baseline_ability,
                'Group': ['Treatment' if t else 'Control' for t in treatment],
                'Final Score': final_score,
                'Treatment': treatment
            })
            
            # Store in session state
            st.session_state['df'] = df
            st.session_state['assignment_method'] = assignment_method
    
    with col2:
        if 'df' in st.session_state:
            df = st.session_state['df']
            
            st.subheader("📈 Results")
            
            # Calculate group statistics
            treatment_baseline = df[df['Treatment'] == 1]['Baseline'].mean()
            control_baseline = df[df['Treatment'] == 0]['Baseline'].mean()
            treatment_final = df[df['Treatment'] == 1]['Final Score'].mean()
            control_final = df[df['Treatment'] == 0]['Final Score'].mean()
            
            # Display balance check
            st.metric(
                "Baseline Difference (should be ~0 if random)",
                f"{treatment_baseline - control_baseline:.1f} points",
                delta=None if abs(treatment_baseline - control_baseline) < 2 else "Imbalanced!",
                delta_color="inverse" if abs(treatment_baseline - control_baseline) > 2 else "off"
            )
            
            # Visualize distributions
            fig = go.Figure()
            
            for group in ['Control', 'Treatment']:
                group_data = df[df['Group'] == group]
                fig.add_trace(go.Box(
                    y=group_data['Baseline'],
                    name=f"{group} Baseline",
                    marker_color='lightblue' if group == 'Control' else 'lightcoral',
                    boxmean=True
                ))
                fig.add_trace(go.Box(
                    y=group_data['Final Score'],
                    name=f"{group} Final",
                    marker_color='blue' if group == 'Control' else 'red',
                    boxmean=True
                ))
            
            fig.update_layout(
                title="Score Distributions",
                yaxis_title="Score",
                showlegend=True,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show the measured effect
            measured_effect = treatment_final - control_final
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Measured Effect", f"{measured_effect:.1f} points")
            with col_b:
                st.metric("True Effect", "5.0 points")
            
            if st.session_state['assignment_method'] == "Let students volunteer (Biased)":
                st.error("""
                **❌ Biased Result!** The measured effect is inflated because better students 
                volunteered for treatment. We can't separate the treatment effect from selection bias!
                """)
            else:
                st.success("""
                **✅ Valid Result!** Random assignment balanced the groups, so the difference 
                we see is due to the treatment, not student characteristics!
                """)

# Tab 2: P-Value Meaning
with tab2:
    st.header("Understanding P-Values")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 The Setup")
        st.info("""
        **Scenario:** An A/B test shows:
        - Control: 5% conversion rate
        - Treatment: 7% conversion rate
        - That's a 40% lift!
        
        **Question:** Could this happen by pure chance?
        """)
        
        sample_size = st.slider("Sample size per group", 100, 10000, 1000, 100)
        true_effect = st.slider("True effect size (0 = no effect)", 0.0, 0.04, 0.02, 0.005)
        
        if st.button("🎲 Run 1000 Experiments", key="pval_sim"):
            
            results = []
            control_rate = 0.05
            treatment_rate = control_rate + true_effect
            
            for _ in range(1000):
                control_conversions = np.random.binomial(sample_size, control_rate)
                treatment_conversions = np.random.binomial(sample_size, treatment_rate)
                
                control_obs_rate = control_conversions / sample_size
                treatment_obs_rate = treatment_conversions / sample_size
                
                lift = (treatment_obs_rate - control_obs_rate) / control_obs_rate if control_obs_rate > 0 else 0
                
                # Calculate p-value
                contingency_table = np.array([
                    [control_conversions, sample_size - control_conversions],
                    [treatment_conversions, sample_size - treatment_conversions]
                ])
                _, p_value, _, _ = stats.chi2_contingency(contingency_table)
                
                results.append({
                    'lift': lift,
                    'p_value': p_value,
                    'significant': p_value < 0.01
                })
            
            results_df = pd.DataFrame(results)
            st.session_state['pval_results'] = results_df
    
    with col2:
        if 'pval_results' in st.session_state:
            results_df = st.session_state['pval_results']
            
            st.subheader("📊 Distribution of Results")
            
            # Histogram of lifts
            fig = px.histogram(
                results_df, 
                x='lift',
                nbins=50,
                title=f"1000 Experiments: Distribution of Observed Lifts",
                labels={'lift': 'Observed Lift', 'count': 'Frequency'},
                color_discrete_sequence=['lightblue']
            )
            
            # Add significance overlay
            significant = results_df[results_df['significant']]
            if len(significant) > 0:
                fig.add_trace(go.Histogram(
                    x=significant['lift'],
                    nbinsx=50,
                    name='p < 0.01',
                    marker_color='red',
                    opacity=0.6
                ))
            
            fig.add_vline(x=0.4, line_dash="dash", line_color="green", 
                         annotation_text="40% lift")
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            sig_count = results_df['significant'].sum()
            sig_pct = sig_count / len(results_df) * 100
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Experiments with p < 0.01", f"{sig_count}/1000")
            with col_b:
                st.metric("Percentage significant", f"{sig_pct:.1f}%")
            
            if true_effect == 0:
                st.info("""
                **💡 Interpretation:** Even with NO real effect, we still see some "significant" 
                results by chance! That's why p < 0.01 means "less than 1% chance if no effect."
                """)
            else:
                st.success(f"""
                **💡 Interpretation:** With a true effect of {true_effect*100:.1f}%, 
                about {sig_pct:.0f}% of experiments correctly detect it as significant.
                This is the "statistical power" of our test!
                """)

# Tab 3: Proof vs Evidence
with tab3:
    st.header("Proof vs Evidence")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔢 Mathematical Proof")
        st.info("""
        **Pythagorean Theorem:** a² + b² = c²
        
        This is ALWAYS true for right triangles. No exceptions. Ever.
        """)
        
        # Interactive Pythagorean theorem
        a = st.slider("Side a", 1, 10, 3)
        b = st.slider("Side b", 1, 10, 4)
        c = np.sqrt(a**2 + b**2)
        
        st.success(f"""
        **Proof:**
        - a = {a}, b = {b}
        - a² + b² = {a}² + {b}² = {a**2 + b**2}
        - c² = {c:.2f}² = {c**2:.2f}
        - ✅ PROVEN: Works every single time!
        """)
        
    with col2:
        st.subheader("📊 Statistical Evidence")
        st.info("""
        **Claim:** This pill reduces blood pressure
        
        We test on samples and gather evidence. Never 100% certain.
        """)
        
        # Simulate drug trial
        if st.button("🧪 Run Clinical Trial", key="trial"):
            n_patients = 200
            
            # Generate data
            placebo_reduction = np.random.normal(2, 5, n_patients//2)  # Small placebo effect
            drug_reduction = np.random.normal(8, 5, n_patients//2)     # Larger drug effect
            
            t_stat, p_value = stats.ttest_ind(drug_reduction, placebo_reduction)
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=placebo_reduction, name='Placebo', 
                                      opacity=0.7, marker_color='lightblue'))
            fig.add_trace(go.Histogram(x=drug_reduction, name='Drug', 
                                      opacity=0.7, marker_color='lightgreen'))
            
            fig.update_layout(
                title="Blood Pressure Reduction (mmHg)",
                xaxis_title="Reduction",
                yaxis_title="Count",
                barmode='overlay',
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("P-value", f"{p_value:.4f}")
            
            if p_value < 0.01:
                st.success(f"""
                **Strong Evidence!** p = {p_value:.4f}
                
                Very unlikely these results are due to chance. But still not "proof"!
                - Maybe this sample was unusual
                - Maybe there's a confounder we missed
                - Maybe the effect varies by person
                
                That's why we say "evidence suggests" not "proves"!
                """)
            else:
                st.warning(f"""
                **Weak Evidence** p = {p_value:.4f}
                
                Results could easily be due to chance.
                Need more data or larger sample.
                """)
    
    st.markdown("---")
    st.markdown("""
    ### 🎯 The Key Difference:
    
    | Proof | Evidence |
    |-------|----------|
    | 100% certain | Degrees of confidence |
    | Deductive logic | Inductive reasoning |
    | Mathematical | Empirical |
    | No exceptions | Probabilistic |
    | "It IS true" | "It's PROBABLY true" |
    
    **Remember:** In data science, we're detectives gathering evidence, not mathematicians writing proofs!
    """)

st.markdown("---")
st.markdown("### 💡 Key Takeaways")
st.success("""
1. **Random Assignment** eliminates bias by giving everyone equal chance
2. **P-values** tell us how surprising our data would be if there's no effect
3. **Statistical Evidence** quantifies uncertainty, unlike mathematical proof
4. Always remember: "Statistical significance" ≠ "Practical importance"
""")