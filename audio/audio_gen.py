from scipy.io.wavfile import write
import numpy as np
import random

samplerate = 44100
fs = 100
duration = 0.15
sample_cnt = int(duration * samplerate)
t_array = np.linspace(0., duration, sample_cnt)
amplitude = np.iinfo(np.int16).max
max_harmonic = 10
byte_sep = int(sample_cnt / (max_harmonic - 1))

def harmonic_gen(fs):
    data = np.zeros(sample_cnt)
    for n in range(1, max_harmonic):

        temp_data = np.zeros(sample_cnt)
        for i in range(sample_cnt):
            
            if i >= byte_sep * (n - 1):
                temp_data[i] = amplitude / (max_harmonic * n) * np.sin(2. * np.pi * fs * n* t_array[i])

        data += temp_data
    return data

s_list = []
notes = [1, 2, 3, 4, 5, 6, 7, 8]
for s in range(0,122):
    r = random.choice(notes)
    s1 = harmonic_gen(100 * r / 2)
    s_list.append(s1)


song = np.tile(np.hstack(s_list), 4)
write("example.mp3", samplerate, song.astype(np.int16))


