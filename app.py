import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import re

# Import prompts from the separate file
from prompts import HEALTH_ALERT_PROMPT, FUN_FACTS_PROMPT, DETAILED_BREED_PROMPT

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Breed Recognition Site",
    page_icon="🐮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE SETUP ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# --- 3. HELPLINE DATA ---
HELPLINE_NUMBERS = {
    "All India (Kisan Call Center)": "1800-180-1551",
    "Andhra Pradesh": "1962",
    "Gujarat": "1962",
    "Haryana": "1800-180-2117",
    "Karnataka": "1800-425-0012",
    "Madhya Pradesh": "1962",
    "Maharashtra": "1962",
    "Punjab": "1962",
    "Tamil Nadu": "1962",
    "Telangana": "1962",
    "Uttar Pradesh": "1800-180-5141"
}

# --- 4. CSS STYLING & THEMES ---
def apply_theme():
    if st.session_state.theme == 'dark':
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
        border_color = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#1e293b"
        card_bg = "#ffffff"
        border_color = "#e2e8f0"

    st.markdown(f"""
        <style>
        .stApp {{ background-color: {bg_color}; color: {text_color}; }}
        .nav-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.2s;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            color: {text_color};
            height: 100%;
        }}
        .nav-card:hover {{ transform: translateY(-5px); border-color: #059669; }}
        .nav-title {{ font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; }}
        .nav-icon {{ font-size: 2.5rem; margin-bottom: 10px; }}
        
        /* Health Alert Cards */
        .alert-critical {{ background-color: #fee2e2; border: 2px solid #ef4444; padding: 20px; border-radius: 10px; color: #991b1b; animation: pulse 2s infinite; }}
        .alert-safe {{ background-color: #dcfce7; border: 2px solid #22c55e; padding: 20px; border-radius: 10px; color: #166534; }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
            70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}
        </style>
    """, unsafe_allow_html=True)

apply_theme()

# --- 5. AI LOGIC HELPER ---
def get_gemini_response(image, prompt):
    # Priority: 1. User Key in Settings, 2. Env Var
    api_key = st.session_state.api_key if st.session_state.api_key else os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "ERROR: API Key missing. Please add it in Settings."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025') # Or 'gemini-1.5-flash'
    
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"

# --- 6. PAGE: HOME ---
def page_home():
    st.title("🏡 Breed Recognition Site")
    st.write("Welcome to your AI-powered veterinary companion.")
    
    st.divider()
    
    # Navigation Cards using Columns
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

# --- 7. PAGE: HEALTH TRIAGE ---
def page_health():
    st.title("🩺 Health Triage & Alert System")
    st.write("Upload an image to scan for visible signs of LSD, FMD, or Wounds.")
    
    uploaded_file = st.file_uploader("Upload Animal Image", type=['jpg', 'png', 'jpeg'], key="health_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300, caption="Specimen")
        
        if st.button("🏥 Scan for Disease"):
            with st.spinner("Analyzing clinical signs..."):
                response = get_gemini_response(image, HEALTH_ALERT_PROMPT)
                
                if "CRITICAL" in response or "WARNING" in response:
                    st.markdown(f"""
                    <div class="alert-critical">
                        <h2>⚠️ MEDICAL ALERT DETECTED</h2>
                        <p>The AI has detected potential signs of disease or injury.</p>
                        <hr style="border-color: #ef4444; opacity: 0.5;">
                        <pre style="white-space: pre-wrap; font-family: sans-serif;">{response}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                elif "HEALTHY" in response:
                    st.markdown(f"""
                    <div class="alert-safe">
                        <h2>✅ No Visible Threats</h2>
                        <p>No immediate signs of severe disease detected.</p>
                        <hr style="border-color: #22c55e; opacity: 0.5;">
                        <pre style="white-space: pre-wrap; font-family: sans-serif;">{response}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(response)

# --- 8. PAGE: FUN FACTS ---
def page_fun_facts():
    st.title("🐮 Breed Check & Fun Facts")
    st.write("Discover the breed and learn something new!")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="fun_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        
        if st.button("🎉 Tell Me About It!"):
            with st.spinner("Consulting nature guide..."):
                response = get_gemini_response(image, FUN_FACTS_PROMPT)
                st.markdown(response)
                st.balloons()

# --- 9. PAGE: DETAILED INFO ---
def page_detailed_info():
    st.title("🧬 Detailed Breed Information")
    st.write("Expert-level evaluation for professionals and breeders.")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="detail_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        
        if st.button("📊 Generate Expert Report"):
            with st.spinner("Analyzing breed standards..."):
                response = get_gemini_response(image, DETAILED_BREED_PROMPT)
                
                # We can render this raw or use the parsing logic from previous turns
                # For simplicity and robustness with the prompt provided, we render Markdown
                st.markdown("---")
                st.markdown(response)
                
                with st.expander("Download Report"):
                    st.download_button("Download Text", response, file_name="breed_report.md")

# --- 10. PAGE: SETTINGS ---
def page_settings():
    st.title("⚙️ Settings & Configuration")
    
    # Language
    st.subheader("🌐 Language & Region")
    lang = st.selectbox("Application Language", ["English", "Hindi", "Gujarati", "Marathi", "Punjabi"])
    if lang != st.session_state.language:
        st.session_state.language = lang
        st.toast(f"Language set to {lang} (AI Output will try to match)")
    
    # Theme
    st.subheader("🎨 Appearance")
    is_dark = st.toggle("Dark Mode", value=(st.session_state.theme == 'dark'))
    if is_dark and st.session_state.theme != 'dark':
        st.session_state.theme = 'dark'
        st.rerun()
    elif not is_dark and st.session_state.theme != 'light':
        st.session_state.theme = 'light'
        st.rerun()

    # API Key
    st.subheader("🔑 API Configuration")
    st.info("By default, the app uses the system key. Enter a key below to override it.")
    user_key = st.text_input("Custom Gemini API Key", type="password", value=st.session_state.api_key)
    
    if st.button("Save API Key"):
        st.session_state.api_key = user_key
        st.success("API Key Saved!")

# --- 11. MAIN NAVIGATION CONTROLLER ---
def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("🧭 Navigation")
        page = st.radio("Go to", 
            ["Home", "Health Triage", "Breed & Facts", "Detailed Info", "Settings"],
            index=0
        )
        st.divider()
        st.caption("Breed Recognition Site v2.0")

    # Page Routing
    if page == "Home":
        page_home()
    elif page == "Health Triage":
        page_health()
    elif page == "Breed & Facts":
        page_fun_facts()
    elif page == "Detailed Info":
        page_detailed_info()
    elif page == "Settings":
        page_settings()

if __name__ == "__main__":
    main()
