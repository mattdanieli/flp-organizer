"""
FLP Organizer - Modern GUI (v1.1)
=================================

FL-Studio-inspired dark theme with energetic orange accents.
Rounded corners, gradient touches, subtle hover animations.
"""
from __future__ import annotations
import os
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    TkinterDnD = None  # type: ignore

import flp_core


APP_NAME = "FLP Organizer"
APP_VERSION = "1.1.1"

# --- FL Studio-inspired palette ------------------------------------------------
BG              = "#141416"
BG_PANEL        = "#1c1c1f"
BG_PANEL_HOVER  = "#232327"
BG_INSET        = "#0f0f11"
BG_ROW          = "#1a1a1d"
BG_ROW_ALT      = "#1e1e21"
BORDER          = "#2a2a2f"
BORDER_STRONG   = "#3a3a41"

FG              = "#f0f0f2"
FG_DIM          = "#9a9aa2"
FG_MUTED        = "#5f5f66"

ACCENT          = "#ff7a00"
ACCENT_HOVER    = "#ff9124"
ACCENT_PRESSED  = "#e66a00"
ACCENT_FG       = "#1a1a1d"

OK_GREEN        = "#4ade80"
WARN_AMBER      = "#fbbf24"
ERROR_RED       = "#f87171"

SELECTION_BG    = "#2a1f0f"
SELECTION_FG    = "#ffb366"


def _lighten(hex_color: str, amount: float = 0.1) -> str:
    hc = hex_color.lstrip("#")
    r, g, b = int(hc[0:2], 16), int(hc[2:4], 16), int(hc[4:6], 16)
    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))
    return f"#{r:02x}{g:02x}{b:02x}"


def _darken(hex_color: str, amount: float = 0.15) -> str:
    hc = hex_color.lstrip("#")
    r, g, b = int(hc[0:2], 16), int(hc[2:4], 16), int(hc[4:6], 16)
    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))
    return f"#{r:02x}{g:02x}{b:02x}"


def _rounded_on(canvas, x1, y1, x2, y2, r, fill, outline=""):
    """Draw a filled rounded rectangle using ovals (robust across tk versions)."""
    if not outline:
        outline = fill
    # Four corner circles
    canvas.create_oval(x1, y1, x1 + 2*r, y1 + 2*r, fill=fill, outline=outline)
    canvas.create_oval(x2 - 2*r, y1, x2, y1 + 2*r, fill=fill, outline=outline)
    canvas.create_oval(x1, y2 - 2*r, x1 + 2*r, y2, fill=fill, outline=outline)
    canvas.create_oval(x2 - 2*r, y2 - 2*r, x2, y2, fill=fill, outline=outline)
    # Two rectangles to cover the inside
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill, outline=outline)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill, outline=outline)


class RoundedButton(tk.Canvas):
    """Rounded canvas button with hover/pressed animation."""

    def __init__(self, parent, text="", command=None, style="accent",
                 width=160, height=40, radius=12, font=None, **kwargs):
        bg_parent = kwargs.pop("bg", BG_PANEL)
        super().__init__(parent, width=width, height=height,
                         bg=bg_parent, highlightthickness=0, bd=0, **kwargs)
        self._command = command
        self._text = text
        self._width = width
        self._height = height
        self._radius = radius
        self._font = font or ("Segoe UI", 10, "bold")
        self._state = "normal"
        self._style = style
        self._colors = self._style_colors(style)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", lambda e: self._redraw())
        self._redraw()

    def _style_colors(self, style):
        if style == "accent":
            return {"normal":   (ACCENT,         ACCENT_FG),
                    "hover":    (ACCENT_HOVER,   ACCENT_FG),
                    "pressed":  (ACCENT_PRESSED, ACCENT_FG),
                    "disabled": ("#3a2a1a",      "#7a6a5a")}
        if style == "secondary":
            return {"normal":   (BG_PANEL,       FG),
                    "hover":    (BG_PANEL_HOVER, FG),
                    "pressed":  (BG_INSET,       FG),
                    "disabled": (BG_PANEL,       FG_MUTED)}
        return {"normal":   (BG, FG_DIM),
                "hover":    (BG_PANEL, FG),
                "pressed":  (BG_INSET, FG_DIM),
                "disabled": (BG, FG_MUTED)}

    def configure_state(self, enabled: bool) -> None:
        self._state = "normal" if enabled else "disabled"
        self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or self._width
        h = self.winfo_height() or self._height
        bg_col, fg_col = self._colors[self._state]
        r = min(self._radius, h // 2, w // 2)

        # Base shape
        _rounded_on(self, 1, 1, w - 1, h - 1, r, fill=bg_col)

        # Gradient accent: draw a slightly lighter rounded shape on top, inset
        if self._style == "accent" and self._state in ("normal", "hover"):
            glow = _lighten(bg_col, 0.22 if self._state == "hover" else 0.14)
            # Shorter rounded band at the top half
            inset_top = 3
            band_h = max(h // 2 - inset_top, 4)
            _rounded_on(self, 3, inset_top,
                        w - 3, inset_top + band_h,
                        max(r - 2, 2), fill=glow)

        # Label
        self.create_text(w // 2, h // 2, text=self._text, fill=fg_col, font=self._font)
        try:
            self.configure(cursor="hand2" if self._state != "disabled" else "arrow")
        except tk.TclError:
            pass

    def _on_enter(self, _e):
        if self._state in ("disabled", "pressed"): return
        self._state = "hover"; self._redraw()

    def _on_leave(self, _e):
        if self._state == "disabled": return
        self._state = "normal"; self._redraw()

    def _on_press(self, _e):
        if self._state == "disabled": return
        self._state = "pressed"; self._redraw()

    def _on_release(self, e):
        if self._state == "disabled": return
        was_pressed = self._state == "pressed"
        if 0 <= e.x <= self.winfo_width() and 0 <= e.y <= self.winfo_height():
            self._state = "hover"
        else:
            self._state = "normal"
        self._redraw()
        if was_pressed and self._command:
            self._command()


class SortModeToggle(tk.Canvas):
    """Two-option segmented pill with a sliding orange indicator."""

    def __init__(self, parent, options, initial=0, on_change=None,
                 height=40, **kwargs):
        bg_parent = kwargs.pop("bg", BG_PANEL)
        super().__init__(parent, height=height, bg=bg_parent,
                         highlightthickness=0, bd=0, **kwargs)
        self._options = options
        self._index = initial
        self._on_change = on_change
        self._height = height
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Button-1>", self._on_click)
        self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or 400
        h = self.winfo_height() or self._height
        r = h // 2
        _rounded_on(self, 1, 1, w - 1, h - 1, r, fill=BG_INSET)

        seg_w = (w - 8) / len(self._options)
        x0 = int(4 + self._index * seg_w)
        x1 = int(x0 + seg_w)
        ir = r - 3
        _rounded_on(self, x0, 4, x1, h - 4, ir, fill=ACCENT)
        glow = _lighten(ACCENT, 0.22)
        _rounded_on(self, x0 + 1, 5, x1 - 1, h // 2 + 2, ir, fill=glow)
        self.create_rectangle(x0 + ir, h // 2, x1 - ir, h - 4, fill=ACCENT, outline="")

        for i, label in enumerate(self._options):
            cx = int(4 + seg_w * i + seg_w / 2)
            if i == self._index:
                self.create_text(cx, h // 2, text=label, fill=ACCENT_FG,
                                 font=("Segoe UI", 9, "bold"))
            else:
                self.create_text(cx, h // 2, text=label, fill=FG_DIM,
                                 font=("Segoe UI", 9))
        self.configure(cursor="hand2")

    def _on_click(self, e):
        w = self.winfo_width() or 400
        seg_w = (w - 8) / len(self._options)
        idx = int(max(0, min(len(self._options) - 1, (e.x - 4) // seg_w)))
        if idx != self._index:
            self._index = idx
            self._redraw()
            if self._on_change:
                self._on_change(self._index)

    def get(self) -> int:
        return self._index


class DropZone(tk.Canvas):
    """Dashed rounded drop area with hover state."""

    def __init__(self, parent, on_click=None, height=130, **kwargs):
        bg_parent = kwargs.pop("bg", BG)
        super().__init__(parent, height=height, bg=bg_parent,
                         highlightthickness=0, bd=0, **kwargs)
        self._hover = False
        self._on_click = on_click
        self._text_main = "Drop your .flp file here"
        self._text_sub = "or click to browse"
        self.bind("<Configure>", lambda e: self._redraw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", lambda e: self._on_click() if self._on_click else None)
        self._redraw()

    def set_text(self, main: str, sub: str = "") -> None:
        self._text_main = main
        self._text_sub = sub
        self._redraw()

    def _on_enter(self, _e): self._hover = True; self._redraw()
    def _on_leave(self, _e): self._hover = False; self._redraw()

    def _redraw(self):
        self.delete("all")
        w = self.winfo_width() or 600
        h = self.winfo_height() or 130
        r = 16
        fill = BG_PANEL_HOVER if self._hover else BG_PANEL
        _rounded_on(self, 2, 2, w - 2, h - 2, r, fill=fill)
        border_col = ACCENT if self._hover else BORDER_STRONG
        self._dashed_border(2, 2, w - 2, h - 2, r, border_col)

        icon_y = h // 2 - 16
        icon_x = w // 2
        col = ACCENT if self._hover else FG_DIM
        self._upload_icon(icon_x, icon_y, col)

        self.create_text(w // 2, h // 2 + 18, text=self._text_main,
                         fill=FG if self._hover else FG_DIM,
                         font=("Segoe UI", 11, "bold"))
        if self._text_sub:
            self.create_text(w // 2, h // 2 + 40, text=self._text_sub,
                             fill=FG_MUTED, font=("Segoe UI", 9))
        self.configure(cursor="hand2")

    def _dashed_border(self, x1, y1, x2, y2, r, color):
        dash, gap = 6, 4
        def hdashes(y):
            x = x1 + r
            while x < x2 - r:
                self.create_line(x, y, min(x + dash, x2 - r), y, fill=color, width=2)
                x += dash + gap
        def vdashes(x):
            y = y1 + r
            while y < y2 - r:
                self.create_line(x, y, x, min(y + dash, y2 - r), fill=color, width=2)
                y += dash + gap
        hdashes(y1); hdashes(y2)
        vdashes(x1); vdashes(x2)
        # Corners: approximate arcs with short line segments
        import math
        for (cx, cy, start_deg) in [(x1 + r, y1 + r, 180),
                                     (x2 - r, y1 + r, 270),
                                     (x1 + r, y2 - r, 90),
                                     (x2 - r, y2 - r, 0)]:
            # Draw ~6 short dashes along the 90-degree arc
            for step in range(0, 90, 15):
                a1 = math.radians(start_deg + step)
                a2 = math.radians(start_deg + step + 8)
                self.create_line(
                    cx + r * math.cos(a1), cy + r * math.sin(a1),
                    cx + r * math.cos(a2), cy + r * math.sin(a2),
                    fill=color, width=2
                )

    def _upload_icon(self, cx, cy, color):
        self.create_polygon(cx, cy - 12, cx - 8, cy - 4, cx + 8, cy - 4,
                            fill=color, outline="")
        self.create_rectangle(cx - 3, cy - 6, cx + 3, cy + 6,
                              fill=color, outline="")
        self.create_rectangle(cx - 12, cy + 8, cx + 12, cy + 10,
                              fill=color, outline="")


class FlpOrganizerApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("880x720")
        self.root.minsize(720, 600)
        self.root.configure(bg=BG)

        self.current_path: Path | None = None
        self.current_result: flp_core.AnalysisResult | None = None
        self.sort_mode_idx = 0

        self._setup_ttk_style()
        self._build_ui()

        if DND_AVAILABLE:
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind("<<Drop>>", self._on_drop)

    def _setup_ttk_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Modern.Treeview",
                        background=BG_ROW, foreground=FG,
                        fieldbackground=BG_ROW, borderwidth=0,
                        font=("Segoe UI", 9), rowheight=26)
        style.configure("Modern.Treeview.Heading",
                        background=BG_INSET, foreground=FG_DIM,
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0, relief="flat", padding=(10, 8))
        style.map("Modern.Treeview",
                  background=[("selected", SELECTION_BG)],
                  foreground=[("selected", SELECTION_FG)])
        style.configure("Accent.Horizontal.TProgressbar",
                        troughcolor=BG_INSET, background=ACCENT,
                        borderwidth=0, thickness=8)
        style.configure("Modern.Vertical.TScrollbar",
                        background=BG_PANEL, troughcolor=BG_INSET,
                        borderwidth=0, arrowsize=0)

    def _build_ui(self) -> None:
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        header = tk.Frame(outer, bg=BG)
        header.pack(fill="x", pady=(0, 16))
        title_frame = tk.Frame(header, bg=BG)
        title_frame.pack(anchor="w")
        tk.Label(title_frame, text="FLP", bg=BG, fg=ACCENT,
                 font=("Segoe UI", 22, "bold")).pack(side="left")
        tk.Label(title_frame, text=" Organizer", bg=BG, fg=FG,
                 font=("Segoe UI", 22, "bold")).pack(side="left")
        tk.Label(title_frame, text=f"  v{APP_VERSION}", bg=BG, fg=FG_MUTED,
                 font=("Segoe UI", 10)).pack(side="left", padx=(4, 0), pady=(8, 0))
        tk.Label(header,
                 text="Automatically groups playlist clips by name onto adjacent tracks. "
                      "Preserves every position, length, color, and property.",
                 bg=BG, fg=FG_DIM, font=("Segoe UI", 10),
                 wraplength=820, justify="left").pack(anchor="w", pady=(6, 0))

        self.drop_zone = DropZone(outer, on_click=self._pick_file, height=120)
        self.drop_zone.pack(fill="x", pady=(0, 16))

        sort_card = tk.Frame(outer, bg=BG_PANEL)
        sort_card.pack(fill="x", pady=(0, 16))
        sort_inner = tk.Frame(sort_card, bg=BG_PANEL)
        sort_inner.pack(fill="x", padx=18, pady=14)

        row1 = tk.Frame(sort_inner, bg=BG_PANEL)
        row1.pack(fill="x")
        tk.Label(row1, text="Track order", bg=BG_PANEL, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(side="left")

        self.sort_toggle = SortModeToggle(
            sort_inner,
            options=["Alphabetical (A–Z)", "By first appearance"],
            initial=0, on_change=self._on_sort_changed, height=36,
        )
        self.sort_toggle.pack(fill="x", pady=(8, 6))

        self.sort_explanation = tk.Label(
            sort_inner, text=self._sort_text(0),
            bg=BG_PANEL, fg=FG_MUTED, font=("Segoe UI", 9),
            wraplength=800, justify="left"
        )
        self.sort_explanation.pack(anchor="w", pady=(4, 0))

        self.info_label = tk.Label(
            outer, text="No file loaded.",
            bg=BG, fg=FG_DIM, font=("Segoe UI", 9),
            anchor="w", justify="left"
        )
        self.info_label.pack(fill="x", pady=(0, 8))

        tree_card = tk.Frame(outer, bg=BG_PANEL)
        tree_card.pack(fill="both", expand=True, pady=(0, 14))
        tree_wrap = tk.Frame(tree_card, bg=BG_PANEL)
        tree_wrap.pack(fill="both", expand=True, padx=2, pady=2)

        columns = ("tracks", "count", "name")
        self.tree = ttk.Treeview(tree_wrap, columns=columns, show="headings",
                                 style="Modern.Treeview", height=12)
        self.tree.heading("tracks", text="  TRACK")
        self.tree.heading("count",  text="  CLIPS")
        self.tree.heading("name",   text="  GROUP NAME")
        self.tree.column("tracks", width=110, anchor="center", stretch=False)
        self.tree.column("count",  width=90,  anchor="center", stretch=False)
        self.tree.column("name",   width=600, anchor="w")
        self.tree.tag_configure("odd", background=BG_ROW)
        self.tree.tag_configure("even", background=BG_ROW_ALT)

        vscroll = ttk.Scrollbar(tree_wrap, orient="vertical",
                                command=self.tree.yview,
                                style="Modern.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=vscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.progress = ttk.Progressbar(outer, mode="determinate", maximum=100,
                                        style="Accent.Horizontal.TProgressbar")

        bottom = tk.Frame(outer, bg=BG)
        bottom.pack(fill="x")
        self.status_label = tk.Label(bottom, text="", bg=BG, fg=FG_DIM,
                                     font=("Segoe UI", 9), anchor="w")
        self.status_label.pack(side="left", fill="x", expand=True)

        self.apply_btn = RoundedButton(
            bottom, text="Apply & Save", style="accent",
            width=180, height=42, command=self._apply, bg=BG,
            font=("Segoe UI", 11, "bold")
        )
        self.apply_btn.pack(side="right")
        self.apply_btn.configure_state(False)

        self.clear_btn = RoundedButton(
            bottom, text="Clear", style="secondary",
            width=110, height=42, command=self._clear, bg=BG,
            font=("Segoe UI", 10)
        )
        self.clear_btn.pack(side="right", padx=(0, 10))
        self.clear_btn.configure_state(False)

    def _sort_text(self, idx: int) -> str:
        if idx == 0:
            return ("Groups are ordered alphabetically, case-insensitive. "
                    "Good for quickly finding a specific sample or pattern by name.")
        return ("Groups are ordered by the earliest time any of their clips plays. "
                "Elements that enter first (kick, bass) end up on top; "
                "elements that come later (build-ups, drop fills, outro) go further down. "
                "Good for reading the arrangement top-to-bottom like a timeline.")

    def _on_sort_changed(self, idx: int) -> None:
        self.sort_mode_idx = idx
        self.sort_explanation.configure(text=self._sort_text(idx))
        if self.current_path and self.current_result is not None:
            threading.Thread(target=self._analyze_worker,
                             args=(self.current_path,), daemon=True).start()
            self.info_label.config(text="Recomputing plan…")

    def _on_drop(self, event) -> None:
        paths = self.root.tk.splitlist(event.data)
        if paths:
            self._load_file(Path(paths[0]))

    def _pick_file(self) -> None:
        fname = filedialog.askopenfilename(
            title="Select an FL Studio project file",
            filetypes=[("FL Studio projects", "*.flp"), ("All files", "*.*")],
        )
        if fname:
            self._load_file(Path(fname))

    def _load_file(self, path: Path) -> None:
        if not path.exists() or path.suffix.lower() != ".flp":
            messagebox.showerror(APP_NAME, f"Not a valid .flp file:\n{path}")
            return
        self.current_path = path
        self.info_label.config(text=f"Loading: {path.name}…", fg=FG_DIM)
        self.status_label.config(text="")
        self.tree.delete(*self.tree.get_children())
        self.apply_btn.configure_state(False)
        self.clear_btn.configure_state(False)
        self.drop_zone.set_text(f"✓  {path.name}", "Click to choose a different file")
        self.root.update_idletasks()
        threading.Thread(target=self._analyze_worker, args=(path,), daemon=True).start()

    def _current_sort_mode(self) -> str:
        return (flp_core.SORT_BY_FIRST_APPEARANCE
                if self.sort_mode_idx == 1
                else flp_core.SORT_ALPHABETICAL)

    def _analyze_worker(self, path: Path) -> None:
        try:
            result = flp_core.analyze(path, sort_mode=self._current_sort_mode())
        except Exception as e:
            self.root.after(0, lambda: self._on_analyze_error(e))
            return
        self.root.after(0, lambda: self._on_analyze_done(result))

    def _on_analyze_error(self, e: Exception) -> None:
        self.info_label.config(text="Failed to read file.", fg=ERROR_RED)
        messagebox.showerror(APP_NAME, f"Failed to read the file:\n\n{e}")
        self.current_path = None
        self.drop_zone.set_text("Drop your .flp file here", "or click to browse")

    def _on_analyze_done(self, result: flp_core.AnalysisResult) -> None:
        self.current_result = result
        self.tree.delete(*self.tree.get_children())
        assert self.current_path is not None

        info = (f"{self.current_path.name}    •    FL {result.fl_version}    •    "
                f"{result.total_clips} clips    •    "
                f"{len(result.groups)} groups    •    "
                f"{result.total_tracks_needed} tracks needed    •    "
                f"{len(result._patches)} clips will move")
        self.info_label.config(text=info, fg=FG_DIM)

        for i, g in enumerate(result.groups):
            track_txt = (f"#{g.first_track}" if g.lanes_used == 1
                         else f"#{g.first_track}–{g.first_track + g.lanes_used - 1}")
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(track_txt, g.clip_count, g.name),
                             tags=(tag,))

        if result.warnings:
            self.status_label.config(text="⚠  " + result.warnings[0], fg=WARN_AMBER)
        else:
            self.status_label.config(text="Ready to apply.", fg=OK_GREEN)

        has_changes = len(result._patches) > 0
        self.apply_btn.configure_state(has_changes)
        self.clear_btn.configure_state(True)
        if not has_changes:
            self.status_label.config(text="Already organized — nothing to change.",
                                     fg=FG_MUTED)

    def _apply(self) -> None:
        if not (self.current_result and self.current_path):
            return
        default_name = self.current_path.stem + "_organized.flp"
        out = filedialog.asksaveasfilename(
            title="Save reorganized project as…",
            defaultextension=".flp",
            initialfile=default_name,
            initialdir=str(self.current_path.parent),
            filetypes=[("FL Studio projects", "*.flp")],
        )
        if not out:
            return
        out_path = Path(out)
        try:
            if out_path.resolve() == self.current_path.resolve():
                messagebox.showerror(
                    APP_NAME,
                    "For safety, you can't overwrite the original file.\n"
                    "Please choose a different filename.",
                )
                return
        except Exception:
            pass

        self.apply_btn.configure_state(False)
        self.clear_btn.configure_state(False)
        self.progress.pack(fill="x", pady=(0, 8), before=self.status_label.master)
        self.progress["value"] = 0
        self.status_label.config(text="Writing…", fg=FG_DIM)
        threading.Thread(target=self._apply_worker, args=(out_path,), daemon=True).start()

    def _apply_worker(self, out_path: Path) -> None:
        assert self.current_result is not None
        try:
            def prog(done: int, tot: int) -> None:
                self.root.after(0, lambda: self.progress.configure(value=done * 100 / tot))
            flp_core.apply_plan(self.current_result, out_path, progress=prog)
        except Exception as e:
            self.root.after(0, lambda: self._on_apply_error(e))
            return
        self.root.after(0, lambda: self._on_apply_done(out_path))

    def _on_apply_error(self, e: Exception) -> None:
        self.progress.pack_forget()
        self.status_label.config(text="Write failed.", fg=ERROR_RED)
        self.apply_btn.configure_state(True)
        self.clear_btn.configure_state(True)
        messagebox.showerror(APP_NAME, f"Could not write the file:\n\n{e}")

    def _on_apply_done(self, out_path: Path) -> None:
        self.progress.pack_forget()
        self.status_label.config(text=f"✓  Saved: {out_path.name}", fg=OK_GREEN)
        self.apply_btn.configure_state(True)
        self.clear_btn.configure_state(True)
        if messagebox.askyesno(
            APP_NAME,
            f"File saved successfully:\n{out_path}\n\nOpen the containing folder?",
        ):
            self._open_folder(out_path.parent)

    def _open_folder(self, folder: Path) -> None:
        try:
            if sys.platform.startswith("win"):
                os.startfile(str(folder))
            elif sys.platform == "darwin":
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')
        except Exception:
            pass

    def _clear(self) -> None:
        self.current_path = None
        self.current_result = None
        self.tree.delete(*self.tree.get_children())
        self.info_label.config(text="No file loaded.", fg=FG_DIM)
        self.status_label.config(text="", fg=FG_DIM)
        self.apply_btn.configure_state(False)
        self.clear_btn.configure_state(False)
        self.drop_zone.set_text("Drop your .flp file here", "or click to browse")


def main() -> None:
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = FlpOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
