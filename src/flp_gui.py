"""
FLP Organizer - GUI
===================

Tkinter-based GUI. Drag and drop an .flp file, preview the grouping plan,
then apply. Zero external dependencies beyond standard Python and tkinterdnd2.
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
APP_VERSION = "1.0.0"

# ----- Color palette (dark theme, FL Studio vibes) -----
BG         = "#1e1e22"
BG_ALT     = "#26262b"
BG_PANEL   = "#2c2c33"
FG         = "#e8e8ea"
FG_DIM     = "#9a9aa2"
ACCENT     = "#ff7a00"
ACCENT_FG  = "#ffffff"
BORDER     = "#3a3a42"
OK_GREEN   = "#4caf50"
WARN_AMBER = "#ffb300"


class FlpOrganizerApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("760x640")
        self.root.minsize(640, 520)
        self.root.configure(bg=BG)

        self.current_path: Path | None = None
        self.current_result: flp_core.AnalysisResult | None = None

        self._setup_style()
        self._build_ui()

        if DND_AVAILABLE:
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind("<<Drop>>", self._on_drop)

    # ---------- UI setup ----------
    def _setup_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=BG_PANEL)
        style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=BG, foreground=FG,
                        font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", background=BG, foreground=FG_DIM,
                        font=("Segoe UI", 9))
        style.configure("Panel.TLabel", background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 10))
        style.configure("PanelDim.TLabel", background=BG_PANEL, foreground=FG_DIM,
                        font=("Segoe UI", 9))

        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"),
                        background=ACCENT, foreground=ACCENT_FG,
                        borderwidth=0, focusthickness=0, padding=(16, 8))
        style.map("Accent.TButton",
                  background=[("active", "#ff9124"), ("disabled", "#555")],
                  foreground=[("disabled", "#aaa")])

        style.configure("Secondary.TButton", font=("Segoe UI", 10),
                        background=BG_PANEL, foreground=FG,
                        borderwidth=1, focusthickness=0, padding=(12, 6))
        style.map("Secondary.TButton",
                  background=[("active", BG_ALT)])

        style.configure("Treeview", background=BG_ALT, foreground=FG,
                        fieldbackground=BG_ALT, borderwidth=0,
                        font=("Segoe UI", 9), rowheight=22)
        style.configure("Treeview.Heading", background=BG_PANEL, foreground=FG,
                        font=("Segoe UI", 9, "bold"), borderwidth=0, relief="flat")
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", ACCENT_FG)])

        style.configure("TProgressbar", troughcolor=BG_PANEL, background=ACCENT,
                        borderwidth=0, thickness=6)

    def _build_ui(self) -> None:
        # Header
        header = ttk.Frame(self.root, padding=(20, 18, 20, 10))
        header.pack(fill="x")
        ttk.Label(header, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Groups playlist clips by name onto adjacent tracks. "
                 "Preserves every clip's position, length, and properties.",
            style="Subtitle.TLabel",
            wraplength=700,
        ).pack(anchor="w", pady=(2, 0))

        # Drop zone
        drop_wrap = ttk.Frame(self.root, padding=(20, 4, 20, 10))
        drop_wrap.pack(fill="x")
        self.drop_zone = tk.Frame(
            drop_wrap, bg=BG_PANEL, height=80,
            highlightbackground=BORDER, highlightthickness=1,
        )
        self.drop_zone.pack(fill="x")
        self.drop_zone.pack_propagate(False)

        drop_inner = tk.Frame(self.drop_zone, bg=BG_PANEL)
        drop_inner.pack(expand=True)
        self.drop_label = tk.Label(
            drop_inner,
            text=("Drag & drop a .flp file here    or" if DND_AVAILABLE
                  else "Drag & drop not available.    Click below to browse:"),
            bg=BG_PANEL, fg=FG_DIM, font=("Segoe UI", 10),
        )
        self.drop_label.pack(side="left", padx=(14, 10), pady=14)
        ttk.Button(drop_inner, text="Browse…", style="Secondary.TButton",
                   command=self._pick_file).pack(side="left", pady=14)

        # Info bar
        info_bar = ttk.Frame(self.root, padding=(20, 0, 20, 6))
        info_bar.pack(fill="x")
        self.info_label = ttk.Label(info_bar, text="No file loaded.", style="Subtitle.TLabel")
        self.info_label.pack(anchor="w")

        # Preview tree
        preview_wrap = ttk.Frame(self.root, padding=(20, 4, 20, 6))
        preview_wrap.pack(fill="both", expand=True)

        tree_frame = tk.Frame(preview_wrap, bg=BG_ALT,
                              highlightbackground=BORDER, highlightthickness=1)
        tree_frame.pack(fill="both", expand=True)

        columns = ("tracks", "count", "name")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=14)
        self.tree.heading("tracks", text="Tracks")
        self.tree.heading("count", text="Clips")
        self.tree.heading("name", text="Group name")
        self.tree.column("tracks", width=90, anchor="center", stretch=False)
        self.tree.column("count",  width=70, anchor="center", stretch=False)
        self.tree.column("name",   width=500, anchor="w")

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode="determinate", maximum=100)

        # Bottom bar
        bottom = ttk.Frame(self.root, padding=(20, 8, 20, 16))
        bottom.pack(fill="x")

        self.status_label = ttk.Label(bottom, text="", style="Subtitle.TLabel")
        self.status_label.pack(side="left")

        self.apply_btn = ttk.Button(bottom, text="Apply & Save…",
                                    style="Accent.TButton", state="disabled",
                                    command=self._apply)
        self.apply_btn.pack(side="right")

        self.clear_btn = ttk.Button(bottom, text="Clear", style="Secondary.TButton",
                                    state="disabled", command=self._clear)
        self.clear_btn.pack(side="right", padx=(0, 8))

    # ---------- File loading ----------
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
        self.info_label.config(text=f"Loading: {path.name}…")
        self.status_label.config(text="")
        self.tree.delete(*self.tree.get_children())
        self.apply_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.root.update_idletasks()

        # Run analysis in thread to keep UI responsive
        threading.Thread(target=self._analyze_worker, args=(path,), daemon=True).start()

    def _analyze_worker(self, path: Path) -> None:
        try:
            result = flp_core.analyze(path)
        except Exception as e:
            self.root.after(0, lambda: self._on_analyze_error(e))
            return
        self.root.after(0, lambda: self._on_analyze_done(result))

    def _on_analyze_error(self, e: Exception) -> None:
        self.info_label.config(text="Failed to read file.")
        messagebox.showerror(APP_NAME, f"Failed to read the file:\n\n{e}")
        self.current_path = None

    def _on_analyze_done(self, result: flp_core.AnalysisResult) -> None:
        self.current_result = result
        assert self.current_path is not None
        path = self.current_path

        info = (f"{path.name}  |  FL {result.fl_version}  |  "
                f"{result.total_clips} clips  |  "
                f"{len(result.groups)} groups  |  "
                f"{result.total_tracks_needed} tracks needed  |  "
                f"{len(result._patches)} clips will move")
        self.info_label.config(text=info)

        for g in result.groups:
            track_txt = (f"{g.first_track}" if g.lanes_used == 1
                         else f"{g.first_track}-{g.first_track + g.lanes_used - 1}")
            self.tree.insert("", "end", values=(track_txt, g.clip_count, g.name))

        if result.warnings:
            self.status_label.config(text="⚠  " + result.warnings[0],
                                     foreground=WARN_AMBER)
        else:
            self.status_label.config(text="Ready to apply.", foreground=OK_GREEN)

        has_changes = len(result._patches) > 0
        self.apply_btn.configure(state=("normal" if has_changes else "disabled"))
        self.clear_btn.configure(state="normal")
        if not has_changes:
            self.status_label.config(text="Nothing to change — file is already organized.",
                                     foreground=FG_DIM)

    # ---------- Apply ----------
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

        # Prevent overwriting the input accidentally
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
        self.progress.pack(fill="x", padx=20, pady=(0, 6), before=self.tree.master.master)
        self.progress["value"] = 0
        self.status_label.config(text="Writing…", foreground=FG_DIM)

        threading.Thread(target=self._apply_worker, args=(out_path,), daemon=True).start()

    def _apply_worker(self, out_path: Path) -> None:
        assert self.current_result is not None
        try:
            total = max(1, len(self.current_result._patches))
            def prog(done: int, tot: int) -> None:
                self.root.after(0, lambda: self.progress.configure(value=done * 100 / tot))
            flp_core.apply_plan(self.current_result, out_path, progress=prog)
        except Exception as e:
            self.root.after(0, lambda: self._on_apply_error(e))
            return
        self.root.after(0, lambda: self._on_apply_done(out_path))

    def _on_apply_error(self, e: Exception) -> None:
        self.progress.pack_forget()
        self.status_label.config(text="Write failed.", foreground=WARN_AMBER)
        self.apply_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        messagebox.showerror(APP_NAME, f"Could not write the file:\n\n{e}")

    def _on_apply_done(self, out_path: Path) -> None:
        self.progress.pack_forget()
        self.status_label.config(text=f"✓  Saved: {out_path.name}", foreground=OK_GREEN)
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
        self.info_label.config(text="No file loaded.")
        self.status_label.config(text="", foreground=FG_DIM)
        self.apply_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")


def main() -> None:
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = FlpOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
