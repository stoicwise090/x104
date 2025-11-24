import streamlit as st
import time

def show():
    st.title("⚙️ Settings")
    st.markdown("Configure your application preferences.")
    st.markdown("---")

    # --- APPEARANCE CARD ---
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.subheader("🎨 Appearance & Language")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Language**")
        languages = ["English", "Hindi", "Gujarati", "Marathi", "Punjabi"]
        current_lang = st.session_state.get('language', 'English')
        try:
            lang_index = languages.index(current_lang)
        except ValueError:
            lang_index = 0
            
        selected_lang = st.selectbox(
            "Select Language", 
            languages,
            index=lang_index,
            label_visibility="collapsed",
            key="lang_select"
        )
        if selected_lang != st.session_state.get('language'):
            st.session_state.language = selected_lang
            st.rerun()

    with c2:
        st.markdown("**Theme**")
        current_theme = st.session_state.get('theme', 'light')
        is_dark_mode = st.toggle("Dark Mode", value=(current_theme == 'dark'))
        
        if is_dark_mode and current_theme != 'dark':
            st.session_state.theme = 'dark'
            st.rerun()
        elif not is_dark_mode and current_theme != 'light':
            st.session_state.theme = 'light'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- API CARD ---
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.subheader("🔑 API Configuration")
    st.info("Your key is stored locally in this session.")
    
    with st.form("api_key_form"):
        current_key = st.session_state.get('api_key', '')
        new_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=current_key,
            placeholder="Enter your sk- key here..."
        )
        submitted = st.form_submit_button("Save Configuration")
        
        if submitted:
            st.session_state.api_key = new_key
            st.success("Configuration Saved!")
            time.sleep(1)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- SYSTEM CARD ---
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    st.subheader("🛡️ System Operations")
    col_sys, col_info = st.columns(2)
    
    with col_sys:
        if st.button("Clear Cache & Reset"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.toast("System Reset Complete", icon="🧹")
            
    with col_info:
        st.caption("Version 2.2.0 (Emerald UI)")
        st.caption("Rashtriya Gokul Mission")
    st.markdown('</div>', unsafe_allow_html=True)
