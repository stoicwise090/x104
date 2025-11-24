import streamlit as st
from PIL import Image
from utils import get_gemini_response
from prompts import HEALTH_ALERT_PROMPT

def show():
    st.title("🩺 Health Triage & Alert System")
    st.write("Upload an image to scan for visible signs of LSD, FMD, or Wounds.")
    
    uploaded_file = st.file_uploader("Upload Animal Image", type=['jpg', 'png', 'jpeg'], key="health_up")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, width=300, caption="Specimen")
        
        if st.button("🏥 Scan for Disease"):
            with st.spinner("Analyzing clinical signs..."):
                response = get_gemini_response(image, HEALTH_ALERT_PROMPT)
                
                if "CRITICAL" in response or "WARNING" in response:
                    st.markdown(f"""
                    <div class="alert-critical">
                        <h2>⚠️ MEDICAL ALERT DETECTED</h2>
                        <p>The AI has detected potential signs of disease or injury.</p>
                        <hr style="border-color: #ef4444; opacity: 0.5;">
                        <pre style="white-space: pre-wrap; font-family: sans-serif;">{response}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                elif "HEALTHY" in response:
                    st.markdown(f"""
                    <div class="alert-safe">
                        <h2>✅ No Visible Threats</h2>
                        <p>No immediate signs of severe disease detected.</p>
                        <hr style="border-color: #22c55e; opacity: 0.5;">
                        <pre style="white-space: pre-wrap; font-family: sans-serif;">{response}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Fallback for unexpected API output
                    st.warning("Analysis Complete. Review results below:")
                    st.text(response)
