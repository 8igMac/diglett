import pyaudio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
# fs = 44100  # Record at 44100 samples per second
seconds = 3

# VAD model preferes:
channels = 1
fs = 16000  # Record at 44100 samples per second
