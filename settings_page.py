import streamlit as st

def show():
    st.title("⚙️ Settings & Configuration")
    
    # Language Section
    st.subheader("🌐 Language & Region")
    lang = st.selectbox(
        "Application Language", 
        ["English", "Hindi", "Gujarati", "Marathi", "Punjabi"],
        index=["English", "Hindi", "Gujarati", "Marathi", "Punjabi"].index(st.session_state.get('language', 'English'))
    )
    if lang != st.session_state.get('language'):
        st.session_state.language = lang
        st.rerun()
    
    # Theme Section
    st.subheader("🎨 Appearance")
    current_theme = st.session_state.get('theme', 'light')
    is_dark = st.toggle("Dark Mode", value=(current_theme == 'dark'))
    
    if is_dark and current_theme != 'dark':
        st.session_state.theme = 'dark'
        st.rerun()
    elif not is_dark and current_theme != 'light':
        st.session_state.theme = 'light'
        st.rerun()

    # API Key Section
    st.subheader("🔑 API Configuration")
    st.info("By default, the app uses the system key. Enter a key below to override it.")
    
    current_key = st.session_state.get('api_key', '')
    user_key = st.text_input("Custom Gemini API Key", type="password", value=current_key)
    
    if st.button("Save API Key"):
        st.session_state.api_key = user_key
        st.success("API Key Saved Successfully!")
