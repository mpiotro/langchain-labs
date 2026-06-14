"""Smoke test: confirm LangChain can reach Claude via the Anthropic API.

Run with: uv run hello_claude.py
Requires a project-scoped .env containing ANTHROPIC_API_KEY=sk-ant-...
"""

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()  # reads ANTHROPIC_API_KEY from .env (project-scoped)

# Default to the latest, most capable model. ChatAnthropic reads
# ANTHROPIC_API_KEY from the environment automatically.
# Cheaper alternatives: "claude-sonnet-4-6", "claude-haiku-4-5".
llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=4096)

resp = llm.invoke("In one sentence, what is LangChain?")
print(resp.content)
