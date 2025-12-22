"""
Mental Health Risk Prediction App
Using Big Five Personality Traits
"""
import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="Mental Health Risk Screener",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .risk-low {
        background: linear-gradient(135deg, #10B981, #34D399);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .risk-medium {
        background: linear-gradient(135deg, #F59E0B, #FBBF24);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .risk-high {
        background: linear-gradient(135deg, #EF4444, #F87171);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .info-box {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .disclaimer {
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.title("🧠 Mental Health Risk Screener")
st.markdown("*Using Big Five Personality Traits*")
st.markdown("</div>", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class='disclaimer'>
⚠️ <strong>Important:</strong> This is a screening tool for educational purposes only. 
It is NOT a clinical diagnosis. If you're experiencing mental health concerns, 
please consult a qualified healthcare professional.
</div>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    model = joblib.load('Paes_Jessica_Capstone2_Model.pkl')
    scaler = joblib.load('feature_scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    return model, scaler, label_encoder

try:
    model, scaler, label_encoder = load_model()
    model_loaded = True
except:
    model_loaded = False
    st.error("⚠️ Model files not found. Please ensure the .pkl files are in the same directory.")

if model_loaded:
    st.markdown("---")
    st.subheader("📝 Rate yourself on each personality trait")
    st.markdown("*Move the sliders based on how well each description fits you (1 = Not at all, 5 = Very much)*")
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Neuroticism** 😰")
        st.caption("Tendency to feel anxiety, worry & emotional instability")
        n1 = st.slider("I get stressed out easily", 1, 6, 3, key="n1")
        n2 = st.slider("I worry about things", 1, 6, 3, key="n2")
        n3 = st.slider("I am easily disturbed", 1, 6, 3, key="n3")
        n4 = st.slider("I get upset easily", 1, 6, 3, key="n4")
        n5 = st.slider("I change my mood a lot", 1, 6, 3, key="n5")
        neuroticism = n1 + n2 + n3 + n4 + n5
        
        st.markdown("**Conscientiousness** 📋")
        st.caption("Organised, disciplined & goal-oriented")
        c1 = st.slider("I am always prepared", 1, 6, 3, key="c1")
        c2 = st.slider("I pay attention to details", 1, 6, 3, key="c2")
        c3 = st.slider("I get chores done right away", 1, 6, 3, key="c3")
        c4 = st.slider("I follow a schedule", 1, 6, 3, key="c4")
        c5 = st.slider("I am exacting in my work", 1, 6, 3, key="c5")
        conscientiousness = c1 + c2 + c3 + c4 + c5
        
        st.markdown("**Openness** 🎨")
        st.caption("Creative, curious & open to new experiences")
        o1 = st.slider("I have a vivid imagination", 1, 6, 3, key="o1")
        o2 = st.slider("I enjoy thinking about things", 1, 6, 3, key="o2")
        o3 = st.slider("I am full of ideas", 1, 6, 3, key="o3")
        o4 = st.slider("I enjoy artistic experiences", 1, 6, 3, key="o4")
        o5 = st.slider("I like to try new things", 1, 6, 3, key="o5")
        openness = o1 + o2 + o3 + o4 + o5
    
    with col2:
        st.markdown("**Extraversion** 🎉")
        st.caption("Outgoing, energetic & enjoys social interaction")
        e1 = st.slider("I am the life of the party", 1, 6, 3, key="e1")
        e2 = st.slider("I talk to a lot of different people", 1, 6, 3, key="e2")
        e3 = st.slider("I feel comfortable around people", 1, 6, 3, key="e3")
        e4 = st.slider("I start conversations", 1, 6, 3, key="e4")
        e5 = st.slider("I don't mind being the center of attention", 1, 6, 3, key="e5")
        extraversion = e1 + e2 + e3 + e4 + e5
        
        st.markdown("**Agreeableness** 🤝")
        st.caption("Cooperative, trusting & helpful to others")
        a1 = st.slider("I am interested in people", 1, 6, 3, key="a1")
        a2 = st.slider("I sympathize with others' feelings", 1, 6, 3, key="a2")
        a3 = st.slider("I have a soft heart", 1, 6, 3, key="a3")
        a4 = st.slider("I take time out for others", 1, 6, 3, key="a4")
        a5 = st.slider("I make people feel at ease", 1, 6, 3, key="a5")
        agreeableness = a1 + a2 + a3 + a4 + a5
        
        st.markdown("**Demographics**")
        age = st.number_input("Your age", min_value=16, max_value=100, value=25)
    
    st.markdown("---")
    
    # Show current scores
    st.subheader("📊 Your Personality Profile")
    score_col1, score_col2, score_col3, score_col4, score_col5 = st.columns(5)
    score_col1.metric("Neuroticism", f"{neuroticism}/30", delta=None)
    score_col2.metric("Extraversion", f"{extraversion}/30", delta=None)
    score_col3.metric("Conscientiousness", f"{conscientiousness}/30", delta=None)
    score_col4.metric("Agreeableness", f"{agreeableness}/30", delta=None)
    score_col5.metric("Openness", f"{openness}/30", delta=None)
    
    st.markdown("---")
    
    # Predict button
    if st.button("🔮 Get My Risk Assessment", type="primary", use_container_width=True):
        # Prepare data
        input_data = pd.DataFrame({
            'neuroticism_score': [neuroticism],
            'extraversion_score': [extraversion],
            'conscientiousness_score': [conscientiousness],
            'agreeableness_score': [agreeableness],
            'openness_score': [openness],
            'age': [age]
        })
        
        # Scale and predict
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)
        probabilities = model.predict_proba(input_scaled)[0]
        risk_level = label_encoder.inverse_transform(prediction)[0]
        
        # Get class order
        classes = label_encoder.classes_
        prob_dict = {cls: prob for cls, prob in zip(classes, probabilities)}
        
        st.markdown("---")
        st.subheader("🎯 Your Results")
        
        # Display result with appropriate styling
        if risk_level == "Low Risk":
            st.markdown(f"<div class='risk-low'>✅ {risk_level}</div>", unsafe_allow_html=True)
            st.success("Your personality profile suggests lower vulnerability to depression and anxiety.")
        elif risk_level == "Medium Risk":
            st.markdown(f"<div class='risk-medium'>⚠️ {risk_level}</div>", unsafe_allow_html=True)
            st.warning("Your personality profile suggests moderate vulnerability. Consider proactive self-care.")
        else:
            st.markdown(f"<div class='risk-high'>🔴 {risk_level}</div>", unsafe_allow_html=True)
            st.error("Your personality profile suggests higher vulnerability. Consider speaking with a professional.")
        
        # Show probabilities
        st.markdown("#### Confidence Breakdown")
        prob_col1, prob_col2, prob_col3 = st.columns(3)
        prob_col1.metric("Low Risk", f"{prob_dict.get('Low Risk', 0)*100:.1f}%")
        prob_col2.metric("Medium Risk", f"{prob_dict.get('Medium Risk', 0)*100:.1f}%")
        prob_col3.metric("High Risk", f"{prob_dict.get('High Risk', 0)*100:.1f}%")
        
        # Key insights
        st.markdown("#### 💡 Key Insights")
        
        insights = []
        if neuroticism > 20:
            insights.append("• **High Neuroticism**: You may experience more intense emotions. Mindfulness and stress management techniques could be helpful.")
        if extraversion < 12:
            insights.append("• **Low Extraversion**: You may prefer solitude. Ensure you maintain meaningful social connections for wellbeing.")
        if conscientiousness < 12:
            insights.append("• **Low Conscientiousness**: Building routines and structure may help improve your sense of control.")
        if neuroticism > 18 and extraversion < 15:
            insights.append("• **Pattern Alert**: The combination of higher neuroticism and lower extraversion is associated with increased vulnerability in research.")
        
        if insights:
            for insight in insights:
                st.markdown(insight)
        else:
            st.markdown("• Your personality profile shows a balanced pattern across traits.")
        
        # Recommendations
        st.markdown("#### 🌟 Recommendations")
        if risk_level == "High Risk":
            st.markdown("""
            - Consider speaking with a mental health professional
            - Practice stress management techniques (meditation, exercise)
            - Build and maintain social support networks
            - Monitor your mood and seek help if symptoms persist
            """)
        elif risk_level == "Medium Risk":
            st.markdown("""
            - Practice regular self-care and stress management
            - Stay connected with friends and family
            - Consider wellness apps for mood tracking
            - Be aware of early warning signs
            """)
        else:
            st.markdown("""
            - Continue your healthy habits
            - Maintain social connections
            - Stay physically active
            - Practice gratitude and mindfulness
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6B7280; font-size: 0.8rem;'>
    <p>Built with Streamlit | Model: Random Forest (96.6% accuracy)</p>
    <p>Capstone Project 2 | Jessica Paes | AI Tech Institute 2025</p>
</div>
""", unsafe_allow_html=True)

