import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import HEALTH_ALERT_PROMPT

def show():
    st.title("🩺 Health Triage")
    st.markdown("Upload a clear photo to scan for visible signs of **LSD, FMD, or Trauma**.")
    
    st.markdown('<div class="ui-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'], key="health_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, caption="Uploaded Specimen")
        
        if st.button("Run Diagnostics"):
            with st.spinner("Analyzing clinical signs..."):
                response = get_gemini_response(image, HEALTH_ALERT_PROMPT)
                
                if "CRITICAL" in response or "WARNING" in response:
                    st.markdown(f"""
                    <div class="alert-box alert-danger">
                        <h3>⚠️ Medical Alert</h3>
                        <div style="white-space: pre-wrap;">{response}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif "HEALTHY" in response:
                    st.markdown(f"""
                    <div class="alert-box alert-safe">
                        <h3>✅ Assessment: Stable</h3>
                        <div style="white-space: pre-wrap;">{response}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(response)
    st.markdown('</div>', unsafe_allow_html=True)
