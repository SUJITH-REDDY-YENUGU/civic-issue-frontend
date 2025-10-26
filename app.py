import streamlit as st
import requests

# 🔗 Backend URLs
RENDER_URL = "https://civic-clip-backend.onrender.com/predict"
HF_SPACE_URL = "https://sujith2121-civic-clip-fastapi.hf.space/classify"

# 🖼️ UI
st.set_page_config(page_title="Civic Issue Classifier", layout="centered")
st.title("🧭 Civic Issue Classifier")

image = st.file_uploader("Upload an image of the issue", type=["jpg", "jpeg", "png"])
description = st.text_input("Describe the issue briefly")

if st.button("Classify") and image and description:
    with st.spinner("Sending to backend..."):
        files = {"image": (image.name, image.read(), image.type)}
        data = {"description": description}  # ✅ consistent key for both backends

        # 🔁 Try Render first
        try:
            response = requests.post(RENDER_URL, files=files, data=data, timeout=1)
            response.raise_for_status()
            result = response.json()
            source = "Render"
        except requests.exceptions.RequestException:
            # 🔁 Fallback to Hugging Face Space
            try:
                response = requests.post(HF_SPACE_URL, files=files, data=data, timeout=30)
                response.raise_for_status()
                result = response.json()
                source = "Hugging Face Space"
            except Exception as e:
                st.error(f"❌ Both backends failed: {str(e)}")
                st.stop()

        # ✅ Show result
        st.success(f"✅ Classification Complete via {source}")
        st.write(f"**Category:** {result.get('category', 'Unknown')}")
        st.write(f"**Department:** {result.get('department', 'Unknown')}")
else:
    st.caption("Upload an image and enter a description to begin.")