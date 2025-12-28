import subprocess
import shutil

def notify(title, message, urgency="normal"):
    """Sends a system notification."""
    notify_bin = shutil.which("notify-send")
    if notify_bin:
        subprocess.run([notify_bin, "-u", urgency, title, message])
    else:
        print(f"[{title}] {message}")
