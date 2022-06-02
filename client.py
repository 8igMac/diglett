import pyaudio
import websockets
import asyncio
import json
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "gg.wav"

frames = []

async def send(websocket, stream):
    for i in range(int(fs / chunk * seconds)):
        try:
            data = stream.read(chunk)
            await websocket.send(data)
        except websockets.exceptions.ConnectionClosedError as e:
            print(e)
            break
        except Exception as e:
            assert False, "Not a websocket 4008 error."
        # Giveup the execution right.
        await asyncio.sleep(0.01)  
    # print("Finished recording sending EOS")
    await websocket.send(bytes("EOS", "utf-8"))

async def receive(websocket):
    async for data in websocket:
        frames.append(data)

async def main():
    p = pyaudio.PyAudio() # Create an interface to PyAudio.

    stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )

    async with websockets.connect("ws://127.0.0.1:8000/ws") as websocket:
        send_result, receive_result = await asyncio.gather(
            receive(websocket),
            send(websocket, stream), 
        )

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Start writing file.")
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
    print("Finished writing file")

if __name__ == "__main__":
    asyncio.run(main())
