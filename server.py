from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import wave
import pyaudio
import asyncio
import json
import time

# TODO: How to encode these data? 
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "server_output.wav"
app = FastAPI()

# with wave.open(filename, "wb") as wf:
#     wf.setnchannels(channels)
#     wf.setsampwidth(pyaudio.get_sample_size(sample_format))
#     wf.setframerate(fs)
#     wf.writeframes(b''.join(frames))
    

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        async for data in websocket.iter_bytes():
            eos_b = bytes("EOS", "utf-8")
            length = len(eos_b)
            if data[-length:] == eos_b:
                break
            else:
                # data = bytes("get message", "utf-8")
                await websocket.send_bytes(data)
    except WebSocketDisconnect:
        print("Client disconnected.")
