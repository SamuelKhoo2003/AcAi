import os
import requests
import streamlit as st

from App.server.constants import BACKEND_URL

def get_image_paths(path = "generated_images"):
    """Return a list of absolute path images in folder"""

    image_paths = []
    for file in os.listdir(path):
        if file.endswith(".png"):
            absolute_path = os.path.abspath(os.path.join(path, file))
            image_paths.append(absolute_path)

    return image_paths

def gen_summary():
    """Calls endpoint and generates a summary of the experiment."""
    URL = f"{BACKEND_URL}/generate_summary"

    plan = st.session_state.streamed_text
    code = st.session_state.code_snippet
    image_paths = get_image_paths()
    output = st.session_state.code_output

    data = {
        "plan": plan,
        "code": code,
        "image_paths": image_paths,
        "output": output
    }
    print(data)

    st.write("#### Insights")

    try:
        response = requests.post(URL, json=data)

        if response.status_code == 200:
            st.write(response.text)
        else:
            st.write("Failed to generate summary.")
    except Exception as e:
        st.write(f"Error: {e}")
