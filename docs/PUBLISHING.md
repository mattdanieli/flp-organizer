# Publishing FLP Organizer to GitHub — Step by Step

This guide assumes you have never published a project before. Follow it in order.

## Part 1 — Create the repository on GitHub

1. Go to **https://github.com** and sign in (or sign up if you don't have an account yet).
2. In the top-right corner, click the **+** icon → **New repository**.
3. Fill in:
   - **Repository name**: `flp-organizer`
   - **Description**: *Organize the FL Studio playlist by grouping every clip by name onto adjacent tracks*
   - **Public** (so anyone can download it)
   - **Do NOT** check "Add a README file", "Add .gitignore", or "Choose a license" — we already have those files
4. Click **Create repository**.
5. You'll see a page with setup instructions. Leave it open — you'll need it in a minute.

## Part 2 — Replace the placeholders in the files

Before uploading, edit two files to put your actual GitHub username:

- `README.md` — search for `YOUR_USERNAME` and replace with your GitHub username
- `LICENSE` — replace `YOUR_USERNAME` with your name (or your GitHub username)

You can do this in any text editor (Notepad works fine).

## Part 3 — Upload the files to the repository

You have two options. Pick one.

### Option A — Upload through the browser (simplest, no git knowledge needed)

1. On the empty repo page GitHub showed you in Part 1, click **uploading an existing file** (the link appears in the "Quick setup" box).
2. Drag the **entire contents** of the `flp-organizer` folder onto the browser window.
   - ⚠ Important: drag the files *inside* the folder, not the folder itself.
3. At the bottom, in the commit message box, write: `Initial commit`
4. Click **Commit changes**.

### Option B — Using Git (if you already have it installed)

Open a terminal inside the `flp-organizer` folder and run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/flp-organizer.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Part 4 — Build the Windows .exe and attach it to a release

The `.exe` is not stored in the git repo (it's too big). Instead, it's attached as a "release asset". You have two options again:

### Option A — Let GitHub build it for you (recommended, automatic)

The repo includes a GitHub Actions workflow that builds the `.exe` automatically whenever you push a version tag.

1. On your repo page, go to **Actions** tab. If prompted, click **I understand my workflows, go ahead and enable them**.
2. Create a tag to trigger a build:
   - Go to **Releases** on the right sidebar (or go to `https://github.com/YOUR_USERNAME/flp-organizer/releases`)
   - Click **Create a new release**
   - **Choose a tag**: type `v1.0.0` and click **Create new tag: v1.0.0 on publish**
   - **Release title**: `v1.0.0 — first release`
   - **Description**: write a few lines about what it does
   - Click **Publish release**
3. Go back to **Actions** tab. You'll see a build running. Wait ~3 minutes.
4. When the build is green, go to **Releases** again. The `FLPOrganizer.exe` should be attached to the release automatically.

### Option B — Build it yourself on Windows

Only do this if Option A fails or you want to build locally.

1. Install Python 3.11+ from https://python.org (during install, tick **Add Python to PATH**).
2. Clone or download the repo to your PC.
3. Open `cmd.exe` inside the repo folder and run:
   ```bat
   build.bat
   ```
4. When it finishes, find `dist\FLPOrganizer.exe`.
5. On the GitHub Releases page, create a new release as in Option A but **attach the `.exe` manually** by dragging it into the "Attach binaries" box.

## Part 5 — Share it

Your release URL is:
```
https://github.com/YOUR_USERNAME/flp-organizer/releases/latest
```

Anyone who opens that URL will see a **Download** button for `FLPOrganizer.exe`.

Share that link with FL Studio users. Consider posting on:
- The Image-Line forum (forum.image-line.com → appropriate subforum)
- r/FL_Studio on Reddit
- FL Studio Discord servers

A good post format:
> **FLP Organizer — a free tool that groups playlist clips by name onto adjacent tracks**
>
> Tired of having your playlist full of scattered clips with no way to tidy them up? I built a tool that does it automatically, safely, directly on the .flp file. Open source, MIT licensed, Windows .exe.
>
> Download: [link]
> Source: [link]

## Part 6 — Accepting updates and bug reports

When someone opens an **Issue** on GitHub, you'll get an email notification. Read it, ask for a sample project if needed, and either fix it yourself or ask the community to help.

When you want to release a new version:
1. Make your changes, commit, push
2. Create a new release with a new tag (`v1.0.1`, `v1.1.0`, etc.)
3. GitHub Actions rebuilds the `.exe` automatically

---

## Troubleshooting

**GitHub Actions build fails**  
Open the failed run and read the log. Usually it's a typo in one of the files. Fix it, commit, push, then go back to Releases and delete the broken release + re-create it with the same tag (or a new one).

**Windows Defender / SmartScreen blocks the .exe when users download it**  
This is normal for unsigned executables. Users need to click **More info → Run anyway**. To get rid of the warning you'd need a code-signing certificate (~$100/year), which isn't worth it for a free tool — just mention the warning in the README.

**"FLPOrganizer.exe isn't compatible with my version of Windows"**  
GitHub Actions builds on the latest Windows runner. If you need compatibility with older Windows, edit `.github/workflows/build.yml` and change `runs-on: windows-latest` to `runs-on: windows-2019`.
