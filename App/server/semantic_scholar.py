import requests
from requests import get
import time

from App.server.datatypes import Node

#Semantic Scholar 
SS_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
SS_PAPER_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/"

def fetch_paper_details(paper_id, retries=5, delay=3):
    api_url = f"https://api.semanticscholar.org/v1/paper/{paper_id}/?citedSort=is-influential"
    
    for attempt in range(retries):
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return response.json()  # Successfully retrieved data
        
        elif response.status_code == 202:
            print(f"Attempt {attempt+1}: Data is being processed. Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
        
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None  # Stop on unexpected errors
    
    print("Max retries reached. Could not fetch paper details.")
    return None

def find_most_relevant_paper(query) -> Node:
    print("Search Semantic Scholar for the most relevant paper on a topic.")
    url = f"{SS_BASE_URL}"
    params = {
        "query": query,
        "fields": "title,url,year,authors,abstract,paperId",
        "limit": 1  # Get the top result
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        top_paper = data["data"][0]
        paper_id = top_paper.get("paperId", None)

        if paper_id: 
            paper_details = fetch_paper_details(paper_id)
            if paper_details:
                abstract = paper_details.get("abstract", "No abstract available")
        
        return Node(
            name=top_paper.get("title", "Unknown"),
            url=top_paper.get("url", ""),
            year=str(top_paper.get("year", "Unknown")),
            authors=top_paper.get("authors", [{}])[0].get("name", "Unknown"),
            abstract=abstract,
            paper_id=paper_id
        )
    
    print("No relevant paper found.")
    return None


def get_influential_papers(paper_id) -> list[Node]:
    details = fetch_paper_details(paper_id)
    if details is None:
        raise Exception("Not found")
    
    influential_papers = []
    
    # Take the first 5 references (if available)
    for reference in details.get("references", [])[:2]:
        ref_paper_id = reference.get("paperId", None)
        abstract = "No abstract available"  # Default value

        # Fetch the full details of the referenced paper (including abstract)
        if ref_paper_id:
            reference_details = fetch_paper_details(ref_paper_id)
            if reference_details:
                abstract = reference_details.get("abstract", "No abstract available")
        
        # Create a Node for the influential paper
        influential_papers.append(
            Node(
                name = reference.get("title", "Unknown"),
                url = reference.get("url", ""),
                authors = reference.get("authors", [{}])[0].get("name", "Unknown"),
                year = reference.get("year", "Unknown"),
                abstract = abstract,
                paper_id = ref_paper_id
            )
        )
    
    return influential_papers

def main():
    topic = "computer vision"
    most_relevant_paper = find_most_relevant_paper(topic)
    print(most_relevant_paper)
    influential_papers = get_influential_papers(most_relevant_paper.paper_id)
    print(influential_papers)

if __name__ == "__main__":
    main()

#https://www.semanticscholar.org/paper/3D-Gaussian-Splatting-for-Real-Time-Radiance-Field-Kerbl-Kopanas/2cc1d857e86d5152ba7fe6a8355c2a0150cc280a?citedSort=is-influential