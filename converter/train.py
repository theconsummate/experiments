from __future__ import division
import os
from scipy import signal
from scipy.io import wavfile
import librosa
import numpy as np

def load_data(root):
    speakers = ["VCC2SF1", "VCC2SF2", "VCC2TF1", "VCC2TF2"]
    target = os.path.join(root, speakers[-1], "10001.wav")
    twav, _ = librosa.load(target)
    
    for spk in speakers[:-1]:
        file = os.path.join(root, spk, "10001.wav")

        wav, _ = librosa.load(file)
        rate = len(wav)/len(twav)
        # print(rate)
        wav_norm = librosa.effects.time_stretch(wav, rate)
        wav_norm = librosa.util.fix_length(wav_norm, len(twav), mode='edge')



        D = librosa.stft(y=wav_norm, n_fft=512, hop_length=80, win_length=400)
        mag = np.abs(D).T
        print(mag.shape)
    D = librosa.stft(y=twav, n_fft=512, hop_length=80, win_length=400)
    print(mag.shape)

def main():
    load_data("/home/dhruv/code/vcc2018_training")
    

if __name__ == '__main__':
    main()