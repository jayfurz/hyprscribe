import os
import uvicorn
from fastapi import FastAPI, UploadFile, File
from transformers import AutoModelForSeq2SeqLM, AutoProcessor
import torch
import io
import soundfile as sf
import numpy as np

app = FastAPI(title="GLM-ASR-Nano Server")

MODEL_ID = "zai-org/GLM-ASR-Nano-2512"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading model {MODEL_ID} on {device}...")
try:
    processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_ID, 
        dtype="auto", 
        device_map="auto", 
        trust_remote_code=True
    )
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Ensure you have installed transformers from source if this is a very new model:")
    print("pip install git+https://github.com/huggingface/transformers")
    raise e

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        # Read audio file
        audio_bytes = await file.read()
        audio_buffer = io.BytesIO(audio_bytes)
        
        # Load audio using soundfile (flexible support for wav, flac, etc)
        # We need to ensure sample rate matches the processor
        data, samplerate = sf.read(audio_buffer)
        
        # If stereo, convert to mono
        if len(data.shape) > 1:
            data = data.mean(axis=1)

        # Resample if necessary (GLM-ASR usually expects 16kHz, but processor handles features)
        # Ideally we trust the processor's feature extractor, but we must pass raw audio array
        # The processor.feature_extractor.sampling_rate is usually 16000
        target_sr = processor.feature_extractor.sampling_rate
        
        if samplerate != target_sr:
            # Simple resampling using scipy if needed, or just warn
            # For now, let's assume input is recorded at 16k or handle simplistic resampling
            import scipy.signal
            number_of_samples = round(len(data) * float(target_sr) / samplerate)
            data = scipy.signal.resample(data, number_of_samples)

        # Process
        inputs = processor.apply_transcription_request(data)
        
        # Move to device
        inputs = inputs.to(model.device, dtype=model.dtype)
        
        # Generate
        outputs = model.generate(**inputs, do_sample=False, max_new_tokens=500)
        
        # Decode
        decoded_output = processor.batch_decode(outputs[:, inputs.input_ids.shape[1] :], skip_special_tokens=True)
        
        text = decoded_output[0] if decoded_output else ""
        return {"text": text}

    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok", "device": device}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
