"""MCP server for GMD math protocol access.

Reads protocol .md files from specs/references/protocols/ directory.
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.constants import find_project_root

server = Server("gmd-protocols")

PROTOCOLS_REL_PATH = Path("src") / "gmd" / "specs" / "references" / "protocols"


def _get_protocols_dir() -> Path:
    """Find the protocols directory."""
    try:
        root = find_project_root()
    except FileNotFoundError:
        root = Path.cwd()
    # Try the src layout first, then fall back to root-level
    candidates = [
        root / PROTOCOLS_REL_PATH,
        root / "specs" / "references" / "protocols",
    ]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return candidates[0]  # Return first even if missing, for error messages


def _list_protocol_files(protocols_dir: Path) -> dict[str, Path]:
    """Map protocol names to their file paths."""
    result = {}
    if protocols_dir.is_dir():
        for f in sorted(protocols_dir.glob("*.md")):
            # e.g. "algebra-protocols.md" -> "algebra"
            name = f.stem.replace("-protocols", "").replace("-protocol", "")
            result[name] = f
    return result


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_protocol",
            description="Get the full content of a math protocol by domain name (e.g. 'algebra', 'analysis').",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Protocol domain name, e.g. 'algebra', 'analysis', 'number-theory'.",
                    },
                },
                "required": ["domain"],
            },
        ),
        Tool(
            name="route_protocol",
            description="Given a math topic description, suggest which protocol(s) are most relevant.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Description of the math topic or problem.",
                    },
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="list_protocols",
            description="List all available math protocol domains.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


# Keyword routing table for protocol suggestions
ROUTING_KEYWORDS: dict[str, list[str]] = {
    "algebra": ["group", "ring", "field", "module", "algebra", "homomorphism", "isomorphism", "galois", "polynomial", "linear", "matrix", "vector space", "eigenvalue"],
    "analysis": ["limit", "continuity", "derivative", "integral", "measure", "series", "sequence", "convergence", "function space", "Banach", "Hilbert", "Lebesgue", "Fourier"],
    "combinatorics": ["counting", "permutation", "combination", "graph", "partition", "generating function", "Ramsey", "pigeonhole", "inclusion-exclusion", "binomial"],
    "number-theory": ["prime", "divisibility", "modular", "congruence", "Diophantine", "quadratic residue", "arithmetic function", "Euler", "Fermat", "RSA"],
    "probability-statistics": ["probability", "random", "distribution", "expectation", "variance", "Bayes", "Markov", "stochastic", "hypothesis", "regression", "sampling"],
    "topology-geometry": ["topology", "manifold", "homotopy", "homology", "cohomology", "metric space", "compact", "connected", "open set", "closed set", "continuous map", "differential geometry", "curvature"],
}


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    protocols_dir = _get_protocols_dir()
    protocol_files = _list_protocol_files(protocols_dir)

    if name == "get_protocol":
        domain = arguments["domain"]
        if domain in protocol_files:
            content = protocol_files[domain].read_text()
            return [TextContent(type="text", text=content)]
        return [TextContent(type="text", text=json.dumps({
            "error": f"Protocol '{domain}' not found.",
            "available": list(protocol_files.keys()),
        }))]

    elif name == "route_protocol":
        topic = arguments["topic"].lower()
        scores: dict[str, int] = {}
        for domain, keywords in ROUTING_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in topic)
            if score > 0:
                scores[domain] = score
        if not scores:
            return [TextContent(type="text", text=json.dumps({
                "suggestion": "No strong match found. Browse all protocols.",
                "available": list(protocol_files.keys()),
            }))]
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        suggestions = [{"domain": d, "relevance_score": s, "available": d in protocol_files} for d, s in ranked]
        return [TextContent(type="text", text=json.dumps({"suggestions": suggestions}, indent=2))]

    elif name == "list_protocols":
        result = []
        for domain, path in protocol_files.items():
            # Read first line as title
            first_line = ""
            try:
                first_line = path.read_text().split("\n", 1)[0].lstrip("# ").strip()
            except Exception:
                pass
            result.append({"domain": domain, "title": first_line, "path": str(path)})
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
