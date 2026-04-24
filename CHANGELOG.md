# Changelog

All notable changes to this project will be documented in this file.

## [1.5.0] - 2026-04-24

### Added
- **Preserve muted tracks.** Clips from originally-muted tracks are placed
  into a dedicated group of muted tracks at the bottom of the playlist
  (labelled `[muted] ...` in the preview). Tracks that used to be muted but
  no longer contain muted content are reactivated automatically.
- **Preserve individual clip mute (ghost clips).** The "X" marker on single
  muted clips is preserved when those clips are moved to new tracks. This
  works automatically (the clip mute bit lives inside the 80-byte playlist
  item which is already moved intact).
- **Auto-color tracks** (opt-in checkbox). Each destination track is coloured
  with the dominant color of the group that lives on it (majority wins
  among the source channel/pattern colors). The "custom colour" override
  flag is also set so FL Studio honours the new colour.
- **Auto-rename tracks** (opt-in checkbox). Each destination track is
  renamed to match the group name (e.g. `Kick Basic.wav` or `Pattern 24`).
  This is implemented by inserting new `ID_TRACK_NAME` (event 239) entries
  in the event stream right after each `ID_TRACK_DATA`. The FLdt chunk
  size is updated to reflect the added bytes.

### Technical
- Reverse-engineered on FL Studio 25.1.6:
  - Track mute: byte 12 of `ID_TRACK_DATA` payload (`0x01` active / `0x00` muted).
  - Clip mute: bit 5 (`0x20`) of byte 19 in the 80-byte playlist item.
  - Track colour: bytes 4-6 of `ID_TRACK_DATA` payload (RGB). Byte-size
    event ID 43 preceding TRACK_DATA is the "custom colour" override flag.
  - Track name: dedicated `ID_TRACK_NAME` (239) text event with UTF-16LE
    null-terminated string.
- Writer now supports mute patches, colour patches, and name-event inserts
  in a single pass. The file growth from name inserts is tracked and the
  FLdt chunk header is updated correctly.

### Roadmap
- **v1.6.0**: remove empty tracks, localisation improvements.

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
