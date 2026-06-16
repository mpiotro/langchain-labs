# langchain-labs

Experiments using [LangChain](https://python.langchain.com) with Anthropic's
Claude models.

## How auth works here

Claude Code and LangChain use **two independent auth/billing systems**:

- **Claude Code** (the coding assistant) runs on your Claude Pro/Max
  subscription.
- **LangChain** talks to Claude through the **Anthropic API**, which needs an API
  key from [console.anthropic.com](https://console.anthropic.com), billed
  per-token. A Claude.ai subscription cannot be used by LangChain.

The API key lives in a project-scoped `.env` (git-ignored) and is read only by
the Python code via `python-dotenv` — not by Claude Code. Keep the key out of
your global shell environment, or Claude Code would bill the API instead of your
subscription.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```sh
# 1. Install dependencies (creates .venv from pyproject.toml / uv.lock)
uv sync

# 2. Create your local .env with an Anthropic API key
cp .env.example .env
# then edit .env and paste your real sk-ant-... key
```

Get the API key at [console.anthropic.com](https://console.anthropic.com): sign
in, add billing/credits, then create a key under **API Keys**.

## Run the smoke test

```sh
uv run hello_claude.py
```

A one-sentence answer confirms the key, billing, and provider wiring all work.
- `401` → the key is wrong or missing.
- billing `400` → the Console account has no credit.

## Model selection

`hello_claude.py` uses a Claude model id directly. Swap it for your needs:

| Model id            | Use for                          |
| ------------------- | -------------------------------- |
| `claude-opus-4-8`   | Most capable (default)           |
| `claude-sonnet-4-6` | Balanced cost/speed, high volume |
| `claude-haiku-4-5`  | Fastest / cheapest               |

## Lovecraft bestiary chat

An agentic chat app over a local DuckDB "encyclopedia" of H.P. Lovecraft beasts and
alien entities. The agent (LangChain + Claude) answers questions in natural language by
querying the database, and can plot data on request.

```
lovecraft/
  database.py    # DuckDB schema + idempotent seeding + read-only query guard
  seed_data.py   # curated entities and their story/book appearances
  tools.py       # agent tools: describe_schema, query_encyclopedia, plot_encyclopedia
  agent.py       # builds the agent (claude-sonnet-4-6 by default)
app.py           # Chainlit chat UI
```

### Run it

```sh
# 1. Install dependencies (adds duckdb, chainlit, matplotlib)
uv sync

# 2. Build the database (also happens automatically on first chat)
uv run python -m lovecraft.database

# 3. Launch the chat UI (-w auto-reloads on code changes)
uv run chainlit run app.py -w
```

Then open the browser tab Chainlit prints and try:

- *Summarize the Outer Gods.*
- *Which entities appear in The Call of Cthulhu?*
- *Plot the five tallest entities by height.*
- *How many entities are there per classification?*

Notes:

- The agent's database access is **read-only** — `lovecraft/database.run_select` rejects
  anything that isn't a single `SELECT`/`WITH`, so the encyclopedia can't be modified
  from chat.
- Generated charts land in `outputs/` and the `data/lovecraft.duckdb` file is created on
  demand; both are git-ignored.
- Uses `claude-sonnet-4-6` by default. Change `MODEL` in `lovecraft/agent.py` to
  `claude-opus-4-8` for the most capable reasoning.
- Extend the bestiary by editing `lovecraft/seed_data.py`, then delete
  `data/lovecraft.duckdb` (or it reseeds only when empty) and re-run step 2.
