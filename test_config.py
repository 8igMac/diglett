import pyaudio
import websockets
import asyncio
import json
import wave
import base64

import config

filename = "config_out.wav"

async def send(websocket, stream):
    """
    Sending JSON:
    {
        "audio_data": {base64 encoded audio chunck}
    }
    """
    frames = list()
    for i in range(int(config.fs / config.chunk * config.seconds)):
        data = stream.read(config.chunk)
        frames.append(data)
    raw_audio = b"".join(frames)

    try: 
        encoded = base64.b64encode(raw_audio).decode("utf-8")
        json_data = json.dumps({"audio_data": str(encoded)})
        await websocket.send(json_data)
    except websockets.exceptions.ConnectionClosedError as e:
        print(e)
    except Exception as e:
        assert False, "Not a websocket 4008 error."

    # Save record for debugging.
    print("Start writing file.")
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(pyaudio.get_sample_size(config.sample_format))
        wf.setframerate(config.fs)
        wf.writeframes(b''.join(frames))
    print("Finished writing file")

async def receive(websocket):
    async for data in websocket:
        message = json.loads(data)
        if "speaker_name" in message:
            print(message["speaker_name"])
        if "speaker_embedding" in message:
            print(message["speaker_embedding"])

async def main():
    p = pyaudio.PyAudio() # Create an interface to PyAudio.

    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )

    async with websockets.connect("ws://127.0.0.1:8000/ws/config") as websocket:
        await send(websocket, stream)
        await receive(websocket)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    asyncio.run(main())
