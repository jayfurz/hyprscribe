import os
import argparse
import time
from recorder import record_audio
from transcriber import Transcriber
from bot import Assistant
from speaker import Speaker
from keyboard_output import KeyboardTyper
from notifier import notify

def process_interaction(transcriber, bot, speaker, keyboard, args):
    """
    Handles a single cycle: Record -> Transcribe -> Think -> Output
    Returns True if successful, False if no audio/silence.
    """
    
    # 1. Record
    notify("Voice Assistant", "Listening...", "low")
    if not record_audio("input.wav"):
        notify("Voice Assistant", "No sound detected.", "low")
        return False

    # 2. Transcribe
    notify("Voice Assistant", "Processing...", "low")
    print("Transcribing...")
    user_text = transcriber.transcribe("input.wav")
    print(f"User: {user_text}")

    if not user_text:
        return False
        
    if "exit" in user_text.lower() or "quit" in user_text.lower():
        return "EXIT"

    # 3. Think
    response = bot.chat(user_text)
    print(f"AI: {response}")

    # 4. Output
    if args.output == "keyboard" or args.output == "both":
        keyboard.type_text(response)
        
    if args.output == "audio" or args.output == "both":
        speaker.speak(response)

    # Clean up
    if os.path.exists("input.wav"):
        os.remove("input.wav")
    if os.path.exists("output.wav"):
        os.remove("output.wav")
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Local Voice Assistant")
    parser.add_argument("--mode", type=str, default="loop", choices=["loop", "oneshot"], help="Run mode: 'loop' (continuous) or 'oneshot' (single run)")
    parser.add_argument("--output", type=str, default="audio", choices=["audio", "keyboard", "both"], help="Output mode")
    parser.add_argument("--model", type=str, default="llama3", help="Ollama model name")
    parser.add_argument("--whisper", type=str, default="base", help="Whisper model size")
    parser.add_argument("--piper", type=str, default="./piper/piper", help="Path to Piper executable")
    parser.add_argument("--voice", type=str, default="./piper/en_US-lessac-medium.onnx", help="Path to Piper voice model")
    args = parser.parse_args()

    # Initialize components
    # (Lazy initialization could speed up oneshot, but models take time to load anyway)
    print("Initializing components...")
    transcriber = Transcriber(model_size=args.whisper)
    bot = Assistant(model=args.model)
    speaker = Speaker(piper_path=args.piper, model_path=args.voice)
    keyboard = KeyboardTyper()
    
    print(f"\n--- Local Voice Assistant ({args.mode} mode) ---")
    
    if args.mode == "oneshot":
        result = process_interaction(transcriber, bot, speaker, keyboard, args)
        if result == "EXIT":
            print("Exit command received.")
    else:
        # Loop mode
        print("Press Ctrl+C to exit.")
        while True:
            try:
                result = process_interaction(transcriber, bot, speaker, keyboard, args)
                if result == "EXIT":
                    print("Exiting...")
                    break
            except KeyboardInterrupt:
                print("\nStopping...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(1)

if __name__ == "__main__":
    main()
