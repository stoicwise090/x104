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

# --- THEME MANAGER (GLOBAL CSS) ---
def apply_theme():
    """Applies a global design system using CSS variables."""
    
    # Define Color Palettes
    if st.session_state.get('theme') == 'dark':
        # Dark Theme (Slate & Emerald)
        colors = {
            "bg": "#0f172a",           # Deep Slate
            "card_bg": "#1e293b",      # Lighter Slate
            "text": "#f8fafc",         # White-ish
            "sub_text": "#94a3b8",     # Grey text
            "border": "#334155",       # Slate Border
            "primary": "#34d399",      # Bright Emerald
            "primary_hover": "#10b981",
            "input_bg": "#020617",     # Almost Black
            "input_text": "#ffffff",
            "success_bg": "#064e3b",
            "success_border": "#059669",
            "danger_bg": "#450a0a",
            "danger_border": "#dc2626"
        }
    else:
        # Light Theme (Clean White & Emerald)
        colors = {
            "bg": "#f0f2f5",           # Light Grey-Blue
            "card_bg": "#ffffff",      # Pure White
            "text": "#1e293b",         # Dark Slate
            "sub_text": "#64748b",     # Grey text
            "border": "#e2e8f0",       # Light Border
            "primary": "#059669",      # Emerald Green
            "primary_hover": "#047857",
            "input_bg": "#ffffff",
            "input_text": "#000000",
            "success_bg": "#ecfdf5",
            "success_border": "#34d399",
            "danger_bg": "#fef2f2",
            "danger_border": "#f87171"
        }

    # Inject CSS
    st.markdown(f"""
        <style>
        /* --- GLOBAL VARIABLES --- */
        :root {{
            --bg-color: {colors['bg']};
            --card-bg: {colors['card_bg']};
            --text-color: {colors['text']};
            --sub-text-color: {colors['sub_text']};
            --border-color: {colors['border']};
            --primary-color: {colors['primary']};
            --primary-hover: {colors['primary_hover']};
            --input-bg: {colors['input_bg']};
            --input-text: {colors['input_text']};
        }}

        /* --- MAIN CONTAINER --- */
        .stApp {{
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Inter', sans-serif;
        }}
        
        /* --- TEXT STYLING --- */
        h1, h2, h3, h4, h5, h6, p, span, li, .stMarkdown {{
            color: var(--text-color) !important;
        }}
        .stCaption {{
            color: var(--sub_text_color) !important;
        }}

        /* --- CARDS & CONTAINERS --- */
        .ui-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .ui-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-color: var(--primary-color);
        }}

        /* --- NAVIGATION CARD (Home Page) --- */
        .nav-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            height: 100%;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .nav-card:hover {{
            border-color: var(--primary-color);
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        .nav-icon {{
            font-size: 2.5rem;
            margin-bottom: 12px;
            background: rgba(16, 185, 129, 0.1);
            width: 60px;
            height: 60px;
            line-height: 60px;
            border-radius: 50%;
            margin-left: auto;
            margin-right: auto;
        }}

        /* --- INPUT FIELDS (The Fix) --- */
        /* Forces inputs to have clear borders and correct text colors */
        div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: var(--input-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
        }}
        div[data-baseweb="input"]:focus-within {{
            border-color: var(--primary-color) !important;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
        }}
        
        input[type="text"], input[type="password"] {{
            color: var(--input-text) !important;
            caret-color: var(--primary-color) !important;
        }}
        div[data-baseweb="select"] span {{
            color: var(--input-text) !important;
        }}

        /* --- BUTTONS --- */
        div.stButton > button {{
            background-color: var(--primary-color) !important;
            color: #ffffff !important;
            border: none;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-weight: 600;
            transition: background-color 0.2s;
            width: 100%;
        }}
        div.stButton > button:hover {{
            background-color: var(--primary-hover) !important;
        }}
        div.stButton > button:active {{
            transform: scale(0.98);
        }}

        /* --- ALERTS --- */
        .alert-box {{
            padding: 16px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid;
        }}
        .alert-safe {{
            background-color: {colors['success_bg']};
            border-color: {colors['success_border']};
            color: {colors['success_border']};
        }}
        .alert-danger {{
            background-color: {colors['danger_bg']};
            border-color: {colors['danger_border']};
            color: {colors['danger_border']};
        }}

        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {{
            background-color: var(--card-bg);
            border-right: 1px solid var(--border-color);
        }}
        </style>
    """, unsafe_allow_html=True)

# --- API HANDLER ---
def get_gemini_response(image, prompt):
    """Handles communication with Google Gemini API."""
    api_key = st.session_state.get('api_key') or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return "ERROR: API Key missing. Please add it in Settings."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025') 
    
    target_language = st.session_state.get('language', 'English')
    language_instruction = f"\n\nIMPORTANT OUTPUT INSTRUCTION: Provide the response strictly in {target_language} language."
    final_prompt = prompt + language_instruction

    try:
        response = model.generate_content([final_prompt, image])
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"
