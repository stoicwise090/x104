import streamlit as st
import time

def show():
    # --- Local CSS for Settings Page ---
    # This fixes the input field colors and creates the card effect
    is_dark = st.session_state.get('theme', 'light') == 'dark'
    
    card_bg = "#1e293b" if is_dark else "#ffffff"
    text_color = "#f8fafc" if is_dark else "#1e293b"
    border_color = "#334155" if is_dark else "#e2e8f0"
    input_bg = "#334155" if is_dark else "#f1f5f9"
    
    st.markdown(f"""
    <style>
        .settings-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .settings-header {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {text_color};
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        /* Fix for Input Fields to match theme */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{
            background-color: {input_bg} !important;
            border-color: {border_color} !important;
            color: {text_color} !important;
        }}
        div[data-baseweb="select"] span {{
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
        lang = st.selectbox(
            "Language", 
            ["English", "Hindi", "Gujarati", "Marathi", "Punjabi"],
            label_visibility="collapsed",
            index=["English", "Hindi", "Gujarati", "Marathi", "Punjabi"].index(st.session_state.get('language', 'English'))
        )
        if lang != st.session_state.get('language'):
            st.session_state.language = lang
            st.rerun()

    with c2:
        st.markdown("**Appearance**")
        st.caption("Toggle between Light and Dark themes.")
        
        current_theme = st.session_state.get('theme', 'light')
        is_dark_mode = st.toggle("Dark Mode", value=(current_theme == 'dark'))
        
        # Logic to switch theme
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
    
    current_key = st.session_state.get('api_key', '')
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        user_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=current_key,
            placeholder="sk-...",
            label_visibility="collapsed"
        )
    with col_btn:
        if st.button("Save Key", use_container_width=True):
            st.session_state.api_key = user_key
            st.success("Saved!")
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
        if st.button("Clear App Cache"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.toast("Cache cleared successfully!", icon="🧹")
            
    with sc2:
        st.markdown("**Application Info**")
        st.caption(f"Version: 2.1.0 | Build: Stable")
        st.caption("Rashtriya Gokul Mission Integration")

    st.markdown('</div>', unsafe_allow_html=True)
