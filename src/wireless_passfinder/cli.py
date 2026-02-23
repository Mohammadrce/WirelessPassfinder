from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from wireless_passfinder.formatters import format_profile_details, format_profiles_table
from wireless_passfinder.netsh_adapter import (
    NetshAdapter,
    NetshExecutionError,
    NetshNotAvailableError,
    NotSupportedOSError,
    ProfileNotFoundError,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wpfinder",
        description="Audit saved WiFi profiles on Windows with safe default output.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List saved WiFi profiles.")
    list_parser.add_argument(
        "--show-keys",
        action="store_true",
        help="Show plaintext passwords in output.",
    )
    list_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of a table.",
    )
    list_parser.add_argument(
        "--filter",
        dest="name_filter",
        default=None,
        help="Filter profiles by case-insensitive name match.",
    )

    show_parser = subparsers.add_parser("show", help="Show details for one WiFi profile.")
    show_parser.add_argument("profile", help="Exact WiFi profile name.")
    show_parser.add_argument(
        "--show-key",
        action="store_true",
        help="Show plaintext password in output.",
    )
    show_parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of plain text.",
    )

    export_parser = subparsers.add_parser("export", help="Export profile data to a JSON file.")
    export_parser.add_argument(
        "--output",
        required=True,
        help="Output file path for JSON export.",
    )
    export_parser.add_argument(
        "--show-keys",
        action="store_true",
        help="Include plaintext passwords in exported JSON.",
    )

    return parser


def _handle_list(args: argparse.Namespace, adapter: NetshAdapter) -> int:
    profiles = adapter.list_profiles_detailed()
    if args.name_filter:
        query = args.name_filter.lower()
        profiles = [profile for profile in profiles if query in profile.name.lower()]

    if args.json:
        payload = [profile.to_dict(show_key_material=args.show_keys) for profile in profiles]
        print(json.dumps(payload, indent=2))
        return 0

    print(format_profiles_table(profiles, show_key_material=args.show_keys))
    return 0


def _handle_show(args: argparse.Namespace, adapter: NetshAdapter) -> int:
    profile = adapter.get_profile(args.profile)

    if args.json:
        print(json.dumps(profile.to_dict(show_key_material=args.show_key), indent=2))
        return 0

    print(format_profile_details(profile, show_key_material=args.show_key))
    return 0


def _handle_export(args: argparse.Namespace, adapter: NetshAdapter) -> int:
    profiles = adapter.list_profiles_detailed()
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "profile_count": len(profiles),
        "profiles": [profile.to_dict(show_key_material=args.show_keys) for profile in profiles],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Exported {len(profiles)} profile(s) to {output_path}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        adapter = NetshAdapter()
        if args.command == "list":
            return _handle_list(args, adapter)
        if args.command == "show":
            return _handle_show(args, adapter)
        if args.command == "export":
            return _handle_export(args, adapter)
    except (NotSupportedOSError, NetshNotAvailableError, ProfileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except NetshExecutionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Error: unknown command.", file=sys.stderr)
    return 2


def entrypoint() -> None:
    raise SystemExit(main())
