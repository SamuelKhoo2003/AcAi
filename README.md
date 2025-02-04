# AcAi

AcAi (Academic AI) is a comprehensive tool designed to assist researchers and academics in generating, analyzing, and visualizing research papers and their citations. The project leverages various technologies and frameworks to provide an interactive and user-friendly interface for academic research.

## Project Framework

The project is built using the following frameworks and technologies:

- **Streamlit**: A powerful framework for creating interactive web applications in Python. Streamlit is used to build the frontend of the application, providing a seamless and interactive user experience.
- **NetworkX**: A Python library for the creation, manipulation, and study of complex networks of nodes and edges. It is used to build and analyze citation graphs.
- **PyVis**: A Python library that integrates with NetworkX to visualize networks in a web browser. It is used to render interactive citation graphs.
- **Matplotlib**: A plotting library for the Python programming language and its numerical mathematics extension NumPy. It is used to generate and save plots and images.
- **Requests**: A simple HTTP library for Python, used to make API calls to external services like Semantic Scholar.
- **Anthropic Claude**: An AI model used to analyze and rank the most influential references for a given research paper.

## Features

- **Knowledge Graph Generation**: Automatically generate a citation graph for a given research topic using the Semantic Scholar API.
- **Experiment Outline**: Generate an experimental outline based on selected research papers.
- **Code Execution**: Execute generated code snippets and display the output.
- **Summary Generation**: Generate a summary of the experiment, including insights and results.

## Usage

1. **Knowledge Graph**: Enter a research topic to generate a citation graph.
2. **Experiment Outline**: Generate an experimental outline based on the selected papers.
3. **Code Execution**: Execute the generated code snippets and view the results.
4. **Summary**: Generate a summary of the experiment, including insights and results.

## Demo

Below are some images and a video demonstrating the features of AcAi:

### Images
![Knowledge Graph](Extras\readme_resources\knowledge_graph.jpg)
![Abstract Selection](Extras\readme_resources\abstraction_selection.jpg)
![Experiment Outline](Extras\readme_resources\experimental_outline.jpg)
![Code Execution](Extras\readme_resources\code_generation.jpg)
![Summary](Extras\readme_resources\experimental_insights.jpg)

### Video
![Demo Video](Extras\readme_resources\demo.mp4)

## Installation

To install and run the project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/SamuelKhoo2003/AcAi.git
    cd App
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```sh
    streamlit run App/frontend/app.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
