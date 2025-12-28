from faster_whisper import WhisperModel
import os

class Transcriber:
    def __init__(self, model_size="tiny", device="cpu", compute_type="int8"):
        """
        Initializes the Faster-Whisper model.
        Args:
            model_size: Size of the model (tiny, base, small, medium, large-v3)
            device: 'cpu' or 'cuda'
            compute_type: 'int8', 'float16', 'float32'
        """
        print(f"Loading Whisper model '{model_size}' on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_file):
        if not os.path.exists(audio_file):
            return ""
        
        segments, info = self.model.transcribe(audio_file, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
