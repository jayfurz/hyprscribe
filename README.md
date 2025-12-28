# HyprScribe

**HyprScribe** is a blazing fast, private, and local voice dictation tool designed for Linux (specifically Hyprland/Wayland). It allows you to press a key, speak, and have the text instantly typed into your active window.

It features a **Client-Server Architecture**:
*   **Server**: Runs the powerful `GLM-ASR-Nano` or `Whisper` model on your GPU (always loaded in VRAM).
*   **Client**: A lightweight script triggered by your hotkey for instant recording and response.

## Quick Start

### 1. Installation

Clone the repo:
```bash
git clone git@github.com:jayfurz/hyprscribe.git
cd hyprscribe
```

Install dependencies (using `uv` is recommended):
```bash
# For the server (GPU/AI)
uv pip install -r requirements_server.txt

# For the client (Recording/Typing)
uv pip install -r requirements.txt

# System dependencies
sudo apt install wtype portaudio19-dev
```

### 2. Start the Server

This runs the AI model. Keep this running in a background terminal.

```bash
./start_server.sh
```

### 3. Configure Hyprland

Add this to your `~/.config/hypr/hyprland.conf` to enable **Push-to-Talk**:

```ini
# Start recording when pressed
bind = SUPER, V, exec, /path/to/hyprscribe/start_dictation.sh

# Stop recording and Type when released
bindr = SUPER, V, exec, /path/to/hyprscribe/stop_dictation.sh
```

### 4. Usage

1.  Focus on any text input (Terminal, VS Code, Browser).
2.  **Hold Super + V**.
3.  Speak your mind.
4.  **Release**.
5.  Watch the text appear instantly.

## Documentation

*   [**Server Setup Guide**](SERVER_README.md): Detailed instructions on the GLM-ASR model and GPU setup.
*   [**Standalone Dictation**](DICTATION_GUIDE.md): How to use the simpler, non-server version (Whisper only).
*   [**Full Assistant Mode**](local_voice_assistant/README.md): (Legacy) The original conversation mode with Ollama.
