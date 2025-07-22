"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function and Wikidata query functionality

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

from langchain_community.tools.wikidata.tool import WikidataQueryRun
from langchain_community.utilities.wikidata import WikidataAPIWrapper
from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

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


TOOLS: List[Callable[..., Any]] = [search, wikidata_query]
