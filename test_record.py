from audio import record, write_wav_file

if __name__ == "__main__":
    audio_bytes = record(3)
    write_wav_file("xx.wav", audio_bytes)
