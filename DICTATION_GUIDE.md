# Local Dictation Tool (Hyprland)

A fast, privacy-focused dictation tool using **Faster Whisper**. It records your voice, converts it to text, and types it directly into your active window.

## Setup

1.  **Install Dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```
    Ensure `wtype` is installed on your system (`sudo apt install wtype` or `sudo pacman -S wtype`).

2.  **Hyprland Configuration**:
    Add the following to `~/.config/hypr/hyprland.conf`:

    ```ini
    # Super + V to dictate
    bind = $mainMod, V, exec, cd /home/justin/code/local_voice_assistant && uv run dictate.py --whisper base
    ```

    *   Change `--whisper base` to `--whisper small` or `--whisper medium` for better accuracy (requires more RAM/CPU).
    *   Use `--whisper large-v3` for the state-of-the-art accuracy if you have a GPU.

## Usage

1.  Focus on a text field (browser, terminal, editor).
2.  Press **Super + V**.
3.  Wait for the notification **"Listening..."**.
4.  Speak.
5.  Wait for **"Transcribing..."**.
6.  Text appears!
