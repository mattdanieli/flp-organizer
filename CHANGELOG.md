# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2026-04-21

### Added
- **Custom app icon** bundled into the executable, visible in the Windows
  taskbar, on the desktop, and in the window title bar.
- **Centred header** at the top of the window: icon + "FLP" (orange) +
  "Organizer" (white) + version number.
- **First-launch disclaimer popup** that clarifies:
  - FLP Organizer is an independent, non-commercial tool.
  - It is not affiliated with, endorsed by, or authorised by Image-Line.
  - No warranty is provided and the author accepts no responsibility for
    issues arising from use.
  - Users are reminded to back up their projects.
  Shown only once; accepted state is stored under
  `~/.flp_organizer_disclaimer_accepted`.
- **Footer** with "Made with 🧡 by Matt Danieli" and a button labelled
  "Help me build more tools" that opens a donation link in the browser.
- Small footer caption reminding users the tool is not affiliated with
  Image-Line.

### Changed
- Window is now **fully resizable** without buttons disappearing. The
  layout uses a grid that expands the preview area while keeping
  controls anchored to the bottom.
- GitHub Actions build now embeds the icon and bundles the PNG logos
  into the exe via `--add-data`.

## [1.1.0] - 2026-04-21

### Added
- **Two sorting modes selectable from the GUI:**
  - **Alphabetical (A–Z)** — groups ordered by name, case-insensitive.
  - **By first appearance** — groups ordered by the earliest time any of
    their clips plays. Good for reading the arrangement top-to-bottom
    like a timeline.
- CLI accepts `--sort alpha` or `--sort first`.

### Changed
- New dark FL-Studio-inspired theme with orange accents.
- GUI rebuilt around standard ttk widgets for better stability across
  Windows setups.

## [1.0.0] - 2026-04-20

### Added
- Initial release
- Drag & drop GUI for Windows (also runs on macOS / Linux from source)
- Byte-level surgical patching: modifies only track-index bytes, leaves
  everything else untouched
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
