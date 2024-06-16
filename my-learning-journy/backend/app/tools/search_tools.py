import json
import os
import requests
from langchain.tools import tool

class SearchTools:

    @tool("Search the internet")
    def search_internet(query):
        """Search the internet for books, eBooks, and PDFs on the given subject and return relevant links."""
        enhanced_query = f"{query} site:goodreads.com OR site:github.com OR site:medium.com OR site:reddit.com"
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": enhanced_query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload)
        
        if 'organic' not in response.json():
            return "Sorry, I couldn't find anything about that, there could be an error with your Serper API key."
        
        results = response.json()['organic']
        links = [result['link'] for result in results if 'link' in result]
        
        return links

def get_search_results(query):
    search_tool = SearchTools()
    return search_tool.search_internet.invoke(query)
