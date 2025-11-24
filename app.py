import streamlit as st

# Import the modularized pages and utils
import utils
import home_page
import health_page
import fun_facts_page
import detailed_info_page
import settings_page

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Breed Recognition Site",
    page_icon="🐮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE STATE ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# Initialize Navigation State
if 'navigation' not in st.session_state:
    st.session_state.navigation = "Home"

# --- APPLY CSS THEME ---
utils.apply_theme()

# --- MAIN NAVIGATION CONTROLLER ---
def main():
    with st.sidebar:
        st.title("🧭 Navigation")
        
        # KEY FIX: Added key="navigation" to bind this to session state
        # This allows buttons on the Home page to update this selection
        st.radio(
            "Go to", 
            ["Home", "Health Triage", "Breed & Facts", "Detailed Info", "Settings"],
            key="navigation"
        )
        
        st.divider()
        st.caption("Breed Recognition Site v2.2")
        st.caption("Rashtriya Gokul Mission")

    # Routing Logic based on Session State
    page_selection = st.session_state.navigation
    
    if page_selection == "Home":
        home_page.show()
    elif page_selection == "Health Triage":
        health_page.show()
    elif page_selection == "Breed & Facts":
        fun_facts_page.show()
    elif page_selection == "Detailed Info":
        detailed_info_page.show()
    elif page_selection == "Settings":
        settings_page.show()

if __name__ == "__main__":
    main()
