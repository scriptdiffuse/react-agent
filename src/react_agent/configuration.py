"""Define the configurable parameters for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from typing import Annotated

from langchain_core.runnables import ensure_config
from langgraph.config import get_config

from react_agent import prompts


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20240620",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )
#Tavily search configuration
    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )
#Wikidata query configuration

# Toolbox MCP configuration

# Search Servers configuration
    mcp_search_query: str = field(
        default="",
        metadata={
            "description": "The search query for finding MCP servers. This can be keywords, a server name, or a short description of the desired capability."
    },
)

    mcp_search_results: int = field(
        default=5,
        metadata={
            "description": "The maximum number of MCP server search results to return. Default is 3, maximum is 5."
    },
)

# Use Tool configuration
    mcp_server_qualified_name: str = field(
        default="",
        metadata={
            "description": "The unique qualified name of the MCP server to use, as returned by the search_servers tool."
    },
)

    mcp_tool_name: str = field(
        default="",
        metadata={
            "description": "The name of the tool to call on the selected MCP server."
    },
)


    @classmethod
    def from_context(cls) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        try:
            config = get_config()
        except RuntimeError:
            config = None
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})
