# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-04-21

### Added
- **Two sorting modes selectable from the GUI:**
  - **Alphabetical (A–Z)** — groups ordered by name, case-insensitive.
  - **By first appearance** — groups ordered by the earliest time any of their
    clips plays. Elements that enter first (kick, bass) end up on top;
    build-ups, fills, and outros go further down. Good for reading the
    arrangement top-to-bottom like a timeline.
- Sort mode radio toggle in the GUI with a caption that explains what each
  mode does.
- Switching sort mode re-computes the plan instantly without reloading the file.
- CLI accepts `--sort alpha` or `--sort first`.

### Changed
- GUI restyled with a dark FL-Studio-inspired theme and orange accents.
- Alternating row colors in the preview table for better readability.
- Track numbers displayed as `#N` / `#N–M` for clarity.
- Uses only standard ttk widgets to guarantee compatibility across Windows,
  macOS, and Linux, without custom Canvas rendering that caused startup issues
  on some Windows setups.

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
