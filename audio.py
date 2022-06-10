import wave
import pyaudio
import config

def record(seconds: int):
    """ Record audio.
    Args:
        seconds: Record duration (seconds).
    Return:
        Raw audio in bytes.
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=config.sample_format,
        channels=config.channels,
        rate=config.fs,
        frames_per_buffer=config.chunk,
        input=True,
    )
    total_chuncks = int(config.fs / config.chunk * config.seconds)
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
        data = wf.readframes(config.chunk)
        while len(data) > 0:
            frames.append(data)
            data = wf.readframes(config.chunk)
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
