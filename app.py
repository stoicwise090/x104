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

# --- APPLY CSS THEME ---
utils.apply_theme()

# --- MAIN NAVIGATION CONTROLLER ---
def main():
    with st.sidebar:
        st.title("🧭 Navigation")
        
        # Determine the current page selection
        # We use a radio button for clear, persistent navigation
        page_selection = st.radio(
            "Go to", 
            ["Home", "Health Triage", "Breed & Facts", "Detailed Info", "Settings"],
            index=0
        )
        
        st.divider()
        st.caption("Breed Recognition Site v2.1")
        st.caption("Rashtriya Gokul Mission")

    # Routing Logic
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
