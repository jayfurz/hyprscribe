# Local Voice Assistant

This is a fully local voice assistant integrating **Faster Whisper** (STT), **Ollama** (LLM), and **Piper** (TTS).

## Prerequisites

1.  **Python 3.10+**
2.  **Ollama**: Installed and running.
    *   Install: `curl -fsSL https://ollama.com/install.sh | sh`
    *   Pull model: `ollama pull llama3` (or your preferred model)
    *   Serve: `ollama serve`
3.  **Piper TTS**: You need the Piper executable and a voice model.
    *   Download Piper: https://github.com/rhasspy/piper/releases
    *   Extract to a folder named `piper` inside this directory (or update the path in arguments).
    *   Download a voice model (ONNX + JSON): https://github.com/rhasspy/piper/blob/master/VOICES.md
    *   Example: `en_US-lessac-medium.onnx` and `en_US-lessac-medium.onnx.json`
    *   Place them in the `piper/` folder.
4.  **System Dependencies** (Ubuntu/Debian):
    ```bash
    sudo apt-get install python3-dev portaudio19-dev libasound2-dev
    ```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Ensure Ollama is running (`ollama serve`). Then run:

```bash
python main.py
```

### Arguments

*   `--model`: Ollama model name (default: `llama3`)
*   `--whisper`: Whisper model size (default: `base`). Options: `tiny`, `base`, `small`, `medium`, `large-v3`.
*   `--piper`: Path to piper executable (default: `./piper/piper`)
*   `--voice`: Path to voice model (default: `./piper/en_US-lessac-medium.onnx`)

## Troubleshooting

*   **PortAudio Error**: If `pip install sounddevice` fails, ensure you installed `portaudio19-dev`.
*   **Piper not found**: Ensure the path to the `piper` binary is correct and executable (`chmod +x piper/piper`).
