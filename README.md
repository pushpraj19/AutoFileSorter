# 🗂️ Auto File Sorter

### Your Downloads folder. Automatically organized.

**Auto File Sorter** is a lightweight Windows desktop utility built with Python that automatically organizes downloaded files into categorized folders.

No complicated setup. No cloud storage. Just a cleaner Downloads folder.

---

## ✨ Features

- 📁 **Automatic Organization** — Sort downloaded files into appropriate categories.
- 🖼️ **Image Sorting** — Keep images organized.
- 📄 **Document Management** — Separate documents and office files.
- 🎵 **Audio & Video Sorting** — Keep media files organized.
- 📦 **Archive Management** — Organize compressed files.
- ⏳ **Download Detection** — Wait for downloads to finish before moving files.
- 🔄 **Automatic Monitoring** — Continuously monitor the Downloads folder.
- 🛑 **Easy Stop & Restart** — Stop the sorter using its dedicated stop utility.
- 🚀 **Windows Startup** — Optionally launch automatically when Windows starts.
- 🔒 **Local Processing** — File organization happens on your computer.

## 📂 File Categories

| Category | Examples |
|---|---|
| Images | PNG, JPG, JPEG, GIF |
| Documents | PDF, TXT |
| Office | DOCX, XLSX, PPTX |
| Audio | MP3, WAV |
| Videos | MP4, MKV |
| Archives | ZIP, RAR |
| Codes | Python and other code files |
| Apps | Application installers |

*Supported extensions depend on the application's current configuration.*

---

## 🖥️ Installation

### Option 1 — Download the application

1.[⬇️ Download AutoFileSorter](https://github.com/pushpraj19/AutoFileSorter/releases/download/v1.0.0/AutoFileSorter.exe)
2. Run the executable.
3. Follow the setup screen.
4. Choose whether to enable Windows startup.
5. Let Auto File Sorter organize your Downloads folder.

### Option 2 — Run from source

Requirements:
- Windows
- Python 3
- Required Python dependencies

Clone the repository:

```bash
git clone https://github.com/pushpraj19/AutoFileSorter.git
```

Enter the project directory:

```bash
cd AutoFileSorter
```

Run the application:

```bash
python main.py
```

---

## ⚙️ How It Works

1. Auto File Sorter monitors your Downloads folder.
2. It detects newly downloaded files.
3. It checks whether a file is still being downloaded.
4. Once the file is ready, it identifies its extension.
5. It moves the file into the appropriate category folder.
6. It records activity in its log file.

---

## 🔐 Privacy

Auto File Sorter is designed to work locally on your Windows computer.

- Files are organized locally.
- No cloud storage is required.
- No file uploads are needed for sorting.
- Your files remain under your control.

The source code is available for inspection.

---

## 🛠️ Built With

- Python
- Tkinter
- PyInstaller
- Windows file-system APIs

---

## 🧑‍💻 Project Information

| Detail | Information |
|---|---|
| Project | Auto File Sorter |
| Developer | Pushpraj |
| Platform | Windows |
| Language | Python |
| Current version | 1.0.0 |
| License | Not specified |

---

## 🗺️ Roadmap

- [x] Automatic file organization
- [x] Download completion detection
- [x] Duplicate filename handling
- [x] Activity logging
- [x] First-run setup screen
- [x] Windows startup option
- [x] Stop and restart functionality
---Next Version--comming soon
- [ ] Settings dashboard
- [ ] More customization options
- [ ] Further installer and upgrade improvements
- [ ] Custom sorting rules and Folders

---

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome!

If you find a bug or have an idea, open an issue in the repository.

---

## 🔗 Links

- **GitHub Repository:** https://github.com/pushpraj19/AutoFileSorter
- **Developer:** Pushpraj Budha

---

<p align="center">
  Made with ❤️ and Python.
  <br>
  <strong>A cleaner Downloads folder starts here.</strong>
</p>