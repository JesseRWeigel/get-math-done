"""MCP server for GMD mathematical verification.

Exposes tools to run verification checks against evidence registries.
"""

from __future__ import annotations

import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from gmd.core.kernel import VerificationKernel, DEFAULT_PREDICATES
from gmd.core.constants import VERIFICATION_CHECKS

server = Server("gmd-verification")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="run_verification",
            description="Run all verification predicates against an evidence registry. Returns a full verdict with pass/fail/skip for each check.",
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence": {
                        "type": "object",
                        "description": "Evidence registry — keys like 'proof_steps', 'logical_gaps', 'base_cases', etc.",
                    },
                },
                "required": ["evidence"],
            },
        ),
        Tool(
            name="get_check_list",
            description="List all available verification checks with their IDs and descriptions.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="get_verdict",
            description="Run verification and return only the summary verdict (overall status, counts).",
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence": {
                        "type": "object",
                        "description": "Evidence registry.",
                    },
                },
                "required": ["evidence"],
            },
        ),
    ]


# Human-readable descriptions for each check
CHECK_DESCRIPTIONS: dict[str, str] = {
    "logical_validity": "Each proof step follows logically from the previous.",
    "base_case_verification": "Induction base cases are explicitly verified.",
    "special_case_testing": "Known solvable instances and boundary cases checked.",
    "counterexample_search": "Systematic attempt to construct counterexamples.",
    "known_identity_matching": "Results compared against established theorems.",
    "type_consistency": "Mathematical objects have correct types throughout.",
    "convergence_verification": "Series, limits, integrals are properly justified.",
    "assumption_tracking": "All hypotheses used, no circular reasoning.",
    "uniqueness_checking": "When uniqueness is claimed, it is verified.",
    "constructive_witness": "Existence proofs produce explicit constructions.",
    "literature_comparison": "Results compared with published work.",
    "notation_consistency": "Convention locks respected throughout.",
    "completeness": "All cases handled, no missing branches.",
}


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "run_verification":
        evidence = arguments["evidence"]
        kernel = VerificationKernel()
        verdict = kernel.verify(evidence)
        return [TextContent(type="text", text=json.dumps(verdict.to_dict(), indent=2))]

    elif name == "get_check_list":
        checks = []
        for check_id in VERIFICATION_CHECKS:
            checks.append({
                "check_id": check_id,
                "description": CHECK_DESCRIPTIONS.get(check_id, ""),
                "has_predicate": check_id in DEFAULT_PREDICATES,
            })
        return [TextContent(type="text", text=json.dumps(checks, indent=2))]

    elif name == "get_verdict":
        evidence = arguments["evidence"]
        kernel = VerificationKernel()
        verdict = kernel.verify(evidence)
        summary = {
            "overall": verdict.overall,
            "summary": verdict.summary,
            "verdict_hash": verdict.verdict_hash,
            "pass_count": verdict.pass_count,
            "fail_count": verdict.fail_count,
            "critical_failures": [
                {"check_id": r.check_id, "message": r.message}
                for r in verdict.critical_failures
            ],
        }
        return [TextContent(type="text", text=json.dumps(summary, indent=2))]

    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
