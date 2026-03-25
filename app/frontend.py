import streamlit as st
import json
import os
import sys
from PIL import Image

# Ensure app module is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ai_generator import generate_tests
from app.test_writer import save_test_code

st.set_page_config(page_title="AI Test Generator", layout="wide")

st.markdown(
    """
    <style>
    /* Make the Primary button pop and glow */
    button[kind="primary"] {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 16px rgba(0, 210, 255, 0.35) !important;
    }
    
    /* Input fields and text areas hover effects */
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 0 1px #00d2ff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("AI Test Generator 🚀")
st.write("Generate Pytest test cases from API definitions, UI screenshots, and custom prompts!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. API Definition (JSON, Optional)")
    api_json_str = st.text_area(
        "Paste your API JSON here", 
        height=150, 
        value='{\n  "method": "POST",\n  "url": "/create-user",\n  "body": {\n    "name": "string",\n    "email": "string"\n  }\n}'
    )
    
    st.subheader("2. UI Screenshot (Optional)")
    uploaded_file = st.file_uploader("Choose an image to test UI features...", type=["jpg", "png", "jpeg"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

    st.subheader("3. Custom Prompt (Optional)")
    custom_prompt = st.text_area("Add specific instructions or assertions for the tests...", height=100)

with col2:
    st.subheader("Generate & Save")
    if st.button("Generate Tests", type="primary"):
        with st.spinner("Generating tests with Gemini..."):
            try:
                parsed_api = None
                if api_json_str.strip():
                    try:
                        parsed_api = json.loads(api_json_str)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format in the API Definition. Please fix it or clear the field.")
                        st.stop()
                
                # Generate tests
                tests_code = generate_tests(parsed_api=parsed_api, image=image, custom_prompt=custom_prompt)
                
                # Save tests
                url = parsed_api.get('url', '/ui-test') if parsed_api else '/ui-test'
                test_file_path = save_test_code(tests_code, url)
                
                st.success(f"Tests successfully generated and saved to `{test_file_path}`!")
                with st.expander("View Generated Code", expanded=True):
                    st.code(tests_code, language='python')
                
            except Exception as e:
                st.error(f"Error generating tests: {e}")
