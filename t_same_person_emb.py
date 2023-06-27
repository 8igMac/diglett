import torchaudio
from speechbrain.pretrained import EncoderClassifier, SpeakerRecognition

def main():
    # tmpdir = getfixture("tmpdir")
    tmpdir = './model/speaker_recog'
    # classifier = EncoderClassifier.from_hparams(
    #     source="speechbrain/spkrec-ecapa-voxceleb",
    #     savedir=tmpdir,
    # )

    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb",
        savedir=tmpdir,
    )

    print("Same speaker, with score")
    # Male
    signal1, fs1 = torchaudio.load("data/speaker_m/audio-oz-julia-000.wav")
    signal3, fs3 = torchaudio.load("data/speaker_m/audio-oz-julia-002.wav")
    signal5, fs5 = torchaudio.load("data/speaker_m/audio-oz-julia-010.wav")
    score, pred = verification.verify_batch(signal1, signal5)
    print(score)
    score, pred = verification.verify_batch(signal3, signal5)
    print(score)
    score, pred = verification.verify_batch(signal3, signal1)
    print(score)

    # Female
    signal2, fs2 = torchaudio.load("data/speaker_f/audio-oz-julia-001.wav")
    signal4, fs4 = torchaudio.load("data/speaker_f/audio-oz-julia-007.wav")
    signal6, fs6 = torchaudio.load("data/speaker_f/audio-oz-julia-009.wav")
    score, pred = verification.verify_batch(signal2, signal4)
    print(score)
    score, pred = verification.verify_batch(signal6, signal4)
    print(score)
    score, pred = verification.verify_batch(signal6, signal2)
    print(score)

    print("Different speaker, with score")
    score, pred = verification.verify_batch(signal1, signal2)
    print(score)
    score, pred = verification.verify_batch(signal1, signal4)
    print(score)
    score, pred = verification.verify_batch(signal1, signal6)
    print(score)
    score, pred = verification.verify_batch(signal3, signal2)
    print(score)
    score, pred = verification.verify_batch(signal3, signal4)
    print(score)
    score, pred = verification.verify_batch(signal3, signal6)
    print(score)
    score, pred = verification.verify_batch(signal5, signal2)
    print(score)
    score, pred = verification.verify_batch(signal5, signal4)
    print(score)
    score, pred = verification.verify_batch(signal5, signal6)
    print(score)

    signal7, fs7 = torchaudio.load("data/mix3.wav")
    signal8, fs8 = torchaudio.load("data/mix2.wav")
    signal9, fs9 = torchaudio.load("data/mix.wav")
    print("Mix vs female.")
    score, pred = verification.verify_batch(signal7, signal2)
    print(score)
    score, pred = verification.verify_batch(signal7, signal4)
    print(score)
    score, pred = verification.verify_batch(signal7, signal6)
    print(score)
    print("Mix vs male.")
    score, pred = verification.verify_batch(signal7, signal1)
    print(score)
    score, pred = verification.verify_batch(signal7, signal3)
    print(score)
    score, pred = verification.verify_batch(signal7, signal5)
    print(score)
    print("Mix vs mix.")
    score, pred = verification.verify_batch(signal7, signal8)
    print(score)
    score, pred = verification.verify_batch(signal7, signal9)
    print(score)

if __name__ == "__main__":
    main()
