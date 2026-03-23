"""MCP server for GMD math pattern management.

Manages a patterns.json file in the .gmd/ directory for storing
reusable proof patterns, problem-solving strategies, and heuristics.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.constants import ProjectLayout, find_project_root

server = Server("gmd-patterns")

PATTERNS_FILENAME = "patterns.json"


def _get_patterns_path() -> Path:
    try:
        root = find_project_root()
    except FileNotFoundError:
        root = Path.cwd()
    layout = ProjectLayout(root=root)
    return layout.gmd_dir / PATTERNS_FILENAME


def _load_patterns(path: Path) -> list[dict]:
    if path.exists():
        try:
            data = json.loads(path.read_text())
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def _save_patterns(path: Path, patterns: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(patterns, indent=2))


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_patterns",
            description="Get all stored math patterns, optionally filtered by domain or tag.",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Filter by domain (e.g. 'algebra', 'analysis').",
                    },
                    "tag": {
                        "type": "string",
                        "description": "Filter by tag.",
                    },
                },
            },
        ),
        Tool(
            name="add_pattern",
            description="Add a new math pattern (proof technique, problem-solving strategy, heuristic).",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Short name for the pattern."},
                    "description": {"type": "string", "description": "What the pattern does and when to use it."},
                    "domain": {"type": "string", "description": "Math domain (e.g. 'algebra', 'analysis')."},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization.",
                        "default": [],
                    },
                    "template": {
                        "type": "string",
                        "description": "Optional proof/solution template text.",
                        "default": "",
                    },
                    "examples": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Example applications.",
                        "default": [],
                    },
                },
                "required": ["name", "description", "domain"],
            },
        ),
        Tool(
            name="search_patterns",
            description="Search patterns by keyword across name, description, domain, and tags.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query.",
                    },
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    patterns_path = _get_patterns_path()

    if name == "get_patterns":
        patterns = _load_patterns(patterns_path)
        domain_filter = arguments.get("domain")
        tag_filter = arguments.get("tag")

        filtered = patterns
        if domain_filter:
            filtered = [p for p in filtered if p.get("domain", "").lower() == domain_filter.lower()]
        if tag_filter:
            filtered = [p for p in filtered if tag_filter.lower() in [t.lower() for t in p.get("tags", [])]]

        return [TextContent(type="text", text=json.dumps({"patterns": filtered, "total": len(filtered)}, indent=2))]

    elif name == "add_pattern":
        patterns = _load_patterns(patterns_path)

        new_pattern = {
            "id": f"P{len(patterns) + 1:03d}",
            "name": arguments["name"],
            "description": arguments["description"],
            "domain": arguments["domain"],
            "tags": arguments.get("tags", []),
            "template": arguments.get("template", ""),
            "examples": arguments.get("examples", []),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        patterns.append(new_pattern)
        _save_patterns(patterns_path, patterns)

        return [TextContent(type="text", text=json.dumps({"status": "added", "pattern": new_pattern}, indent=2))]

    elif name == "search_patterns":
        patterns = _load_patterns(patterns_path)
        query = arguments["query"].lower()

        matches = []
        for p in patterns:
            searchable = " ".join([
                p.get("name", ""),
                p.get("description", ""),
                p.get("domain", ""),
                " ".join(p.get("tags", [])),
                p.get("template", ""),
            ]).lower()
            if query in searchable:
                matches.append(p)

        return [TextContent(type="text", text=json.dumps({"query": query, "matches": matches, "count": len(matches)}, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
