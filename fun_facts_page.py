import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import FUN_FACTS_PROMPT

def show():
    st.title("🎉 Breed & Trivia")
    st.markdown("Identify the animal and learn fun facts!")
    
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="fun_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
        
        if st.button("Discover Facts"):
            with st.spinner("Finding cool facts..."):
                response = get_gemini_response(image, FUN_FACTS_PROMPT)
                st.markdown(response)
                st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)
