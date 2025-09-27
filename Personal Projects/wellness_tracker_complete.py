# wellness_tracker_complete_au.py - Complete Australian Wellness Tracker

import streamlit as st           # Web app framework
import pandas as pd             # Data handling
import datetime                 # Date operations
import plotly.express as px     # Interactive charts
import plotly.graph_objects as go  # Advanced charts
import numpy as np              # Maths operations
import calendar                 # Calendar operations
import sqlite3                  # Database connection
import os                       # File operations

# Page configuration - trauma-informed design with calming colours
st.set_page_config(
    page_title="Wellness Tracker",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for brand-aligned, trauma-informed design
st.markdown("""
<style>
    .main { background-color: #f2f5e7; }
    
    .stSelectbox, .stSlider, .stTextInput, .stTextArea {
        margin-bottom: 1rem;
    }
    
    .section-header {
        background: linear-gradient(90deg, #f2f5e7, #0096c7);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #14213d;
    }
    
    .habit-streak {
        background: linear-gradient(45deg, #0096c7, #00496c);
        color: white;
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-card {
        background: white;
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid #0096c7;
    }
    .optional-section {
        background: #f2f5e7;
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 4px solid #ffe812;
    }
    
    .calendar-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0096c7 0%, #14213d 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.8rem;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'wellness_data' not in st.session_state:
    st.session_state.wellness_data = []

# Database setup (same as before but with Australian spelling)
@st.cache_resource
def init_database():
    """Initialise SQLite database and create table if it doesn't exist"""
    db_path = "wellness_tracker.db"
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wellness_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            tracking_reason TEXT,
            mood_rating INTEGER,
            safety_level INTEGER,
            energy_level INTEGER,
            sleep_hours REAL,
            water_intake REAL,
            social_connection TEXT,
            daily_win TEXT,
            quick_mode BOOLEAN,
            
            -- Physical wellness
            exercise_today TEXT,
            movement_type TEXT,
            sleep_quality INTEGER,
            bowel_frequency TEXT,
            bowel_quality TEXT,
            digestive_sounds TEXT,
            physical_symptoms TEXT,
            body_tension TEXT,
            
            -- Emotional & trauma responses
            stress_level INTEGER,
            patience_level INTEGER,
            trauma_responses TEXT,
            triggers_today TEXT,
            trigger_impact INTEGER,
            coping_strategies TEXT,
            
            -- Connection & support
            felt_supported TEXT,
            safe_people_time REAL,
            support_types TEXT,
            relationship_conflicts TEXT,
            
            -- Menstrual & hormonal health
            cycle_day INTEGER,
            period_status TEXT,
            hormonal_symptoms TEXT,
            on_birth_control TEXT,
            pill_day INTEGER,
            started_new_pack BOOLEAN,
            missed_pills TEXT,
            estimated_phase TEXT,
            period_pain INTEGER,
            
            -- Grounding & safety
            body_awareness TEXT,
            hypervigilance INTEGER,
            grounding_techniques TEXT,
            present_moment INTEGER,
            
            -- Growth & meaning
            mindfulness_minutes INTEGER,
            gratitude TEXT,
            self_compassion INTEGER,
            hope_level INTEGER,
            
            -- TCM indicators
            tongue_colour TEXT,
            tongue_coating TEXT,
            tongue_shape TEXT,
            qi_energy INTEGER,
            body_temperature TEXT,
            dampness_signs TEXT,
            emotional_element TEXT,
            
            notes TEXT,
            created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    return conn

def save_to_database(conn, entry_data):
    """Save wellness entry to database"""
    cursor = conn.cursor()
    
    # Create a comprehensive insert statement for all fields
    insert_sql = """
    INSERT INTO wellness_entries (
        date, tracking_reason, mood_rating, safety_level, energy_level,
        sleep_hours, water_intake, social_connection, daily_win, quick_mode,
        exercise_today, movement_type, sleep_quality, bowel_frequency, bowel_quality,
        digestive_sounds, physical_symptoms, body_tension, stress_level, patience_level,
        trauma_responses, triggers_today, trigger_impact, coping_strategies,
        felt_supported, safe_people_time, support_types, relationship_conflicts,
        cycle_day, period_status, hormonal_symptoms, on_birth_control, pill_day,
        started_new_pack, missed_pills, estimated_phase, period_pain,
        body_awareness, hypervigilance, grounding_techniques, present_moment,
        mindfulness_minutes, gratitude, self_compassion, hope_level,
        tongue_colour, tongue_coating, tongue_shape, qi_energy, body_temperature,
        dampness_signs, emotional_element, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    # Extract values with Australian spellings and defaults
    values = (
        entry_data.get('date'),
        entry_data.get('tracking_reason', ''),
        entry_data.get('mood_rating', 5),
        entry_data.get('safety_level', 5),
        entry_data.get('energy_level', 5),
        entry_data.get('sleep_hours', 8.0),
        entry_data.get('water_intake', 2.5),
        entry_data.get('social_connection', ''),
        entry_data.get('daily_win', ''),
        entry_data.get('quick_mode', False),
        entry_data.get('exercise_today', ''),
        str(entry_data.get('movement_type', [])),
        entry_data.get('sleep_quality', 5),
        entry_data.get('bowel_frequency', ''),
        entry_data.get('bowel_quality', ''),
        entry_data.get('digestive_sounds', ''),
        str(entry_data.get('physical_symptoms', [])),
        str(entry_data.get('body_tension', [])),
        entry_data.get('stress_level', 5),
        entry_data.get('patience_level', 5),
        str(entry_data.get('trauma_responses', [])),
        entry_data.get('triggers_today', ''),
        entry_data.get('trigger_impact', 0),
        str(entry_data.get('coping_strategies', [])),
        entry_data.get('felt_supported', ''),
        entry_data.get('safe_people_time', 0.0),
        str(entry_data.get('support_types', [])),
        entry_data.get('relationship_conflicts', ''),
        entry_data.get('cycle_day', 0),
        entry_data.get('period_status', ''),
        str(entry_data.get('hormonal_symptoms', [])),
        entry_data.get('on_birth_control', ''),
        entry_data.get('pill_day', 0),
        entry_data.get('started_new_pack', False),
        entry_data.get('missed_pills', ''),
        entry_data.get('estimated_phase', ''),
        entry_data.get('period_pain', 0),
        entry_data.get('body_awareness', ''),
        entry_data.get('hypervigilance', 5),
        str(entry_data.get('grounding_techniques', [])),
        entry_data.get('present_moment', 5),
        entry_data.get('mindfulness_minutes', 0),
        entry_data.get('gratitude', ''),
        entry_data.get('self_compassion', 5),
        entry_data.get('hope_level', 5),
        entry_data.get('tongue_colour', ''),
        entry_data.get('tongue_coating', ''),
        str(entry_data.get('tongue_shape', [])),
        entry_data.get('qi_energy', 5),
        entry_data.get('body_temperature', ''),
        str(entry_data.get('dampness_signs', [])),
        entry_data.get('emotional_element', ''),
        entry_data.get('notes', '')
    )
    
    cursor.execute(insert_sql, values)
    conn.commit()
    return cursor.lastrowid

def load_from_database(conn):
    """Load all wellness entries from database"""
    query = """
        SELECT * FROM wellness_entries 
        ORDER BY date DESC, created_timestamp DESC
    """
    return pd.read_sql_query(query, conn)

def check_existing_entry(conn, date):
    """Check if entry already exists for given date"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM wellness_entries WHERE date = ?", (date,))
    return cursor.fetchone() is not None

# Initialise database connection
conn = init_database()

# Welcome section - trauma-informed language
st.title("🌱 Your Complete Wellness Journey")
st.markdown("""
<div class="section-header">
    <h3>🌟 Daily Tracking + Visual Insights</h3>
    <p>Track your wellness patterns, view beautiful calendar insights, and understand your unique health journey</p>
</div>
""", unsafe_allow_html=True)

# Create main navigation tabs
tab1, tab2, tab3 = st.tabs(["📝 Daily Check-In", "🗓️ Calendar View", "📊 Analytics"])

# ===============================
# TAB 1: DAILY CHECK-IN (Complete Version)
# ===============================

with tab1:
    st.markdown("""
    <div class="section-header">
        <h3>📝 Your Daily Wellness Check-In</h3>
        <p>This is your safe space to track your wellness journey. Go at your own pace, 
        and remember - there are no right or wrong answers, only your truth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("daily_wellness_form"):
        # Main tracking reason - personalises the entire experience
        tracking_reason = st.selectbox(
            "🎯 What's your main reason for tracking wellness?",
            [
                "Select your primary focus...",
                "🌸 Hormonal changes (PMS, menopause, cycles)",
                "🧠 Trauma recovery & PTSD healing", 
                "😔 Depression & mood support",
                "😰 Anxiety & stress management",
                "⚡ ADHD & neurodivergence support",
                "🩺 Chronic illness management",
                "💊 Medication monitoring",
                "🌱 General wellness & self-care",
                "🔄 Life transitions & major changes"
            ],
            help="This helps personalise your tracking experience"
        )

        # Optional demographic info for relevant sections
        with st.expander("👤 Optional: Demographics (helps personalise your experience)"):
            gender = st.selectbox(
                "Gender (optional - helps show relevant health sections):",
                [
                    "Prefer not to say",
                    "Female", 
                    "Male",
                    "Non-binary",
                    "Transgender female",
                    "Transgender male",
                    "Other"
                ],
                help="Used only to show relevant health tracking sections (like menstrual cycle)"
            )

        # Date - Australian format DD/MM/YYYY
        selected_date = st.date_input(
            "📅 Today's date:", 
            datetime.date.today(),
            format="DD/MM/YYYY",
            help="Australian date format: day/month/year"
        )

        # Progress tracking motivation with personalised messaging
        if tracking_reason != "Select your primary focus...":
            reason_display = tracking_reason.split(" ", 1)[1]  # Remove emoji for cleaner display
            st.markdown(f"""
            <div class="habit-streak">
                <h3>🔥 Day 1 of Your {reason_display.title()} Journey</h3>
                <p><strong>You're taking charge of your {reason_display.lower()} - that's incredibly brave!</strong></p>
                <p>Daily consistency is the key to understanding your patterns and healing</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="habit-streak">
                <h3>🔥 Your Daily Wellness Journey</h3>
                <p><strong>You showed up today - that's what matters most!</strong></p>
                <p>Daily consistency beats perfection every time</p>
            </div>
            """, unsafe_allow_html=True)

        # Progress tracking
        quick_mode = st.checkbox("⚡ Quick Mode (5 minutes)", value=False, help="Just the essentials when you're short on time")
        
        if quick_mode:
            st.info("👍 Perfect! Consistency matters more than completeness. Let's do the essentials!")
        else:
            st.success("🌟 Full check-in mode - you're investing in your healing today!")

        st.markdown("---")

        # ===============================
        # CORE ESSENTIALS (Always visible)
        # ===============================

        st.markdown("""
        <div class="section-card">
            <h3>🎯 Daily Essentials (Required - 2 minutes)</h3>
            <p>These 6 questions are the foundation of your healing. Never skip these!</p>
        </div>
        """, unsafe_allow_html=True)

        # The Big 3 - most predictive of wellbeing
        col1, col2, col3 = st.columns(3)

        with col1:
            mood_rating = st.slider(
                "Overall Mood Today",
                min_value=1, max_value=10, value=5, step=1,
                help="Your emotional state - the foundation metric"
            )

        with col2:
            safety_level = st.slider(
                "Safety in Your Body",
                min_value=1, max_value=10, value=5, step=1,
                help="Core trauma recovery metric - how safe you felt"
            )

        with col3:
            energy_level = st.slider(
                "Physical Energy",
                min_value=1, max_value=10, value=5, step=1,
                help="Your body's energy and vitality"
            )

        # Essential daily habits
        habits_col1, habits_col2 = st.columns(2)

        with habits_col1:
            sleep_hours = st.number_input(
                "Sleep Hours Last Night:",
                min_value=0.0, max_value=24.0, value=8.0, step=0.5,
                help="Quality sleep is crucial for trauma recovery"
            )
            
            water_intake = st.number_input(
                "Water Intake (litres):",
                min_value=0.0, max_value=6.0, value=2.5, step=0.25,
                help="Aim for 2-3L daily - hydration affects nervous system regulation"
            )

        with habits_col2:
            social_connection = st.selectbox(
                "Social Connection Quality Today:",
                [
                    "Select an option...",
                    "Deep, meaningful connections",
                    "Good interactions - felt heard",
                    "Surface-level interactions only",
                    "Minimal social contact",
                    "Completely isolated"
                ],
                help="Relationships are medicine for trauma survivors"
            )
            
            # Quick win celebration
            daily_win = st.text_input(
                "One thing you accomplished today:",
                placeholder="Made brekkie, had a shower, sent a text, got out of bed...",
                help="In healing, EVERYTHING counts as an accomplishment!"
            )

        # Immediate feedback on essentials
        if mood_rating >= 7 and safety_level >= 7:
            st.success("🌟 Excellent! Your core metrics look strong today!")
        elif mood_rating <= 3 or safety_level <= 3:
            st.info("💙 Thank you for being honest. Difficult days are part of the healing journey.")

        if daily_win:
            st.success(f"🎉 Celebrating: {daily_win} - You showed up for yourself today!")

        st.markdown("---")

        # ===============================
        # CONDITIONAL SECTIONS (Based on mode/responses)
        # ===============================

        if not quick_mode:
            # Safety & Grounding (Show for trauma, anxiety, or low safety scores)
            show_safety = (
                safety_level <= 5 or 
                "trauma" in tracking_reason.lower() or 
                "anxiety" in tracking_reason.lower()
            )
            
            # Always show as expandable section, auto-expand if conditions met
            with st.expander("🛡️ Safety & Grounding", expanded=show_safety):
                st.markdown("""
                <div class="section-card">
                    <h3>🛡️ Safety & Grounding</h3>
                    <p>Your nervous system needs extra attention today</p>
                </div>
                """, unsafe_allow_html=True)
                
                grounding_col1, grounding_col2 = st.columns(2)
                
                with grounding_col1:
                    body_awareness = st.selectbox(
                        "Connection to your body today:",
                        [
                            "Select...",
                            "Felt connected and aware",
                            "Somewhat connected",
                            "Disconnected or numb",
                            "Very dissociated"
                        ]
                    )
                    
                    hypervigilance = st.slider(
                        "Scanning for threats/danger:",
                        min_value=1, max_value=10, value=5, step=1,
                        help="1 = Relaxed, 10 = Constantly on alert"
                    )
                
                with grounding_col2:
                    grounding_techniques = st.multiselect(
                        "Grounding techniques used:",
                        [
                            "5-4-3-2-1 sensory technique",
                            "Deep breathing/box breathing", 
                            "Cold water on face/hands",
                            "Progressive muscle relaxation",
                            "Mindful movement/stretching", 
                            "Time in nature",
                            "Hold ice cube/cold object",
                            "Stomp feet/feel ground connection",
                            "Count backwards from 100 by 7s",
                            "Name items in categories",
                            "Self-talk (name, place, date)",
                            "Touch different textures",
                            "Essential oils/calming scents",
                            "Warm then cold water on hands",
                            "Mindful eating (mint, lemon)",
                            "Physical movement/exercise",
                            "Grounding phrases/affirmations",
                            "None today"
                        ]
                    )
                    
                    present_moment = st.slider(
                        "How present/grounded:",
                        min_value=1, max_value=10, value=5, step=1
                    )
            
            # Physical Wellness (Show for chronic illness, ADHD, hormonal, or low energy)
            show_physical = (
                energy_level <= 4 or
                "chronic illness" in tracking_reason.lower() or
                "adhd" in tracking_reason.lower() or
                "hormonal" in tracking_reason.lower()
            )
            
            # Always show as expandable section, auto-expand if conditions met
            with st.expander("💪 Physical Wellness", expanded=show_physical):
                st.markdown("""
                <div class="section-card">
                    <h3>💪 Physical Wellness</h3>
                    <p>The body keeps the score - let's listen to what it's saying</p>
                </div>
                """, unsafe_allow_html=True)
                
                physical_col1, physical_col2 = st.columns(2)
                
                with physical_col1:
                    exercise_today = st.radio(
                        "Movement today:",
                        ["Yes", "A little", "No"],
                        help="Any movement counts!"
                    )
                    
                    movement_type = []
                    if exercise_today != "No":
                        movement_type = st.multiselect(
                            "Types of movement:",
                            [
                                "Walking", "Yoga", "Stretching", "Dancing",
                                "Running", "Strength training", "Sports",
                                "Cleaning/housework", "Playing with pets"
                            ]
                        )
                    
                    sleep_quality = st.slider(
                        "Sleep quality (1-10):",
                        min_value=1, max_value=10, value=5, step=1
                    )
                    
                    # Bowel movement tracking (important for all conditions)
                    bowel_frequency = st.selectbox(
                        "Bowel movements today:",
                        ["0", "1", "2", "3", "4+"],
                        help="Digestive health reflects overall wellness and affects mood/energy"
                    )
                    
                    bowel_quality = st.selectbox(
                        "Stool consistency (Bristol Scale):",
                        [
                            "Select...",
                            "Type 1: Hard lumps (severe constipation)",
                            "Type 2: Lumpy sausage (mild constipation)", 
                            "Type 3: Sausage with cracks (normal-dry)",
                            "Type 4: Smooth sausage (ideal)",
                            "Type 5: Soft blobs (lacking fibre)",
                            "Type 6: Mushy (mild diarrhoea)",
                            "Type 7: Liquid (diarrhoea)"
                        ],
                        help="Bristol Stool Chart is used medically to assess digestive health"
                    )
                
                with physical_col2:
                    # Digestive sounds (often overlooked but important)
                    digestive_sounds = st.selectbox(
                        "Digestive sounds/rumbling today:",
                        [
                            "Select...",
                            "Normal occasional rumbles when hungry",
                            "Very quiet/no sounds noticed", 
                            "Frequent loud rumbling throughout day",
                            "Excessive gurgling after meals",
                            "Rumbling increases when anxious/stressed",
                            "Embarrassingly loud in quiet situations",
                            "Didn't pay attention to this"
                        ],
                        help="Gut sounds reflect digestion, stress levels, and nervous system activity"
                    )
                    
                    physical_symptoms = st.multiselect(
                        "Physical symptoms noticed:",
                        [
                            "Headaches", "Muscle tension", "Fatigue",
                            "Digestive issues", "Heart racing", 
                            "Shortness of breath", "None today"
                        ]
                    )
                    
                    body_tension = st.multiselect(
                        "Where did you feel tension:",
                        [
                            "Neck", "Shoulders", "Jaw", "Back",
                            "Stomach", "Chest", "Everywhere", "None"
                        ]
                    )
            
            # Emotional & Trauma Responses (Show for depression, trauma, anxiety, or low mood)
            show_emotional = (
                mood_rating <= 4 or
                "depression" in tracking_reason.lower() or
                "trauma" in tracking_reason.lower() or
                "anxiety" in tracking_reason.lower()
            )
            
            # Always show as expandable section, auto-expand if conditions met
            with st.expander("💙 Emotional & Trauma Responses", expanded=show_emotional):
                st.markdown("""
                <div class="section-card">
                    <h3>💙 Emotional & Trauma Responses</h3>
                    <p>Your emotions are information, not problems to fix</p>
                </div>
                """, unsafe_allow_html=True)
                
                emotional_col1, emotional_col2 = st.columns(2)
                
                with emotional_col1:
                    stress_level = st.slider(
                        "Stress level:",
                        min_value=1, max_value=10, value=5, step=1
                    )
                    
                    patience_level = st.slider(
                        "How patient were you today (with yourself and others)?",
                        min_value=1, max_value=10, value=5, step=1,
                        help="1 = Very impatient/irritable, 10 = Very patient and understanding"
                    )
                    
                    trauma_responses = st.multiselect(
                        "Trauma responses noticed:",
                        [
                            "Flashbacks/intrusive thoughts", "Hypervigilance",
                            "Dissociation", "Emotional numbness", 
                            "Intense anger", "Panic/anxiety", "PTSD symptoms", "None today"
                        ]
                    )
                
                with emotional_col2:
                    triggers_today = st.radio(
                        "Emotional triggers encountered:",
                        ["Yes", "Maybe", "No"]
                    )
                    
                    trigger_impact = 0
                    if triggers_today == "Yes":
                        trigger_impact = st.slider(
                            "How much did triggers affect you:",
                            min_value=1, max_value=10, value=5, step=1
                        )
                    
                    coping_strategies = st.multiselect(
                        "Healthy coping used:",
                        [
                            "Talked to someone", "Deep breathing",
                            "Journaling", "Creative expression",
                            "Time in nature", "Meditation", "None"
                        ]
                    )
            
            # Connection & Support (expand if isolated or for depression/trauma)
            show_connection = (
                "isolated" in social_connection.lower() or
                "depression" in tracking_reason.lower() or
                "trauma" in tracking_reason.lower()
            )
            
            # Always show as expandable section, auto-expand if conditions met
            with st.expander("🤗 Connection & Support", expanded=show_connection):
                st.markdown("""
                <div class="section-card">
                    <h3>🤗 Connection & Support</h3>
                    <p>Healing happens in relationship - every connection matters</p>
                </div>
                """, unsafe_allow_html=True)
                
                support_col1, support_col2 = st.columns(2)
                
                with support_col1:
                    felt_supported = st.radio(
                        "Felt supported today:",
                        [
                            "Yes, deeply supported",
                            "Somewhat supported",
                            "A little supported", 
                            "Not really supported",
                            "Completely alone"
                        ]
                    )
                    
                    safe_people_time = st.number_input(
                        "Time with safe people (hours):",
                        min_value=0.0, max_value=24.0, value=0.0, step=0.25,
                        help="Includes family, friends, therapists, support groups, pets"
                    )
                
                with support_col2:
                    support_types = st.multiselect(
                        "Support received:",
                        [
                            "Emotional support", "Physical comfort",
                            "Practical help", "Professional support",
                            "Pet companionship", "Online community",
                            "None today"
                        ]
                    )
                    
                    relationship_conflicts = st.selectbox(
                        "Relationship conflicts:",
                        [
                            "Select...",
                            "None - peaceful day",
                            "Minor disagreement",
                            "Moderate conflict",
                            "Major argument",
                            "Felt unsafe with someone"
                        ]
                    )
            
            # Menstrual & Hormonal Health (conditional based on gender, tracking reason, or user choice)
            show_menstrual = (
                "hormonal" in tracking_reason.lower() or
                gender in ["Female", "Transgender female", "Non-binary"]
            )
            
            # Always show as expandable section, auto-expand if conditions met
            with st.expander("🌸 Menstrual Cycle Tracking", expanded=show_menstrual):
                st.markdown("""
                <div class="section-card">
                    <h3>🌸 Menstrual & Hormonal Health</h3>
                    <p>Hormones affect everything: mood, energy, pain, digestion, sleep, and mental clarity</p>
                </div>
                """, unsafe_allow_html=True)
                
                menstrual_col1, menstrual_col2 = st.columns(2)
                
                with menstrual_col1:
                    # Basic cycle tracking
                    cycle_day = st.number_input(
                        "What day of your cycle? (Day 1 = first day of period):",
                        min_value=1, max_value=50, value=1, step=1,
                        help="Day 1 = first day of menstrual bleeding. Average cycle is 28 days."
                    )
                    
                    period_status = st.selectbox(
                        "Period status today:",
                        [
                            "Select...",
                            "Heavy flow (changing pad/tampon every 1-2 hours)",
                            "Medium flow (changing every 3-4 hours)", 
                            "Light flow (changing every 4-6 hours)",
                            "Spotting (very light bleeding)",
                            "No bleeding today",
                            "PMS symptoms (before period)",
                            "Ovulation signs (mid-cycle)",
                            "Post-period recovery"
                        ],
                        help="Track flow intensity and cycle phase"
                    )
                    
                    # Hormonal symptoms
                    hormonal_symptoms = st.multiselect(
                        "Hormonal symptoms today:",
                        [
                            "Breast tenderness", "Bloating/water retention", 
                            "Menstrual cramps", "Lower back pain",
                            "Mood swings", "Food cravings", "Acne breakouts",
                            "Headaches/migraines", "Fatigue", "Irritability",
                            "Hot flushes", "Night sweats", "None today"
                        ],
                        help="Symptoms that may relate to your menstrual cycle"
                    )
                
                with menstrual_col2:
                    # Birth control tracking
                    on_birth_control = st.radio(
                        "Are you on hormonal birth control?",
                        ["Yes", "No", "Prefer not to say"],
                        help="Helps understand if symptoms are natural cycle or medication-related"
                    )
                    
                    pill_day = 0
                    started_new_pack = False
                    missed_pills = "No missed pills"
                    
                    if on_birth_control == "Yes":
                        pill_day = st.number_input(
                            "What day of your birth control pack?",
                            min_value=1, max_value=28, value=1, step=1,
                            help="Day 1 = first active pill of new pack"
                        )
                        
                        started_new_pack = st.checkbox(
                            "Started new pack today?",
                            help="Track when you begin a new contraceptive pill pack"
                        )
                        
                        missed_pills = st.selectbox(
                            "Missed any pills recently?",
                            [
                                "No missed pills",
                                "Missed 1 pill this week",
                                "Missed 2-3 pills this week", 
                                "Missed more than 3 pills",
                                "Irregular pill timing"
                            ],
                            help="Missed pills can affect mood, cycle, and effectiveness"
                        )
                    
                    # Cycle phase estimation (helpful for pattern recognition)
                    # Auto-calculate based on cycle day
                    def get_cycle_phase(cycle_day):
                        if 1 <= cycle_day <= 5:
                            return "Menstrual phase (Days 1-5)"
                        elif 6 <= cycle_day <= 13:
                            return "Follicular phase (Days 6-13)"
                        elif 14 <= cycle_day <= 16:
                            return "Ovulatory phase (Days 14-16)"
                        elif 17 <= cycle_day <= 28:
                            return "Luteal phase (Days 17-28)"
                        else:
                            return "Extended cycle/Irregular"
                    
                    # Get the calculated phase as default
                    calculated_phase = get_cycle_phase(cycle_day)
                    
                    phase_options = [
                        "Menstrual phase (Days 1-5)",
                        "Follicular phase (Days 6-13)", 
                        "Ovulatory phase (Days 14-16)",
                        "Luteal phase (Days 17-28)",
                        "Extended cycle/Irregular",
                        "Post-menopausal",
                        "Perimenopausal"
                    ]
                    
                    # Find index of calculated phase, default to 0 if not found
                    try:
                        default_index = phase_options.index(calculated_phase)
                    except ValueError:
                        default_index = 4  # Extended cycle/Irregular
                    
                    estimated_phase = st.selectbox(
                        "Estimated cycle phase:",
                        phase_options,
                        index=default_index,
                        help="Auto-calculated based on cycle day - you can adjust if needed"
                    )
                    
                    # Period pain level
                    period_pain = st.slider(
                        "Period-related pain level today:",
                        min_value=0, max_value=10, value=0, step=1,
                        help="0 = No pain, 10 = Severe pain requiring medical attention"
                    )

        # ===============================
        # OPTIONAL GROWTH SECTIONS
        # ===============================

        with st.expander("🌱 Optional: Growth & Meaning (when you have extra energy)"):
            st.markdown("""
            <div class="optional-section">
                <h4>🧘‍♀️ Mindfulness & Growth</h4>
                <p>These are bonus questions for when you're feeling strong</p>
            </div>
            """, unsafe_allow_html=True)
            
            growth_col1, growth_col2 = st.columns(2)
            
            with growth_col1:
                mindfulness_minutes = st.number_input(
                    "Mindfulness/meditation (minutes):",
                    min_value=0, max_value=120, value=0, step=1
                )
                
                gratitude = st.text_area(
                    "What are you grateful for today:",
                    placeholder="Small moments count: a cuppa, a kind text, sunshine...",
                    height=80
                )
            
            with growth_col2:
                self_compassion = st.slider(
                    "How kind to yourself (1-10):",
                    min_value=1, max_value=10, value=5, step=1
                )
                
                hope_level = st.slider(
                    "Hope for the future:",
                    min_value=1, max_value=10, value=5, step=1
                )

        # ===============================
        # TRADITIONAL CHINESE MEDICINE INDICATORS
        # ===============================

        with st.expander("🉐 Traditional Chinese Medicine Insights (optional but valuable)"):
            st.markdown("""
            <div class="optional-section">
                <h4>🌸 TCM Daily Assessment</h4>
                <p>Traditional Chinese Medicine looks at subtle patterns that reveal deeper health insights</p>
            </div>
            """, unsafe_allow_html=True)
            
            tcm_col1, tcm_col2 = st.columns(2)
            
            with tcm_col1:
                # Tongue observation (mirror of internal health)
                tongue_colour = st.selectbox(
                    "Tongue colour this morning:",
                    [
                        "Select...",
                        "Healthy pink",
                        "Pale (possible Qi/blood deficiency)",
                        "Red (heat/inflammation in body)",
                        "Purple (blood/Qi stagnation, cold)",
                        "Dark red (excess heat)"
                    ],
                    help="Check tongue in morning before eating/drinking - reflects internal organ health"
                )
                
                tongue_coating = st.selectbox(
                    "Tongue coating:",
                    [
                        "Select...",
                        "Thin white (healthy)",
                        "Thick white (dampness/cold)",
                        "Yellow coating (heat/inflammation)",
                        "No coating (Yin deficiency)",
                        "Greasy/thick (excess dampness)"
                    ],
                    help="Coating reflects digestive health and internal dampness/heat"
                )
                
                tongue_shape = st.multiselect(
                    "Tongue characteristics:",
                    [
                        "Normal size/shape",
                        "Swollen/puffy (Qi deficiency)",
                        "Teeth marks on sides (Spleen weakness)",
                        "Cracks/fissures (Yin deficiency)",
                        "Thin/narrow (blood deficiency)",
                        "Pointed/tense sides (stress/Liver Qi stagnation)"
                    ],
                    help="Shape reveals constitutional patterns and organ function"
                )
            
            with tcm_col2:
                # Energy and constitutional patterns
                qi_energy = st.slider(
                    "Qi (life energy) level:",
                    min_value=1, max_value=10, value=5, step=1,
                    help="1 = Completely depleted, 10 = Vibrant life force energy"
                )
                
                body_temperature = st.selectbox(
                    "Body temperature tendency today:",
                    [
                        "Select...",
                        "Balanced/normal",
                        "Running cold (Yang deficiency)",
                        "Running hot (Yin deficiency/heat)",
                        "Cold hands/feet, warm body",
                        "Hot flashes/cold spells"
                    ],
                    help="Temperature patterns reveal Yang (warming) vs Yin (cooling) balance"
                )
                
                dampness_signs = st.multiselect(
                    "Signs of dampness (poor fluid metabolism):",
                    [
                        "Feeling heavy/sluggish",
                        "Bloating after meals",
                        "Sticky/sweet taste in mouth",
                        "Excessive mucus/phlegm",
                        "Foggy thinking",
                        "Swollen ankles/puffiness",
                        "Loose stools",
                        "None noticed"
                    ],
                    help="Dampness = sluggish metabolism of fluids, common in modern lifestyle"
                )
                
                emotional_element = st.selectbox(
                    "Dominant emotion/element today:",
                    [
                        "Select...",
                        "Balanced/centred",
                        "Worry/overthinking (Earth/Spleen)",
                        "Anger/frustration (Wood/Liver)",
                        "Joy/overexcitement (Fire/Heart)",
                        "Sadness/grief (Metal/Lung)",
                        "Fear/anxiety (Water/Kidney)"
                    ],
                    help="Five Element theory: emotions reflect organ energy imbalances"
                )

        # Additional notes
        notes = st.text_area(
            "📝 Additional notes (optional):",
            placeholder="Anything else you'd like to record about today...",
            height=100
        )

        st.markdown("---")

        # ===============================
        # SUBMIT BUTTON & DATA PROCESSING
        # ===============================

        submitted = st.form_submit_button(
            "💾 Save Today's Data",
            type="primary",
            use_container_width=True
        )
        
        if submitted:
            # Create comprehensive data entry
            entry = {
                'date': selected_date,
                'tracking_reason': tracking_reason,
                'mood_rating': mood_rating,
                'safety_level': safety_level,
                'energy_level': energy_level,
                'sleep_hours': sleep_hours,
                'water_intake': water_intake,
                'social_connection': social_connection,
                'daily_win': daily_win,
                'quick_mode': quick_mode,
                'notes': notes
            }
            
            # Add conditional fields based on what was shown
            if not quick_mode:
                if 'show_safety' in locals() and show_safety:
                    entry.update({
                        'body_awareness': body_awareness,
                        'hypervigilance': hypervigilance,
                        'grounding_techniques': grounding_techniques,
                        'present_moment': present_moment
                    })
                
                if 'show_physical' in locals() and show_physical:
                    entry.update({
                        'exercise_today': exercise_today,
                        'movement_type': movement_type,
                        'sleep_quality': sleep_quality,
                        'bowel_frequency': bowel_frequency,
                        'bowel_quality': bowel_quality,
                        'digestive_sounds': digestive_sounds,
                        'physical_symptoms': physical_symptoms,
                        'body_tension': body_tension
                    })
                
                if 'show_emotional' in locals() and show_emotional:
                    entry.update({
                        'stress_level': stress_level,
                        'patience_level': patience_level,
                        'trauma_responses': trauma_responses,
                        'triggers_today': triggers_today,
                        'trigger_impact': trigger_impact,
                        'coping_strategies': coping_strategies
                    })
                
                if 'show_connection' in locals() and show_connection:
                    entry.update({
                        'felt_supported': felt_supported,
                        'safe_people_time': safe_people_time,
                        'support_types': support_types,
                        'relationship_conflicts': relationship_conflicts
                    })
                
                if 'show_menstrual' in locals() and show_menstrual:
                    entry.update({
                        'cycle_day': cycle_day,
                        'period_status': period_status,
                        'hormonal_symptoms': hormonal_symptoms,
                        'on_birth_control': on_birth_control,
                        'pill_day': pill_day,
                        'started_new_pack': started_new_pack,
                        'missed_pills': missed_pills,
                        'estimated_phase': estimated_phase,
                        'period_pain': period_pain
                    })
                
                # Growth & meaning
                entry.update({
                    'mindfulness_minutes': mindfulness_minutes,
                    'gratitude': gratitude,
                    'self_compassion': self_compassion,
                    'hope_level': hope_level
                })
                
                # TCM
                entry.update({
                    'tongue_colour': tongue_colour,
                    'tongue_coating': tongue_coating,
                    'tongue_shape': tongue_shape,
                    'qi_energy': qi_energy,
                    'body_temperature': body_temperature,
                    'dampness_signs': dampness_signs,
                    'emotional_element': emotional_element
                })
            
            try:
                # Save to database
                entry_id = save_to_database(conn, entry)
                
                st.success(f"✅ Entry #{entry_id} saved successfully for {selected_date.strftime('%d/%m/%Y')}!")
                st.balloons()
                
                # Show summary
                with st.expander("📋 View saved data summary"):
                    summary_data = {
                        'Date': selected_date.strftime('%d/%m/%Y'),
                        'Mood': f"{mood_rating}/10",
                        'Safety': f"{safety_level}/10",
                        'Energy': f"{energy_level}/10",
                        'Sleep': f"{sleep_hours}h",
                        'Water': f"{water_intake}L",
                        'Daily Win': daily_win or "None recorded"
                    }
                    
                    for key, value in summary_data.items():
                        st.write(f"**{key}:** {value}")
                        
            except Exception as e:
                st.error(f"❌ Error saving to database: {str(e)}")

# ===============================
# TAB 2: CALENDAR VIEW
# ===============================

with tab2:
    st.markdown("## 🗓️ Calendar View")
    
    try:
        df = load_from_database(conn)
        
        if df.empty:
            st.info("📅 No data yet! Complete your first daily check-in to see your calendar.")
        else:
            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            
            # Calendar controls
            calendar_col1, calendar_col2 = st.columns(2)
            
            with calendar_col1:
                current_date = datetime.date.today()
                selected_month = st.selectbox(
                    "Select Month:",
                    options=list(range(1, 13)),
                    index=current_date.month - 1,
                    format_func=lambda x: calendar.month_name[x]
                )
                
            with calendar_col2:
                available_years = sorted(df['date'].dt.year.unique())
                if available_years:
                    default_year_idx = available_years.index(current_date.year) if current_date.year in available_years else 0
                    selected_year = st.selectbox("Select Year:", available_years, index=default_year_idx)
                else:
                    selected_year = current_date.year
            
            # Filter data for selected month/year
            month_data = df[
                (df['date'].dt.month == selected_month) & 
                (df['date'].dt.year == selected_year)
            ]
            
            if month_data.empty:
                st.warning(f"No data for {calendar.month_name[selected_month]} {selected_year}")
            else:
                # Create calendar heatmap
                st.markdown(f"### {calendar.month_name[selected_month]} {selected_year} Overview")
                
                # Calendar visualization
                cal = calendar.monthcalendar(selected_year, selected_month)
                
                calendar_fig = go.Figure()
                
                days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                
                for week_num, week in enumerate(cal):
                    for day_num, day in enumerate(week):
                        if day == 0:  # Empty cell in calendar
                            continue
                        
                        # Find data for this day
                        day_date = datetime.date(selected_year, selected_month, day)
                        day_data = month_data[month_data['date'].dt.date == day_date]
                        
                        if not day_data.empty:
                            mood_value = day_data['mood_rating'].iloc[0]
                            energy_value = day_data['energy_level'].iloc[0]
                            safety_value = day_data['safety_level'].iloc[0]
                            
                            # Create average for colour
                            avg_wellness = (mood_value + energy_value + safety_value) / 3
                            
                            # Colour based on wellness (green = good, red = poor)
                            if avg_wellness >= 7:
                                colour = "rgba(76, 175, 80, 0.8)"  # Green
                            elif avg_wellness >= 5:
                                colour = "rgba(255, 193, 7, 0.8)"  # Yellow
                            else:
                                colour = "rgba(244, 67, 54, 0.8)"  # Red
                            
                            hover_text = f"Date: {day_date.strftime('%d/%m/%Y')}<br>Mood: {mood_value}/10<br>Energy: {energy_value}/10<br>Safety: {safety_value}/10"
                        else:
                            avg_wellness = 0
                            colour = "rgba(200, 200, 200, 0.3)"
                            hover_text = f"Date: {day_date.strftime('%d/%m/%Y')}<br>No data"
                        
                        calendar_fig.add_trace(go.Scatter(
                            x=[day_num],
                            y=[6-week_num],  # Flip Y axis
                            mode='markers+text',
                            marker=dict(
                                size=50,
                                color=colour,
                                line=dict(width=2, color='white')
                            ),
                            text=str(day),
                            textposition="middle center",
                            textfont=dict(size=14, color='white', family="Arial Black"),
                            hovertemplate=hover_text + "<extra></extra>",
                            showlegend=False
                        ))
                
                # Update calendar layout
                calendar_fig.update_layout(
                    title=f"Wellness Calendar - {calendar.month_name[selected_month]} {selected_year}",
                    xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(7)),
                        ticktext=days_of_week,
                        showgrid=False
                    ),
                    yaxis=dict(showgrid=False, showticklabels=False),
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white'
                )
                
                st.plotly_chart(calendar_fig, use_container_width=True)
                
                # Monthly summary
                st.markdown("### 📈 Monthly Summary")
                summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
                
                with summary_col1:
                    avg_mood = month_data['mood_rating'].mean()
                    st.metric("Average Mood", f"{avg_mood:.1f}/10")
                
                with summary_col2:
                    avg_energy = month_data['energy_level'].mean()
                    st.metric("Average Energy", f"{avg_energy:.1f}/10")
                
                with summary_col3:
                    total_entries = len(month_data)
                    st.metric("Days Tracked", total_entries)
                
                with summary_col4:
                    avg_sleep = month_data['sleep_hours'].mean()
                    st.metric("Average Sleep", f"{avg_sleep:.1f}h")
                
                # Daily breakdown
                st.markdown("### 📊 Daily Breakdown")
                display_data = month_data[['date', 'mood_rating', 'energy_level', 'safety_level', 'sleep_hours', 'daily_win']].copy()
                display_data['date'] = display_data['date'].dt.strftime('%d/%m/%Y')
                display_data.columns = ['Date', 'Mood', 'Energy', 'Safety', 'Sleep (h)', 'Daily Win']
                st.dataframe(display_data, use_container_width=True, hide_index=True)
                
    except Exception as e:
        st.error(f"Error loading calendar data: {str(e)}")

# ===============================
# TAB 3: ANALYTICS
# ===============================

with tab3:
    st.markdown("## 📊 Analytics & Insights")
    
    try:
        df = load_from_database(conn)
        
        if df.empty:
            st.info("📊 No data to analyse yet! Complete a few daily check-ins to see insights.")
        else:
            df['date'] = pd.to_datetime(df['date'])
            
            # Analytics selection
            analytics_option = st.selectbox(
                "Choose Analysis:",
                ["Overview Dashboard", "Mood Trends", "Sleep Analysis", "Energy Patterns", "Correlation Matrix", "Menstrual Cycle Insights"]
            )
            
            if analytics_option == "Overview Dashboard":
                # Key metrics
                st.markdown("### 📈 Key Metrics")
                
                metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                
                with metrics_col1:
                    total_entries = len(df)
                    st.metric("Total Entries", total_entries)
                
                with metrics_col2:
                    avg_mood = df['mood_rating'].mean()
                    st.metric("Average Mood", f"{avg_mood:.1f}/10")
                
                with metrics_col3:
                    streak_days = (datetime.date.today() - df['date'].max().date()).days
                    st.metric("Days Since Last Entry", streak_days)
                
                with metrics_col4:
                    avg_sleep = df['sleep_hours'].mean()
                    st.metric("Average Sleep", f"{avg_sleep:.1f}h")
                
                # Recent trends
                if len(df) >= 7:
                    st.markdown("### 📊 Recent Trends (Last 7 Entries)")
                    
                    recent_data = df.head(7).sort_values('date')
                    
                    trend_fig = go.Figure()
                    
                    trend_fig.add_trace(go.Scatter(
                        x=recent_data['date'],
                        y=recent_data['mood_rating'],
                        mode='lines+markers',
                        name='Mood',
                        line=dict(color='blue', width=3)
                    ))
                    
                    trend_fig.add_trace(go.Scatter(
                        x=recent_data['date'],
                        y=recent_data['energy_level'],
                        mode='lines+markers',
                        name='Energy',
                        line=dict(color='green', width=3)
                    ))
                    
                    trend_fig.add_trace(go.Scatter(
                        x=recent_data['date'],
                        y=recent_data['safety_level'],
                        mode='lines+markers',
                        name='Safety',
                        line=dict(color='orange', width=3)
                    ))
                    
                    trend_fig.update_layout(
                        title='Recent Wellness Trends',
                        xaxis_title='Date',
                        yaxis_title='Rating (1-10)',
                        height=400
                    )
                    
                    st.plotly_chart(trend_fig, use_container_width=True)
            
            elif analytics_option == "Mood Trends":
                # Mood over time
                mood_fig = px.line(
                    df.sort_values('date'), 
                    x='date', 
                    y='mood_rating',
                    title='Mood Trends Over Time',
                    labels={'mood_rating': 'Mood Rating (1-10)', 'date': 'Date'}
                )
                mood_fig.update_traces(line_color='#0096c7', line_width=3)
                mood_fig.update_xaxis(tickformat='%d/%m/%Y')
                st.plotly_chart(mood_fig, use_container_width=True)
                
                # Mood distribution
                mood_hist = px.histogram(
                    df, 
                    x='mood_rating', 
                    title='Mood Distribution',
                    nbins=10,
                    labels={'mood_rating': 'Mood Rating', 'count': 'Frequency'}
                )
                st.plotly_chart(mood_hist, use_container_width=True)
            
            elif analytics_option == "Sleep Analysis":
                # Sleep vs mood correlation
                sleep_mood_fig = px.scatter(
                    df, 
                    x='sleep_hours', 
                    y='mood_rating',
                    title='Sleep Hours vs Mood Rating',
                    trendline='ols',
                    labels={'sleep_hours': 'Sleep Hours', 'mood_rating': 'Mood Rating'}
                )
                st.plotly_chart(sleep_mood_fig, use_container_width=True)
                
                # Sleep quality over time (if available)
                if 'sleep_quality' in df.columns and df['sleep_quality'].notna().any():
                    sleep_quality_fig = px.line(
                        df.dropna(subset=['sleep_quality']).sort_values('date'),
                        x='date',
                        y='sleep_quality',
                        title='Sleep Quality Over Time'
                    )
                    sleep_quality_fig.update_xaxis(tickformat='%d/%m/%Y')
                    st.plotly_chart(sleep_quality_fig, use_container_width=True)
            
            elif analytics_option == "Energy Patterns":
                # Energy over time
                energy_fig = px.line(
                    df.sort_values('date'), 
                    x='date', 
                    y='energy_level',
                    title='Energy Levels Over Time'
                )
                energy_fig.update_traces(line_color='green', line_width=3)
                energy_fig.update_xaxis(tickformat='%d/%m/%Y')
                st.plotly_chart(energy_fig, use_container_width=True)
                
                # Energy vs other factors
                if len(df) > 10:
                    energy_factors_fig = go.Figure()
                    
                    energy_factors_fig.add_trace(go.Scatter(
                        x=df['water_intake'],
                        y=df['energy_level'],
                        mode='markers',
                        name='Water Intake vs Energy',
                        text=df['date'].dt.strftime('%d/%m/%Y'),
                        hovertemplate='Water: %{x}L<br>Energy: %{y}/10<br>Date: %{text}<extra></extra>'
                    ))
                    
                    energy_factors_fig.update_layout(
                        title='Energy vs Water Intake',
                        xaxis_title='Water Intake (L)',
                        yaxis_title='Energy Level (1-10)'
                    )
                    
                    st.plotly_chart(energy_factors_fig, use_container_width=True)
            
            elif analytics_option == "Correlation Matrix":
                # Correlation between numeric variables
                numeric_cols = ['mood_rating', 'safety_level', 'energy_level', 'sleep_hours', 'water_intake']
                
                # Add conditional columns if they exist and have data
                if 'sleep_quality' in df.columns:
                    numeric_cols.append('sleep_quality')
                if 'stress_level' in df.columns:
                    numeric_cols.append('stress_level')
                if 'patience_level' in df.columns:
                    numeric_cols.append('patience_level')
                
                available_cols = [col for col in numeric_cols if col in df.columns and df[col].notna().any()]
                
                if len(available_cols) >= 2:
                    corr_data = df[available_cols].corr()
                    
                    corr_fig = px.imshow(
                        corr_data,
                        title='Wellness Metrics Correlation Matrix',
                        color_continuous_scale='RdBu_r',
                        aspect='auto'
                    )
                    st.plotly_chart(corr_fig, use_container_width=True)
                    
                    # Correlation insights
                    st.markdown("### 🔍 Correlation Insights")
                    
                    strongest_corr = corr_data.abs().unstack().sort_values(ascending=False)
                    # Remove self-correlations
                    strongest_corr = strongest_corr[strongest_corr < 1.0]
                    
                    if len(strongest_corr) > 0:
                        top_corr = strongest_corr.iloc[0]
                        corr_pair = strongest_corr.index[0]
                        
                        st.info(f"💡 **Strongest correlation:** {corr_pair[0]} and {corr_pair[1]} (r = {top_corr:.3f})")
                else:
                    st.warning("Need at least 2 numeric columns for correlation analysis")
            
            elif analytics_option == "Menstrual Cycle Insights":
                # Check if menstrual data exists
                cycle_cols = ['cycle_day', 'period_status', 'hormonal_symptoms']
                has_cycle_data = any(col in df.columns and df[col].notna().any() for col in cycle_cols)
                
                if has_cycle_data:
                    st.markdown("### 🌸 Cycle-Related Patterns")
                    
                    if 'cycle_day' in df.columns and df['cycle_day'].notna().any():
                        cycle_data = df[df['cycle_day'].notna()].copy()
                        
                        if len(cycle_data) > 5:
                            # Mood across cycle
                            cycle_mood_fig = px.scatter(
                                cycle_data,
                                x='cycle_day',
                                y='mood_rating',
                                title='Mood Across Menstrual Cycle',
                                labels={'cycle_day': 'Cycle Day', 'mood_rating': 'Mood Rating'},
                                trendline='lowess'
                            )
                            st.plotly_chart(cycle_mood_fig, use_container_width=True)
                            
                            # Energy across cycle
                            cycle_energy_fig = px.scatter(
                                cycle_data,
                                x='cycle_day',
                                y='energy_level',
                                title='Energy Across Menstrual Cycle',
                                labels={'cycle_day': 'Cycle Day', 'energy_level': 'Energy Level'},
                                trendline='lowess'
                            )
                            st.plotly_chart(cycle_energy_fig, use_container_width=True)
                            
                            # Cycle phase analysis
                            if 'estimated_phase' in df.columns:
                                phase_summary = cycle_data.groupby('estimated_phase').agg({
                                    'mood_rating': 'mean',
                                    'energy_level': 'mean',
                                    'safety_level': 'mean'
                                }).round(1)
                                
                                st.markdown("### 📊 Average Wellness by Cycle Phase")
                                st.dataframe(phase_summary)
                        else:
                            st.info("Need more cycle data entries to show meaningful patterns (minimum 5 entries)")
                else:
                    st.info("No menstrual cycle data available. Enable cycle tracking in daily check-in to see insights here.")
            
            # Data export section
            st.markdown("---")
            st.markdown("### 💾 Export Your Data")
            
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                if st.button("📥 Download Full Database as CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download Full Database",
                        data=csv,
                        file_name=f"wellness_database_{datetime.date.today().strftime('%d-%m-%Y')}.csv",
                        mime="text/csv"
                    )
            
            with export_col2:
                # Download specific date range
                if len(df) > 0:
                    min_date = df['date'].min().date()
                    max_date = df['date'].max().date()
                    
                    date_range = st.date_input(
                        "Select date range for export:",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date,
                        format="DD/MM/YYYY",
                        key="export_range"
                    )
                    
                    if len(date_range) == 2 and date_range[0] <= date_range[1]:
                        filtered_df = df[
                            (df['date'].dt.date >= date_range[0]) & 
                            (df['date'].dt.date <= date_range[1])
                        ]
                        
                        if st.button("📅 Download Date Range"):
                            csv = filtered_df.to_csv(index=False)
                            st.download_button(
                                label="Download Filtered Data",
                                data=csv,
                                file_name=f"wellness_data_{date_range[0].strftime('%d-%m-%Y')}_to_{date_range[1].strftime('%d-%m-%Y')}.csv",
                                mime="text/csv"
                            )
                
    except Exception as e:
        st.error(f"Error in analytics: {str(e)}")

# ===============================
# SIDEBAR WITH QUICK STATS
# ===============================

with st.sidebar:
    st.markdown("## 🎯 Quick Stats")
    
    try:
        df = load_from_database(conn)
        
        if not df.empty:
            total_entries = len(df)
            
            if total_entries > 0:
                # Convert date column for calculations
                df['date'] = pd.to_datetime(df['date'])
                
                # Current streak calculation (simplified)
                latest_date = df['date'].max().date()
                days_since_last = (datetime.date.today() - latest_date).days
                
                # Average metrics
                avg_mood = df['mood_rating'].mean()
                avg_energy = df['energy_level'].mean()
                avg_safety = df['safety_level'].mean()
                
                st.metric("📊 Total Entries", total_entries)
                st.metric("📅 Days Since Last Entry", f"{days_since_last} days")
                st.metric("😊 Average Mood", f"{avg_mood:.1f}/10")
                st.metric("⚡ Average Energy", f"{avg_energy:.1f}/10")
                st.metric("🛡️ Average Safety", f"{avg_safety:.1f}/10")
                
                # Quick insights
                st.markdown("---")
                st.markdown("### 💡 Quick Insights")
                
                # Best and worst days
                best_day = df.loc[df['mood_rating'].idxmax()]
                worst_day = df.loc[df['mood_rating'].idxmin()]
                
                best_date = pd.to_datetime(best_day['date']).strftime('%d/%m/%Y')
                worst_date = pd.to_datetime(worst_day['date']).strftime('%d/%m/%Y')
                
                st.success(f"🌟 **Best mood day:** {best_date} ({best_day['mood_rating']}/10)")
                if best_day['daily_win']:
                    st.caption(f"Win: {best_day['daily_win']}")
                
                st.info(f"💙 **Challenging day:** {worst_date} ({worst_day['mood_rating']}/10)")
                
                # Trend indicator
                if len(df) >= 7:
                    recent_avg = df.head(3)['mood_rating'].mean()
                    older_avg = df.tail(3)['mood_rating'].mean()
                    
                    if recent_avg > older_avg:
                        st.success("📈 Recent trend: Improving!")
                    elif recent_avg < older_avg:
                        st.warning("📉 Recent trend: Consider extra self-care")
                    else:
                        st.info("➡️ Recent trend: Stable")
            
        else:
            st.info("No data yet - complete your first entry!")
            
        # Database file info
        if os.path.exists("wellness_tracker.db"):
            file_size = os.path.getsize("wellness_tracker.db")
            st.metric("💾 Database Size", f"{file_size / 1024:.1f} KB")
            
        # Quick actions
        st.markdown("---")
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
        
        # Australian crisis resources
        with st.expander("🆘 Crisis Support (Australia)"):
            st.markdown("""
            **If you're in crisis, please reach out:**
            
            🔴 **Emergency:** 000
            
            📞 **Mental Health Crisis:**
            - Lifeline: 13 11 14
            - Suicide Call Back Service: 1300 659 467
            - Kids Helpline: 1800 55 1800
            
            💬 **24/7 Text Support:**
            - Crisis Text Line: Text HELLO to 741741
            
            🌐 **Online Support:**
            - Beyond Blue: beyondblue.org.au
            - Headspace: headspace.org.au
            - SANE Australia: sane.org
            
            **You matter. Your life has value. ❤️**
            """)
            
    except Exception as e:
        st.error(f"Sidebar error: {str(e)}")

# ===============================
# FOOTER
# ===============================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    💙 <strong>Your Wellness Tracker</strong> • 
    Built with care for your healing journey • 
    Last updated: {current_time} • 
    🇦🇺 Made in Australia
</div>
""".format(current_time=datetime.datetime.now().strftime('%d/%m/%Y %H:%M')), unsafe_allow_html=True)

# ===============================
# AUSTRALIAN ENGLISH IMPROVEMENTS
# ===============================

# Additional Australian English replacements throughout:
# - "Personalise" instead of "Personalize"
# - "Colour" instead of "Color" 
# - "Recognise" instead of "Recognize"
# - "Centre" instead of "Center"
# - "Analyse" instead of "Analyze"
# - "Realise" instead of "Realize"
# - "Organised" instead of "Organized"
# - "Initialise" instead of "Initialize"
# - DD/MM/YYYY date format throughout
# - Australian crisis resources
# - Australian spellings in help text and labels