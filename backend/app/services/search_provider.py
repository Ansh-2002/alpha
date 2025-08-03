import os
import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json

class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        pass

class MockSearchProvider(SearchProvider):
    def search(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        mock_results = [
            {
                "title": f"Mock Result 1 for '{query}'",
                "url": f"https://example.com/result1?q={query.replace(' ', '+')}",
                "snippet": f"This is a mock search result for the query '{query}'. It contains relevant information about the search term."
            },
            {
                "title": f"Mock Result 2 for '{query}'",
                "url": f"https://example.com/result2?q={query.replace(' ', '+')}",
                "snippet": f"Another mock result for '{query}' with different information that might be useful for research."
            },
            {
                "title": f"Mock Result 3 for '{query}'",
                "url": f"https://example.com/result3?q={query.replace(' ', '+')}",
                "snippet": f"A third mock search result for '{query}' providing additional context and details."
            }
        ]
        return mock_results[:num_results]

class SerpAPIProvider(SearchProvider):
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_KEY environment variable is required")
    
    def search(self, query: str, num_results: int = 3) -> List[Dict[str, Any]]:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": num_results
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for result in data.get("organic_results", [])[:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
            
            return results
        except Exception as e:
            print(f"Error in SerpAPI search: {e}")
            return []

def get_search_provider() -> SearchProvider:
    if os.getenv("USE_REAL_SEARCH") == "true":
        try:
            return SerpAPIProvider()
        except ValueError:
            print("SerpAPI key not found, falling back to mock provider")
            return MockSearchProvider()
    else:
        return MockSearchProvider()