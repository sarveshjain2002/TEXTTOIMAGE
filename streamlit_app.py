
import streamlit as st
import replicate
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
        .main {background-color: #f0f4f7;}
        .stButton > button {background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px;}
        .stTextInput input {border-radius: 8px; padding: 12px; font-size: 16px; width: 100%;}
        .stSpinner {color: #f39c12;}
    </style>
""", unsafe_allow_html=True)

st.title("AI Image Generator with Replicate API")
st.markdown("Welcome to the **AI Image Generator Dashboard**. Please enter your **Replicate API Key** below to get started.")

# API Key input
api_key = st.text_input("Enter your Replicate API Key:", type="password", placeholder="Your API Key here...")

# Check if API Key is provided
if api_key:
    # Save the API Key to the environment
    import os
    os.environ["REPLICATE_API_KEY"] = api_key

    # Set up the Replicate API client
    replicate.Client(api_token=api_key)

    # Sidebar navigation
    st.sidebar.title("AI Tools")
    current_page = st.sidebar.radio("Select a Tool", 
                                    ["Generate Image", "Image to Prompt", "Remove Background"],
                                    key="page_selector", label_visibility="visible")

    # Function for Image Generation
    def generate_image():
        st.subheader("Generate Image")
        st.markdown("Create an image from a **text prompt**.")
        prompt = st.text_input(label="Enter your prompt here:", key="generate_image_prompt", max_chars=500, placeholder="e.g., A futuristic city skyline")

        if st.button("Generate Image", key="generate_image_button"):
            if prompt:
                with st.spinner("Generating image..."):
                    start_time = time.time()
                    try:
                        output = replicate.run(
                            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                            input={
                                "width": 1024,
                                "height": 1024,
                                "prompt": prompt,
                                "refine": "expert_ensemble_refiner",
                                "num_outputs": 1,
                                "apply_watermark": False,
                                "negative_prompt": "low quality, worst quality",
                                "num_inference_steps": 25
                            }
                        )
                        st.image(output, caption="Generated Image", use_column_width=True)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        st.write(f"Image generated in {elapsed_time:.2f} seconds")
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
            else:
                st.warning("Please enter a prompt to generate the image.")

    # Function for Image to Prompt Generation
    def image_to_prompt():
        st.subheader("Image to Prompt")
        st.markdown("Generate a **text prompt** from your uploaded image.")
        uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="image_to_prompt_upload")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            if st.button("Generate Prompt"):
                with st.spinner('Generating prompt...'):
                    start_time = time.time()
                    try:
                        input = {"image": uploaded_file}
                        output = replicate.run(
                            "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5",
                            input=input
                        )
                        st.write(f"**Generated Prompt:**\n\n{output}")
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        st.write(f"Prompt generated in {elapsed_time:.2f} seconds")
                    except Exception as e:
                        st.error(f"Error generating prompt: {e}")
        else:
            st.info("Upload an image to generate a prompt.")

    # Function for Background Removal
    def remove_background():
        st.subheader("Background Remover")
        st.markdown("Remove the background from your uploaded image.")
        uploaded_file = st.file_uploader(label="Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"], key="remove_background")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            if st.button("Remove Background"):
                with st.spinner('Removing background...'):
                    start_time = time.time()
                    try:
                        input = {"image": uploaded_file}
                        output = replicate.run(
                            "cjwbw/rembg:fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003",
                            input=input
                        )
                        st.image(output, caption="Processed Image", use_column_width=True)
                        end_time = time.time()
                        elapsed_time = end_time - start_time
                        st.write(f"Background removed in {elapsed_time:.2f} seconds")
                    except Exception as e:
                        st.error(f"Error removing background: {e}")
        else:
            st.info("Upload an image to remove its background.")

    # Page content based on selected tool
    if current_page == "Generate Image":
        generate_image()

    if current_page == "Image to Prompt":
        image_to_prompt()

    if current_page == "Remove Background":
        remove_background()

else:
    st.warning("Please enter a valid API key to get started.")
