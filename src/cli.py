"""
FLP Organizer - Command-line interface
======================================

For scripting, batch processing, and headless use.

Usage:
    python cli.py INPUT.flp [OUTPUT.flp]
    python cli.py INPUT.flp --dry-run

If OUTPUT.flp is omitted, the output is written as INPUT_organized.flp next to
the input.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import flp_core


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organize an FL Studio playlist by grouping clips by name."
    )
    parser.add_argument("input", type=Path, help="Input .flp file")
    parser.add_argument("output", type=Path, nargs="?",
                        help="Output .flp file (default: INPUT_organized.flp)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only analyze and print the plan, don't write output.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Only print errors.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1

    if args.output is None:
        args.output = args.input.with_name(args.input.stem + "_organized.flp")

    if args.output.resolve() == args.input.resolve():
        print("Error: output must differ from input", file=sys.stderr)
        return 1

    try:
        result = flp_core.analyze(args.input)
    except Exception as e:
        print(f"Error while reading {args.input}: {e}", file=sys.stderr)
        return 2

    if not args.quiet:
        print(f"Input:          {args.input}")
        print(f"FL version:     {result.fl_version}")
        print(f"PPQ:            {result.ppq}")
        print(f"Clips:          {result.total_clips}")
        print(f"Groups:         {len(result.groups)}")
        print(f"Tracks needed:  {result.total_tracks_needed}")
        print(f"Clips to move:  {len(result._patches)}")
        print()
        for g in result.groups:
            rng = (f"track {g.first_track}" if g.lanes_used == 1
                   else f"tracks {g.first_track}-{g.first_track + g.lanes_used - 1}")
            print(f"  {rng:20s}  {g.clip_count:3d} clip(s)  -  {g.name}")
        for w in result.warnings:
            print(f"\nWARNING: {w}")

    if args.dry_run:
        if not args.quiet:
            print("\nDry run — no file written.")
        return 0

    try:
        flp_core.apply_plan(result, args.output)
    except Exception as e:
        print(f"Error while writing {args.output}: {e}", file=sys.stderr)
        return 3

    if not args.quiet:
        print(f"\nOutput:         {args.output}")
        print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
