"""LangChain tools the bestiary agent can call.

All three are read-only with respect to the database. ``plot_encyclopedia``
writes a PNG to ``outputs/`` and returns its path; the Chainlit layer turns that
path into an inline image.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: render to file, never open a window
import matplotlib.pyplot as plt  # noqa: E402
from langchain_core.tools import tool  # noqa: E402

from .database import get_schema_text, run_select  # noqa: E402

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
_CHART_TYPES = ("bar", "barh", "line", "scatter")


@tool
def describe_schema() -> str:
    """Return the database schema (tables, columns, notes) and a few example rows.

    Call this first when you are unsure how to shape a SQL query.
    """
    return get_schema_text()


@tool
def query_encyclopedia(sql: str) -> str:
    """Run a read-only SQL query against the Lovecraft DuckDB database and return rows.

    Only a single SELECT/WITH statement is allowed. Prefer aggregating in SQL over
    fetching many rows. Use the `entities` and `appearances` tables (see describe_schema).
    """
    try:
        rows = run_select(sql)
    except Exception as exc:  # surface the error to the model so it can fix the query
        return f"Query error: {exc}"
    if not rows:
        return "No rows returned."
    return json.dumps(rows, default=str, indent=2)


@tool
def plot_encyclopedia(
    sql: str, chart_type: str, x: str, y: str, title: str
) -> str:
    """Render a chart from a read-only SQL query and save it as a PNG.

    Args:
        sql: A SELECT/WITH query that returns the columns named by `x` and `y`.
        chart_type: One of "bar", "barh", "line", "scatter".
        x: Column name to use for the x-axis (categories or values).
        y: Column name to use for the y-axis (numeric values).
        title: Chart title.

    Returns a confirmation including the saved file path. The image is shown to the
    user automatically — do not ask them to open the file.
    """
    if chart_type not in _CHART_TYPES:
        return f"Unknown chart_type '{chart_type}'. Choose one of {_CHART_TYPES}."

    try:
        rows = run_select(sql)
    except Exception as exc:
        return f"Query error: {exc}"
    if not rows:
        return "No rows returned, nothing to plot."

    missing = [c for c in (x, y) if c not in rows[0]]
    if missing:
        return (
            f"Columns {missing} are not in the query result "
            f"(available: {list(rows[0].keys())})."
        )

    xs = [r[x] for r in rows]
    ys = [r[y] for r in rows]
    if any(v is None for v in ys):
        return (
            f"Column '{y}' contains NULL values; filter them out in SQL "
            f"(e.g. WHERE {y} IS NOT NULL) before plotting."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{uuid.uuid4().hex}.png"

    fig, ax = plt.subplots(figsize=(8, 5))
    try:
        if chart_type == "bar":
            ax.bar([str(v) for v in xs], ys)
            plt.xticks(rotation=45, ha="right")
        elif chart_type == "barh":
            ax.barh([str(v) for v in xs], ys)
        elif chart_type == "line":
            ax.plot(xs, ys, marker="o")
            plt.xticks(rotation=45, ha="right")
        elif chart_type == "scatter":
            ax.scatter(xs, ys)
        ax.set_title(title)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        fig.tight_layout()
        fig.savefig(path, dpi=120)
    finally:
        plt.close(fig)

    return f"Chart rendered and saved to {path}"


TOOLS = [describe_schema, query_encyclopedia, plot_encyclopedia]
