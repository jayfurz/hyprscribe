import argparse
import os
import requests
import time
import signal
import threading
import sys
from recorder import record_audio
from keyboard_output import KeyboardTyper
from notifier import notify

SERVER_URL = "http://localhost:8000/transcribe"
PID_FILE = "/tmp/voice_assist_dictate.pid"

def main():
    parser = argparse.ArgumentParser(description="GLM-ASR Dictation Client")
    parser.add_argument("--hold", action="store_true", help="Hold-to-record mode (waits for SIGTERM to stop recording)")
    args = parser.parse_args()

    # Check for existing instance if in hold mode
    if args.hold:
        if os.path.exists(PID_FILE):
            print("Already running.")
            sys.exit(0)
        
        # Write PID
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))

    keyboard = KeyboardTyper()
    stop_event = threading.Event() if args.hold else None

    # Handle signals for Hold Mode
    def signal_handler(sig, frame):
        print("Signal received, stopping recording...")
        if stop_event:
            stop_event.set()

    if args.hold:
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

    # 1. Record
    notify("GLM-ASR", "Listening...", "low")
    
    try:
        # Record at 16000Hz as standard for speech models
        # If stop_event is passed, it waits for the signal
        recording_success = record_audio("dictation_input.wav", sample_rate=16000, stop_event=stop_event)
        
        if not recording_success:
            notify("GLM-ASR", "No sound detected.", "low")
            return

        # 2. Send to Server
        notify("GLM-ASR", "Transcribing...", "low")
        with open("dictation_input.wav", "rb") as f:
            files = {"file": ("dictation_input.wav", f, "audio/wav")}
            response = requests.post(SERVER_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()
            text = result.get("text", "")
            if result.get("error"):
                notify("Server Error", result["error"], "critical")
            elif text:
                print(f"Transcribed: {text}")
                keyboard.type_text(text + " ")
                notify("GLM-ASR", "Done.", "low")
            else:
                notify("GLM-ASR", "No text recognized.", "low")
        else:
            notify("Connection Error", f"Status: {response.status_code}", "critical")

    except requests.exceptions.ConnectionError:
        notify("Error", "Is the server running on localhost:8000?", "critical")
    except Exception as e:
        notify("Client Error", str(e), "critical")
    finally:
        # Cleanup
        if os.path.exists("dictation_input.wav"):
            os.remove("dictation_input.wav")
        if args.hold and os.path.exists(PID_FILE):
            os.remove(PID_FILE)

if __name__ == "__main__":
    main()
