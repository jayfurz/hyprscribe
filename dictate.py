import argparse
import os
import sys
from recorder import record_audio
from transcriber import Transcriber
from keyboard_output import KeyboardTyper
from notifier import notify

def main():
    parser = argparse.ArgumentParser(description="Local Dictation Tool")
    parser.add_argument("--whisper", type=str, default="base", help="Whisper model size (tiny, base, small, medium, large-v3)")
    parser.add_argument("--lang", type=str, default=None, help="Language code (e.g., 'en', 'fr'). None = auto-detect.")
    args = parser.parse_args()

    # Initialize
    # We initialize Transcriber first so the model is loaded before we notify the user to speak
    # This prevents the "Listening..." notification from appearing while the model is still loading from disk
    try:
        transcriber = Transcriber(model_size=args.whisper)
        keyboard = KeyboardTyper()
    except Exception as e:
        notify("Dictation Error", f"Failed to load model: {e}", "critical")
        sys.exit(1)

    # 1. Record
    notify("Dictation", "Listening...", "low")
    if not record_audio("dictation_input.wav"):
        notify("Dictation", "No sound detected.", "low")
        return

    # 2. Transcribe
    notify("Dictation", "Transcribing...", "low")
    try:
        # We can add language support to the transcriber if needed, 
        # but faster-whisper auto-detects well.
        text = transcriber.transcribe("dictation_input.wav")
        
        if text:
            print(f"Transcribed: {text}")
            # 3. Type
            keyboard.type_text(text + " ") 
            notify("Dictation", "Done.", "low")
        else:
            notify("Dictation", "No text recognized.", "low")
            
    except Exception as e:
        notify("Dictation Error", str(e), "critical")
    finally:
        if os.path.exists("dictation_input.wav"):
            os.remove("dictation_input.wav")

if __name__ == "__main__":
    main()
