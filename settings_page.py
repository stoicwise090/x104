import streamlit as st
import time

def show():
    # --- Local CSS for Settings Page ---
    is_dark = st.session_state.get('theme', 'light') == 'dark'
    
    if is_dark:
        main_bg = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#ffffff"
        sub_text_color = "#cbd5e1"
        border_color = "#475569"
        input_bg = "#334155"
        input_text = "#ffffff"
        btn_bg = "#3b82f6"
        btn_text = "#ffffff"
    else:
        main_bg = "#f8fafc"
        card_bg = "#ffffff"
        text_color = "#0f172a"
        sub_text_color = "#475569"
        border_color = "#cbd5e1"
        input_bg = "#f1f5f9"
        input_text = "#000000"
        btn_bg = "#059669"
        btn_text = "#ffffff"
    
    st.markdown(f"""
    <style>
        /* Force Main Background to match theme */
        .stApp {{
            background-color: {main_bg};
        }}

        /* Card Styling */
        .settings-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .settings-header {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {text_color};
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        /* --- TEXT VISIBILITY FIXES --- */
        h1, h2, h3, p, li, span, label, .stMarkdown, .stCaption {{
            color: {text_color} !important;
        }}
        .stCaption {{
            color: {sub_text_color} !important;
        }}

        /* --- INPUT FIELDS (Stronger Borders) --- */
        /* Targets the container of the input box */
        div[data-baseweb="input"], div[data-baseweb="select"] {{
            background-color: {input_bg} !important;
            border: 2px solid {border_color} !important; 
            border-radius: 8px !important;
        }}
        
        /* Targets the actual text inside the input */
        input[type="text"], input[type="password"] {{
            color: {input_text} !important;
            -webkit-text-fill-color: {input_text} !important;
            background-color: transparent !important;
        }}

        /* --- TOGGLE SWITCH FIX --- */
        /* Ensures the toggle label is visible */
        div[data-testid="stToggle"] label p {{
            font-weight: 600;
            font-size: 1rem;
        }}
        
        /* --- BUTTONS --- */
        div.stButton > button {{
            background-color: {btn_bg} !important;
            color: {btn_text} !important;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border-radius: 8px;
        }}
        div.stButton > button:hover {{
            filter: brightness(110%);
        }}
    </style>
    """, unsafe_allow_html=True)

    st.title("⚙️ Settings & Configuration")
    st.markdown("Manage your application preferences and system connections.")
    st.divider()

    # --- SECTION 1: PREFERENCES ---
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">🎨 Application Preferences</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Language & Region**")
        st.caption("Select the language for AI reports.")
        
        languages = ["English", "Hindi", "Gujarati", "Marathi", "Punjabi"]
        current_lang = st.session_state.get('language', 'English')
        try:
            lang_index = languages.index(current_lang)
        except ValueError:
            lang_index = 0
            
        selected_lang = st.selectbox(
            "Language Selection", 
            languages,
            index=lang_index,
            label_visibility="collapsed",
            key="lang_select"
        )
        
        if selected_lang != st.session_state.get('language'):
            st.session_state.language = selected_lang
            st.rerun()

    with c2:
        st.markdown("**Appearance**")
        st.caption("Toggle between Light and Dark themes.")
        
        current_theme = st.session_state.get('theme', 'light')
        is_dark_mode = st.toggle("Dark Mode", value=(current_theme == 'dark'))
        
        if is_dark_mode and current_theme != 'dark':
            st.session_state.theme = 'dark'
            st.rerun()
        elif not is_dark_mode and current_theme != 'light':
            st.session_state.theme = 'light'
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)


    # --- SECTION 2: API CONFIGURATION ---
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">🔑 API Connection</div>', unsafe_allow_html=True)
    
    st.info("💡 By default, the app uses the system-provided API key. Entering a key below will override it.")
    
    # Use a Form to prevent click errors/reloads while typing
    with st.form("api_key_form"):
        current_key = st.session_state.get('api_key', '')
        
        # Using columns to layout the input and button
        col_input, col_btn = st.columns([3, 1])
        
        with col_input:
            new_key_input = st.text_input(
                "Gemini API Key", 
                type="password", 
                value=current_key,
                placeholder="sk-...",
                label_visibility="collapsed",
                help="Enter your Google Gemini API Key here"
            )
        
        with col_btn:
            # Add a little top margin to align with input box
            st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Save Key", use_container_width=True)
            
        if submitted:
            st.session_state.api_key = new_key_input
            st.success("API Key Saved Successfully!")
            time.sleep(1)
            st.rerun()
            
    if st.session_state.get('api_key'):
        st.caption("✅ Custom API Key is currently active.")
    else:
        st.caption("ℹ️ Using System Default Key (if available).")

    st.markdown('</div>', unsafe_allow_html=True)

    # --- SECTION 3: SYSTEM ---
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    st.markdown('<div class="settings-header">🛡️ System & Data</div>', unsafe_allow_html=True)
    
    sc1, sc2 = st.columns(2)
    
    with sc1:
        st.markdown("**Cache Control**")
        st.caption("Clear temporary files and reset app state.")
        if st.button("Clear App Cache", key="clear_cache_btn"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.toast("Cache cleared successfully!", icon="🧹")
            
    with sc2:
        st.markdown("**Application Info**")
        st.caption(f"Version: 2.1.0 | Build: Stable")
        st.caption("Rashtriya Gokul Mission Integration")

    st.markdown('</div>', unsafe_allow_html=True)
