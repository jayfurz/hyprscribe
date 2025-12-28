import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import sys

def record_audio(filename="input.wav", sample_rate=16000, threshold=0.01, silence_duration=1.5, stop_event=None):
    """
    Records audio.
    If stop_event is provided: records until stop_event is set.
    If stop_event is None: records until silence is detected.
    """
    print("Listening...")
    
    audio_data = []
    start_time = time.time()
    last_sound_time = time.time()
    recording = False
    
    # Callback function to process audio chunks
    def callback(indata, frames, time_info, status):
        nonlocal audio_data, last_sound_time, recording
        if status:
            print(status, file=sys.stderr)
        
        # Calculate volume
        volume_norm = np.linalg.norm(indata) * 10
        
        # Check for sound (only relevant for silence detection mode)
        if volume_norm > threshold:
            last_sound_time = time.time()
            if not recording and stop_event is None:
                recording = True
                print("Sound detected, recording...")
        
        # In hold mode (stop_event set), we always record once started
        if stop_event is not None:
            audio_data.append(indata.copy())
        elif recording:
            audio_data.append(indata.copy())

    # Open stream
    with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):
        while True:
            # Mode 1: Stop Event (Push-to-Talk)
            if stop_event is not None:
                if stop_event.is_set():
                    print("Stop signal received.")
                    break
                sd.sleep(50)
                continue

            # Mode 2: Silence Detection
            if recording and (time.time() - last_sound_time > silence_duration):
                print("Silence detected, stopping.")
                break
            # Timeout if no sound ever detected
            if not recording and (time.time() - start_time > 10):
                print("No sound detected for 10s, timing out.")
                return False
            
            sd.sleep(100)
            
    # Save file
    if audio_data:
        audio_concat = np.concatenate(audio_data, axis=0)
        # Normalize
        max_val = np.max(np.abs(audio_concat))
        if max_val > 0:
            audio_concat = audio_concat / max_val
        # Convert to 16-bit PCM
        audio_int16 = (audio_concat * 32767).astype(np.int16)
        wav.write(filename, sample_rate, audio_int16)
        return True
    return False
