import numpy as np

def get_mean_energy(raw_audio: bytes):
    """Calculate mean energy level of input audio.

    Args:
        raw_audio: Raw audio in bytes.
    Return:
        Mean energy level of input audio.
    """
    arr = np.frombuffer(raw_audio, dtype=np.int16) # bit depth is 16bits.
    arr = np.abs(arr)
    mean = np.mean(arr)

    return mean