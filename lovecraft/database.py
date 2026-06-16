"""DuckDB access for the Lovecraft bestiary.

The database file is built idempotently from ``seed_data`` and is queried
**read-only** by the agent. ``run_select`` is the safety boundary: it opens a
read-only connection and refuses anything that isn't a ``SELECT``/``WITH`` query,
so a misbehaving (or jailbroken) agent cannot mutate or drop the data.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from .seed_data import APPEARANCES, ENTITIES

# data/lovecraft.duckdb relative to the project root (this file lives in lovecraft/).
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "lovecraft.duckdb"

_SCHEMA = """
CREATE TABLE entities (
    name           TEXT PRIMARY KEY,  -- e.g. "Cthulhu"
    classification TEXT,              -- "Great Old One", "Outer God", "Lesser race", ...
    description    TEXT,              -- short blurb
    height_m       DOUBLE,            -- approximate height in metres (NULL if unstated/incomprehensible)
    weight_kg      DOUBLE,            -- approximate mass in kilograms (NULL if unstated)
    size_note      TEXT               -- prose qualifier, e.g. "mountainous"
);

CREATE TABLE appearances (
    entity_name TEXT,   -- references entities.name
    work_title  TEXT,   -- e.g. "The Call of Cthulhu"
    work_type   TEXT,   -- "short story" | "novella" | "novel" | ...
    year        INTEGER -- first publication year
);
"""


def ensure_database() -> None:
    """Create and seed the database if it is missing or empty. Idempotent."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))
    try:
        tables = {row[0] for row in con.execute("SHOW TABLES").fetchall()}
        already_seeded = (
            "entities" in tables
            and con.execute("SELECT count(*) FROM entities").fetchone()[0] > 0
        )
        if already_seeded:
            return

        con.execute("DROP TABLE IF EXISTS appearances")
        con.execute("DROP TABLE IF EXISTS entities")
        con.execute(_SCHEMA)
        con.executemany(
            "INSERT INTO entities VALUES (?, ?, ?, ?, ?, ?)", ENTITIES
        )
        con.executemany(
            "INSERT INTO appearances VALUES (?, ?, ?, ?)", APPEARANCES
        )
    finally:
        con.close()


def run_select(sql: str) -> list[dict]:
    """Run a read-only query and return rows as dicts.

    Rejects anything that is not a single SELECT/WITH statement.
    """
    stripped = sql.strip().rstrip(";").lstrip("(")
    first_word = stripped.split(None, 1)[0].lower() if stripped else ""
    if first_word not in ("select", "with"):
        raise ValueError(
            "Only read-only SELECT/WITH queries are allowed; "
            f"got a statement starting with '{first_word or '(empty)'}'."
        )
    if ";" in sql.strip().rstrip(";"):
        raise ValueError("Only a single statement is allowed (no ';' chaining).")

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        cur = con.execute(sql)
        columns = [d[0] for d in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        con.close()


def get_schema_text() -> str:
    """Schema DDL plus a few example rows, for grounding the agent's SQL."""
    examples = run_select(
        "SELECT name, classification, height_m, weight_kg FROM entities "
        "ORDER BY name LIMIT 3"
    )
    example_lines = "\n".join(
        f"  {r['name']} | {r['classification']} | height_m={r['height_m']} "
        f"| weight_kg={r['weight_kg']}"
        for r in examples
    )
    return (
        "Tables (DuckDB, read-only):\n"
        f"{_SCHEMA.strip()}\n\n"
        "Notes:\n"
        "  - height_m and weight_kg are frequently NULL (entities with no canonical size).\n"
        "  - appearances.entity_name joins to entities.name (many appearances per entity).\n\n"
        "Example entity rows:\n"
        f"{example_lines}"
    )


if __name__ == "__main__":
    ensure_database()
    count = run_select("SELECT count(*) AS n FROM entities")[0]["n"]
    works = run_select("SELECT count(DISTINCT work_title) AS n FROM appearances")[0]["n"]
    print(f"Database ready at {DB_PATH}")
    print(f"  {count} entities across {works} distinct works")
