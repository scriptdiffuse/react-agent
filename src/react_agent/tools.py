"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function, Wikidata query functionality, 
and Smithery MCP toolbox integration for access to 6000+ tools.

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

import os
from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.wikidata.tool import WikidataQueryRun
from langchain_community.utilities.wikidata import WikidataAPIWrapper
from langchain_tavily import TavilySearch  # type: ignore[import-not-found]
from mcpadapt.core import MCPAdapt
from mcpadapt.langchain_adapter import LangChainAdapter

from react_agent.configuration import Configuration


async def search(query: str) -> Optional[dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events.
    """
    configuration = Configuration.from_context()
    wrapped = TavilySearch(max_results=configuration.max_search_results)
    return cast(dict[str, Any], await wrapped.ainvoke({"query": query}))


async def wikidata_query(entity: str) -> Optional[str]:
    """Query Wikidata for information about entities.

    This function performs a query using the Wikidata API to retrieve structured
    information about people, places, companies, facts, historical events, or other
    subjects. Input should be the exact name of the item you want information about
    or a Wikidata QID (e.g., 'Q42' for Douglas Adams).
    """
    api_wrapper = WikidataAPIWrapper()
    wikidata_tool = WikidataQueryRun(api_wrapper=api_wrapper)
    return cast(Optional[str], await wikidata_tool.ainvoke(entity))


async def get_smithery_toolbox() -> Optional[List[Any]]:
    """Connect to Smithery's dynamic toolbox for access to 6000+ tools.
    
    This function connects to Smithery's MCP toolbox server which provides 
    access to thousands of tools across various domains including productivity,
    development, data analysis, and more. Requires SMITHERY_API_KEY environment variable.
    """
    smithery_api_key = os.environ.get('SMITHERY_API_KEY')
    if not smithery_api_key:
        raise ValueError("SMITHERY_API_KEY environment variable is required")
    
    # Smithery toolbox connection parameters
    server_config = {
        "url": "https://server.smithery.ai/@smithery/toolbox/mcp",
        "headers": {
            "Authorization": f"Bearer {smithery_api_key}",
            "Content-Type": "application/json"
        }
    }
    
    try:
        # Use MCPAdapt to connect to Smithery's toolbox with LangChain adapter
        with MCPAdapt(
            server_config,
            LangChainAdapter(),
        ) as tools:
            return cast(Optional[List[Any]], tools)
    except Exception as e:
        # Log error but don't crash the agent
        print(f"Warning: Failed to connect to Smithery toolbox: {e}")
        return None


TOOLS: List[Callable[..., Any]] = [search, wikidata_query, get_smithery_toolbox]
