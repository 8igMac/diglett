import pyaudio
import websockets
import asyncio
import json
import wave
import base64

import config

async def send(websocket, stream):
    for i in range(int(config.fs / config.chunk * config.seconds)):
        try:
            data = stream.read(config.chunk)
            """
            Sending JSON:
            {
                "audio_data": {base64 encoded audio chunck}
            }
            """
            data = base64.b64encode(data).decode("utf-8")
            message = {
                "speaker_embedding": [[0.5, 0.2], [0.1, 0.2]],
                "audio_data": str(data),
            }
            json_data = json.dumps(message)

            await websocket.send(json_data)
        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error."
        # Giveup the execution right.
        # await asyncio.sleep(0.01)  
        await asyncio.sleep(0.01)  
    # print("Finished recording sending EOS")
    message = {
        "terminate_session": True,
    }
    json_data = json.dumps(message)
    await websocket.send(json_data)

async def receive(websocket):
    async for data in websocket:
        print(data)

async def main():
    p = pyaudio.PyAudio() # Create an interface to PyAudio.

    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )

    async with websockets.connect("ws://127.0.0.1:8000/ws/stream") as websocket:
        send_result, receive_result = await asyncio.gather(
            receive(websocket),
            send(websocket, stream), 
        )

    stream.stop_stream()
    stream.close()
    p.terminate()

    # print("Start writing file.")
    # with wave.open(filename, "wb") as wf:
    #     wf.setnchannels(channels)
    #     wf.setsampwidth(pyaudio.get_sample_size(sample_format))
    #     wf.setframerate(fs)
    #     wf.writeframes(b''.join(frames))
    # print("Finished writing file")

if __name__ == "__main__":
    asyncio.run(main())
