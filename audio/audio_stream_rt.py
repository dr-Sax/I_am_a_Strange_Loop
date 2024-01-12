import pyaudio
import numpy as np
from collections import deque
import threading
from time import sleep
from scipy.io.wavfile import write
import random
import sys
import math


class AudioBuffer:

    RATE = 8000
    CHUNK = int(RATE / 10)  # Number of samples read at a time
    
    def __init__(self, chunks: int = 5) -> None:
        self.chunks = chunks  # control size of the deque buffer
        self.raw_data = None
        self.input_stream = pyaudio.PyAudio().open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.RATE,
            input = True,  # microphone used as the stream
            frames_per_buffer = self.CHUNK,
            )
        
        self.output_stream =  pyaudio.PyAudio().open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.RATE,
            output = True,  # speaker to stream
            frames_per_buffer = self.CHUNK,
            )

        self.input_thread = threading.Thread(
            target = self._collect_data,
            daemon = True
        )

        self.output_thread = threading.Thread(
            target = self._emit_data,
            daemon = True
        )


        self.frames = deque(
            maxlen = self.chunks
        )  # double ended queue
    
    # https://medium.com/py-bits/sound-generation-python-904e54f5398d
    # sounds gross tho!
    def harmonic_gen(self, fs):
        BITRATE = self.RATE    #number of frames per second/frameset.
        FREQUENCY = fs     #Hz, waves per second, 261.63=C4-note.
        LENGTH = 0.2    #seconds to play sound
        if FREQUENCY > BITRATE:
            BITRATE = FREQUENCY + 100
        NUMBEROFFRAMES = int(BITRATE * LENGTH)
        RESTFRAMES = NUMBEROFFRAMES % BITRATE
        WAVEDATA = ''
        #generating waves
        for x in range(NUMBEROFFRAMES):
            WAVEDATA = WAVEDATA + chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))
        for x in range(RESTFRAMES):
            WAVEDATA = WAVEDATA+chr(128)

        return WAVEDATA
    
    def __call__(self):
        return np.concatenate(self.frames)
    
    def __len__(self):
        return self.CHUNK * self.chunks
    
    def is_full(self):
        return len(self.frames) == self.chunks
    
    def start(self):
        self.input_thread.start()
        #self.output_thread.start()
        while not self.is_full(): # wait until the buffer is filled
            sleep(0.1)
    
    def _collect_data(self):
        while True:
            raw_data = self.input_stream.read(self.CHUNK)  # returns bytes data
            decoded = np.frombuffer(raw_data, np.int16) # decoded to integers
            self.frames.append(decoded)  # represents the last chunks of the recorded signal

    def _emit_data(self):
        notes = [1, 2, 3, 4, 5, 6, 7, 8]
    
        while True:
            r = random.choice(notes)
            raw_data = self.harmonic_gen(100 * r / 2)
            print(sys.getsizeof(raw_data[0]))
            print()
            self.output_stream.write(
                frames = raw_data, 
                num_frames = int(self.RATE * .2)
                )
            
if __name__ == "__main__":
    audio_buffer = AudioBuffer()
    audio_buffer.start()
    sleep(0.5) # wait until the buffer is not empty
    print(audio_buffer.audio.shape)