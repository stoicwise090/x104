import streamlit as st
from utils import HELPLINE_NUMBERS

def show():
    st.title("🏡 Breed Recognition Site")
    st.write("Welcome to your AI-powered veterinary companion.")
    
    st.divider()
    
    # Navigation Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📸</div>
            <div class="nav-title">Fun Facts</div>
            <p>Identify breed & learn cool trivia.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🩺</div>
            <div class="nav-title">Health Triage</div>
            <p>Scan for visible diseases & injuries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🧬</div>
            <div class="nav-title">Detailed Info</div>
            <p>Expert evaluation & physical analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">⚙️</div>
            <div class="nav-title">Settings</div>
            <p>Configure API & Preferences.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Helpline Section
    st.subheader("📞 Animal Helpline Directory")
    c1, c2 = st.columns([1, 2])
    with c1:
        state_selection = st.selectbox("Select your State/Region", list(HELPLINE_NUMBERS.keys()))
    with c2:
        st.info(f"🚑 Emergency Number for **{state_selection}**: **{HELPLINE_NUMBERS[state_selection]}**")
        st.caption("*Use this number for ambulance or veterinary emergencies.*")
