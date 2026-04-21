"""
FLP Organizer - GUI (v1.1.2)
============================

Robust, standard-widget GUI with a dark FL-Studio-ish theme.
Uses only stock ttk widgets (no custom Canvas drawing) to avoid rendering
bugs on Windows/PyInstaller.
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
APP_VERSION = "1.1.0"

# --- Dark theme palette -----------------------------------------------------
BG          = "#141416"
BG_PANEL    = "#1f1f24"
BG_INSET    = "#0f0f11"
BG_ROW      = "#1a1a1d"
BG_ROW_ALT  = "#1e1e22"
BORDER      = "#2e2e35"

FG          = "#eeeef0"
FG_DIM      = "#9a9aa2"
FG_MUTED    = "#5f5f66"

ACCENT      = "#ff7a00"
ACCENT_HOV  = "#ff9124"
ACCENT_DIS  = "#5a3a1a"
ACCENT_FG   = "#1a1a1d"
ACCENT_DIM  = "#8a6340"

OK_GREEN    = "#4ade80"
WARN_AMBER  = "#fbbf24"
ERROR_RED   = "#f87171"


class FlpOrganizerApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("860x700")
        self.root.minsize(720, 580)
        self.root.configure(bg=BG)

        self.current_path: Path | None = None
        self.current_result: flp_core.AnalysisResult | None = None
        self.sort_mode_var = tk.StringVar(value="alpha")

        self._setup_style()
        self._build_ui()

        if DND_AVAILABLE:
            self.drop_area.drop_target_register(DND_FILES)
            self.drop_area.dnd_bind("<<Drop>>", self._on_drop)

    # ---------- style ----------
    def _setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=BG_PANEL)

        style.configure("TLabel", background=BG, foreground=FG,
                        font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=BG, foreground=FG,
                        font=("Segoe UI", 18, "bold"))
        style.configure("TitleAccent.TLabel", background=BG, foreground=ACCENT,
                        font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", background=BG, foreground=FG_DIM,
                        font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10, "bold"))
        style.configure("Caption.TLabel", background=BG_PANEL, foreground=FG_MUTED,
                        font=("Segoe UI", 9))
        style.configure("Status.TLabel", background=BG, foreground=FG_DIM,
                        font=("Segoe UI", 9))
        style.configure("StatusOK.TLabel", background=BG, foreground=OK_GREEN,
                        font=("Segoe UI", 9))
        style.configure("StatusWarn.TLabel", background=BG, foreground=WARN_AMBER,
                        font=("Segoe UI", 9))
        style.configure("StatusErr.TLabel", background=BG, foreground=ERROR_RED,
                        font=("Segoe UI", 9))

        # Accent button (orange)
        style.configure("Accent.TButton",
                        background=ACCENT, foreground=ACCENT_FG,
                        font=("Segoe UI", 10, "bold"),
                        borderwidth=0, focusthickness=0, padding=(22, 10))
        style.map("Accent.TButton",
                  background=[("active", ACCENT_HOV),
                              ("pressed", ACCENT_HOV),
                              ("disabled", ACCENT_DIS)],
                  foreground=[("disabled", ACCENT_DIM)])

        # Secondary button (dark panel)
        style.configure("Secondary.TButton",
                        background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10),
                        borderwidth=1, focusthickness=0, padding=(16, 8))
        style.map("Secondary.TButton",
                  background=[("active", BG_INSET),
                              ("pressed", BG_INSET),
                              ("disabled", BG_PANEL)],
                  foreground=[("disabled", FG_MUTED)])

        # Radiobutton (used for sort mode)
        style.configure("Toggle.TRadiobutton",
                        background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10, "bold"),
                        indicatorsize=0, focusthickness=0,
                        padding=(12, 8))
        style.map("Toggle.TRadiobutton",
                  background=[("selected", ACCENT),
                              ("active", BG_INSET)],
                  foreground=[("selected", ACCENT_FG)])

        # Treeview
        style.configure("Modern.Treeview",
                        background=BG_ROW, foreground=FG,
                        fieldbackground=BG_ROW, borderwidth=0,
                        font=("Segoe UI", 9), rowheight=24)
        style.configure("Modern.Treeview.Heading",
                        background=BG_INSET, foreground=FG_DIM,
                        font=("Segoe UI", 9, "bold"),
                        borderwidth=0, relief="flat", padding=(10, 6))
        style.map("Modern.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", ACCENT_FG)])

        # Progressbar
        style.configure("Accent.Horizontal.TProgressbar",
                        troughcolor=BG_INSET, background=ACCENT,
                        borderwidth=0, thickness=8)

        # LabelFrame
        style.configure("Card.TLabelframe",
                        background=BG_PANEL, foreground=FG_DIM,
                        borderwidth=1, relief="solid",
                        bordercolor=BORDER)
        style.configure("Card.TLabelframe.Label",
                        background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10, "bold"))

    # ---------- build ----------
    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, style="TFrame")
        outer.pack(fill="both", expand=True, padx=20, pady=16)

        # Header
        header = ttk.Frame(outer, style="TFrame")
        header.pack(fill="x", pady=(0, 14))

        title_row = ttk.Frame(header, style="TFrame")
        title_row.pack(anchor="w")
        ttk.Label(title_row, text="FLP",
                  style="TitleAccent.TLabel").pack(side="left")
        ttk.Label(title_row, text=" Organizer",
                  style="Title.TLabel").pack(side="left")
        ttk.Label(title_row, text=f"  v{APP_VERSION}",
                  style="Subtitle.TLabel").pack(side="left", padx=(6, 0))

        ttk.Label(
            header,
            text="Automatically groups playlist clips by name onto adjacent "
                 "tracks. Preserves every position, length, color, and property.",
            style="Subtitle.TLabel", wraplength=820, justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # Drop area (Frame with label inside)
        drop_wrap = ttk.Frame(outer, style="TFrame")
        drop_wrap.pack(fill="x", pady=(0, 14))

        self.drop_area = tk.Frame(
            drop_wrap, bg=BG_PANEL, height=90,
            highlightbackground=BORDER, highlightthickness=1,
            cursor="hand2",
        )
        self.drop_area.pack(fill="x")
        self.drop_area.pack_propagate(False)
        self.drop_area.bind("<Button-1>", lambda e: self._pick_file())
        self.drop_area.bind("<Enter>", lambda e: self._drop_hover(True))
        self.drop_area.bind("<Leave>", lambda e: self._drop_hover(False))

        self.drop_label = tk.Label(
            self.drop_area,
            text="  Drop your .flp file here   —   or click to browse",
            bg=BG_PANEL, fg=FG_DIM, font=("Segoe UI", 11, "bold"),
        )
        self.drop_label.pack(expand=True)
        self.drop_label.bind("<Button-1>", lambda e: self._pick_file())

        # Sort mode card
        sort_card = ttk.Labelframe(outer, text="  Track order  ",
                                   style="Card.TLabelframe", padding=14)
        sort_card.pack(fill="x", pady=(0, 14))

        radio_row = ttk.Frame(sort_card, style="Panel.TFrame")
        radio_row.pack(fill="x")

        ttk.Radiobutton(
            radio_row, text="  Alphabetical (A–Z)  ",
            variable=self.sort_mode_var, value="alpha",
            style="Toggle.TRadiobutton",
            command=self._on_sort_changed,
        ).pack(side="left", padx=(0, 8))

        ttk.Radiobutton(
            radio_row, text="  By first appearance  ",
            variable=self.sort_mode_var, value="first",
            style="Toggle.TRadiobutton",
            command=self._on_sort_changed,
        ).pack(side="left")

        self.sort_caption = ttk.Label(
            sort_card, text=self._caption_for("alpha"),
            style="Caption.TLabel", wraplength=780, justify="left"
        )
        self.sort_caption.pack(anchor="w", pady=(10, 0), fill="x")

        # Info bar
        self.info_label = ttk.Label(outer, text="No file loaded.",
                                    style="Subtitle.TLabel")
        self.info_label.pack(anchor="w", pady=(0, 6))

        # Treeview preview
        tree_wrap = tk.Frame(outer, bg=BG_PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        tree_wrap.pack(fill="both", expand=True, pady=(0, 12))

        columns = ("tracks", "count", "name")
        self.tree = ttk.Treeview(
            tree_wrap, columns=columns, show="headings",
            style="Modern.Treeview", height=11
        )
        self.tree.heading("tracks", text="  Track")
        self.tree.heading("count",  text="  Clips")
        self.tree.heading("name",   text="  Group name")
        self.tree.column("tracks", width=110, anchor="center", stretch=False)
        self.tree.column("count",  width=80,  anchor="center", stretch=False)
        self.tree.column("name",   width=600, anchor="w")

        self.tree.tag_configure("odd",  background=BG_ROW)
        self.tree.tag_configure("even", background=BG_ROW_ALT)

        vscroll = ttk.Scrollbar(tree_wrap, orient="vertical",
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        # Progress bar
        self.progress = ttk.Progressbar(
            outer, mode="determinate", maximum=100,
            style="Accent.Horizontal.TProgressbar"
        )

        # Bottom bar
        bottom = ttk.Frame(outer, style="TFrame")
        bottom.pack(fill="x")

        self.status_label = ttk.Label(bottom, text="", style="Status.TLabel")
        self.status_label.pack(side="left", fill="x", expand=True)

        self.apply_btn = ttk.Button(
            bottom, text="Apply & Save",
            style="Accent.TButton", command=self._apply, state="disabled",
        )
        self.apply_btn.pack(side="right")

        self.clear_btn = ttk.Button(
            bottom, text="Clear",
            style="Secondary.TButton", command=self._clear, state="disabled",
        )
        self.clear_btn.pack(side="right", padx=(0, 10))

    # ---------- helpers ----------
    def _caption_for(self, mode: str) -> str:
        if mode == "alpha":
            return ("Groups are ordered alphabetically, case-insensitive. "
                    "Good for quickly finding a specific sample or pattern by name.")
        return ("Groups are ordered by the earliest time any of their clips plays. "
                "Elements that enter first (kick, bass) end up on top tracks; "
                "build-ups, fills, and outros go further down. "
                "Good for reading the arrangement top-to-bottom like a timeline.")

    def _drop_hover(self, hovering: bool) -> None:
        color = ACCENT if hovering else BORDER
        try:
            self.drop_area.configure(highlightbackground=color)
        except tk.TclError:
            pass

    def _set_status(self, text: str, kind: str = "dim") -> None:
        styles = {"dim": "Status.TLabel", "ok": "StatusOK.TLabel",
                  "warn": "StatusWarn.TLabel", "err": "StatusErr.TLabel"}
        self.status_label.configure(text=text, style=styles.get(kind, "Status.TLabel"))

    def _on_sort_changed(self) -> None:
        mode = self.sort_mode_var.get()
        self.sort_caption.configure(text=self._caption_for(mode))
        if self.current_path is not None:
            threading.Thread(target=self._analyze_worker,
                             args=(self.current_path,), daemon=True).start()
            self.info_label.configure(text="Recomputing plan…")

    # ---------- file loading ----------
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
        self.info_label.configure(text=f"Loading: {path.name}…")
        self._set_status("")
        self.tree.delete(*self.tree.get_children())
        self.apply_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.drop_label.configure(text=f"  Loaded: {path.name}   —   click to choose a different file")
        threading.Thread(target=self._analyze_worker, args=(path,), daemon=True).start()

    def _current_sort_mode(self) -> str:
        return (flp_core.SORT_BY_FIRST_APPEARANCE
                if self.sort_mode_var.get() == "first"
                else flp_core.SORT_ALPHABETICAL)

    def _analyze_worker(self, path: Path) -> None:
        try:
            result = flp_core.analyze(path, sort_mode=self._current_sort_mode())
        except Exception as e:
            self.root.after(0, lambda: self._on_analyze_error(e))
            return
        self.root.after(0, lambda: self._on_analyze_done(result))

    def _on_analyze_error(self, e: Exception) -> None:
        self.info_label.configure(text="Failed to read file.")
        messagebox.showerror(APP_NAME, f"Failed to read the file:\n\n{e}")
        self.current_path = None
        self.drop_label.configure(text="  Drop your .flp file here   —   or click to browse")

    def _on_analyze_done(self, result: flp_core.AnalysisResult) -> None:
        self.current_result = result
        self.tree.delete(*self.tree.get_children())
        assert self.current_path is not None

        info = (f"{self.current_path.name}    •    FL {result.fl_version}    •    "
                f"{result.total_clips} clips    •    "
                f"{len(result.groups)} groups    •    "
                f"{result.total_tracks_needed} tracks needed    •    "
                f"{len(result._patches)} clips will move")
        self.info_label.configure(text=info)

        for i, g in enumerate(result.groups):
            track_txt = (f"#{g.first_track}" if g.lanes_used == 1
                         else f"#{g.first_track}–{g.first_track + g.lanes_used - 1}")
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end",
                             values=(track_txt, g.clip_count, g.name),
                             tags=(tag,))

        if result.warnings:
            self._set_status("⚠  " + result.warnings[0], kind="warn")
        else:
            self._set_status("Ready to apply.", kind="ok")

        has_changes = len(result._patches) > 0
        self.apply_btn.configure(state=("normal" if has_changes else "disabled"))
        self.clear_btn.configure(state="normal")
        if not has_changes:
            self._set_status("Already organized — nothing to change.", kind="dim")

    # ---------- apply ----------
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

        self.apply_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.progress.pack(fill="x", pady=(0, 6),
                           before=self.status_label.master)
        self.progress["value"] = 0
        self._set_status("Writing…", kind="dim")
        threading.Thread(target=self._apply_worker,
                         args=(out_path,), daemon=True).start()

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
        self._set_status("Write failed.", kind="err")
        self.apply_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        messagebox.showerror(APP_NAME, f"Could not write the file:\n\n{e}")

    def _on_apply_done(self, out_path: Path) -> None:
        self.progress.pack_forget()
        self._set_status(f"✓  Saved: {out_path.name}", kind="ok")
        self.apply_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
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
        self.info_label.configure(text="No file loaded.")
        self._set_status("")
        self.apply_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.drop_label.configure(text="  Drop your .flp file here   —   or click to browse")


def main() -> None:
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = FlpOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
