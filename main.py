import logging
import subprocess
import time
from pathlib import Path
import shutil
import os
import tkinter as tk
from tkinter import messagebox
import json
import sys
import ctypes
from welcome import welcome_screen




#APPLICATION PATHS

MAIN_FOLDER = Path.home() / "Downloads"
LOG_FILE = MAIN_FOLDER / "sorter.log"
APP_FOLDER = Path.home() / "AutoFileSorter"
LOCK_FILE = APP_FOLDER / "sorter.lock"
SETTINGS_FILE = APP_FOLDER / "settings.json"
STARTUP_FOLDER = (
    Path(os.environ["APPDATA"])
    / "Microsoft"
    / "Windows"
    / "Start Menu"
    / "Programs"
    / "Startup"
)

STARTUP_FILE = STARTUP_FOLDER / "AutoFileSorter.bat"
STOP_FILE = APP_FOLDER / "stop.request"
STOP_BAT = APP_FOLDER / "stop_sorter.bat"
APP_VERSION = "1.0.0"

#LOGGING SETUP

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)



#FILE CATEGORIES

file_categories = {
    # Codes
    '.py': 'Codes',
    '.html': 'Codes',
    '.js': 'Codes',
    '.css': 'Codes',
    '.cpp': 'Codes',
    '.c': 'Codes',
    '.java': 'Codes',
    '.json': 'Codes',
    '.php': 'Codes',
    '.ts': 'Codes',
    '.jsx': 'Codes',

    # Images
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.webp': 'Images',
    '.gif': 'Images',
    '.bmp': 'Images',
    '.svg': 'Images',
    '.tiff': 'Images',
    '.ico': 'Images',

    # Documents
    '.txt': 'Documents',
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.doc': 'Documents',
    '.odt': 'Documents',
    '.rtf': 'Documents',

    # Office
    '.xlsx': 'Office',
    '.xls': 'Office',
    '.pptx': 'Office',
    '.ppt': 'Office',
    '.csv': 'Office',

    # Apps
    '.exe': 'Apps',
    '.msi': 'Apps',
    '.apk': 'Apps',
    '.dmg': 'Apps',
    '.deb': 'Apps',
    '.rpm': 'Apps',
    '.bat': 'Apps',
    '.sh': 'Apps',
    '.jar': 'Apps',

    # Audio
    '.mp3': 'Audio',
    '.wav': 'Audio',
    '.flac': 'Audio',
    '.aac': 'Audio',
    '.ogg': 'Audio',
    '.wma': 'Audio',
    '.m4a': 'Audio',

    # Archives
    '.zip': 'Archives',
    '.rar': 'Archives',
    '.7z': 'Archives',
    '.tar': 'Archives',
    '.gz': 'Archives',
    '.bz2': 'Archives',
    '.iso': 'Archives',

    # Videos
    '.mp4': 'Videos',
    '.mkv': 'Videos',
    '.avi': 'Videos',
    '.mov': 'Videos',
    '.wmv': 'Videos',
    '.flv': 'Videos',
    '.webm': 'Videos',
    '.mpeg': 'Videos',
    '.mpg': 'Videos'
}



#TRACKING VARIABLES

temporary_extensions = {
    '.crdownload', '.part', '.tmp', '.download',
    '.partial', '.temp', '.filepart', '.unconfirmed'
}

ignored_files = set()
failed_files = set()
file_sizes = {}
stable_counts = {}
retry_counts = {}
retry_after = {}
MAX_RETRIES = 3
running = False


#LOAD SETTING
def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with SETTINGS_FILE.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            logging.exception("Could not read settings file")

    return {}

def installer_error(message):
    messagebox.showerror("Auto File Sorter Setup", message)


def install_app():

    # Only install when running as a packaged EXE
    if not getattr(sys, "frozen", False):
        return False

    APP_FOLDER.mkdir(parents=True, exist_ok=True)

    current_exe = Path(sys.executable).resolve()
    installed_exe = (APP_FOLDER / "AutoFileSorter.exe").resolve()

    # Already running from the installation folder
    if current_exe == installed_exe:
        return False

    # Detect existing installation
    is_upgrade = installed_exe.exists()

    # Load existing settings
    settings = load_settings()

    old_version = settings.get("version", "Unknown")
    current_autostart = settings.get("autostart", False)

    # Show welcome or upgrade screen
    if is_upgrade:
        choice = welcome_screen(
            is_upgrade=True,
            old_version=old_version,
            current_autostart=current_autostart,
            new_version=APP_VERSION
        )
    else:
        choice = welcome_screen(new_version=APP_VERSION)

    # User cancelled
    if not choice["continue"]:
        sys.exit()

    # Ask the old sorter to stop
    if is_upgrade and LOCK_FILE.exists():

        try:
            pid = int(LOCK_FILE.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            installer_error(
                "Could not verify the running version.\n\n"
                f"Please delete this file and try again:\n{LOCK_FILE}"
            )
            sys.exit()

        if pid > 0 and is_process_running(pid):
            STOP_FILE.touch()

            timeout = 30
            start_time = time.time()

            while LOCK_FILE.exists():

                if time.time() - start_time > timeout:
                    STOP_FILE.unlink(missing_ok=True)
                    installer_error(
                        "The previous version did not stop.\n\n"
                        "Please close Auto File Sorter and try again."
                    )
                    sys.exit()

                time.sleep(0.5)

        else:
            # No active process owns this lock
            LOCK_FILE.unlink(missing_ok=True)

    # Make sure a leftover stop request can't stop the new version
    STOP_FILE.unlink(missing_ok=True)

    # Copy to a temporary file first
    temp_exe = APP_FOLDER / "AutoFileSorter.new.exe"

    try:
        shutil.copy2(current_exe, temp_exe)

        # The old process may need a moment to release its EXE
        for attempt in range(10):
            try:
                os.replace(temp_exe, installed_exe)
                break
            except PermissionError:
                if attempt == 9:
                    raise
                time.sleep(0.5)

        # Update settings after successful replacement
        settings["autostart"] = choice["autostart"]
        settings["version"] = APP_VERSION
        save_settings(settings)

        logging.info(
            f"Installed version {APP_VERSION} (previous: {old_version})"
        )

        # Launch installed application
        subprocess.Popen([str(installed_exe)])

        sys.exit()

    except Exception as e:
        logging.exception("Installation failed")
        temp_exe.unlink(missing_ok=True)
        installer_error(f"Installation failed:\n\n{e}")
        sys.exit()





#SAVE SETTINGS
def save_settings(settings):
    APP_FOLDER.mkdir(parents=True, exist_ok=True)
    with SETTINGS_FILE.open("w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


#SETUP START
def setup_autostart():
    settings = load_settings()

    if "autostart" not in settings:
        choice = welcome_screen(new_version=APP_VERSION)

        if not choice["continue"]:
            return False

        settings["autostart"] = choice["autostart"]
        save_settings(settings)

    return True

#ASK USER FOR AUTOSTART
def ask_autostart():
    if messagebox.askyesno("Autostart", "Do you want to enable autostart?"):
        settings = load_settings()
        settings['autostart'] = True
        save_settings(settings)
        print("Autostart enabled.")
    else:
        settings = load_settings()
        settings['autostart'] = False
        save_settings(settings)
        print("Autostart disabled.")



def configure_autostart():
    settings = load_settings()

    if settings.get("autostart") is True:
        if not getattr(sys, "frozen", False):
            print("Build the EXE before enabling auto-start.")
            return

        STARTUP_FOLDER.mkdir(parents=True, exist_ok=True)

        with STARTUP_FILE.open("w", encoding="utf-8") as file:
            file.write(f'@echo off\nstart "" "{sys.executable}"\n')

        print("Auto-start registered.")

    else:
        if STARTUP_FILE.exists():
            STARTUP_FILE.unlink()

        print("Auto-start disabled.")

#PROCESS CHECK
def is_process_running(pid):
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    kernel32.OpenProcess.argtypes = [
        ctypes.c_ulong,
        ctypes.c_int,
        ctypes.c_ulong
    ]
    kernel32.OpenProcess.restype = ctypes.c_void_p

    kernel32.GetExitCodeProcess.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_ulong)
    ]
    kernel32.GetExitCodeProcess.restype = ctypes.c_int

    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]

    handle = kernel32.OpenProcess(
        PROCESS_QUERY_LIMITED_INFORMATION,
        False,
        pid
    )

    if not handle:
        error = ctypes.get_last_error()

        # Access denied: don't assume the process is dead.
        if error == 5:
            return True

        # Process doesn't exist.
        if error == 87:
            return False

        return True

    try:
        exit_code = ctypes.c_ulong()

        if not kernel32.GetExitCodeProcess(
            handle,
            ctypes.byref(exit_code)
        ):
            return True

        return exit_code.value == 259  # STILL_ACTIVE

    finally:
        kernel32.CloseHandle(handle)
    
#LOCK FILE SYSTEM
def acquire_lock():
    APP_FOLDER.mkdir(parents=True, exist_ok=True)

    try:
        with LOCK_FILE.open("x", encoding="utf-8") as lock:
            lock.write(str(os.getpid()))

        print("Lock created:", LOCK_FILE)
        return True

    except FileExistsError:
        try:
            pid_text = LOCK_FILE.read_text(encoding="utf-8").strip()
            pid = int(pid_text)

            if pid <= 0:
                raise ValueError("Invalid PID")

        except (ValueError, OSError):
            print("Lock file is unreadable or corrupted. Manual recovery needed.")
            return False

        if is_process_running(pid):
            print("Another sorter instance is already running!")
            return False

        # Previous process is no longer running
        try:
            LOCK_FILE.unlink()
            print("Removed stale lock. Retrying...")

            return acquire_lock()

        except OSError as e:
            print("Could not remove stale lock:", e)
            return False

    except OSError as e:
        print("Lock creation failed:", e)
        return False


#MAIN SORTER
def start_sorter():
    global running
    if running:
        return
    if not acquire_lock():
        return
    running = True
    create_stop_bat()
    print("Auto File Sorter started!")
    try:
        while running:

            # Check for stop request
            if STOP_FILE.exists():
                STOP_FILE.unlink(missing_ok=True)
                break
            for file in MAIN_FOLDER.iterdir():
                if not running or STOP_FILE.exists():
                    break
                if not file.is_file():
                    continue
                if (
                    file.name == 'desktop.ini'
                    or file.name.startswith('~$')
                    or file.name == 'sorter.log'
                ):
                    continue

                if file.suffix.lower() in temporary_extensions:
                    continue

                if file.name not in stable_counts:
                    stable_counts[file.name] = 0

                file_size = file.stat().st_size
                if file.name not in file_sizes:
                    file_sizes[file.name] = file_size

                if file_sizes[file.name] != file_size:
                    file_sizes[file.name] = file_size
                    stable_counts[file.name] = 0

                elif stable_counts[file.name] < 2:
                    stable_counts[file.name] += 1

                if stable_counts[file.name] >= 2:
                    short(file)

                    if not file.exists():
                        file_sizes.pop(file.name, None)
                        stable_counts.pop(file.name, None)

            time.sleep(2)

    except KeyboardInterrupt:
        pass

    except Exception:
        logging.exception("Unexpected sorter error")

    finally:
        running = False

        STOP_FILE.unlink(missing_ok=True)
        STOP_BAT.unlink(missing_ok=True)
        LOCK_FILE.unlink(missing_ok=True)

        print("Auto File Sorter stopped.")


def create_stop_bat():
    STOP_BAT.write_text(
        '@echo off\n'
        'echo Stopping Auto File Sorter...\n'
        'type nul > "%~dp0stop.request"\n'
        'echo Stop request sent.\n'
        'timeout /t 2 >nul\n',
        encoding="utf-8"
    )

    
#STOP SORTER
def stop_sorter():
    STOP_FILE.touch()


#FILE MOVING
def file_move(file, final):
    try:
        final.parent.mkdir(parents=True, exist_ok=True)
        new_file = give_new_name(final)
        shutil.move(file, new_file)
        logging.info(
            f'{new_file.name} moved to {new_file.parent.name}'
        )
        return True

    except PermissionError as e:
        logging.error(
            f'Permission denied moving {file.name}: {e}'
        )
        retry_counts[file.name] += 1
        return False
    except OSError as e:
        logging.error(
            f'Error moving {file.name}: {e}'
        )
        retry_counts[file.name] += 1
        return False

#DUPLICATE FILE NAMING

def give_new_name(final):
    add = 1
    new_file = final
    while new_file.exists():
        new_file = final.with_name(
            final.stem + str(add) + final.suffix
        )
        add += 1
    return new_file

#SORTING LOGIC
def short(file):
    if file.name in failed_files:
        return
    if not file.is_file():
        return
    category = file_categories.get(file.suffix.lower())
    if category is None:
        if file.name not in ignored_files:
            logging.warning(
                f"Unknown file type: {file.name}"
            )
            ignored_files.add(file.name)
        return
    final = MAIN_FOLDER / category / file.name
    if file.name not in retry_counts:
        retry_counts[file.name] = 0
    if file.name in retry_after:
        if time.time() < retry_after[file.name]:
            return
    success = file_move(file, final)
    if success:
        retry_counts.pop(file.name, None)
        retry_after.pop(file.name, None)
    else:
        if retry_counts[file.name] >= MAX_RETRIES:
            logging.error(
                f"Giving up on {file.name} after {MAX_RETRIES} attempts."
            )
            failed_files.add(file.name)
            retry_counts.pop(file.name, None)
            retry_after.pop(file.name, None)
        else:
            if retry_counts[file.name] == 1:
                retry_after[file.name] = time.time() + 10

            elif retry_counts[file.name] == 2:
                retry_after[file.name] = time.time() + 20


#APPLICATION ENTRY POINT
if __name__ == "__main__":
    install_app()

    if setup_autostart():
        configure_autostart()
        start_sorter()