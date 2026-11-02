<h1 align="center">🗂️ Auto File Sorter</h1>

<p align="center">
  <strong>Your Downloads folder. Automatically organized.</strong>
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/python-3-3776AB?logo=python&logoColor=white">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-2563eb">
  <img alt="Dependencies" src="https://img.shields.io/badge/dependencies-none-16a34a">
  <img alt="Privacy" src="https://img.shields.io/badge/100%25-local-15803d">
</p>

<p align="center">
  <a href="https://github.com/pushpraj19/AutoFileSorter/releases/latest"><strong>⬇️ Download for Windows</strong></a>
</p>

---

**Auto File Sorter** is a lightweight Windows utility that quietly runs in the background and moves your downloads into tidy category folders (`Images`, `Documents`, `Videos` and so on) as soon as they finish downloading.

No cloud. No accounts. No dependencies. Just a cleaner Downloads folder.

<!-- Add a screenshot of the setup window here:
<p align="center"><img src="docs/setup.png" width="600" alt="Auto File Sorter setup window"></p>
-->

## 📑 Table of Contents

- [Features](#-features)
- [Before and After](#-before-and-after)
- [Supported File Types](#-supported-file-types)
- [Installation](#-installation)
- [Upgrading](#-upgrading)
- [How It Works](#-how-it-works)
- [Stopping and Uninstalling](#-stopping-and-uninstalling)
- [Where Things Are Stored](#-where-things-are-stored)
- [Building From Source](#-building-from-source)
- [Troubleshooting](#-troubleshooting)
- [Privacy](#-privacy)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## ✨ Features

- 📁 **Automatic organization**: files are sorted into category folders by extension.
- ⏳ **Download detection**: ignores partial files (`.crdownload`, `.part`, `.tmp` and more) and waits until the file size stops changing before moving anything.
- 🔁 **Duplicate-safe**: never overwrites. A second `report.pdf` becomes `report1.pdf`, then `report2.pdf`.
- 🔄 **Retries on failure**: if a file is locked or in use, it tries again later (up to 3 attempts) instead of getting stuck.
- 🚀 **Optional Windows startup**: choose during setup whether it should launch with Windows.
- 🛑 **Easy stop**: a `stop_sorter.bat` is created for you, no Task Manager needed.
- ⬆️ **Built-in upgrades**: run a newer version and it detects, stops and replaces the old one while keeping your settings.
- 🧱 **Single instance**: a lock file prevents two sorters from running at once and recovers from stale locks.
- 📝 **Activity log**: every move, warning and error is written to `sorter.log`.
- 🔒 **100% local**: nothing is uploaded, ever.

## 🔀 Before and After

```text
Downloads/                         Downloads/
├── photo.png                      ├── Images/
├── invoice.pdf                    │   └── photo.png
├── notes.txt              ──▶     ├── Documents/
├── setup.exe                      │   ├── invoice.pdf
├── song.mp3                       │   └── notes.txt
└── project.zip                    ├── Apps/
                                   │   └── setup.exe
                                   ├── Audio/
                                   │   └── song.mp3
                                   └── Archives/
                                       └── project.zip
```

> Only files directly inside your Downloads folder are sorted. Existing subfolders are left alone.

---

## 📂 Supported File Types

| Category | Extensions |
|---|---|
| 🖼️ **Images** | `.jpg` `.jpeg` `.png` `.webp` `.gif` `.bmp` `.svg` `.tiff` `.ico` |
| 📄 **Documents** | `.pdf` `.txt` `.docx` `.doc` `.odt` `.rtf` |
| 📊 **Office** | `.xlsx` `.xls` `.pptx` `.ppt` `.csv` |
| 🎵 **Audio** | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.wma` `.m4a` |
| 🎬 **Videos** | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.webm` `.mpeg` `.mpg` |
| 📦 **Archives** | `.zip` `.rar` `.7z` `.tar` `.gz` `.bz2` `.iso` |
| 💻 **Codes** | `.py` `.html` `.js` `.css` `.cpp` `.c` `.java` `.json` `.php` `.ts` `.jsx` |
| ⚙️ **Apps** | `.exe` `.msi` `.apk` `.dmg` `.deb` `.rpm` `.bat` `.sh` `.jar` |

Files with an extension that isn't listed stay where they are. They are noted once in the log as `Unknown file type`.

Want to change the mapping? Edit the `file_categories` dictionary in `main.py`.

---

## 🖥️ Installation

### Option 1: Download the app (recommended)

1. [⬇️ Download the latest `AutoFileSorter.exe`](https://github.com/pushpraj19/AutoFileSorter/releases/latest).
2. Run it.
3. In the setup window, choose whether to **start automatically when Windows starts**.
4. Click **Install**.

The app installs itself to `C:\Users\<you>\AutoFileSorter`, starts sorting right away, and you can delete the downloaded file.

> Windows SmartScreen may warn about an unrecognized app because the executable isn't code-signed. Click **More info → Run anyway**. The full source code is in this repository if you'd like to inspect or build it yourself.

### Option 2: Run from source

Requirements:

- Windows
- Python 3 (with Tkinter, which is included in the standard python.org installer)
- **No third-party packages**: only the standard library is used

```bash
git clone https://github.com/pushpraj19/AutoFileSorter.git
cd AutoFileSorter
python main.py
```

> Running from source starts the sorter, but the installer and the Windows-startup option only work from the packaged `.exe`.

---

## ⬆️ Upgrading

Just download the newer `AutoFileSorter.exe` and run it. Setup detects your existing installation and switches to upgrade mode:

1. Shows the **old → new** version.
2. Safely asks the running sorter to stop.
3. Replaces the old executable.
4. Keeps your settings (including your startup choice, which you can change in the window).
5. Starts the new version automatically.

If you run the same version again, the button says **Reinstall** and repairs the installation.

---

## ⚙️ How It Works

1. Every 2 seconds, the sorter scans the top level of your Downloads folder.
2. Temporary or partial downloads (`.crdownload`, `.part`, `.tmp`, `.download`, `.partial`, `.temp`, `.filepart`, `.unconfirmed`) are skipped.
3. For each file, it compares the size between scans. A file is treated as finished once the size has stopped changing for two checks in a row.
4. It looks up the extension and moves the file into the matching category folder, creating the folder if needed.
5. If a file with the same name already exists, a number is added to the new name instead of overwriting.
6. If a move fails (for example, the file is still locked by another program), it retries after 10 seconds, then 20 seconds, and gives up after 3 attempts. The failure is logged.
7. Every action is written to `Downloads\sorter.log`.

---

## 🛑 Stopping and Uninstalling

### Stop the sorter

Double-click:

```text
C:\Users\<you>\AutoFileSorter\stop_sorter.bat
```

It sends a stop request, and the sorter shuts down cleanly within a few seconds. To start it again, run `AutoFileSorter.exe` from the same folder.

### Disable startup

Run the installer again and untick the startup option, or delete:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AutoFileSorter.bat
```

### Uninstall

1. Run `stop_sorter.bat`.
2. Delete the startup file above, if it exists.
3. Delete the `C:\Users\<you>\AutoFileSorter` folder.

Your sorted files stay in your Downloads folder, so nothing is lost.

---

## 📍 Where Things Are Stored

| What | Location |
|---|---|
| App and settings | `C:\Users\<you>\AutoFileSorter\` |
| Settings file | `AutoFileSorter\settings.json` (version and startup preference) |
| Stop utility | `AutoFileSorter\stop_sorter.bat` |
| Activity log | `Downloads\sorter.log` |
| Startup entry | `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\AutoFileSorter.bat` |

---

## 🔨 Building From Source

To create your own executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name AutoFileSorter main.py
```

The result is in `dist\AutoFileSorter.exe`. When you release a new version, bump `APP_VERSION` in `main.py` so existing users see the upgrade screen.

---

## 🩺 Troubleshooting

<details>
<summary><strong>A file isn't being moved</strong></summary>

- Its extension may not be in the list above. Check `sorter.log` for an `Unknown file type` entry.
- It may still be downloading, or locked by another program. The sorter retries up to 3 times.
- It may be inside a subfolder. Only top-level files are sorted.
</details>

<details>
<summary><strong>"Another sorter instance is already running"</strong></summary>

The sorter is already running in the background. Use `stop_sorter.bat` first if you want to restart it.
</details>

<details>
<summary><strong>Setup says the lock file is unreadable, or the previous version didn't stop</strong></summary>

Run `stop_sorter.bat`, then delete `AutoFileSorter\sorter.lock` and try again.
</details>

<details>
<summary><strong>Windows startup isn't working</strong></summary>

Startup only works with the installed `.exe`, not when running `main.py` from source. Reinstall and make sure the startup option is ticked.
</details>

---

## 🔐 Privacy

Auto File Sorter works entirely on your computer.

- Files are moved locally and never uploaded.
- No accounts, telemetry or cloud storage.
- No network access is needed for sorting.
- The code is open for you to read.

---

## 🛠️ Built With

- **Python** (standard library only)
- **Tkinter** for the setup window
- **PyInstaller** for the Windows executable
- **ctypes / Windows APIs** for safe process detection

---

## 🗺️ Roadmap

**Done**

- [x] Automatic file organization
- [x] Download completion detection
- [x] Duplicate filename handling
- [x] Retry handling for locked files
- [x] Activity logging
- [x] Installer-style setup window
- [x] Windows startup option
- [x] Stop utility
- [x] In-place upgrades that keep your settings

**Planned for the next version**

- [ ] Settings dashboard
- [ ] Custom sorting rules and folders
- [ ] More customization options
- [ ] Further installer and upgrade improvements

Have an idea? [Open an issue](https://github.com/pushpraj19/AutoFileSorter/issues).

---

## 🤝 Contributing

Suggestions, bug reports and pull requests are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Test it on Windows.
4. Open a pull request describing what you changed.

---

## 📋 Project Information

| Detail | Information |
|---|---|
| Project | Auto File Sorter |
| Developer | Pushpraj Budha |
| Platform | Windows |
| Language | Python 3 |
| Current version | 1.0.0 |
| License | Not specified yet |
| Repository | https://github.com/pushpraj19/AutoFileSorter |

---

<p align="center">
  Made with ❤️ and Python.
  <br>
  <strong>A cleaner Downloads folder starts here.</strong>
</p>