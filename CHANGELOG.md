# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2026-04-21

### Fixed
- Fixed crash on startup on Windows (`TypeError: 'list' object is not callable`
  caused by `Canvas.create_arc` inside custom widgets). Replaced the arc-based
  rounded-corner rendering with an `create_oval` based approach that is
  compatible across all Tcl/Tk versions bundled by PyInstaller.
- Dashed border corners on the drop zone are now drawn as short line segments,
  for the same reason.

## [1.1.0] - 2026-04-20

### Added
- **Two sorting modes selectable from the GUI:**
  - **Alphabetical (A–Z)** — groups ordered by name, case-insensitive (original default).
  - **By first appearance** — groups ordered by the earliest time any of their
    clips plays. Elements that enter first (kick, bass) end up on top; build-ups,
    fills, and outros go further down. Perfect for reading the arrangement
    top-to-bottom like a timeline.
- GUI redesign with FL Studio-inspired dark theme and orange accents.
- Rounded corners, hover animations, gradient highlights on the accent button.
- Sliding segmented toggle for sort mode selection, with an explanation of what
  each mode does below it.
- Switching sort mode re-computes the plan instantly without reloading the file.
- CLI now accepts `--sort alpha` or `--sort first`.

### Changed
- GUI font and spacing refined for a more modern look.
- Alternating row colors in the preview table for better readability.
- Track numbers displayed as `#N` / `#N–M` for clarity.

## [1.0.0] - 2026-04-20

### Added
- Initial release
- Drag & drop GUI for Windows (also runs on macOS / Linux from source)
- Byte-level surgical patching: modifies only track-index bytes, leaves everything else untouched
- Auto-detection of playlist item size (supports FL Studio 21, 24, 25)
- Grouping by sample name / channel name / pattern name
- Lane assignment for overlapping clips of the same group
- Alphabetical sorting (case-insensitive)
- Preview pane before applying changes
- Threaded analysis/write with progress bar
- Safety: refuses to overwrite the input file
- Python library API (`flp_core`) for scripting / batch use
- Command-line interface (`cli.py`) for headless / batch processing
- GitHub Actions workflow for automatic Windows release builds
