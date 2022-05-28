import torchaudio
from speechbrain.pretrained import VAD

def main():
    tmpdir = './model/vad'
    vad = VAD.from_hparams(
        source="speechbrain/vad-crdnn-libriparty",
        savedir=tmpdir,
    )

    boundaries = vad.get_speech_segments("data/vad_test.wav")
    print(f'Should be [5, 10]: {boundaries}')

    boundaries = vad.get_speech_segments("data/vad_test_3_seg.wav")
    print(f'Should be [5, 10, 15, 20, 25, 30]: {boundaries}')

if __name__ == "__main__":
    main()
