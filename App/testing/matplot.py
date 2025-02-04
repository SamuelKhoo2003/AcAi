import requests
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

from App.server.datatypes import Node
from App.server.semantic_scholar import find_most_relevant_paper, get_influential_papers

# Semantic Scholar API endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def get_references(paper_id: str):
    """Retrieve the list of references (citations used) in the given paper."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "references.title,references.authors,references.year,references.url"}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"
    
    data = response.json()
    
    if "references" in data:
        references = [
            {
                "title": ref.get("title", "Unknown"),
                "authors": [author["name"] for author in ref.get("authors", [])],
                "year": ref.get("year", "N/A"),
                "url": ref.get("url", ""),
                "citationCount": ref.get("citationCount", 0)
            }
            for ref in data["references"]
        ]
        
        # Sort references by citation count in descending order
        references_sorted = sorted(references, key=lambda x: x["citationCount"], reverse=True)

        # Return top 5 references
        return references_sorted[:5]
    
    return []

def build_graph(knowledge_graph: dict, start_node: Node, depth: int = 3):
    if depth == 0:
        return

    if start_node:
        references: list[Node] = get_influential_papers(start_node.paper_id)

        for ref in references:
            knowledge_graph[start_node].append(ref)
            build_graph(knowledge_graph, ref, depth - 1)

def plot_citation_graph(citation_dict):
    """
    Plots a directed graph where nodes are paper titles, and edges represent citations.
    
    Args:
    citation_dict (dict): A dictionary where keys are paper titles and values are lists of cited paper titles.
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges from the dictionary
    for paper, citations in citation_dict.items():
        for cited_paper in citations:
            G.add_edge(paper.name, cited_paper.name)
    
    # Set figure size
    plt.figure(figsize=(12, 8))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='skyblue', edgecolors='black')
    
    # Draw edges with arrows
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray', width=1.5)
    
    # Add labels with smaller font size for clarity
    nx.draw_networkx_labels(G, pos, font_size=5, font_color='black', font_weight='bold')
    
    # Remove axis
    plt.axis('off')
    
    # Add title
    plt.title("Citation Graph", fontsize=15)
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    knowledge_graph = defaultdict(list)

    topic = "Gaussian Splatting"
    most_relevant_paper = find_most_relevant_paper(topic)
    build_graph(knowledge_graph, most_relevant_paper, depth=3)
    print(f'{knowledge_graph=}')
    plot_citation_graph(knowledge_graph)