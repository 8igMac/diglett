"""
Example Python client for Respberry Pi.
"""
import pyaudio
import requests
import websockets
import asyncio
import json
import wave
import base64
from dotenv import dotenv_values

import diglett.config as config

# Load sensitive data from .env
info = dotenv_values(".env")
SERVER_IP = info["SERVER_IP"]
PORT = info["PORT"]

def record(seconds: int):
    """ record audio.
    args:
        seconds: record duration (seconds).
    return:
        raw audio in bytes.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )
    total_chuncks = int(config.fs / config.chunk * seconds)
    frames = list()
    for i in range(total_chuncks):
        data = stream.read(config.chunk)
        frames.append(data)
    return b"".join(frames)

def read_wav_file(filename:str):
    """
    Args:
        filename: path to audio file.
    Return:
        Raw audio in bytes.
    """
    frames = list()
    with wave.open(filename, "rb") as wf:
        while len(data := wf.readframes(config.chunk)):
            frames.append(data)
    return b"".join(frames)

def write_wav_file(filename: str, raw_audio: bytes):
    """ Write audio bytes into wave file.

    Args:
        filename: Filename of output wave.
        raw_audio: Raw audio in bytes.
    """
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(pyaudio.get_sample_size(config.sample_format))
        wf.setframerate(config.fs)
        wf.writeframes(raw_audio)

async def send(websocket, stream, spkemb1, spkemb2):
    while True:
        try:
            data = stream.read(int(config.fs / 3))
            """
            Sending JSON:
            {
                "audio_data": {base64 encoded audio chunck}
            }
            """
            data = base64.b64encode(data).decode("utf-8")
            message = {
                "speaker_embedding": [spkemb1, spkemb2],
                "audio_data": str(data),
            }
            json_data = json.dumps(message)

            await websocket.send(json_data)
        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error."
        # Setting the delay to 0 provides an optimized path
        # to allow other tasks to run.
        # (see https://docs.python.org/3/library/asyncio-task.html#asyncio.sleep)
        await asyncio.sleep(0)
    message = {
        "terminate_session": True,
    }
    json_data = json.dumps(message)
    await websocket.send(json_data)


async def receive(websocket, spkemb1, spkemb2):
    async for data in websocket:
        message = json.loads(data)
        if "speaker" in message:
            emb = message["speaker"]
        else:
            print("error: no speaker emb returned")

        if "db" in message:
            db = message["db"]
        else:
            print("error: no db returned")

        if emb == spkemb1:
            speaker = "speaker  1"
        elif emb == spkemb2:
            speaker = "speaker  2"
        else:
            speaker = "sil       "

        print(f"speaker: {speaker}, db: {db:5.0f}")


def get_speaker_info(filename: str):
    """Get speaker embedding and db from server.

    Args:
        filename: Audio file.
    Return
        (embedding, db)
    """
    with open(filename, "rb") as f:
        res = requests.post(f"http://{SERVER_IP}:{PORT}/embed", files={"file": f})
        json_data = res.json()
        return json_data["speaker_embedding"], json_data["avg_db"]


async def main():
    f1 = "1.wav"
    f2 = "2.wav"

    # Speaker1 config.
    print("speaker 1")
    audio_data = record(5)
    write_wav_file(f1, audio_data)

    # Speaker2 config.
    print("speaker 2")
    audio_data = record(5)
    write_wav_file(f2, audio_data)

    # Get speaker embedding and db.
    spkemb1, db1 = get_speaker_info(f1)
    spkemb2, db2 = get_speaker_info(f2)
    print("Got speaker info")
    print(len(spkemb1), db1)
    print(len(spkemb2), db2)

    # Init stream.
    p = pyaudio.PyAudio()
    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )

    # Listening
    async with websockets.connect(f"ws://{SERVER_IP}:{PORT}/stream") as websocket:
        send_result, receive_result = await asyncio.gather(
            receive(websocket, spkemb1, spkemb2),
            send(websocket, stream, spkemb1, spkemb2),
        )

    # Close stream.
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    asyncio.run(main())
