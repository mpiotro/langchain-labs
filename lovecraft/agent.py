"""Builds the Lovecraft bestiary agent: Claude (via LangChain) plus the database
and plotting tools, wired together with the LangChain 1.x ``create_agent`` API.
"""

from __future__ import annotations

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

from .database import get_schema_text
from .tools import TOOLS

# Test-phase model. Bump to "claude-opus-4-8" for the most capable text-to-SQL/reasoning.
MODEL = "claude-sonnet-4-6"


def _system_prompt() -> str:
    return (
        "You are the keeper of a bestiary of H.P. Lovecraft's beasts and alien "
        "entities, backed by a small DuckDB database. Answer questions about the "
        "entities and the stories they appear in.\n\n"
        "Rules:\n"
        "- Ground every factual claim in the database. Use `query_encyclopedia` to "
        "look things up; never invent entities, sizes, or story references.\n"
        "- Prefer aggregating and filtering in SQL over dumping many rows.\n"
        "- height_m and weight_kg are often NULL — say the size is unrecorded rather "
        "than guessing, and read `size_note` for the prose description.\n"
        "- When the user asks for a chart, comparison, or visualization, call "
        "`plot_encyclopedia`. It returns a saved-file path and the image is shown to "
        "the user automatically.\n"
        "- The database is read-only. If asked to add, change, or delete data, explain "
        "that you can only read the encyclopedia.\n"
        "- Write in a tone befitting the eldritch subject matter, but stay accurate.\n\n"
        "Database schema for reference:\n"
        f"{get_schema_text()}"
    )


def build_agent():
    """Create the bestiary agent. Reads ANTHROPIC_API_KEY from the project .env."""
    load_dotenv()
    model = ChatAnthropic(model=MODEL, max_tokens=4096)
    return create_agent(model, TOOLS, system_prompt=_system_prompt())
