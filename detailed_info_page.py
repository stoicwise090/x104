import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import DETAILED_BREED_PROMPT

def show():
    st.title("🧬 Detailed Evaluation")
    st.markdown("Expert-level breed and physical conformation analysis.")
    
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="detail_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
        
        if st.button("Generate Expert Report"):
            with st.spinner("Consulting breed standards..."):
                response = get_gemini_response(image, DETAILED_BREED_PROMPT)
                
                st.markdown("---")
                st.markdown(response)
                
                st.download_button("Download Report (TXT)", response, file_name="breed_analysis.txt")
    st.markdown('</div>', unsafe_allow_html=True)
