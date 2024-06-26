import torch
import numpy as np

import diglett.config as config

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
    data = np.frombuffer(raw_bytes, dtype="int16")
    data = np.copy(data) # NOTE: Need a copy here, otherwise PyTorch will complain the data is not writable.
    data = torch.from_numpy(data)
    # [time, channels]
    data = data.reshape(-1, config.channels)
    # [channels, time]
    data = data.permute(1, 0)
    # Normalize int26: 2^15 = 32768
    data = data / 32768

    return data
