# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2026-04-21

### Added
- **Sort by color** — new sub-sort modifier that orders groups by a
  perceptual rainbow hue (red → orange → yellow → green → blue → purple).
  Greys go in the middle, uncoloured groups at the end.
- The color of a group is the most frequent color among its source
  channels or patterns (majority wins).
- Core now parses `ID_CHANNEL_COLOR` (event 128) and `ID_PATTERN_COLOR`
  (event 149). `ClipInfo` exposes a new `color` field.
- CLI: `--sub-color` is now fully functional.

### Roadmap (coming in v1.5.0)
- Auto-rename tracks from group names
- Auto-color tracks
- Remove empty tracks
- Preserve muted track state (strada B from v1.3.x discussion)

## [1.3.1] - 2026-04-21

### Fixed
- Language selector dropdown was invisible because the top-bar frame was
  placed on the same grid row as the header, causing the header to overlap
  and hide it. The layout now reserves a dedicated row for the language
  selector above the header.

## [1.3.0] - 2026-04-21

### Added
- **Batch mode** — process up to 30 .flp files in one run. New "Single file /
  Batch" tab selector at the top. In batch mode you can choose a custom output
  folder or leave the default (outputs saved next to each input).
- **Sub-sort modifiers** — checkboxes that refine the primary track order:
  - *Group by type*: audio clips come before patterns.
  - *Sort by clip length*: groups with longer clips first.
  - *Sort by color* (placeholder, coming soon).
  These combine freely with both Alphabetical and By-first-appearance.
- **Post-process options card** with checkboxes for upcoming features
  (auto-rename tracks, auto-color tracks, remove empty tracks). These are
  visible but disabled ("coming soon") and will be implemented in v1.4.0.
- **Multi-language UI** — language selector in the top-right corner. Choose
  between English, Deutsch, Español, Français, Italiano, and Русский. The
  choice is persisted in `~/.flp_organizer_config.json` and remembered across
  launches. All labels, captions, buttons, status messages, and the disclaimer
  text are translated.
- CLI: `--batch`, `--output-dir`, `--sub-length`, `--sub-type`, `--sub-color`.

### Changed
- CLI now accepts multiple input paths; existing single-file usage is
  backwards-compatible.
- Default window size slightly larger (920×780) to fit the new controls card.

### Technical
- New module `src/translations.py` holding every UI string for 6 languages.
- `flp_core.analyze()` and `flp_core.reorganize()` accept an optional
  `sub_sort` list argument.

## [1.2.1] - 2026-04-21

### Fixed
- Disclaimer dialog buttons ("I agree" / "Decline") no longer get clipped off
  the bottom on some display configurations. Dialog is now larger (620×500),
  resizable with a minimum size, and the buttons reserve fixed space at the
  bottom.

## [1.2.0] - 2026-04-21

### Added
- Custom app icon bundled into the executable (taskbar + window title bar).
- Centred header at the top: icon + "FLP" (orange) + "Organizer" (white) +
  version.
- First-launch disclaimer popup clarifying that FLP Organizer is independent
  and not affiliated with Image-Line.
- Footer with "Made with 🧡 by Matt Danieli" and a "Help me build more tools"
  button that opens a donation link in the browser.

### Changed
- Window is now fully resizable without buttons disappearing (grid layout).

## [1.1.0] - 2026-04-21

### Added
- **Two sorting modes selectable from the GUI:**
  - Alphabetical (A–Z)
  - By first appearance
- CLI accepts `--sort alpha` or `--sort first`.

### Changed
- Dark FL-Studio-inspired theme with orange accents.
- GUI rebuilt around standard ttk widgets for stability on Windows.

## [1.0.0] - 2026-04-20

### Added
- Initial release.
- Drag & drop GUI for Windows (also runs on macOS / Linux from source).
- Byte-level surgical patching: modifies only track-index bytes, leaves
  everything else untouched.
- Auto-detection of playlist item size (supports FL Studio 21, 24, 25).
- Grouping by sample name / channel name / pattern name.
- Lane assignment for overlapping clips of the same group.
- Alphabetical sorting (case-insensitive).
- Preview pane before applying changes.
- Threaded analysis/write with progress bar.
- Safety: refuses to overwrite the input file.
- Python library API (`flp_core`) for scripting / batch use.
- Command-line interface (`cli.py`) for headless / batch processing.
- GitHub Actions workflow for automatic Windows release builds.
