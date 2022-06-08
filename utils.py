import torch
import numpy as np
import wave
import pyaudio

import config

def bytes_preproc(raw_bytes: bytes):
    """
    Preprocessing pipeline:
    1. Bytes to tensor.
    2. Reshape: [time, channels]
    3. Normalize int16: 2^15 = 32768
    4. Reshap: [batch, time, channels]

    Args:
    - audio_data: raw audio data in bytes (int16).

    Return:
    - Normalized tensor, [time, channel]
    """
    # Bytes to tensor.
    data = np.fromstring(raw_bytes, dtype="int16")
    data = torch.from_numpy(data)
    # [time, channels]
    data = data.reshape(-1, config.channels)
    # [channels, time]
    data = data.permute(1, 0)
    # Normalize int26: 2^15 = 32768
    data = data / 32768

    return data

def read_wav_file(filename:str):
    """
    Args:
        filename: path to audio file.
    Return:
        Raw audio in bytes.
    """
    frames = list()
    with wave.open(filename, "rb") as wf:
        data = wf.readframes(config.chunk)
        while len(data) > 0:
            frames.append(data)
            data = wf.readframes(config.chunk)
    return b"".join(frames)

def write_wav_file(filename: str, raw_audio: bytes):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(config.channels)
        wf.setsampwidth(pyaudio.get_sample_size(config.sample_format))
        wf.setframerate(config.fs)
        wf.writeframes(raw_audio)

