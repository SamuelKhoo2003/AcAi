from dataclasses import dataclass

@dataclass
class Node:
    name: str
    url: str
    year: str
    authors: str
    abstract: str
    paper_id: str

    def __init__(self, name, url, authors, paper_id, abstract, year):
        self.name = name
        self.url = url
        self.paper_id = paper_id
        self.authors = authors
        self.abstract = abstract
        self.year = year

    def __repr__(self):
        return f"{self.name=}, {self.url=}, {self.year=},{self.authors=}, {self.abstract=}, {self.paper_id=}"

    def __hash__(self):
        return hash(self.name)