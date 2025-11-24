import streamlit as st
import google.generativeai as genai
import os

# --- CONSTANTS ---
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

# --- THEME MANAGER ---
def apply_theme():
    """Applies CSS based on the current session state theme."""
    if st.session_state.get('theme') == 'dark':
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

# --- API HANDLER ---
def get_gemini_response(image, prompt):
    """Handles communication with Google Gemini API."""
    # Priority: 1. User Key in Settings, 2. Env Var
    api_key = st.session_state.get('api_key') or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "ERROR: API Key missing. Please add it in Settings."
    
    genai.configure(api_key=api_key)
    # Using the preview model as requested
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025') 
    
    # --- LANGUAGE INJECTION ---
    # This ensures the AI speaks the user's selected language
    target_language = st.session_state.get('language', 'English')
    language_instruction = f"\n\nIMPORTANT OUTPUT INSTRUCTION: Provide the response strictly in {target_language} language."
    
    final_prompt = prompt + language_instruction

    try:
        response = model.generate_content([final_prompt, image])
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"
