import requests
import os
import networkx as nx
import anthropic
import matplotlib.pyplot as plt
import json


# Set up API keys (replace with your actual keys)
SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"

def find_most_relevant_paper(query):
    print("Search Semantic Scholar for the most relevant paper on a topic.")
    url = f"{SEMANTIC_SCHOLAR_BASE}/paper/search"
    params = {
        "query": query,
        "fields": "title,url,year,citationCount,paperId",
        "limit": 1  # Get the top result
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        top_paper = data["data"][0]
        return {
            "title": top_paper.get("title", "Unknown"),
            "url": top_paper.get("url", ""),
            "year": top_paper.get("year", "N/A"),
            "citationCount": top_paper.get("citationCount", 0),
            "paperId": top_paper.get("paperId", None)
        }
    
    return None

CLAUDE_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# try:
#     available_models = client.models.list()
#     print(available_models)
# except Exception as e:
#     print(f"Error retrieving models: {e}")


def analyze_paper_relevance_claude(paper):
    print("Use Claude to analyze and rank the most influential references.")
    
    prompt = f"""
    The following research paper is highly relevant:
    Title: {paper['title']}
    Year: {paper['year']}
    Citation Count: {paper['citationCount']}

    Please analyze and rank the **top 3 most important references** that likely had the greatest influence on this paper. 
    Consider their year, relevance to the field, and conceptual importance.
    
    Return your response in this structured JSON format:
    ```json
    {{
        "important_references": [
            {{"title": "Title 1", "reason": "Brief reasoning"}},
            {{"title": "Title 2", "reason": "Brief reasoning"}},
            {{"title": "Title 3", "reason": "Brief reasoning"}}
        ]
    }}
    ```
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use "claude-3" if available
        max_tokens=1024,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract structured JSON response from Claude
    try:
        response_text = response.content[0].text.strip()
        important_references = json.loads(response_text)["important_references"]
        return [ref["title"] for ref in important_references]  # Return ranked paper titles
    
    except Exception as e:
        print(f"Error parsing Claude response: {e}")
        return []

topic = "Gaussian Splatting"
most_rel_paper = find_most_relevant_paper(topic)
layer1 = analyze_paper_relevance_claude(most_rel_paper)

print(layer1)

