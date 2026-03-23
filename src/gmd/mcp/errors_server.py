"""MCP server for GMD LLM math error catalog.

Reads and searches the llm-math-errors.md file for known failure modes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.constants import find_project_root

server = Server("gmd-errors")

ERRORS_REL_PATHS = [
    Path("src") / "gmd" / "specs" / "references" / "verification" / "llm-math-errors.md",
    Path("specs") / "references" / "verification" / "llm-math-errors.md",
]


def _find_errors_file() -> Path | None:
    try:
        root = find_project_root()
    except FileNotFoundError:
        root = Path.cwd()
    for rel in ERRORS_REL_PATHS:
        candidate = root / rel
        if candidate.exists():
            return candidate
    return None


def _parse_errors(content: str) -> list[dict]:
    """Parse error entries from the markdown file."""
    errors = []
    current: dict | None = None

    for line in content.split("\n"):
        # Match error headers like "### E001: Sign Errors in Combinatorial Arguments"
        m = re.match(r"^###\s+(E\d+):\s+(.+)", line)
        if m:
            if current:
                errors.append(current)
            current = {
                "id": m.group(1),
                "title": m.group(2).strip(),
                "pattern": "",
                "example": "",
                "guard": "",
                "raw": line + "\n",
            }
            continue

        if current:
            current["raw"] += line + "\n"
            if line.startswith("**Pattern**:"):
                current["pattern"] = line.split(":", 1)[1].strip()
            elif line.startswith("**Example**:"):
                current["example"] = line.split(":", 1)[1].strip()
            elif line.startswith("**Guard**:"):
                current["guard"] = line.split(":", 1)[1].strip()

    if current:
        errors.append(current)

    return errors


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_error_catalog",
            description="Get the full LLM math error catalog with all known failure modes.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_error_by_id",
            description="Get a specific error entry by its ID (e.g. 'E001').",
            inputSchema={
                "type": "object",
                "properties": {
                    "error_id": {
                        "type": "string",
                        "description": "Error ID like 'E001', 'E002', etc.",
                    },
                },
                "required": ["error_id"],
            },
        ),
        Tool(
            name="search_errors",
            description="Search the error catalog by keyword. Matches against title, pattern, example, and guard fields.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query — matches against all error fields.",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    errors_file = _find_errors_file()
    if errors_file is None:
        return [TextContent(type="text", text=json.dumps({"error": "llm-math-errors.md not found"}))]

    content = errors_file.read_text()
    errors = _parse_errors(content)

    if name == "get_error_catalog":
        # Return structured catalog without raw markdown
        catalog = [
            {"id": e["id"], "title": e["title"], "pattern": e["pattern"], "guard": e["guard"]}
            for e in errors
        ]
        return [TextContent(type="text", text=json.dumps({"errors": catalog, "total": len(catalog)}, indent=2))]

    elif name == "get_error_by_id":
        error_id = arguments["error_id"].upper()
        for e in errors:
            if e["id"] == error_id:
                return [TextContent(type="text", text=json.dumps({
                    "id": e["id"],
                    "title": e["title"],
                    "pattern": e["pattern"],
                    "example": e["example"],
                    "guard": e["guard"],
                }, indent=2))]
        return [TextContent(type="text", text=json.dumps({
            "error": f"Error ID '{error_id}' not found.",
            "available": [e["id"] for e in errors],
        }))]

    elif name == "search_errors":
        query = arguments["query"].lower()
        matches = []
        for e in errors:
            searchable = f"{e['id']} {e['title']} {e['pattern']} {e['example']} {e['guard']}".lower()
            if query in searchable:
                matches.append({
                    "id": e["id"],
                    "title": e["title"],
                    "pattern": e["pattern"],
                    "guard": e["guard"],
                })
        return [TextContent(type="text", text=json.dumps({"query": query, "matches": matches, "count": len(matches)}, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
