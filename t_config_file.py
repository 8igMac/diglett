import websockets
import asyncio
import json
import base64
import os
from dotenv import load_dotenv

import audio
import config

# Load sensitive data from .env
load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
PORT = os.getenv("PORT")

async def send(websocket, raw_audio: bytes):
    """
    Sending JSON:
    {
        "audio_data": {base64 encoded audio chunck}
    }
    """
    try: 
        encoded = base64.b64encode(raw_audio).decode("utf-8")
        json_data = json.dumps({"audio_data": str(encoded)})
        await websocket.send(json_data)
    except websockets.exceptions.ConnectionClosedError as e:
        print(e)
    except Exception as e:
        assert False, "Not a websocket 4008 error."

async def receive(websocket):
    async for data in websocket:
        message = json.loads(data)
        if "speaker_name" in message:
            print(message["speaker_name"])
        if "speaker_embedding" in message:
            print(message["speaker_embedding"])
        if "avg_db" in message:
            print(message["avg_db"])

async def main():
    raw_audio = audio.read_wav_file("gg.wav")
    async with websockets.connect(f"ws://{SERVER_IP}:{PORT}/ws/config") as websocket:
        await send(websocket, raw_audio)
        await receive(websocket)
    # # Write audio for debugging.
    # audio.write_wav_file("hh.wav", raw_audio)

if __name__ == "__main__":
    asyncio.run(main())
