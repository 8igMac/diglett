import wave
import pyaudio

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
