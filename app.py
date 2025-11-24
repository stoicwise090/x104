import streamlit as st
import google.generativeai as genai
from PIL import Image
import re

# --- 1. CONFIGURATION & STYLES ---
st.set_page_config(
    page_title="RGM Breed Analyst",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS to make it look attractive (Like the React Dashboard)
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background-color: #059669;
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #047857;
        color: white;
    }
    .hero-card {
        background: linear-gradient(135deg, #059669 0%, #0f766e 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stat-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    .feature-list {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
    }
    .reasoning-box {
        background-color: #fffbeb;
        border: 1px solid #fcd34d;
        color: #92400e;
        padding: 1.5rem;
        border-radius: 0.75rem;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE PROMPT ---
BREED_RECOGNITION_PROMPT = """
### ROLE
You are an expert veterinarian and cattle/buffalo breed specialist with extensive knowledge of Indian indigenous and crossbred cattle and buffalo breeds.

### TASK
Your task is to analyze the provided image and identify the breed of cattle or buffalo shown.

### CONTEXT & LISTS
Common Indian Cattle Breeds to consider:
- Gir, Sahiwal, Red Sindhi, Tharparkar, Rathi, Hariana, Ongole, Krishna Valley, Amritmahal, Hallikar, Khillari, Dangi, Deoni, Nimari, Malvi, Mewati, Nagori, Kankrej, etc.

Common Indian Buffalo Breeds to consider:
- Murrah, Nili-Ravi, Bhadawari, Jaffarabadi, Mehsana, Surti, Nagpuri, Toda, Pandharpuri, etc.

### OUTPUT FORMAT
Analyze the image carefully considering body structure, coat color, horn shape, facial features, body size, and any distinctive breed markers.
Provide your analysis in the following structured Markdown format. DO NOT change the header titles:

## 🧬 Primary Breed Identification
* **Breed Name:** [The most likely breed name]
* **Species:** [Cattle or Buffalo]

## 🎯 Confidence Level
* **Level:** [High/Medium/Low]

## 📏 Key Physical Characteristics
[List the specific visual features that led to this identification, such as horn shape, forehead, coat color, etc. separate with new lines]

## 🔄 Alternative Possibilities
[If uncertain, mention 1-2 other possible breeds]

## 🌍 Breed Category & Origin
* **Category:** [Indigenous/Crossbred/Exotic]
* **Geographic Origin:** [Traditional region/state where this breed is commonly found]

## 📝 Reasoning
[Detailed reasoning for your identification based on the visual evidence.]
"""

# --- 3. HELPER FUNCTIONS ---
def analyze_image(image, api_key):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
        return None

    genai.configure(api_key=api_key)
    
    # Use the specific model requested
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025') # Or 'gemini-1.5-flash' if preview not available

    try:
        response = model.generate_content([
            BREED_RECOGNITION_PROMPT,
            image
        ])
        return response.text
    except Exception as e:
        st.error(f"Error connecting to Gemini: {e}")
        return None

def parse_markdown_response(text):
    """Parses the markdown text into a dictionary for the dashboard."""
    data = {
        "breed_name": "Unknown",
        "species": "Unknown",
        "confidence": "Low",
        "characteristics": [],
        "alternatives": "None",
        "category": "Unknown",
        "origin": "Unknown",
        "reasoning": ""
    }
    
    # Simple regex based parsing (robust enough for structured AI output)
    breed_match = re.search(r"\*\*Breed Name:\*\*\s*(.*)", text)
    if breed_match: data["breed_name"] = breed_match.group(1).strip()
    
    species_match = re.search(r"\*\*Species:\*\*\s*(.*)", text)
    if species_match: data["species"] = species_match.group(1).strip()
    
    conf_match = re.search(r"\*\*Level:\*\*\s*(.*)", text)
    if conf_match: data["confidence"] = conf_match.group(1).strip()

    cat_match = re.search(r"\*\*Category:\*\*\s*(.*)", text)
    if cat_match: data["category"] = cat_match.group(1).strip()

    origin_match = re.search(r"\*\*Geographic Origin:\*\*\s*(.*)", text)
    if origin_match: data["origin"] = origin_match.group(1).strip()
    
    # Extract Reasoning
    reasoning_parts = text.split("## 📝 Reasoning")
    if len(reasoning_parts) > 1:
        data["reasoning"] = reasoning_parts[1].strip()
        
    # Extract Characteristics
    char_section = re.search(r"## 📏 Key Physical Characteristics\n(.*?)(?=\n##)", text, re.DOTALL)
    if char_section:
        raw_chars = char_section.group(1).strip().split('\n')
        data["characteristics"] = [c.strip().lstrip('*').lstrip('-').strip() for c in raw_chars if c.strip()]

    return data

# --- 4. MAIN UI LAYOUT ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get your key from aistudio.google.com")
    st.info("Upload an image of Cattle or Buffalo to identify its breed according to RGM standards.")

st.title("🧬 RGM Breed Analyst")
st.markdown("### Rashtriya Gokul Mission - AI Identification Tool")

col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    st.markdown("#### 📸 Specimen Photo")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Specimen", use_column_width=True, channels="RGB")
        
        analyze_btn = st.button("🔍 Identify Breed")

with col2:
    if uploaded_file and analyze_btn:
        with st.spinner("Consulting Breed Standards..."):
            raw_result = analyze_image(image, api_key)
            
            if raw_result:
                data = parse_markdown_response(raw_result)
                
                # --- DASHBOARD UI ---
                
                # 1. Hero Card
                st.markdown(f"""
                <div class="hero-card">
                    <p style="margin:0; opacity:0.8; font-size:0.9rem; text-transform:uppercase; letter-spacing:1px;">Identified Breed</p>
                    <h1 style="margin:0.5rem 0; font-size:2.5rem;">{data['breed_name']}</h1>
                    <div style="display:flex; gap:10px; margin-top:10px;">
                        <span style="background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:0.8rem;">🧬 {data['species']}</span>
                        <span style="background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:0.8rem;">🏆 {data['category']}</span>
                        <span style="background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:0.8rem;">📊 {data['confidence']} Confidence</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 2. Stats Grid
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <small style="color:#64748b; text-transform:uppercase; font-weight:bold;">🌍 Geographic Origin</small>
                        <h3 style="margin:5px 0 0 0; color:#1e293b;">{data['origin']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <small style="color:#64748b; text-transform:uppercase; font-weight:bold;">⚖️ Breed Type</small>
                        <h3 style="margin:5px 0 0 0; color:#1e293b;">{data['category']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("") # Spacer

                # 3. Characteristics
                st.subheader("📏 Key Physical Markers")
                for char in data['characteristics']:
                    st.info(f"✅ {char}")

                # 4. Reasoning
                st.subheader("🛡️ Expert Reasoning")
                st.markdown(f"""
                <div class="reasoning-box">
                    "{data['reasoning']}"
                </div>
                """, unsafe_allow_html=True)

                # Export (Raw text)
                with st.expander("View Raw Report"):
                    st.markdown(raw_result)
    
    elif not uploaded_file:
        st.info("👈 Upload an image on the left to begin analysis.")
        st.markdown("""
        <div style="text-align: center; color: #94a3b8; padding: 2rem;">
            <h4>Waiting for Input</h4>
            <p>Upload a clear side-profile photo of the animal.</p>
        </div>
        """, unsafe_allow_html=True)
