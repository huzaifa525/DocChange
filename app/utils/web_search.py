from duckduckgo_search import DDGS
from typing import List

class WebSearchTool:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 3) -> List[str]:
        try:
            results = []
            for r in self.ddgs.text(query, max_results=max_results):
                results.append(f"Title: {r['title']}\nContent: {r['body']}")
            return results
        except Exception as e:
            return []