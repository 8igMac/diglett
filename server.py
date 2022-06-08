from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
import base64
from speechbrain.pretrained import VAD

from utils import bytes_preproc

app = FastAPI()
tmpdir = './model/vad'
vad = VAD.from_hparams(
    source="speechbrain/vad-crdnn-libriparty",
    savedir=tmpdir,
)

@app.websocket("/ws/config")
async def config(websocket: WebSocket):
    """ Configuration

    Extract speaker embedding from a audio segment.

    Input: A speech segment.
    Ouput: Speaker embedding, (ASR?).
    """
    await websocket.accept()

    try:
        message = await websocket.receive_json()
        if "audio_data" in message:
            print("server config: got audio data")

            # Decode audio.
            encoded = message["audio_data"]
            audio_data = base64.b64decode(encoded)

            # Send message.
            message = {
                "speaker_name": "小芬姊",
                "speaker_embedding": [0.5, 0.1],
                "avg_db": 100,
            }

            # Send audio label.
            await websocket.send_json(message)
        else:
            print("Wrong format: no 'audio_data'")
    except WebSocketDisconnect:
        print("Client disconnected.")

@app.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    """Streaming

    Stream audio input and return speaker labels.

    Input: Continuous audio stream.
        {
            "audio_data": [base64 encoded bytes],
            "speaker_embedding": [speaker emb1, speaker emb2]
            "terminate_session": bool,
        }
    Output: Continuous label stream.
        {
            "speaker": speaker_emb,
            "db": float,
        }
    """
    await websocket.accept()

    try:
        async for message in websocket.iter_json():
            if "terminate_session" in message and message["terminate_session"] == True: 
                print("terminate session")
                break

            # Decode audio.
            encoded = message["audio_data"]
            audio_data = base64.b64decode(encoded)

            # Decode speaker embedding.
            spks = message["speaker_embedding"]
            assert len(spks) == 2
            spk1, spk2 = spks
            print(f"Speaker1: {spk1}")
            print(f"Speaker2: {spk2}")

            # TODO: VAD
            # TODO: Speaker verification.
            message = {
                "speaker": [0.5, 0.1],
                "db": 56,
            }

            # Send audio label.
            await websocket.send_json(message)
    except WebSocketDisconnect:
        print("Client disconnected.")
