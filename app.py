"""Chainlit chat UI for the Lovecraft bestiary agent.

Run with:  uv run chainlit run app.py -w
"""

from __future__ import annotations

import re

import chainlit as cl
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableConfig

from lovecraft.agent import build_agent
from lovecraft.database import ensure_database

# Matches the path that plot_encyclopedia reports back, e.g. outputs/<hex>.png
_PLOT_PATH_RE = re.compile(r"[\w./\\:-]*outputs[/\\][0-9a-f]+\.png")

WELCOME = (
    "**The Bestiary of the Old Ones** awaits your questions. \n\n"
    "Ask about Lovecraft's entities and the tales they haunt — for example:\n"
    "- *Summarize the Outer Gods.*\n"
    "- *Which entities appear in The Call of Cthulhu?*\n"
    "- *Plot the five tallest entities by height.*\n"
    "- *How many entities are there per classification?*"
)


@cl.on_chat_start
async def on_chat_start() -> None:
    ensure_database()
    cl.user_session.set("agent", build_agent())
    cl.user_session.set("history", [])
    await cl.Message(content=WELCOME).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    agent = cl.user_session.get("agent")
    history = cl.user_session.get("history")
    history.append(HumanMessage(content=message.content))

    # The Chainlit callback handler renders the agent's tool calls and reasoning
    # as collapsible steps while the run is in flight.
    config = RunnableConfig(callbacks=[cl.LangchainCallbackHandler()])
    state = await agent.ainvoke({"messages": history}, config=config)

    messages = state["messages"]
    cl.user_session.set("history", messages)

    # Collect any charts produced by plot_encyclopedia during this run.
    elements: list[cl.Image] = []
    for msg in messages[len(history) - 1 :]:
        if isinstance(msg, ToolMessage) and msg.name == "plot_encyclopedia":
            match = _PLOT_PATH_RE.search(str(msg.content))
            if match:
                elements.append(
                    cl.Image(path=match.group(0), name="chart", display="inline")
                )

    # The final assistant turn is the last AIMessage with text content.
    answer = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and isinstance(msg.content, str) and msg.content:
            answer = msg.content
            break

    await cl.Message(content=answer, elements=elements).send()
