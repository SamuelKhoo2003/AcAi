import requests
import time
import streamlit as st
from App.server.constants import BACKEND_URL

# Initialize session state for streamed text
if "streamed_text" not in st.session_state:
    st.session_state.streamed_text = ""
if "text_buffer" not in st.session_state:
    st.session_state.text_buffer = ""

def experiment_outline_frontend():
    st.session_state.setdefault('streamed_text', "")
    st.session_state.setdefault('text_buffer', "")

    # Custom CSS for height and button positioning
    st.markdown("""
        <style>
            .text-area {
                height: 70vh !important;
            }
            .stButton > button {
                padding: 0.5em 2em;
                font-size: 1.2rem;
                min-width: 150px;
                transition: all 0.2s ease;
            }
            .stButton > button:hover {
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("#### Experiment Outline")

    # Text Area with streamed content (replaced with markdown display)
    dynamic_container = st.empty()

    # Initially render the content with the current streamed text
    dynamic_container.markdown(st.session_state.streamed_text, unsafe_allow_html=True)

    if st.session_state.streamed_text == "":
        stream_claude_section("Experiment Outline", dynamic_container)

    # Button for Regenerating the outline
    _, regen_btn, _, cont_btn, _ = st.columns([5, 4, 1, 4, 5])

    with regen_btn:
        if st.button("Regenerate"):
            st.session_state.streamed_text = ""
            stream_claude_section("Regenerate", dynamic_container)
            

    with cont_btn:
        if st.button("Continue"):
            st.session_state.experiment_outline_complete = True

def stream_claude_section(section_text, dynamic_container):
    # Reset the streamed text and text buffer
    st.session_state.streamed_text = ""
    st.session_state.text_buffer = ""

    # Replace this with your actual Claude streaming API endpoint
    url = f"{BACKEND_URL}/generate_outline"  # Example endpoint
    
    payload = st.session_state.selected_paper_data
    response = requests.post(url, json=payload, stream=True)
    
    if response.status_code == 200:
        # Temporary variable to accumulate text
        temp_text = ""

        # Stream and update the content line-by-line in the dynamic container
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')

                # Append the line to the text buffer
                st.session_state.text_buffer += decoded_line + "\n"

                # Markdown-compatible unique key for each update (e.g., adding a timestamp)
                unique_key = f"experiment_outline_{time.time()}"  # Unique key based on timestamp

                # Update the dynamic container with the new streamed text
                dynamic_container.markdown(
                    st.session_state.streamed_text + st.session_state.text_buffer, 
                    unsafe_allow_html=True  # To allow markdown and other formatting
                )

                # Optionally, simulate a small delay to allow for smoother updates
                time.sleep(0.2)  # You can adjust this delay based on your desired speed

        # If any leftover text remains in the buffer, display it
        if st.session_state.text_buffer:
            st.session_state.streamed_text += st.session_state.text_buffer
            dynamic_container.markdown(
                st.session_state.streamed_text, 
                unsafe_allow_html=True  # To allow markdown and other formatting
            )

    else:
        st.error("Error: Unable to stream from Claude API.")
