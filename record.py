import audio

if __name__ == "__main__":
    raw_audio = audio.record(10)
    audio.write_wav_file("mix.wav", raw_audio)
