import subprocess
import shutil
import os


class KeyboardTyper:
    def __init__(self):
        # Check for wtype (Wayland)
        self.wtype_path = shutil.which("wtype")

        # Fallback for common linux paths if shutil.which fails in limited envs
        if not self.wtype_path and os.path.exists("/usr/bin/wtype"):
            self.wtype_path = "/usr/bin/wtype"

        # Check for xdotool (X11/XWayland - though less reliable on Hyprland native)
        self.xdotool_path = shutil.which("xdotool")

    def type_text(self, text):
        if not text:
            return

        if self.wtype_path:
            try:
                # wtype doesn't handle some special chars well, but basic text is fine
                # Using stdin is safer for special chars
                process = subprocess.Popen(
                    [self.wtype_path, "-"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )
                process.communicate(input=text.encode("utf-8"))
            except Exception as e:
                print(f"Error using wtype: {e}")

        elif self.xdotool_path:
            # Fallback (might work depending on Hyprland config)
            try:
                subprocess.run([self.xdotool_path, "type", text], check=True)
            except Exception as e:
                print(f"Error using xdotool: {e}")
        else:
            print(
                "Error: No typing tool found. Please install 'wtype' (recommended for Hyprland) or 'xdotool'."
            )

    def press_enter(self):
        if self.wtype_path:
            subprocess.run([self.wtype_path, "-k", "Return"])
