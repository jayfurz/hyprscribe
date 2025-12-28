import subprocess
import sounddevice as sd
import soundfile as sf
import os

class Speaker:
    def __init__(self, piper_path="./piper/piper", model_path="./piper/en_US-lessac-medium.onnx"):
        self.piper_path = piper_path
        self.model_path = model_path
        self.output_file = "output.wav"

    def speak(self, text):
        if not text:
            return

        # Prepare the command
        # piper reads from stdin
        command = [
            self.piper_path,
            "--model", self.model_path,
            "--output_file", self.output_file
        ]

        print(f"Generating speech with Piper...")
        try:
            # Run piper
            process = subprocess.Popen(
                command, 
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(input=text.encode('utf-8'))
            
            if process.returncode != 0:
                print(f"Piper error: {stderr.decode()}")
                return

            # Play audio
            self.play_audio()

        except FileNotFoundError:
            print("Piper executable not found. Please verify the path.")
        except Exception as e:
            print(f"Error in speech generation: {e}")

    def play_audio(self):
        if os.path.exists(self.output_file):
            data, fs = sf.read(self.output_file)
            sd.play(data, fs)
            sd.wait()
