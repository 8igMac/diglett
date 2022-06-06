"""
After applying `bytes_preproc`, audio stream data 
must have the same tensor as torchaudio.load
"""
import wave
import pyaudio
import torchaudio
import torch
import numpy as np

import utils
import config

filename = "gg.wav"

if __name__ == "__main__":

    # Record 3s.
    p = pyaudio.PyAudio() # Create an interface to PyAudio.
    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )
    frames = list()
    for i in range(int(config.fs / config.chunk * config.seconds)):
        data = stream.read(config.chunk)
        frames.append(data)
    raw_bytes = b''.join(frames)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Bytes preprocessing. 
    torch_data = utils.bytes_preproc(raw_bytes)

    # Write record to file.
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(pyaudio.get_sample_size(config.sample_format))
        wf.setframerate(config.fs)
        wf.writeframes(raw_bytes)

    # Read using torchaudio.load() with default
    # normalization=true 
    # channel_first=true
    waves, fs = torchaudio.load(filename)

    # Print wav tensor.
    print(waves.shape)
    print(waves)

    # Compare the 2 tensor.
    print(torch.equal(torch_data, waves))
