"""MCP server for GMD convention lock management.

Exposes tools to set, get, check, diff, list, and describe conventions.
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.constants import ProjectLayout, find_project_root, CONVENTION_FIELDS
from gmd.core.state import StateEngine
from gmd.core.conventions import (
    check_conventions,
    diff_conventions,
    get_field_description,
    get_field_examples,
    list_all_fields,
)

server = Server("gmd-conventions")


def _get_engine() -> StateEngine:
    try:
        root = find_project_root()
    except FileNotFoundError:
        root = Path.cwd()
    return StateEngine(ProjectLayout(root=root))


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="convention_set",
            description="Lock a convention field to a specific value.",
            inputSchema={
                "type": "object",
                "properties": {
                    "field": {"type": "string", "description": "Convention field name."},
                    "value": {"type": "string", "description": "Value to lock."},
                    "locked_by": {"type": "string", "description": "Who/what is locking this (e.g. phase ID)."},
                    "rationale": {"type": "string", "description": "Why this value was chosen.", "default": ""},
                },
                "required": ["field", "value", "locked_by"],
            },
        ),
        Tool(
            name="convention_get",
            description="Get the current locked value of a convention field.",
            inputSchema={
                "type": "object",
                "properties": {
                    "field": {"type": "string", "description": "Convention field name."},
                },
                "required": ["field"],
            },
        ),
        Tool(
            name="convention_check",
            description="Check which conventions are locked vs unlocked, with coverage stats.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="convention_diff",
            description="Compare proposed convention values against current locks. Returns conflicts, new fields, and matches.",
            inputSchema={
                "type": "object",
                "properties": {
                    "proposed": {
                        "type": "object",
                        "description": "Map of field names to proposed values.",
                        "additionalProperties": {"type": "string"},
                    },
                },
                "required": ["proposed"],
            },
        ),
        Tool(
            name="convention_list",
            description="List all available convention fields with descriptions and examples.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="convention_describe",
            description="Get a detailed description and examples for a specific convention field.",
            inputSchema={
                "type": "object",
                "properties": {
                    "field": {"type": "string", "description": "Convention field name."},
                },
                "required": ["field"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    engine = _get_engine()

    if name == "convention_set":
        field = arguments["field"]
        if field not in CONVENTION_FIELDS:
            return [TextContent(type="text", text=json.dumps({
                "error": f"Unknown convention field: {field}",
                "valid_fields": CONVENTION_FIELDS,
            }))]
        engine.set_convention(
            field=field,
            value=arguments["value"],
            locked_by=arguments["locked_by"],
            rationale=arguments.get("rationale", ""),
        )
        return [TextContent(type="text", text=json.dumps({"status": "locked", "field": field, "value": arguments["value"]}))]

    elif name == "convention_get":
        field = arguments["field"]
        value = engine.get_convention(field)
        if value is None:
            return [TextContent(type="text", text=json.dumps({"field": field, "locked": False, "value": None}))]
        return [TextContent(type="text", text=json.dumps({"field": field, "locked": True, "value": value}))]

    elif name == "convention_check":
        report = check_conventions(engine)
        return [TextContent(type="text", text=json.dumps(report, indent=2))]

    elif name == "convention_diff":
        proposed = arguments["proposed"]
        result = diff_conventions(engine, proposed)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "convention_list":
        fields = list_all_fields()
        return [TextContent(type="text", text=json.dumps(fields, indent=2))]

    elif name == "convention_describe":
        field = arguments["field"]
        desc = get_field_description(field)
        examples = get_field_examples(field)
        return [TextContent(type="text", text=json.dumps({
            "field": field,
            "description": desc,
            "examples": examples,
        }, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
