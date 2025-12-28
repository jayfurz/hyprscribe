# Local Voice Assistant (Wayland/Hyprland Ready)

This is a local voice assistant that can listen, think (Ollama), and either speak back (Piper) or type the answer (Keyboard).

## Hyprland Integration

To use this with a custom key (e.g., `Super + V`) in Hyprland to start recording and type the answer:

1.  **Install dependencies**:
    *   Ensure `wtype` (for typing) and `notify-send` (for notifications) are installed.
    *   `sudo apt install wtype libnotify-bin` (or `pacman -S wtype libnotify` on Arch).

2.  **Add Keybinding to Hyprland Config** (`~/.config/hypr/hyprland.conf`):
    
    Replace `/path/to/local_voice_assistant` with your actual path.

    ```ini
    bind = $mainMod, V, exec, cd /path/to/local_voice_assistant && uv run main.py --mode oneshot --output keyboard
    ```

    *   When you press `Super + V`, a notification "Listening..." will appear.
    *   Speak your prompt. 
    *   Wait for silence (1.5s).
    *   The assistant will process and type the response into the active window.

## Usage Options

You can run it manually too:

```bash
# Continuous loop with audio output
uv run main.py --mode loop --output audio

# Single run with keyboard output (good for keybinds)
uv run main.py --mode oneshot --output keyboard

# Both audio and keyboard
uv run main.py --mode oneshot --output both
```
