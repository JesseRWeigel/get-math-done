"""MCP server for GMD project state management.

Exposes tools to read/write project state via the StateEngine.
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.constants import ProjectLayout, find_project_root
from gmd.core.state import StateEngine

server = Server("gmd-state")


def _get_engine() -> StateEngine:
    """Get a StateEngine for the current project."""
    try:
        root = find_project_root()
    except FileNotFoundError:
        root = Path.cwd()
    return StateEngine(ProjectLayout(root=root))


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_state",
            description="Get the full project state as JSON.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_phase_status",
            description="Get the status of a specific phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "phase_id": {
                        "type": "string",
                        "description": "The phase ID to check.",
                    },
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="get_current_position",
            description="Get the current milestone, phase, and plan.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="advance_plan",
            description="Mark a phase as complete and advance to the next pending phase.",
            inputSchema={
                "type": "object",
                "properties": {
                    "phase_id": {
                        "type": "string",
                        "description": "The phase ID to mark complete.",
                    },
                },
                "required": ["phase_id"],
            },
        ),
        Tool(
            name="run_health_check",
            description="Run a health check on the project state: crash recovery, sync, and summary.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    engine = _get_engine()

    if name == "get_state":
        state = engine.load()
        return [TextContent(type="text", text=json.dumps(state.model_dump(mode="json"), indent=2, default=str))]

    elif name == "get_phase_status":
        phase_id = arguments["phase_id"]
        state = engine.load()
        phase = state.phases.get(phase_id)
        if phase is None:
            return [TextContent(type="text", text=json.dumps({"error": f"Phase '{phase_id}' not found", "available": list(state.phases.keys())}))]
        return [TextContent(type="text", text=json.dumps(phase.model_dump(mode="json"), indent=2))]

    elif name == "get_current_position":
        state = engine.load()
        result = {
            "current_milestone": state.current_milestone,
            "current_phase": state.current_phase,
            "current_plan": state.current_plan,
            "research_mode": state.research_mode,
            "autonomy_mode": state.autonomy_mode,
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "advance_plan":
        phase_id = arguments["phase_id"]
        engine.advance_phase(phase_id)
        state = engine.load()
        return [TextContent(type="text", text=json.dumps({
            "advanced_from": phase_id,
            "current_phase": state.current_phase,
            "status": "ok",
        }))]

    elif name == "run_health_check":
        recovered = engine.recover_if_needed()
        state = engine.sync()
        result = {
            "recovery_needed": recovered,
            "project_name": state.project_name,
            "current_phase": state.current_phase,
            "phases_count": len(state.phases),
            "conventions_locked": len(state.conventions),
            "decisions_count": len(state.decisions),
            "total_tasks_completed": state.total_tasks_completed,
            "status": "healthy",
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
