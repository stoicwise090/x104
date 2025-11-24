import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import FUN_FACTS_PROMPT

def show():
    st.title("🐮 Breed Check & Fun Facts")
    st.write("Discover the breed and learn something new!")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'], key="fun_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        
        if st.button("🎉 Tell Me About It!"):
            with st.spinner("Consulting nature guide..."):
                response = get_gemini_response(image, FUN_FACTS_PROMPT)
                st.markdown(response)
                st.balloons()
