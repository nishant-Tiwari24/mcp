# math_server.py
...

# weather_server.py
from typing import List
from mcp.server.fastmcp import FastMCP
import requests
import xml.etree.ElementTree as ET

mcp = FastMCP("arxiv_server")


@mcp.tool()
async def search_arxiv(topic, max_results=5):
    """
    Search for arXiv papers related to a topic.

    Parameters:
        topic (str): The topic or keywords to search for.
        max_results (int): Number of results to retrieve.

    Returns:
        List of dictionaries with paper details (title, authors, summary, link).
    """
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{topic}&start=0&max_results={max_results}"
    response = requests.get(base_url + query)

    if response.status_code != 200:
        raise Exception("Failed to fetch results from arXiv API.")

    root = ET.fromstring(response.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        link = entry.find('atom:id', ns).text.strip()
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        papers.append({
            'title': title,
            'authors': authors,
            'summary': summary,
            'link': link
        })

    return papers


if __name__ == "__main__":
    mcp.run(transport="sse")
