import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import DETAILED_BREED_PROMPT

def show():
    st.title("🧬 Detailed Breed Information")
    st.write("Expert-level evaluation for professionals and breeders.")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="detail_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        
        if st.button("📊 Generate Expert Report"):
            with st.spinner("Analyzing breed standards..."):
                response = get_gemini_response(image, DETAILED_BREED_PROMPT)
                
                st.markdown("---")
                st.markdown(response)
                
                with st.expander("Download Report"):
                    st.download_button("Download Text", response, file_name="breed_report.md")
