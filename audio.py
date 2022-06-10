import wave
import pyaudio
import config
import numpy as np
import matplotlib.pyplot as plt

def plot_energy(filename: str, audio_arr: np.ndarray):
    """ Plot the energy.
    
    Args:
        filename: Output plot file name.
        audio_arr: numpy array of audio energy.
    """
    plt.figure(1)
    plt.title("Signal Wave...")
    plt.plot(audio_arr)
    plt.savefig(filename)

def get_mean_energy(raw_audio: bytes):
    """Calculate mean energy level of input audio.

    Args:
        raw_audio: Raw audio in bytes.
    Return:
        Mean energy level of input audio.
    """
    arr = np.fromstring(raw_audio, dtype=np.int16)
    arr = np.abs(arr)
    mean = np.mean(arr)

    # # Plot the energy.
    # plot_energy("gg.png", arr)

    return mean

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
