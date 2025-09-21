"""
Law of Large Numbers & Central Limit Theorem Interactive Demo
AI Tech Institute - Week 4 Statistical Foundations

Run with: streamlit run lln_clt_demo_app.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import time

# Page configuration
st.set_page_config(
    page_title="LLN & CLT Interactive Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    div[data-testid="metric-container"] {
        background-color: rgba(28, 131, 225, 0.1);
        border: 1px solid rgba(28, 131, 225, 0.2);
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("🎲 Law of Large Numbers & Central Limit Theorem")
st.markdown("### *Interactive Statistical Foundations Explorer*")

# Sidebar Configuration
st.sidebar.header("⚙️ Configuration")

# Choose demonstration type
demo_type = st.sidebar.selectbox(
    "Select Demonstration",
    ["Law of Large Numbers", "Central Limit Theorem", "Both Combined"]
)

# Distribution selection
distribution_type = st.sidebar.selectbox(
    "Select Distribution",
    ["Normal", "Exponential", "Uniform", "Binomial", "Poisson", "Beta", "Gamma", "Custom Bimodal"]
)

# Distribution parameters
st.sidebar.subheader("Distribution Parameters")

def get_distribution_params():
    """Get parameters based on selected distribution"""
    params = {}
    
    if distribution_type == "Normal":
        params['mean'] = st.sidebar.slider("Mean (μ)", -10.0, 10.0, 0.0, 0.1)
        params['std'] = st.sidebar.slider("Std Dev (σ)", 0.1, 5.0, 1.0, 0.1)
    elif distribution_type == "Exponential":
        params['scale'] = st.sidebar.slider("Scale (λ)", 0.5, 5.0, 1.0, 0.1)
    elif distribution_type == "Uniform":
        params['low'] = st.sidebar.slider("Lower Bound", -10.0, 0.0, 0.0, 0.5)
        params['high'] = st.sidebar.slider("Upper Bound", 0.0, 10.0, 1.0, 0.5)
    elif distribution_type == "Binomial":
        params['n'] = st.sidebar.slider("Number of Trials", 1, 100, 10, 1)
        params['p'] = st.sidebar.slider("Probability", 0.0, 1.0, 0.5, 0.01)
    elif distribution_type == "Poisson":
        params['lambda'] = st.sidebar.slider("Lambda (λ)", 0.5, 10.0, 3.0, 0.5)
    elif distribution_type == "Beta":
        params['a'] = st.sidebar.slider("Alpha (α)", 0.5, 10.0, 2.0, 0.5)
        params['b'] = st.sidebar.slider("Beta (β)", 0.5, 10.0, 2.0, 0.5)
    elif distribution_type == "Gamma":
        params['shape'] = st.sidebar.slider("Shape (k)", 0.5, 10.0, 2.0, 0.5)
        params['scale'] = st.sidebar.slider("Scale (θ)", 0.5, 10.0, 2.0, 0.5)
    elif distribution_type == "Custom Bimodal":
        params['mean1'] = st.sidebar.slider("Mean 1", -10.0, 0.0, -2.0, 0.5)
        params['mean2'] = st.sidebar.slider("Mean 2", 0.0, 10.0, 2.0, 0.5)
        params['std'] = st.sidebar.slider("Std Dev", 0.5, 3.0, 1.0, 0.1)
        params['weight'] = st.sidebar.slider("Weight of Mode 1", 0.1, 0.9, 0.5, 0.1)
    
    return params

params = get_distribution_params()

# Sample size controls
st.sidebar.subheader("Sample Size Controls")

if demo_type in ["Law of Large Numbers", "Both Combined"]:
    max_samples_lln = st.sidebar.slider(
        "Max Samples for LLN",
        100, 50000, 10000, 100
    )
    
if demo_type in ["Central Limit Theorem", "Both Combined"]:
    sample_size_clt = st.sidebar.slider(
        "Sample Size (n) for CLT",
        2, 500, 30, 1
    )
    n_samples_clt = st.sidebar.slider(
        "Number of Samples for CLT",
        100, 10000, 1000, 100
    )

# Animation speed
animate = st.sidebar.checkbox("Animate Convergence", value=False)
if animate:
    animation_speed = st.sidebar.slider("Animation Speed", 0.01, 0.5, 0.1, 0.01)

# Helper Functions
def generate_samples(dist_type, params, size):
    """Generate samples from selected distribution"""
    if dist_type == "Normal":
        return np.random.normal(params['mean'], params['std'], size)
    elif dist_type == "Exponential":
        return np.random.exponential(params['scale'], size)
    elif dist_type == "Uniform":
        return np.random.uniform(params['low'], params['high'], size)
    elif dist_type == "Binomial":
        return np.random.binomial(params['n'], params['p'], size)
    elif dist_type == "Poisson":
        return np.random.poisson(params['lambda'], size)
    elif dist_type == "Beta":
        return np.random.beta(params['a'], params['b'], size)
    elif dist_type == "Gamma":
        return np.random.gamma(params['shape'], params['scale'], size)
    elif dist_type == "Custom Bimodal":
        n1 = int(size * params['weight'])
        n2 = size - n1
        mode1 = np.random.normal(params['mean1'], params['std'], n1)
        mode2 = np.random.normal(params['mean2'], params['std'], n2)
        samples = np.concatenate([mode1, mode2])
        np.random.shuffle(samples)
        return samples

def get_theoretical_mean_std(dist_type, params):
    """Get theoretical mean and standard deviation"""
    if dist_type == "Normal":
        return params['mean'], params['std']
    elif dist_type == "Exponential":
        return params['scale'], params['scale']
    elif dist_type == "Uniform":
        mean = (params['low'] + params['high']) / 2
        std = (params['high'] - params['low']) / np.sqrt(12)
        return mean, std
    elif dist_type == "Binomial":
        mean = params['n'] * params['p']
        std = np.sqrt(params['n'] * params['p'] * (1 - params['p']))
        return mean, std
    elif dist_type == "Poisson":
        return params['lambda'], np.sqrt(params['lambda'])
    elif dist_type == "Beta":
        mean = params['a'] / (params['a'] + params['b'])
        var = (params['a'] * params['b']) / ((params['a'] + params['b'])**2 * (params['a'] + params['b'] + 1))
        return mean, np.sqrt(var)
    elif dist_type == "Gamma":
        return params['shape'] * params['scale'], np.sqrt(params['shape']) * params['scale']
    elif dist_type == "Custom Bimodal":
        mean = params['weight'] * params['mean1'] + (1 - params['weight']) * params['mean2']
        # Approximate std for bimodal
        var1 = params['std']**2
        var2 = params['std']**2
        var = params['weight'] * (var1 + params['mean1']**2) + (1 - params['weight']) * (var2 + params['mean2']**2) - mean**2
        return mean, np.sqrt(var)

# Main Content Area
if demo_type == "Law of Large Numbers":
    st.header("Law of Large Numbers Demonstration")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("""
        **Law of Large Numbers (LLN)**: As the sample size increases, the sample mean converges to the population mean.
        
        Watch how the running average stabilizes around the true mean as more samples are added!
        """)
    
    # Generate samples
    samples = generate_samples(distribution_type, params, max_samples_lln)
    theoretical_mean, theoretical_std = get_theoretical_mean_std(distribution_type, params)
    
    # Calculate running average
    running_avg = np.cumsum(samples) / np.arange(1, max_samples_lln + 1)
    
    # Calculate confidence bands
    n_points = np.arange(1, max_samples_lln + 1)
    ci_width = 1.96 * theoretical_std / np.sqrt(n_points)
    upper_bound = theoretical_mean + ci_width
    lower_bound = theoretical_mean - ci_width
    
    # Create plots
    col1, col2 = st.columns(2)
    
    with col1:
        # Convergence plot
        fig_convergence = go.Figure()
        
        # Add confidence bands
        fig_convergence.add_trace(go.Scatter(
            x=n_points, y=upper_bound,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_convergence.add_trace(go.Scatter(
            x=n_points, y=lower_bound,
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(0, 100, 200, 0.2)',
            line=dict(width=0),
            name='95% CI',
            hoverinfo='skip'
        ))
        
        # Add running average
        fig_convergence.add_trace(go.Scatter(
            x=n_points, y=running_avg,
            mode='lines',
            name='Running Average',
            line=dict(color='blue', width=2),
            hovertemplate='<b>Samples:</b> %{x}<br><b>Average:</b> %{y:.4f}<extra></extra>'
        ))
        
        # Add theoretical mean
        fig_convergence.add_hline(
            y=theoretical_mean, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"True Mean: {theoretical_mean:.3f}"
        )
        
        fig_convergence.update_layout(
            title="Convergence to True Mean",
            xaxis_title="Number of Samples",
            yaxis_title="Running Average",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_convergence, use_container_width=True)
    
    with col2:
        # Error plot
        error = np.abs(running_avg - theoretical_mean)
        
        fig_error = go.Figure()
        fig_error.add_trace(go.Scatter(
            x=n_points, y=error,
            mode='lines',
            name='Absolute Error',
            line=dict(color='orange', width=2),
            hovertemplate='<b>Samples:</b> %{x}<br><b>Error:</b> %{y:.6f}<extra></extra>'
        ))
        
        # Add 1/sqrt(n) reference line
        theoretical_error = 2 * theoretical_std / np.sqrt(n_points)
        fig_error.add_trace(go.Scatter(
            x=n_points, y=theoretical_error,
            mode='lines',
            name='Theoretical (2σ/√n)',
            line=dict(color='green', width=2, dash='dash'),
            hovertemplate='<b>Samples:</b> %{x}<br><b>Expected:</b> %{y:.6f}<extra></extra>'
        ))
        
        fig_error.update_layout(
            title="Error Decay with Sample Size",
            xaxis_title="Number of Samples",
            yaxis_title="Absolute Error",
            yaxis_type="log",
            xaxis_type="log",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_error, use_container_width=True)
    
    # Statistics display
    st.subheader("📊 Convergence Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "True Mean",
            f"{theoretical_mean:.4f}",
            help="Theoretical mean of the distribution"
        )
    
    with col2:
        final_avg = running_avg[-1]
        st.metric(
            "Final Sample Mean",
            f"{final_avg:.4f}",
            f"{final_avg - theoretical_mean:+.4f}",
            help="Mean after all samples"
        )
    
    with col3:
        final_error = abs(final_avg - theoretical_mean)
        st.metric(
            "Final Error",
            f"{final_error:.6f}",
            f"{(final_error / theoretical_mean * 100):.2f}%",
            help="Absolute error from true mean"
        )
    
    with col4:
        convergence_n = np.where(error < 0.01)[0]
        conv_point = convergence_n[0] if len(convergence_n) > 0 else max_samples_lln
        st.metric(
            "Convergence at",
            f"{conv_point:,} samples",
            help="When error < 0.01"
        )

elif demo_type == "Central Limit Theorem":
    st.header("Central Limit Theorem Demonstration")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("""
        **Central Limit Theorem (CLT)**: The distribution of sample means approaches a normal distribution 
        as sample size increases, regardless of the population distribution.
        
        Watch how even non-normal distributions produce normal sample mean distributions!
        """)
    
    # Generate many samples and calculate their means
    sample_means = []
    all_samples = []
    
    for _ in range(n_samples_clt):
        sample = generate_samples(distribution_type, params, sample_size_clt)
        sample_means.append(np.mean(sample))
        all_samples.extend(sample)
    
    sample_means = np.array(sample_means)
    theoretical_mean, theoretical_std = get_theoretical_mean_std(distribution_type, params)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f"Original {distribution_type} Distribution",
            f"Distribution of Sample Means (n={sample_size_clt})",
            "Q-Q Plot (Testing Normality)",
            "Sample Size Effect on Normality"
        ),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "scatter"}]]
    )
    
    # Plot 1: Original distribution
    fig.add_trace(
        go.Histogram(
            x=all_samples[:5000],  # Limit for performance
            nbinsx=50,
            name="Original",
            marker_color='lightblue',
            showlegend=False,
            histnorm='probability density'
        ),
        row=1, col=1
    )
    
    # Plot 2: Sample means distribution
    fig.add_trace(
        go.Histogram(
            x=sample_means,
            nbinsx=50,
            name="Sample Means",
            marker_color='lightgreen',
            showlegend=False,
            histnorm='probability density'
        ),
        row=1, col=2
    )
    
    # Add normal curve overlay
    x_range = np.linspace(sample_means.min(), sample_means.max(), 100)
    theoretical_se = theoretical_std / np.sqrt(sample_size_clt)
    normal_curve = stats.norm.pdf(x_range, theoretical_mean, theoretical_se)
    
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=normal_curve,
            mode='lines',
            name='Normal Fit',
            line=dict(color='red', width=2),
            showlegend=True
        ),
        row=1, col=2
    )
    
    # Plot 3: Q-Q plot
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(sample_means)))
    sample_quantiles = np.sort(sample_means)
    
    fig.add_trace(
        go.Scatter(
            x=theoretical_quantiles,
            y=sample_quantiles,
            mode='markers',
            marker=dict(color='purple', size=4),
            name='Q-Q Points',
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Add diagonal reference line
    min_val = min(theoretical_quantiles.min(), sample_quantiles.min())
    max_val = max(theoretical_quantiles.max(), sample_quantiles.max())
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            line=dict(color='red', dash='dash'),
            name='Perfect Normal',
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Plot 4: Effect of sample size
    sample_sizes_test = [2, 5, 10, 30, 50, 100]
    skewness_values = []
    
    for n in sample_sizes_test:
        test_means = [np.mean(generate_samples(distribution_type, params, n)) 
                     for _ in range(500)]
        skewness_values.append(stats.skew(test_means))
    
    fig.add_trace(
        go.Scatter(
            x=sample_sizes_test,
            y=skewness_values,
            mode='lines+markers',
            marker=dict(size=10, color='orange'),
            line=dict(width=2),
            name='Skewness',
            showlegend=False
        ),
        row=2, col=2
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="green", row=2, col=2)
    
    # Update layout
    fig.update_xaxes(title_text="Value", row=1, col=1)
    fig.update_xaxes(title_text="Sample Mean", row=1, col=2)
    fig.update_xaxes(title_text="Theoretical Quantiles", row=2, col=1)
    fig.update_xaxes(title_text="Sample Size", row=2, col=2)
    
    fig.update_yaxes(title_text="Density", row=1, col=1)
    fig.update_yaxes(title_text="Density", row=1, col=2)
    fig.update_yaxes(title_text="Sample Quantiles", row=2, col=1)
    fig.update_yaxes(title_text="Skewness", row=2, col=2)
    
    fig.update_layout(height=800, showlegend=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.subheader("📊 CLT Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Population Mean",
            f"{theoretical_mean:.4f}",
            help="True population mean"
        )
    
    with col2:
        st.metric(
            "Mean of Sample Means",
            f"{np.mean(sample_means):.4f}",
            f"{np.mean(sample_means) - theoretical_mean:+.4f}"
        )
    
    with col3:
        expected_se = theoretical_std / np.sqrt(sample_size_clt)
        actual_se = np.std(sample_means)
        st.metric(
            "Standard Error",
            f"{actual_se:.4f}",
            f"Expected: {expected_se:.4f}",
            help="Standard deviation of sample means"
        )
    
    with col4:
        shapiro_stat, shapiro_p = stats.shapiro(sample_means[:5000])
        normality = "✅ Normal" if shapiro_p > 0.05 else "⚠️ Not Normal"
        st.metric(
            "Normality Test",
            normality,
            f"p-value: {shapiro_p:.4f}",
            help="Shapiro-Wilk test"
        )

else:  # Both Combined
    st.header("Combined LLN & CLT Demonstration")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📈 Interactive Visualization", "📊 Comparative Analysis", "🎓 Educational Insights"])
    
    with tab1:
        # Interactive combined visualization
        st.subheader("Watch Both Principles in Action")
        
        # Generate data
        population_size = 100000
        population = generate_samples(distribution_type, params, population_size)
        theoretical_mean, theoretical_std = get_theoretical_mean_std(distribution_type, params)
        
        # LLN data
        samples_lln = generate_samples(distribution_type, params, max_samples_lln)
        running_avg = np.cumsum(samples_lln) / np.arange(1, max_samples_lln + 1)
        
        # CLT data
        sample_means = []
        for _ in range(n_samples_clt):
            sample = generate_samples(distribution_type, params, sample_size_clt)
            sample_means.append(np.mean(sample))
        
        # Create interactive plot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Law of Large Numbers",
                "Central Limit Theorem",
                "Population Distribution",
                "Sampling Distribution of Means"
            )
        )
        
        # LLN plot
        n_points = np.arange(1, max_samples_lln + 1)
        fig.add_trace(
            go.Scatter(
                x=n_points,
                y=running_avg,
                mode='lines',
                name='Running Average',
                line=dict(color='blue', width=1.5)
            ),
            row=1, col=1
        )
        
        fig.add_hline(
            y=theoretical_mean,
            line_dash="dash",
            line_color="red",
            row=1, col=1
        )
        
        # CLT histogram
        fig.add_trace(
            go.Histogram(
                x=sample_means,
                nbinsx=30,
                name='Sample Means',
                marker_color='green',
                histnorm='probability density'
            ),
            row=1, col=2
        )
        
        # Population distribution
        fig.add_trace(
            go.Histogram(
                x=population[:5000],
                nbinsx=50,
                name='Population',
                marker_color='lightblue',
                histnorm='probability density'
            ),
            row=2, col=1
        )
        
        # Different sample sizes effect
        sample_sizes_demo = [5, 30, 100]
        colors = ['red', 'green', 'blue']
        
        for n, color in zip(sample_sizes_demo, colors):
            means = [np.mean(generate_samples(distribution_type, params, n)) 
                    for _ in range(1000)]
            fig.add_trace(
                go.Histogram(
                    x=means,
                    nbinsx=30,
                    name=f'n={n}',
                    marker_color=color,
                    opacity=0.5,
                    histnorm='probability density'
                ),
                row=2, col=2
            )
        
        fig.update_layout(height=700, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Comparative Analysis: Sample Size Effects")
        
        # Create comparison for different sample sizes
        sample_sizes_compare = [10, 30, 50, 100, 200, 500]
        
        results = []
        for n in sample_sizes_compare:
            # LLN convergence
            samples_temp = generate_samples(distribution_type, params, n)
            sample_mean = np.mean(samples_temp)
            
            # CLT normality
            means_temp = [np.mean(generate_samples(distribution_type, params, n)) 
                         for _ in range(500)]
            _, normality_p = stats.shapiro(means_temp[:500])
            
            results.append({
                'Sample Size': n,
                'Sample Mean': sample_mean,
                'Error from True Mean': abs(sample_mean - theoretical_mean),
                'Standard Error': theoretical_std / np.sqrt(n),
                'Normality p-value': normality_p,
                'Is Normal?': '✅' if normality_p > 0.05 else '❌'
            })
        
        results_df = pd.DataFrame(results)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Error vs sample size
            fig_error = px.line(
                results_df,
                x='Sample Size',
                y='Error from True Mean',
                markers=True,
                title='LLN: Error Reduction with Sample Size'
            )
            fig_error.update_layout(yaxis_type="log")
            st.plotly_chart(fig_error, use_container_width=True)
        
        with col2:
            # Normality vs sample size
            fig_normal = px.line(
                results_df,
                x='Sample Size',
                y='Normality p-value',
                markers=True,
                title='CLT: Normality Improves with Sample Size'
            )
            fig_normal.add_hline(y=0.05, line_dash="dash", line_color="red",
                               annotation_text="α = 0.05")
            st.plotly_chart(fig_normal, use_container_width=True)
        
        # Display table
        st.subheader("Detailed Results")
        st.dataframe(
            results_df.style.format({
                'Sample Mean': '{:.4f}',
                'Error from True Mean': '{:.6f}',
                'Standard Error': '{:.4f}',
                'Normality p-value': '{:.4f}'
            }),
            use_container_width=True
        )
    
    with tab3:
        st.subheader("🎓 Key Insights & Learning Points")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Law of Large Numbers (LLN)
            
            **What it tells us:**
            - Sample statistics converge to population parameters
            - Larger samples = More accurate estimates
            - Works for ANY distribution
            
            **Practical implications:**
            - 📊 Polls become more accurate with more respondents
            - 🎰 Casinos always win in the long run
            - 📈 Investment returns approach expected values over time
            
            **Rule of thumb:**
            - Error decreases proportionally to 1/√n
            - To halve the error, need 4× the samples
            - Diminishing returns after certain sample size
            """)
        
        with col2:
            st.markdown("""
            ### Central Limit Theorem (CLT)
            
            **What it tells us:**
            - Sample means are normally distributed
            - Works regardless of population distribution
            - Enables hypothesis testing and confidence intervals
            
            **Practical implications:**
            - 📊 Can use normal-based statistics for any data
            - 🔬 Scientific experiments rely on CLT
            - 💊 Drug trials use CLT for efficacy testing
            
            **Rule of thumb:**
            - n ≥ 30 usually sufficient for normality
            - More skewed populations need larger n
            - Standard error = σ/√n
            """)
        
        # Interactive calculator
        st.markdown("---")
        st.subheader("🧮 Quick Calculator")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            calc_mean = st.number_input("Population Mean", value=100.0)
            calc_std = st.number_input("Population Std Dev", value=15.0, min_value=0.1)
        
        with col2:
            calc_n = st.number_input("Sample Size", value=30, min_value=1)
            confidence = st.selectbox("Confidence Level", [0.90, 0.95, 0.99])
        
        with col3:
            se = calc_std / np.sqrt(calc_n)
            z_score = stats.norm.ppf((1 + confidence) / 2)
            margin = z_score * se
            
            st.metric("Standard Error", f"{se:.4f}")
            st.metric("Margin of Error", f"±{margin:.4f}")
            st.metric("Confidence Interval", f"[{calc_mean-margin:.2f}, {calc_mean+margin:.2f}]")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Created for AI Tech Institute - Week 4: Statistical Foundations</p>
    <p>Understanding LLN & CLT is fundamental to statistical inference and A/B testing</p>
</div>
""", unsafe_allow_html=True)

# Add info box
with st.expander("ℹ️ How to Use This App"):
    st.markdown("""
    1. **Choose a demonstration type** from the sidebar
    2. **Select a distribution** to explore how LLN and CLT work with different data types
    3. **Adjust parameters** to see how they affect convergence and normality
    4. **Experiment with sample sizes** to understand their impact
    5. **Use the animation feature** to watch convergence in real-time
    
    **Key Questions to Explore:**
    - How does sample size affect the accuracy of estimates? (LLN)
    - At what sample size do sample means become normal? (CLT)
    - How do different distributions affect convergence rates?
    - Why is n=30 often cited as a "magic number"?
    
    **Try These Experiments:**
    - Compare normal vs exponential distributions
    - See how bimodal distributions behave
    - Test extreme parameters (very high/low variance)
    - Compare small vs large sample sizes
    """)