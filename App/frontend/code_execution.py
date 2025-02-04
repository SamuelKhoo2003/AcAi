import streamlit as st
import sys
import io
import os
import requests
from App.server.constants import BACKEND_URL
# import matplotlib.pyplot as plt
# import numpy as np

# Set page layout to wide
# st.set_page_config(layout="wide")

# Define the images folder path
IMAGES_FOLDER = "generated_images"

# Ensure the 'images' folder exists
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

# def fetch_code_snippet():
#     return """import numpy as np
# import matplotlib.pyplot as plt
# import os

# # Define the images folder path
# IMAGES_FOLDER = "generated_images"

# # Create data for 4 different graphs
# x = np.linspace(0, 10, 100)

# # First graph: Sine wave
# y1 = np.sin(x)
# plt.plot(x, y1)
# plt.title('Sine Wave')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.savefig(os.path.join(IMAGES_FOLDER, 'graph1.png'))
# plt.close()  # Close the plot to free memory
# print("Graph 1 (Sine Wave) saved.")

# # Second graph: Cosine wave
# y2 = np.cos(x)
# plt.plot(x, y2)
# plt.title('Cosine Wave')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.savefig(os.path.join(IMAGES_FOLDER, 'graph2.png'))
# plt.close()
# print("Graph 2 (Cosine Wave) saved.")

# # Third graph: Tangent wave
# y3 = np.tan(x)
# plt.plot(x, y3)
# plt.title('Tangent Wave')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.ylim(-10, 10)  # Limit y-axis for better visualization
# plt.savefig(os.path.join(IMAGES_FOLDER, 'graph3.png'))
# plt.close()
# print("Graph 3 (Tangent Wave) saved.")

# # Fourth graph: Exponential growth
# y4 = np.exp(x)
# plt.plot(x, y4)
# plt.title('Exponential Growth')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.savefig(os.path.join(IMAGES_FOLDER, 'graph4.png'))
# plt.close()
# print("Graph 4 (Exponential Growth) saved.")

# print("Matplotlib is DONE!")"""

def fetch_code_snippet():
    """Fetch generated code snippet from the backend based on the experiment plan."""
    try:
        # Send a request to the backend to generate the code
        response = requests.post(f"{BACKEND_URL}/generate_code", json={"plan":st.session_state.streamed_text})
        
        if response.status_code == 200:
            # Return the generated code as a string
            return "\n".join(response.text.split('\n')[1:-1])
        else:
            st.error(f"Error: Unable to fetch code (Status code: {response.status_code})")
            return ""
    except Exception as e:
        st.error(f"Error: {e}")
        return ""

def execute_code(code):
    """Executes the given Python code and captures the output."""
    output_buffer = io.StringIO()
    try:
        # Redirect stdout to capture print statements
        sys.stdout = output_buffer
        
        # Execute the provided Python code
        exec(code, {})
        
        # Get the printed output and store it in session state
        output_text = output_buffer.getvalue()
    except Exception as e:
        output_text = f"Error: {e}"
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout

    return output_text

def display_code_ide(code):
    st.markdown("## Code Execution")
    st.markdown("""
        <style>
            .stColumns {
                display: flex;
                align-items: stretch;  /* Makes columns the same height */
            }
            .code-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .code-header h4 {
                margin: 0;
            }
            # .stButton {
            #     display: flex;
            #     justify-content: center;
            # }
            # .stButton > button {
            #     background-color: #4CAF50;
            #     color: white;
            #     border: none;
            #     padding: 5px 10px;
            #     cursor: pointer;
            #     border-radius: 5px;
            #     font-size: 14px;
            # }
            # .stButton > button:hover {
            #     background-color: #45a049;
            # }
            # .button-container {
            #     display: flex;
            #     justify-content: flex-end;  /* Right-aligns the button */
            # }
            /* Set st.code height equal to st.text_area */
            .stCodeBlock {
                height: 400px !important;
                overflow-y: auto;
            }
            pre {
                height: 50vh !important;
                overflow-y: auto;  /* Enable scrolling inside the code block */
            }
            /* Remove extra padding/margin above the text area */
            textarea, .stTextArea label {
                margin-top: 0px !important;
                padding-top: 0px !important;
            }
            .stTextArea label {
                display: none;  /* Completely hide any label above the text area */
            }
        </style>
    """, unsafe_allow_html=True)
    # Ensure session state variable is initialized
    if "code_output" not in st.session_state:
        st.session_state["code_output"] = ""
    
    container = st.container()
    with container:
        col1, col2 = st.columns([1, 1])  # Adjust column width for better layout
        
        with col1:
            st.markdown("""<div class="code-header"><h4>Python Code:</h4></div>""", unsafe_allow_html=True)

            st.code(code, language="python", line_numbers=True)
            if st.button("Run Code"):
                st.session_state["code_output"] = execute_code(code)

        
        with col2:
            st.markdown("#### Output:")
            # Display the output text (either print statements or errors)
            st.text_area("", st.session_state.get("code_output", ""), height=400, label_visibility="collapsed")

def check_images_generated():
    """Check if there are any images in the images folder."""
    # List all .png files in the 'images' folder
    image_files = [f for f in os.listdir(IMAGES_FOLDER) if f.endswith('.png')]
    return len(image_files) > 0  # Returns True if images are found

def display_images():
    # Get list of image filenames in the images folder
    image_urls = [os.path.join(IMAGES_FOLDER, filename) for filename in os.listdir(IMAGES_FOLDER) if filename.endswith('.png')]

    st.markdown("## Images:")
    num_images = len(image_urls)
    num_columns_per_row = 3

    # Display images
    for i in range(0, num_images, num_columns_per_row):
        cols = st.columns(num_columns_per_row)
        for j in range(num_columns_per_row):
            if i + j < num_images:
                with cols[j]:
                    st.image(image_urls[i + j], width=400)

# st.title("Knowledge Graph Viewer")
def code_execution_frontend():
# # Fetch Python code and display the IDE
    code_snippet = fetch_code_snippet()

    st.session_state.code_snippet = code_snippet
    display_code_ide(code_snippet)
    images_generated = check_images_generated()
    if images_generated:
        display_images()

    st.session_state.code_execution_complete = True