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
