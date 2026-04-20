# Suggested announcement post

Copy-paste this (or adapt it) to announce your tool on Reddit, the Image-Line forum, Discord, etc.

---

## Short version (Discord, Twitter, Instagram caption)

> 🎛️ **FLP Organizer** — a free tool that auto-groups your FL Studio playlist clips by name onto adjacent tracks. Keeps every position, length, color, and automation intact. Zero config, drag-and-drop.
>
> Download (Windows): [your-release-link]
> Source (MIT): [your-repo-link]

---

## Medium version (r/FL_Studio, Image-Line forum "Utilities" section)

**Title:** FLP Organizer — free tool to automatically group playlist clips by name onto adjacent tracks

Hey everyone,

I got tired of manually reorganizing my FL Studio playlist so I built a small open-source tool that does it automatically.

**What it does:** Takes an .flp file and reorganizes the playlist so that every clip sharing the same name (sample, channel, or pattern) ends up on adjacent tracks, alphabetically ordered. If clips of the same group overlap in time, they get placed on adjacent lanes instead of being stacked.

**What it preserves:** every clip's position, length, stretched length, color, muted state, group assignment, offsets — literally everything. The tool works by patching only the 2 bytes per clip that encode the track index. Nothing else in the .flp is modified.

**What it doesn't do:** modify your patterns, your mixer, your plugins, your channels, or anything else inside the project. Just rearranges the playlist.

**How to use:** download the .exe, drag your .flp onto the window, preview the grouping plan, click Apply. It writes a new file — your original is never touched.

**Tested on:** FL Studio 25.1.6. Should work with FL 21+ (item size is auto-detected).

**Important:** Always keep a backup of your project. The tool won't overwrite the original but storage/software can always surprise you.

**Download (Windows .exe):** [your-release-link]
**Source code (MIT licensed, Python):** [your-repo-link]

Feedback and bug reports welcome — especially if you have a project from an older FL version and something breaks.

---

## Long version (blog post, YouTube description)

**FLP Organizer: the tool FL Studio should have shipped**

If you've ever worked on a big FL Studio project, you know the feeling: by the time you've got 30+ clips on the playlist — sampled drums, automation clips, pattern clips scattered across tracks 1 through 40 — finding anything becomes a nightmare. `Select source channel` helps a bit, and `Shift+drag` moves clips in parallel, but there's no way to say "take every 'Kick' clip everywhere in the playlist and put them all on the same track."

I built FLP Organizer to solve exactly that. It's a free, open-source tool that reads your .flp file directly, groups every playlist clip by its name (sample filename, channel name, or pattern name), and rewrites the file with each group occupying adjacent tracks. Clips that overlap in time automatically go on separate lanes inside the same group, so nothing gets stacked on top of anything else.

**What makes it safe:** the tool doesn't re-encode your project. It does surgical byte-level patches — modifying only the 2 bytes that store each clip's track index and leaving every other byte untouched. On a typical 2 MB project it changes about 400 bytes out of 2 million. Your patterns, automations, mixer state, plugin parameters, channel rack — everything stays bit-for-bit identical to the original.

**How to use:** download `FLPOrganizer.exe`, drag your .flp file onto the window, see the preview of what will go where, click Apply. The tool saves a new file next to your original (never overwrites).

**Why not a plugin?** FL Studio's scripting API doesn't expose playlist clip manipulation — only the Channel Rack, Mixer, and Piano Roll can be scripted. So the only way to do this automation is from outside, directly on the project file.

Download, source code, and full docs: [your-repo-link]

Built in Python with zero external dependencies at runtime. MIT licensed. PRs welcome.
