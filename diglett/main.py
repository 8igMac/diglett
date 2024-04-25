from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File
from typing import Annotated
import asyncio
import json
import base64
import torch
from speechbrain.inference.classifiers import EncoderClassifier

import diglett.config as cfg
from diglett.utils import bytes_preproc
from diglett.audio import get_mean_energy

app = FastAPI()
classifier_dir = './model/classifier'
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=classifier_dir,
)
similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)

@app.post("/embed")
async def embed(file: Annotated[bytes, File()]):
    """Embed the speaker's voice signiture.

    Send a 5 seconds recording of a speaker and 
    get mean energy, speaker embeddings.

    Parameters:
    file (bytes): Binary data of an 5 secs audio file. 

    Returns:
    json: {
        "speaker_name": str,
        "speaker_embedding": ndarray,
        "avg_db": float,
    }
    """

    # Get mean energy.
    mean = get_mean_energy(file)

    # Get speaker embedding.
    processed_audio = bytes_preproc(file)
    emb = classifier.encode_batch(processed_audio)
    # (batch, channel, time) -> (time)
    emb = emb.reshape(-1).numpy().tolist()

    print(len(emb))

    return {
        "speaker_name": "Alice",
        "speaker_embedding": emb,
        "avg_db": mean,
    }

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

            # Get mean energy.
            mean = get_mean_energy(audio_data)

            # Decode speaker embedding.
            spks = message["speaker_embedding"]
            assert len(spks) == 2
            spk1, spk2 = spks

            # Speaker verification.
            processed_audio = bytes_preproc(audio_data)
            emb = classifier.encode_batch(processed_audio)

            spk1_tensor = torch.tensor(spk1).reshape(1, 1, -1)
            score1 = similarity(emb, spk1_tensor)
            score1 = score1.reshape(-1).numpy().tolist()[0]

            spk2_tensor = torch.tensor(spk2).reshape(1, 1, -1)
            score2 = similarity(emb, spk2_tensor)
            score2 = score2.reshape(-1).numpy().tolist()[0]

            if score1 > cfg.threshold:
                spk = spk1
                print(f"1, score: {score1:.3f}, db: {mean:.0f}")
            elif score2 > cfg.threshold:
                spk = spk2
                print(f"2, score: {score2:.3f}, db: {mean:.0f}")
            else:
                spk = [0]
                print(f"sil, score1: {score1:.3f}, score2: {score2:.3f}, db: {mean:.0f}")

            # Create message.
            message = {
                "speaker": spk,
                "db": mean,
            }

            # Send audio label.
            await websocket.send_json(message)
    except WebSocketDisconnect:
        print("Client disconnected.")

@app.get("/")
async def root():
    return {"msg": "Hello World"}