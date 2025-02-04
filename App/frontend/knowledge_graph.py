import requests
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
import streamlit as st
import json
import matplotlib.pyplot as plt
from App.server.datatypes import Node
from App.server.semantic_scholar import find_most_relevant_paper, get_influential_papers

# Semantic Scholar API endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def build_graph(knowledge_graph: dict, start_node: Node, depth: int = 3, node_metadata=None):
    """Recursively builds a citation graph up to the specified depth."""
    print("Building graph")
    if depth == 0:
        return

    references = get_influential_papers(start_node.paper_id)

    # Store metadata for the starting paper
    if node_metadata is not None and str(start_node) not in node_metadata:
        node_metadata[str(start_node)] = {
            "title": start_node.name,
            "author": start_node.authors,
            "abstract": start_node.abstract,
            "year": str(start_node.year) if hasattr(start_node, "year") else "N/A"
        }

    for ref in references:
        key = str(start_node)
        if key not in knowledge_graph:
            knowledge_graph[key] = []

        knowledge_graph[key].append(str(ref))

        # Store metadata for the reference
        if node_metadata is not None and str(ref) not in node_metadata:
            node_metadata[str(ref)] = {
                "title": ref.name,
                "author": ref.authors,
                "abstract": ref.abstract,
                "year": str(ref.year) if hasattr(ref, "year") else "N/A"
            }

        # Recursively build the graph for the reference
        build_graph(knowledge_graph, ref, depth - 1, node_metadata)

def plot_citation_graph_streamlit(citation_dict, node_metadata):
    """Generates and stores citation graph HTML in session state for persistence."""
    G = nx.DiGraph()
    for paper, citations in citation_dict.items():
        G.add_node(paper)
        for cited_paper in citations:
            G.add_node(cited_paper)
            G.add_edge(paper, cited_paper)

    net = Network(notebook=False, directed=True)
    
    # Configure the network
    net.set_options(""" 
        var options = {
          "nodes": {
            "shape": "dot",
            "size": 40,
            "font": {
                "size": 14,
                "face": "arial",
                "multi": true,
                "align": "center"
            }
          },
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": false
          },
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -150,
              "springLength": 200
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
    """)

    for node in G.nodes:
        meta = node_metadata.get(node, {})
        title_text = meta.get("title", node)
        author = meta.get("author", "Unknown")
        abstract = meta.get("abstract", "Unknown")
        year = meta.get("year", "Unknown")

        abstract_chunks = [abstract[i:i+100] for i in range(0, len(abstract), 100)]
        formatted_abstract = '\n'.join(abstract_chunks)

        label = f"{title_text[:30]}..." if len(title_text) > 30 else title_text
        hover_text = f"{title_text}\nAuthor: {author}\nYear: {year}\nAbstract: {formatted_abstract}..."
        net.add_node(node, label=label, title=hover_text)

    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Save HTML to session state
    html_path = "citation_graph.html"
    net.write_html(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.session_state.citation_graph_html = html_content  # Store HTML persistently

def knowledge_graph_frontend():
    # Ensure session state is initialized
    if "selected_paper_data" not in st.session_state:
        st.session_state.selected_paper_data = {"data": []}
    if "selected_titles" not in st.session_state:
        st.session_state.selected_titles = []
    if "knowledge_graph" not in st.session_state:
        st.session_state.knowledge_graph = None
    if "node_metadata" not in st.session_state:
        st.session_state.node_metadata = None

    # Streamlit UI
    st.title("Knowledge Graph")

    topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

    # Generate Graph Button
    if st.button("Generate Graph"):
        with st.spinner("Generating citation graph..."):
            most_relevant_paper = find_most_relevant_paper(topic)
            knowledge_graph = defaultdict(list)
            node_metadata = {}

            build_graph(knowledge_graph, most_relevant_paper, depth=2, node_metadata=node_metadata)

            st.session_state.knowledge_graph = knowledge_graph
            st.session_state.node_metadata = node_metadata

            plot_citation_graph_streamlit(knowledge_graph, node_metadata)  # Generate and store graph

    # Display the Graph If It Exists
    if "citation_graph_html" in st.session_state:
        st.components.v1.html(st.session_state.citation_graph_html, height=600)

    # Ensure graph exists before displaying paper selection
    if st.session_state.knowledge_graph and st.session_state.node_metadata:
        st.subheader("Select Papers to View Abstracts")

        paper_options = {meta["title"]: meta for meta in st.session_state.node_metadata.values()}

        # Ensure default selection
        if not st.session_state.selected_titles and paper_options:
            st.session_state.selected_titles = [list(paper_options.keys())[0]]

        # **Add logic to handle session state properly**
        selected_titles = st.multiselect(
            "Choose at least one paper:",
            list(paper_options.keys()),
            # default=st.session_state.selected_titles # CAUSES GHOSTING ERROR!
        )

        # Only update session state if the selections have changed
        if selected_titles != st.session_state.selected_titles:
            st.session_state.selected_titles = selected_titles  # Sync with multiselect

        # Ensure deselected papers are removed
        st.session_state.selected_paper_data["data"] = [
            {"title": title, "abstract": paper_options[title].get("abstract", "No abstract available.")}
            for title in selected_titles
        ]

        # Warn if no papers are selected
        if not selected_titles:
            st.warning("Please select at least one paper to view abstracts.")

        # Make the Selected Papers Section Scrollable
        st.subheader("Selected Papers and Abstracts")

        for entry in st.session_state.selected_paper_data["data"]:
            st.markdown(f"**{entry['title']}**")
            st.markdown(f"**Abstract:** {entry['abstract']}")
            st.markdown("---")

        # # Display JSON representation
        # st.subheader("Selected Papers JSON")
        # st.json(st.session_state.selected_paper_data)

        # Disable "Next" button if no papers are selected
        next_disabled = not bool(selected_titles)
        if st.button("Next / Generate Ideas", disabled=next_disabled):
            # st.subheader("Final Selected Papers")
            # st.write(json.dumps(st.session_state.selected_paper_data, indent=4))
            st.session_state.knowledge_graph_complete = True

