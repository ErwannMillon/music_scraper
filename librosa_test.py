import torchaudio

wav, sr = torchaudio.load("./test.mp3")
torchaudio.save("saved.mp3", wav, sr)
print(sr)