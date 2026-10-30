
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Configure Page Layout & Branding
st.set_page_config(
    page_title="VisionAI - Image Captioning Studio",
    page_icon="👁️‍🗨️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# App Header
st.title("👁️‍🗨️ VisionAI: Automated Image Captioning")
st.markdown("""
Transform visual imagery into descriptive text using state-of-the-art Deep Learning. 
This application combines **Computer Vision (CNN/Vision Transformer)** for feature extraction 
and **Natural Language Processing (Transformer Decoders)** to generate contextual captions.
""")

# Hardware Acceleration Check
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource(show_spinner=False)
def load_ai_model():
    """Loads the pre-trained BLIP model and processor into memory (cached for performance)."""
    model_id = "Salesforce/blip-image-captioning-base"
    processor = BlipProcessor.from_pretrained(model_id)
    model = BlipForConditionalGeneration.from_pretrained(model_id).to(DEVICE)
    return processor, model

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.info(f"**Compute Device:** `{DEVICE.upper()}`")
    max_length = st.slider("Max Caption Length", min_value=10, max_value=100, value=50)
    temperature = st.slider("Generation Creativity (Temp)", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
    
    st.markdown("---")
    st.markdown("### 🛠️ Built With")
    st.markdown("- PyTorch & Hugging Face\n- BLIP Transformer\n- Streamlit UI")

# Main Interface: File Uploader
uploaded_file = st.file_uploader("Upload an image (PNG, JPG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file).convert('RGB')
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Analysis & Output")
        
        if st.button("Generate Caption 🚀", type="primary"):
            with st.spinner("Analyzing visual features & synthesizing text..."):
                try:
                    # Load model
                    processor, model = load_ai_model()
                    
                    # Preprocess image
                    inputs = processor(images=image, return_tensors="pt").to(DEVICE)
                    
                    # Generate tokens
                    outputs = model.generate(
                        **inputs, 
                        max_new_tokens=max_length,
                        do_sample=True,
                        temperature=temperature
                    )
                    
                    # Decode text
                    caption = processor.decode(outputs[0], skip_special_tokens=True)
                    
                    # Display Result
                    st.success("Caption generated successfully!")
                    st.markdown(f"### 📝 Result:")
                    st.info(f"*{caption.capitalize()}*")
                    
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
else:
    st.markdown("""
    > 💡 **Tip:** Upload any image—whether it's a landscape, a pet, or a street photo—and watch the AI describe what it sees in real-time.
    """)