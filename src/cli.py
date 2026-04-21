"""
FLP Organizer - Command-line interface
======================================

For scripting, batch processing, and headless use.

Usage:
    Single file:
        python cli.py INPUT.flp [OUTPUT.flp]
        python cli.py INPUT.flp --dry-run

    Batch (up to 30 files):
        python cli.py --batch INPUT1.flp INPUT2.flp ...
        python cli.py --batch *.flp --output-dir organized/

If OUTPUT.flp is omitted, the output is written as INPUT_organized.flp next to
the input.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import flp_core


BATCH_LIMIT = 30


def _sort_from_args(args) -> tuple[str, list[str]]:
    sort_mode = (flp_core.SORT_BY_FIRST_APPEARANCE
                 if args.sort == "first"
                 else flp_core.SORT_ALPHABETICAL)
    sub_sort: list[str] = []
    if args.sub_length:
        sub_sort.append(flp_core.SUB_BY_LENGTH)
    if args.sub_type:
        sub_sort.append(flp_core.SUB_BY_TYPE)
    if args.sub_color:
        sub_sort.append(flp_core.SUB_BY_COLOR)
    return sort_mode, sub_sort


def process_one(input_path: Path, output_path: Path, sort_mode: str,
                sub_sort: list[str], quiet: bool, dry_run: bool) -> int:
    try:
        result = flp_core.analyze(input_path, sort_mode=sort_mode, sub_sort=sub_sort)
    except Exception as e:
        print(f"Error while reading {input_path}: {e}", file=sys.stderr)
        return 2

    if not quiet:
        print(f"--- {input_path.name} ---")
        print(f"  FL {result.fl_version}  •  {result.total_clips} clips  •  "
              f"{len(result.groups)} groups  •  {len(result._patches)} clips will move")
        for w in result.warnings:
            print(f"  WARNING: {w}")

    if dry_run:
        if not quiet:
            print(f"  (dry run, not writing)")
        return 0

    try:
        flp_core.apply_plan(result, output_path)
    except Exception as e:
        print(f"Error while writing {output_path}: {e}", file=sys.stderr)
        return 3

    if not quiet:
        print(f"  Saved: {output_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Organize one or many FL Studio playlists by grouping clips by name."
    )
    parser.add_argument("input", type=Path, nargs="*",
                        help="Input .flp file(s). In single-file mode only the "
                             "first one is used; with --batch, all are processed.")
    parser.add_argument("output", type=Path, nargs="?",
                        help="Output .flp file (single-file mode only). "
                             "Default: INPUT_organized.flp")
    parser.add_argument("--batch", action="store_true",
                        help=f"Process multiple .flp files (max {BATCH_LIMIT}).")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Directory for batch outputs (default: next to each input).")
    parser.add_argument("--sort", default="alpha",
                        choices=["alpha", "first"],
                        help="Track order: 'alpha' = alphabetical A-Z (default), "
                             "'first' = by time of first appearance.")
    parser.add_argument("--sub-length", action="store_true",
                        help="Sub-sort modifier: group by average clip length.")
    parser.add_argument("--sub-type", action="store_true",
                        help="Sub-sort modifier: audio clips before patterns.")
    parser.add_argument("--sub-color", action="store_true",
                        help="Sub-sort modifier: group by color (placeholder, no-op).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only analyze and print the plan, don't write output.")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Only print errors.")
    args = parser.parse_args()

    if not args.input:
        parser.error("at least one input file is required")

    sort_mode, sub_sort = _sort_from_args(args)

    if args.batch:
        if len(args.input) > BATCH_LIMIT:
            parser.error(f"batch mode supports up to {BATCH_LIMIT} files")
        if args.output_dir:
            args.output_dir.mkdir(parents=True, exist_ok=True)
        had_error = 0
        for i, in_path in enumerate(args.input, 1):
            if not in_path.exists():
                print(f"[{i}/{len(args.input)}] File not found: {in_path}",
                      file=sys.stderr)
                had_error = max(had_error, 1)
                continue
            if args.output_dir:
                out_path = args.output_dir / (in_path.stem + "_organized.flp")
            else:
                out_path = in_path.with_name(in_path.stem + "_organized.flp")
            rc = process_one(in_path, out_path, sort_mode, sub_sort,
                             args.quiet, args.dry_run)
            had_error = max(had_error, rc)
        if not args.quiet:
            print(f"\nProcessed {len(args.input)} file(s).")
        return had_error

    # Single-file mode
    in_path = args.input[0]
    if not in_path.exists():
        print(f"Error: file not found: {in_path}", file=sys.stderr)
        return 1

    out_path = args.output or in_path.with_name(in_path.stem + "_organized.flp")
    if out_path.resolve() == in_path.resolve():
        print("Error: output must differ from input", file=sys.stderr)
        return 1

    return process_one(in_path, out_path, sort_mode, sub_sort,
                       args.quiet, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
