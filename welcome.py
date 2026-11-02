import webbrowser
import tkinter as tk
from pathlib import Path
APP_FOLDER = Path.home() / "AutoFileSorter"


def welcome_screen(
    is_upgrade=False,
    old_version=None,
    current_autostart=False,
    new_version=None
):
    """
    Installer window.

    Fresh install : welcome_screen(new_version="1.0.0")
    Upgrade       : welcome_screen(is_upgrade=True, old_version="1.0.0",
                                   current_autostart=True, new_version="1.1.0")

    Returns {"continue": bool, "autostart": bool}
    """

    result = {
        "continue": False,
        "autostart": False
    }

    ACCENT = "#2563eb"
    ACCENT_DARK = "#1d4ed8"
    SIDEBAR = "#0f2a5e"

    # ---------- Decide what to show ----------
    reinstall = is_upgrade and old_version == new_version

    if reinstall:
        title = "Reinstall Auto File Sorter"
        description = (
            f"Version {new_version} is already installed. "
            "Setup will repair the installation. "
            "Your settings will be kept."
        )
        button_text = "Reinstall"
    elif is_upgrade:
        title = "Upgrade Auto File Sorter"
        description = (
            f"Version {old_version} is currently installed. "
            f"Setup will upgrade it to version {new_version}. "
            "Your settings will be kept."
        )
        button_text = "Upgrade"
    else:
        title = "Welcome to Auto File Sorter Setup"
        description = (
            "Keep your Downloads folder clean automatically. "
            "Auto File Sorter organizes files into categories "
            "while running quietly in the background."
        )
        button_text = "Install"

    if is_upgrade:
        features = [
            "Safely stops the running sorter",
            "Replaces the app with the new version",
            "Keeps your existing settings",
            "Starts the new version automatically",
        ]
    else:
        features = [
            "Automatically organizes downloaded files",
            "Keeps different file types in separate folders",
            "Waits for downloads to finish before moving files",
        ]

    if is_upgrade and not reinstall:
        version_text = f"{old_version}  →  {new_version}"
    elif new_version:
        version_text = f"Version {new_version}"
    else:
        version_text = ""

    # ---------- Window ----------
    root = tk.Tk()
    root.title("Auto File Sorter Setup")
    root.resizable(False, False)
    root.configure(bg="white")

    # Center window on screen
    w, h = 660, 460
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 3
    root.geometry(f"{w}x{h}+{x}+{y}")

    # On upgrade, keep the user's current autostart choice
    autostart = tk.BooleanVar(
        value=bool(current_autostart) if is_upgrade else False
    )

    # ---------- Bottom button bar ----------
    bar = tk.Frame(root, bg="#f3f4f6")
    bar.pack(side="bottom", fill="x")
    tk.Frame(root, height=1, bg="#e5e7eb").pack(side="bottom", fill="x")

    def cancel_page():
        result["continue"] = False
        root.destroy()

    def install_page():
        result["continue"] = True
        result["autostart"] = autostart.get()
        root.destroy()

    tk.Button(
        bar, text="Cancel", command=cancel_page,
        font=("Segoe UI", 9), fg="#374151", bg="white",
        activebackground="#e5e7eb", relief="flat", bd=0,
        highlightthickness=1, highlightbackground="#d1d5db",
        cursor="hand2", padx=16, pady=6, width=8,
    ).pack(side="right", padx=(8, 18), pady=12)

    tk.Button(
        bar, text=button_text, command=install_page,
        font=("Segoe UI", 9, "bold"), fg="white", bg=ACCENT,
        activebackground=ACCENT_DARK, activeforeground="white",
        relief="flat", bd=0, cursor="hand2",
        padx=16, pady=6, width=8,
    ).pack(side="right", pady=12)

    # GitHub link in the button bar (always visible, left side)
    link = tk.Label(
        bar, text="View source on GitHub ↗",
        font=("Segoe UI", 9, "underline"), fg=ACCENT,
        bg="#f3f4f6", cursor="hand2"
    )
    link.pack(side="left", padx=18)
    link.bind(
        "<Button-1>",
        lambda e: webbrowser.open("https://github.com/pushpraj19/AutoFileSorter")
    )

    # ---------- Left sidebar ----------
    sidebar = tk.Frame(root, bg=SIDEBAR, width=190)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(
        sidebar, text="🗂", font=("Segoe UI Emoji", 34),
        fg="white", bg=SIDEBAR
    ).pack(anchor="w", padx=24, pady=(30, 0))

    tk.Label(
        sidebar, text="Auto File\nSorter", font=("Segoe UI", 16, "bold"),
        fg="white", bg=SIDEBAR, justify="left"
    ).pack(anchor="w", padx=24, pady=(6, 0))

    if version_text:
        tk.Label(
            sidebar, text=version_text, font=("Segoe UI", 9),
            fg="#93c5fd", bg=SIDEBAR
        ).pack(anchor="w", padx=24, pady=(2, 0))

    tk.Label(
        sidebar,
        text="🔒 100% Local\nYour files stay on\nyour computer.",
        font=("Segoe UI", 8), fg="#93c5fd", bg=SIDEBAR, justify="left"
    ).pack(side="bottom", anchor="w", padx=24, pady=20)

    # ---------- Main content ----------
    main = tk.Frame(root, bg="white", padx=30, pady=24)
    main.pack(side="right", fill="both", expand=True)

    tk.Label(
        main, text=title,
        font=("Segoe UI", 16, "bold"), fg="#111827", bg="white"
    ).pack(anchor="w")

    tk.Label(
        main, text=description,
        font=("Segoe UI", 10), fg="#64748b", bg="white",
        justify="left", wraplength=400
    ).pack(anchor="w", pady=(8, 12))

    for feature in features:
        tk.Label(
            main, text=f"✓  {feature}", font=("Segoe UI", 10),
            fg="#334155", bg="white"
        ).pack(anchor="w", pady=2)

    tk.Frame(main, height=1, bg="#e2e8f0").pack(fill="x", pady=14)

    # Fixed install location (read-only)
    tk.Label(
        main, text="Install location", font=("Segoe UI", 10, "bold"),
        fg="#1e293b", bg="white"
    ).pack(anchor="w")

    tk.Label(
        main, text=str(APP_FOLDER), font=("Segoe UI", 9),
        fg="#475569", bg="#f1f5f9", anchor="w", padx=10, pady=6,
        wraplength=380, justify="left"
    ).pack(fill="x", pady=(5, 10))

    # Autostart option
    tk.Checkbutton(
        main, text="Start automatically when Windows starts",
        variable=autostart, font=("Segoe UI", 10),
        fg="#1e293b", bg="white", activebackground="white",
        selectcolor="white", cursor="hand2"
    ).pack(anchor="w")

    root.protocol("WM_DELETE_WINDOW", cancel_page)
    root.mainloop()

    return result