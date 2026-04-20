# Changelog

All notable changes to this project will be documented in this file.

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
