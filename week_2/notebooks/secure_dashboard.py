import streamlit as st
import hashlib
import sqlite3
import time
from datetime import datetime

def init_auth_db():
    conn = sqlite3.connect('auth.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            role TEXT,
            last_login TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            timestamp TEXT,
            username TEXT,
            action TEXT,
            details TEXT
        )
    ''')
    # Create default admin user
    admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
    conn.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)', 
                ('admin', admin_hash, 'admin', ''))
    conn.commit()
    conn.close()

def verify_password(username, password):
    conn = sqlite3.connect('auth.db')
    cursor = conn.execute('SELECT password_hash, role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        stored_hash, role = result
        if hashlib.sha256(password.encode()).hexdigest() == stored_hash:
            return role
    return None

def log_action(username, action, details=""):
    conn = sqlite3.connect('auth.db')
    conn.execute('INSERT INTO audit_log VALUES (?, ?, ?, ?)',
                (datetime.now().isoformat(), username, action, details))
    conn.commit()
    conn.close()

st.set_page_config(page_title="Secure Dashboard", layout="wide")

init_auth_db()

# Session timeout (30 minutes)
SESSION_TIMEOUT = 1800

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.login_time = None

# Check session timeout
if st.session_state.authenticated and st.session_state.login_time:
    if time.time() - st.session_state.login_time > SESSION_TIMEOUT:
        st.session_state.authenticated = False
        st.warning("Session expired. Please login again.")

# Login form
if not st.session_state.authenticated:
    st.title("Login Required")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            role = verify_password(username, password)
            if role:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.session_state.login_time = time.time()
                log_action(username, "LOGIN", "Successful login")
                st.success("Login successful!")
                st.rerun()
            else:
                log_action(username, "LOGIN_FAILED", "Invalid credentials")
                st.error("Invalid credentials")

# Main dashboard
else:
    st.title(f"Secure Dashboard - Welcome {st.session_state.username}")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Logout"):
            log_action(st.session_state.username, "LOGOUT", "User logged out")
            st.session_state.authenticated = False
            st.rerun()
    
    # Role-based content
    if st.session_state.role == 'admin':
        st.subheader("Admin Panel")
        
        # Audit log
        if st.checkbox("Show Audit Log"):
            conn = sqlite3.connect('auth.db')
            df = pd.read_sql_query('SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 100', conn)
            conn.close()
            st.dataframe(df)
    
    st.subheader("Dashboard Content")
    st.write("This content is visible to authenticated users.")
    
    # Log page access
    log_action(st.session_state.username, "PAGE_ACCESS", "Dashboard viewed")