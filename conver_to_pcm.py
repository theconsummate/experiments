import sys
import glob
import scipy
import numpy
from tqdm import tqdm

files = glob.glob(sys.argv[1])
for file in tqdm(files):
    sr, in_audio = scipy.io.wavfile.read(file)
    scipy.io.wavfile.write(file, sr, (in_audio*300).astype(np.int16))
