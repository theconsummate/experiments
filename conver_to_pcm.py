import sys
import glob
from scipy.io import wavfile
import numpy as np
from tqdm import tqdm

files = glob.glob(sys.argv[1])
for file in tqdm(files):
    try:
        sr, in_audio = wavfile.read(file)
        wavfile.write(file, sr, (in_audio*300).astype(np.int16))
    except ValueError:
        print("problem with "+ file)
