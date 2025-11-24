import streamlit as st
import time

def show():
    # --- Local CSS for Settings Page ---
    # We explicitly define high-contrast colors here to fix the visibility issues
    is_dark = st.session_state.get('theme', 'light') == 'dark'
    
    if is_dark:
        card_bg = "#1e293b"       # Dark Blue-Grey
        text_color = "#f8fafc"    # White
        border_color = "#334155"  # Lighter Grey border
        input_bg = "#0f172a"      # Very Dark background for inputs
        input_text = "#ffffff"    # Pure White text
        btn_bg = "#3b82f6"        # Bright Blue for buttons
        btn_text = "#ffffff"
    else:
        card_bg = "#ffffff"       # Pure White
        text_color = "#1e293b"    # Dark Grey
        border_color = "#cbd5e1"  # Light Grey border
        input_bg = "#f8fafc"      # Off-white background for inputs
        input_text = "#000000"    # Pure Black text
        btn_bg = "#059669"        # Emerald Green for buttons
        btn_text = "#ffffff"
    
    st.markdown(f"""
    <style>
        .settings-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .settings-header {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {text_color};
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* --- FORCE INPUT VISIBILITY --- */
        /* This forces the text box and dropdowns to have distinct colors */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div {{
            background-color: {input_bg} !important;
            border: 1px solid {border_color} !important;
            color: {input_text} !important;
        }}
        
        /* Force the actual text inside inputs to be visible */
        input[type="text"], input[type="password"] {{
            color: {input_text} !important;
            -webkit-text-fill-color: {input_text} !important;
            caret-color: {text_color};
        }}
        
        /* Fix Dropdown Text */
        div[data-baseweb="select"] span {{
            color: {input_text} !important;
        }}
        
        /* --- BUTTON STYLING --- */
        /* Makes buttons pop with color */
        div.stButton > button {{
            background-color: {btn_bg} !important;
            color: {btn_text} !important;
            border: none;
            font-weight: 600;
            transition: all 0.2s;
        }}
        div.stButton > button:hover {{
            opacity: 0.9;
            transform: scale(1.01);
        }}
        
        /* --- LABEL STYLING --- */
        label, .stMarkdown p {{
            color: {text_color} !important;
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
            # Added some spacing for alignment
            st.markdown("<div style='margin-top: 2px;'></div>", unsafe_allow_html=True)
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
