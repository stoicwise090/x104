import streamlit as st
from utils import HELPLINE_NUMBERS

# Helper function to change pages
def navigate_to(page_name):
    st.session_state.navigation = page_name
    st.rerun()

def show():
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1>🐮 Breed Recognition Site</h1>
        <p style="font-size: 1.2rem; opacity: 0.8;">AI-Powered Veterinary & Breed Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Grid
    st.markdown("### 🧭 Quick Access")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📸</div>
            <h3 style="margin:0">Fun Facts</h3>
            <p style="font-size: 0.9rem;">Identify breeds & learn trivia.</p>
        </div>
        """, unsafe_allow_html=True)
        # ACTION BUTTON
        if st.button("Go to Fun Facts", key="btn_facts", use_container_width=True):
            navigate_to("Breed & Facts")
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🩺</div>
            <h3 style="margin:0">Health Triage</h3>
            <p style="font-size: 0.9rem;">Scan for diseases & injuries.</p>
        </div>
        """, unsafe_allow_html=True)
        # ACTION BUTTON
        if st.button("Go to Triage", key="btn_health", use_container_width=True):
            navigate_to("Health Triage")

    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🧬</div>
            <h3 style="margin:0">Deep Analysis</h3>
            <p style="font-size: 0.9rem;">Expert breed evaluation.</p>
        </div>
        """, unsafe_allow_html=True)
        # ACTION BUTTON
        if st.button("Go to Analysis", key="btn_detail", use_container_width=True):
            navigate_to("Detailed Info")
        
    with col4:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">⚙️</div>
            <h3 style="margin:0">Settings</h3>
            <p style="font-size: 0.9rem;">Configure API & Theme.</p>
        </div>
        """, unsafe_allow_html=True)
        # ACTION BUTTON
        if st.button("Open Settings", key="btn_settings", use_container_width=True):
            navigate_to("Settings")

    st.markdown("<br>", unsafe_allow_html=True)

    # Emergency Section
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.subheader("🚑 Emergency Helpline Directory")
    c1, c2 = st.columns([2, 1])
    with c1:
        state_selection = st.selectbox("Select State/Region", list(HELPLINE_NUMBERS.keys()))
    with c2:
        number = HELPLINE_NUMBERS[state_selection]
        st.markdown(f"""
        <div style="background-color: #ef4444; color: white; padding: 10px; border-radius: 8px; text-align: center;">
            <div style="font-size: 0.8rem; opacity: 0.9;">EMERGENCY NUMBER</div>
            <div style="font-size: 1.5rem; font-weight: bold;">{number}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
