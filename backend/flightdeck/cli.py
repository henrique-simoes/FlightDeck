from __future__ import annotations

import argparse
import json

from .generation import generate_all, generate_for_persona
from .models import PersonaId


def main() -> None:
    parser = argparse.ArgumentParser(prog="flightdeck")
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser("generate", help="Generate and activate persona blueprints")
    generate.add_argument(
        "--persona",
        choices=["scanner", "comparer", "explorer", "expert_operator"],
        help="Generate only one persona blueprint",
    )
    generate.add_argument("--all", action="store_true", help="Generate all persona blueprints")
    generate.add_argument(
        "--fallback",
        action="store_true",
        help="Use the local deterministic generator if LangGraph/CopilotKit is unavailable",
    )

    args = parser.parse_args()

    if args.command == "generate":
        if args.all:
            print(json.dumps(generate_all(allow_fallback=args.fallback), indent=2))
            return
        if args.persona:
            print(json.dumps(generate_for_persona(args.persona, allow_fallback=args.fallback), indent=2))
            return
        parser.error("generate requires --persona or --all")
