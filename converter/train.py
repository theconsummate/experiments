import os
from scipy import signal
from scipy.io import wavfile
import librosa
import numpy as np

def load_data(root):
    speakers = ["VCC2SF1", "VCC2SF2", "VCC2TF1", "VCC2TF2"]
    file = os.path.join(root, speakers[0], "10002.wav")

    sample_rate, samples = wavfile.read(file)
    print(samples)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
    print(spectrogram.shape)

    D = librosa.stft(y=np.array([float(x) for x in samples]), n_fft=512, hop_length=80, win_length=400)
    mag = np.abs(D)
    print(mag.shape)

def main():
    load_data("/home/dhruv/code/vcc2018_training")
    

if __name__ == '__main__':
    main()