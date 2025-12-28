# Server-Based GLM-ASR Setup

This setup runs the heavy AI model (`zai-org/GLM-ASR-Nano-2512`) on your GPU via a local server, and uses a lightweight client for the hotkey dictation.

## 1. Setup

**Install Server Dependencies**:
```bash
# Important: ensure you have pytorch with cuda support
uv pip install -r requirements_server.txt
```

**Note**: If the model is very new, `transformers` via pip might be too old. If you get loading errors:
```bash
uv pip install git+https://github.com/huggingface/transformers
```

## 2. Start the Server

Run this in a dedicated terminal (or add to your system startup):

```bash
/home/justin/code/local_voice_assistant/start_server.sh
```

*   The first time it runs, it will download the model (~3GB) from Hugging Face.
*   It will run on port 8000.

## 3. Configure Hyprland

Your existing keybind can remain pointing to `dictate.sh`, which has been updated to use the new client.

```ini
bind = SUPER, V, exec, /home/justin/code/local_voice_assistant/dictate.sh
```

## 4. Usage

1.  Ensure server is running.
2.  Press **Super+V**.
3.  Speak.
4.  The server processes it on the GPU and returns the text.

## Troubleshooting

*   **Server not running**: The client will notify you if it can't connect.
*   **CUDA errors**: Check `nvidia-smi` and ensure your Pytorch is CUDA-enabled (`python -c "import torch; print(torch.cuda.is_available())"`).
