"""
FLP Organizer - Core engine
===========================

Surgical byte-level reorganizer for FL Studio project files (.flp).

Groups all playlist clips by name (sample name, automation name, pattern name)
onto adjacent tracks while preserving every clip's original time position,
length, color, automation data, and every other property.

Works by patching only the 2 bytes that encode the track index of each playlist
item. The rest of the file is left byte-for-byte identical to the original.

Compatible with FL Studio 21 and newer. Tested on FL Studio 25.1.6 (item size
320 bytes). Automatic detection of item size for other versions (falls back to
64, 60, or 32 bytes).

Public API:
    analyze(flp_path) -> AnalysisResult
        Reads the .flp file and returns the grouping plan without modifying it.

    reorganize(flp_path, output_path) -> AnalysisResult
        Reads, reorganizes, and writes the output file.
"""
from __future__ import annotations
import struct
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

# ----- FLP format constants -----
BYTE_BASE, WORD_BASE, DWORD_BASE, TEXT_BASE, DATA_BASE = 0, 64, 128, 192, 208

ID_CHANNEL_NEW      = WORD_BASE + 0          # 64  - opens a channel, payload u16 iid
ID_PATTERN_NEW      = WORD_BASE + 1          # 65  - opens a pattern, payload u16 num
ID_PATTERN_NAME     = TEXT_BASE + 1          # 193
ID_CHANNEL_SAMPLE   = TEXT_BASE + 4          # 196 - sample path
ID_FL_VERSION       = TEXT_BASE + 7          # 199
ID_DEFAULT_NAME     = TEXT_BASE + 9          # 201 - default channel name
ID_CHANNEL_NAME     = TEXT_BASE + 39         # 231 - user channel name
ID_ARRANGEMENT_NEW  = WORD_BASE + 35         # 99
ID_TRACK_NAME       = TEXT_BASE + 47         # 239
ID_ARRANGEMENT_NAME = TEXT_BASE + 49         # 241
ID_PLAYLIST         = DATA_BASE + 25         # 233
ID_TRACK_DATA       = DATA_BASE + 30         # 238
ID_CHANNEL_COLOR    = DWORD_BASE + 0         # 128 - channel colour, 4 bytes 0x00RRGGBB
ID_PATTERN_COLOR    = DWORD_BASE + 21        # 149 - pattern colour (tentative)

PATTERN_BASE_VAL = 20480   # item_index > PATTERN_BASE_VAL => pattern clip
MAX_TRACKS = 500           # FL Studio 21+ has 500 playlist tracks

ITEM_SIZE_CANDIDATES = (32, 60, 64, 80, 320)  # smallest first — 80 is FL 25+


# ----- Sort mode constants -----
SORT_ALPHABETICAL        = "alphabetical"
SORT_BY_FIRST_APPEARANCE = "first_appearance"

# Sub-sort modifiers (applied on top of the primary sort mode)
SUB_BY_LENGTH   = "length"    # longer clips first within the same primary order
SUB_BY_TYPE     = "type"      # audio clips first, then patterns, then automation
SUB_BY_COLOR    = "color"     # groups with the same primary rank are then grouped by color


# ----- Data classes -----

@dataclass
class ClipInfo:
    name: str                   # Group name (sample file, channel name, pattern name)
    kind: str                   # 'channel' or 'pattern'
    position: int               # Start position in PPQ ticks
    length: int                 # Length in PPQ ticks
    old_track: int              # Original track, 1-based
    new_track: int = 0          # Assigned track, 1-based
    color: Optional[int] = None  # 24-bit RGB of source channel/pattern (0xRRGGBB) or None
    # Byte offsets in the file (used by the writer)
    item_offset: int = 0
    rvidx_offset: int = 0
    old_rvidx: int = 0


@dataclass
class GroupPlan:
    name: str
    first_track: int            # 1-based
    lanes_used: int             # number of adjacent tracks used by this group
    clip_count: int


@dataclass
class AnalysisResult:
    fl_version: str = ""
    ppq: int = 0
    channel_count: int = 0
    pattern_count: int = 0
    arrangement_count: int = 0
    total_clips: int = 0
    total_tracks_needed: int = 0
    groups: list[GroupPlan] = field(default_factory=list)
    clips: list[ClipInfo] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    # Internal: for the writer
    _data: bytes = b""
    _patches: list[tuple[int, int]] = field(default_factory=list)  # (offset, new_rvidx)


# ----- Low-level parsing helpers -----

def _read_varint(data: bytes, offset: int) -> tuple[int, int]:
    result, shift = 0, 0
    while True:
        b = data[offset]
        offset += 1
        result |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            return result, offset
        shift += 7


def _decode_str(raw: bytes, is_unicode: bool) -> str:
    try:
        if is_unicode:
            return raw.decode("utf-16-le").rstrip("\0")
        return raw.decode("latin-1").rstrip("\0")
    except Exception:
        return raw.decode("utf-16-le", errors="replace").rstrip("\0")


def _detect_item_size(data: bytes, offset: int, total_size: int) -> Optional[int]:
    """Picks the item size where every item's pattern_base field equals 20480.

    Returns None if no candidate matches cleanly.
    """
    # Prefer perfect matches first
    for candidate in ITEM_SIZE_CANDIDATES:
        if total_size % candidate != 0:
            continue
        n = total_size // candidate
        if n == 0:
            continue
        ok = True
        for k in range(n):
            pb = struct.unpack_from("<H", data, offset + k * candidate + 4)[0]
            if pb != PATTERN_BASE_VAL:
                ok = False
                break
        if ok:
            return candidate

    # Fallback: best ratio above 50%
    best, best_ratio = None, 0.5
    for candidate in ITEM_SIZE_CANDIDATES:
        if total_size % candidate != 0:
            continue
        n = total_size // candidate
        if n == 0:
            continue
        good = sum(
            1 for k in range(n)
            if struct.unpack_from("<H", data, offset + k * candidate + 4)[0] == PATTERN_BASE_VAL
        )
        ratio = good / n
        if ratio > best_ratio:
            best_ratio, best = ratio, candidate
    return best


def _group_name(pattern_base: int, item_index: int,
                channels: dict, patterns: dict) -> tuple[Optional[str], Optional[str]]:
    if pattern_base != PATTERN_BASE_VAL:
        return None, None
    if item_index > PATTERN_BASE_VAL:
        pnum = item_index - PATTERN_BASE_VAL
        p = patterns.get(pnum, {})
        name = p.get("name") or f"Pattern {pnum}"
        return name, "pattern"

    ch = channels.get(item_index, {})
    nm = ch.get("name")
    if nm:
        return nm, "channel"
    sp = ch.get("sample_path")
    if sp:
        return Path(sp.replace("\\", "/")).name, "channel"
    dn = ch.get("default_name")
    if dn:
        return dn, "channel"
    return f"Chan#{item_index}", "channel"


def _dominant_color(clips: list[ClipInfo]) -> Optional[int]:
    """Return the most frequent non-None colour in the clip list, or None."""
    counts: dict[int, int] = {}
    for c in clips:
        if c.color is not None:
            counts[c.color] = counts.get(c.color, 0) + 1
    if not counts:
        return None
    # Highest count wins; if tie, the lowest RGB value wins (deterministic)
    return max(counts.items(), key=lambda kv: (kv[1], -kv[0]))[0]


def _rgb_to_hue_key(rgb: Optional[int]) -> tuple[int, float, float]:
    """Convert a 0xRRGGBB colour to a sort key that produces a perceptual
    rainbow order (red → orange → yellow → green → cyan → blue → magenta).
    Greys and blacks (low saturation) go at the end.

    Returns (bucket, hue, brightness) where:
        bucket = 0 for coloured values, 1 for greys (sorted last)
        hue    = 0-360 degree wheel position
        brightness = tiebreaker within the same hue
    """
    if rgb is None:
        return (2, 0.0, 0.0)   # no colour info -> absolute last
    r = ((rgb >> 16) & 0xFF) / 255.0
    g = ((rgb >> 8)  & 0xFF) / 255.0
    b = ( rgb        & 0xFF) / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    delta = mx - mn
    # Saturation used to separate greys from colours
    sat = 0 if mx == 0 else delta / mx

    if delta < 1e-6 or sat < 0.1:
        # Grey: bucket 1, sorted by brightness
        return (1, 0.0, mx)

    if mx == r:
        h = ((g - b) / delta) % 6
    elif mx == g:
        h = (b - r) / delta + 2
    else:
        h = (r - g) / delta + 4
    hue_deg = h * 60.0
    return (0, hue_deg, mx)


def _assign_lanes(clips: list[ClipInfo], base_track_0: int) -> int:
    """Classic lane-assignment. Mutates each clip's .new_track (1-based).
    Returns the number of lanes used.
    """
    order = sorted(range(len(clips)), key=lambda i: clips[i].position)
    lanes_end: list[int] = []
    for idx in order:
        c = clips[idx]
        placed = False
        for li, le in enumerate(lanes_end):
            if c.position >= le:
                lanes_end[li] = c.position + c.length
                c.new_track = base_track_0 + li + 1  # convert to 1-based
                placed = True
                break
        if not placed:
            lanes_end.append(c.position + c.length)
            c.new_track = base_track_0 + len(lanes_end)  # 1-based
    return len(lanes_end)


# ----- Main entry points -----

SORT_ALPHABETICAL_OLD = "alphabetical"  # legacy alias kept for compatibility


def analyze(flp_path: Path | str,
            sort_mode: str = SORT_ALPHABETICAL,
            sub_sort: Optional[list[str]] = None) -> AnalysisResult:
    """Parse the .flp file and compute the grouping plan. Does not modify anything.

    sort_mode:
        SORT_ALPHABETICAL        - groups ordered A-Z, case-insensitive (default)
        SORT_BY_FIRST_APPEARANCE - groups ordered by the earliest position of
                                   any clip in that group

    sub_sort: optional list of sub-sort modifiers that refine the order within
              the primary sort. They are applied as tie-breakers in the listed
              order. Available modifiers:
                SUB_BY_LENGTH - groups with longer average clip length first
                SUB_BY_TYPE   - audio clips first, then patterns
                SUB_BY_COLOR  - groups ordered by perceptual rainbow hue
                                (red → orange → yellow → green → blue → purple).
                                Greys and uncoloured groups go at the end.
    """
    path = Path(flp_path)
    data = path.read_bytes()

    if data[:4] != b"FLhd":
        raise ValueError("Not a valid FLP file (missing 'FLhd' header)")
    if data[14:18] != b"FLdt":
        raise ValueError("Not a valid FLP file (missing 'FLdt' chunk)")

    ppq = struct.unpack("<H", data[12:14])[0]
    events_size = struct.unpack("<I", data[18:22])[0]
    if len(data) != events_size + 22:
        raise ValueError("Corrupted FLP: data chunk size mismatch")

    result = AnalysisResult(ppq=ppq, _data=data)

    # Parse events
    pos = 22
    end = 22 + events_size
    is_unicode = True
    channels: dict[int, dict] = {}
    patterns: dict[int, dict] = {}
    arrangements: list[dict] = []
    cur_ch: Optional[int] = None
    cur_pat: Optional[int] = None
    cur_arr: Optional[dict] = None
    cur_track_idx = -1

    while pos < end:
        evt_id = data[pos]
        pos += 1
        payload_start = pos
        if evt_id < WORD_BASE:
            payload_size = 1; pos += 1
        elif evt_id < DWORD_BASE:
            payload_size = 2; pos += 2
        elif evt_id < TEXT_BASE:
            payload_size = 4; pos += 4
        else:
            length, new_pos = _read_varint(data, pos)
            payload_size = length
            payload_start = new_pos
            pos = new_pos + length
        payload = data[payload_start:payload_start + payload_size]

        if evt_id == ID_FL_VERSION:
            try:
                ver = payload.decode("ascii", errors="replace").rstrip("\0")
                result.fl_version = ver
                parts = ver.split(".")
                major = int(parts[0])
                minor = int(parts[1]) if len(parts) > 1 else 0
                is_unicode = (major >= 12) or (major == 11 and minor >= 5)
            except Exception:
                pass

        elif evt_id == ID_CHANNEL_NEW:
            cur_ch = struct.unpack("<H", payload)[0]
            channels.setdefault(cur_ch, {"name": None, "sample_path": None,
                                          "default_name": None, "color": None})

        elif evt_id == ID_CHANNEL_NAME and cur_ch is not None:
            channels[cur_ch]["name"] = _decode_str(payload, is_unicode)

        elif evt_id == ID_CHANNEL_SAMPLE and cur_ch is not None:
            channels[cur_ch]["sample_path"] = _decode_str(payload, is_unicode)

        elif evt_id == ID_DEFAULT_NAME and cur_ch is not None:
            if not channels[cur_ch].get("default_name"):
                channels[cur_ch]["default_name"] = _decode_str(payload, is_unicode)

        elif evt_id == ID_CHANNEL_COLOR and cur_ch is not None:
            # 4-byte DWORD, low 24 bits are RGB (0x00RRGGBB, alpha unused)
            channels[cur_ch]["color"] = struct.unpack("<I", payload)[0] & 0xFFFFFF

        elif evt_id == ID_PATTERN_NEW:
            cur_pat = struct.unpack("<H", payload)[0]
            patterns.setdefault(cur_pat, {"name": None, "color": None})

        elif evt_id == ID_PATTERN_NAME and cur_pat is not None:
            patterns[cur_pat]["name"] = _decode_str(payload, is_unicode)

        elif evt_id == ID_PATTERN_COLOR and cur_pat is not None:
            patterns[cur_pat]["color"] = struct.unpack("<I", payload)[0] & 0xFFFFFF

        elif evt_id == ID_ARRANGEMENT_NEW:
            iid = struct.unpack("<H", payload)[0]
            cur_arr = {
                "iid": iid, "name": None, "playlist_offset": None,
                "playlist_size": 0, "item_size": 0,
            }
            arrangements.append(cur_arr)
            cur_track_idx = -1

        elif evt_id == ID_ARRANGEMENT_NAME and cur_arr is not None:
            cur_arr["name"] = _decode_str(payload, is_unicode)

        elif evt_id == ID_PLAYLIST and cur_arr is not None:
            cur_arr["playlist_offset"] = payload_start
            cur_arr["playlist_size"] = payload_size
            detected = _detect_item_size(data, payload_start, payload_size)
            cur_arr["item_size"] = detected or 0
            if detected is None:
                result.warnings.append(
                    f"Could not detect playlist item size for arrangement '{cur_arr['name']}'."
                )

        elif evt_id == ID_TRACK_DATA:
            cur_track_idx += 1

        elif evt_id == ID_TRACK_NAME and cur_arr is not None and cur_track_idx >= 0:
            # track name -- currently not used, but could be useful later
            pass

    result.channel_count = len(channels)
    result.pattern_count = len(patterns)
    result.arrangement_count = len(arrangements)

    # Collect clips and compute the plan
    all_clips: list[ClipInfo] = []
    total_tracks = 0

    for arr in arrangements:
        off = arr["playlist_offset"]
        isz = arr["item_size"]
        if off is None or isz <= 0:
            continue
        n = arr["playlist_size"] // isz

        arr_clips: list[ClipInfo] = []
        for i in range(n):
            base = off + i * isz
            position     = struct.unpack_from("<I", data, base + 0)[0]
            pattern_base = struct.unpack_from("<H", data, base + 4)[0]
            item_index   = struct.unpack_from("<H", data, base + 6)[0]
            length       = struct.unpack_from("<I", data, base + 8)[0]
            rvidx        = struct.unpack_from("<H", data, base + 12)[0]
            u1           = bytes(data[base + 16:base + 18])
            u2           = bytes(data[base + 20:base + 24])

            # Skip ghost items and any record that doesn't match the known
            # signature of real playlist items. Real items have fixed "magic"
            # bytes at offsets 16-17 and 20-23.
            if (pattern_base != PATTERN_BASE_VAL
                    or rvidx >= MAX_TRACKS
                    or length > 10_000_000
                    or u1 != b"\x78\x00"
                    or u2 != b"\x40\x64\x80\x80"):
                continue
            name, kind = _group_name(pattern_base, item_index, channels, patterns)
            if name is None:
                continue
            # Look up source colour
            if kind == "channel":
                src_color = channels.get(item_index, {}).get("color")
            else:
                src_color = patterns.get(item_index - PATTERN_BASE_VAL, {}).get("color")
            clip = ClipInfo(
                name=name, kind=kind,
                position=position, length=length,
                old_track=(MAX_TRACKS - 1 - rvidx) + 1,  # 1-based
                color=src_color,
                item_offset=base,
                rvidx_offset=base + 12,
                old_rvidx=rvidx,
            )
            arr_clips.append(clip)

        # Group by name
        groups: dict[str, list[ClipInfo]] = defaultdict(list)
        for c in arr_clips:
            groups[c.name].append(c)

        # ---------- Compute the ordering of groups ----------
        # Build the primary sort key per group
        def primary_key(group_name: str):
            clips_in_group = groups[group_name]
            if sort_mode == SORT_BY_FIRST_APPEARANCE:
                return min(c.position for c in clips_in_group)
            # Alphabetical - case-insensitive. Use the name itself as key.
            return group_name.lower()

        # Build the sub-sort composite key (applied as tie-breaker AND also
        # used to re-group within the primary order)
        def composite_key(group_name: str):
            clips_in_group = groups[group_name]
            key = [primary_key(group_name)]
            for modifier in (sub_sort or []):
                if modifier == SUB_BY_LENGTH:
                    # Longer average length first — negate for ascending sort
                    avg_len = sum(c.length for c in clips_in_group) / len(clips_in_group)
                    key.append(-avg_len)
                elif modifier == SUB_BY_TYPE:
                    # Channel (audio) = 0, pattern = 1  → audio goes first
                    most_common_kind = clips_in_group[0].kind  # clips in a group share name
                    key.append(0 if most_common_kind == "channel" else 1)
                elif modifier == SUB_BY_COLOR:
                    # Perceptual rainbow ordering based on the dominant color
                    # in the group (majority wins among source channels/patterns)
                    dom = _dominant_color(clips_in_group)
                    key.append(_rgb_to_hue_key(dom))
            return tuple(key)

        # If there is no sub-sort, the behaviour is identical to before
        if not sub_sort:
            if sort_mode == SORT_BY_FIRST_APPEARANCE:
                sorted_names = sorted(groups.keys(),
                                      key=lambda n: min(c.position for c in groups[n]))
            else:
                sorted_names = sorted(groups.keys(), key=lambda s: s.lower())
        else:
            # With sub-sort: the composite key decides the order. The sub-sort
            # acts as BOTH a tie-breaker AND a grouping criterion — for example
            # "Alphabetical + By type" produces all audio names A-Z first, then
            # all pattern names A-Z.
            # To do this we reverse the order: apply sub-sort modifiers first,
            # then primary. That way groups with the same sub-sort key stay
            # contiguous and are internally sorted by the primary key.
            def grouping_key(group_name: str):
                clips_in_group = groups[group_name]
                parts = []
                for modifier in sub_sort:
                    if modifier == SUB_BY_TYPE:
                        parts.append(0 if clips_in_group[0].kind == "channel" else 1)
                    elif modifier == SUB_BY_LENGTH:
                        avg_len = sum(c.length for c in clips_in_group) / len(clips_in_group)
                        parts.append(-avg_len)
                    elif modifier == SUB_BY_COLOR:
                        # Dominant color of the group, sorted by hue
                        dom = _dominant_color(clips_in_group)
                        parts.append(_rgb_to_hue_key(dom))
                # Primary sort added last -> becomes the innermost ordering
                parts.append(primary_key(group_name))
                return tuple(parts)

            sorted_names = sorted(groups.keys(), key=grouping_key)
        base_track_0 = 0
        for name in sorted_names:
            group_clips = groups[name]
            used = _assign_lanes(group_clips, base_track_0)
            result.groups.append(GroupPlan(
                name=name,
                first_track=base_track_0 + 1,
                lanes_used=used,
                clip_count=len(group_clips),
            ))
            base_track_0 += used

        if base_track_0 > MAX_TRACKS:
            result.warnings.append(
                f"Arrangement '{arr['name']}' needs {base_track_0} tracks "
                f"but the playlist has only {MAX_TRACKS}. Some clips will not be moved."
            )

        # Build patches: one per clip where track changed
        for c in arr_clips:
            new_track_0 = c.new_track - 1
            new_rvidx = MAX_TRACKS - 1 - new_track_0
            if new_rvidx != c.old_rvidx and 0 <= new_track_0 < MAX_TRACKS:
                result._patches.append((c.rvidx_offset, new_rvidx))

        total_tracks = max(total_tracks, base_track_0)
        all_clips.extend(arr_clips)

    result.total_clips = len(all_clips)
    result.total_tracks_needed = total_tracks
    result.clips = all_clips
    return result


def apply_plan(result: AnalysisResult, output_path: Path | str,
               progress: Optional[Callable[[int, int], None]] = None) -> None:
    """Writes the reorganized file using the patches computed by analyze()."""
    out = bytearray(result._data)
    total = len(result._patches)
    for i, (offset, new_rvidx) in enumerate(result._patches):
        struct.pack_into("<H", out, offset, new_rvidx)
        if progress and (i % 50 == 0 or i == total - 1):
            progress(i + 1, total)
    Path(output_path).write_bytes(bytes(out))


def reorganize(flp_path: Path | str, output_path: Path | str,
               progress: Optional[Callable[[int, int], None]] = None,
               sort_mode: str = SORT_ALPHABETICAL,
               sub_sort: Optional[list[str]] = None) -> AnalysisResult:
    """One-shot: analyze + write. Returns the AnalysisResult."""
    result = analyze(flp_path, sort_mode=sort_mode, sub_sort=sub_sort)
    apply_plan(result, output_path, progress=progress)
    return result
