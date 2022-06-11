import torch
import wave
from speechbrain.pretrained import EncoderClassifier

import audio
import config
from utils import bytes_preproc

classifier_dir = './model/classifier'
classifier = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=classifier_dir,
)
similarity = torch.nn.CosineSimilarity(dim=-1, eps=1e-6)

if __name__ == "__main__":
    audio_data = audio.read_wav_file("male.wav")
    processed_audio = bytes_preproc(audio_data)
    male_emb = classifier.encode_batch(processed_audio)

    audio_data = audio.read_wav_file("female.wav")
    processed_audio = bytes_preproc(audio_data)
    female_emb = classifier.encode_batch(processed_audio)

    # audio_data = audio.read_wav_file("test.wav")
    # processed_audio = bytes_preproc(audio_data)
    # emb = classifier.encode_batch(processed_audio)

    # chunk = config.chunk
    chunk = int(config.fs / 2)
    with wave.open("test.wav", "rb") as wf:
        audio_data = wf.readframes(chunk)
        while len(audio_data) > 0:
            processed_audio = bytes_preproc(audio_data)
            emb = classifier.encode_batch(processed_audio)
            score_male = similarity(emb, male_emb)
            print(f"score male: {score_male}")
            score_female = similarity(emb, female_emb)
            print(f"score female: {score_female}")

            audio_data = wf.readframes(chunk)
