import pyaudio
import numpy as np
from collections import deque
import threading
from time import sleep


class AudioBuffer:

    RATE = 8000
    CHUNK = int(RATE / 10)  # Number of samples read at a time
    
    def __init__(self, chunks: int = 5) -> None:
        self.chunks = chunks  # control size of the deque buffer
        self.stream = pyaudio.PyAudio().open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = self.RATE,
            input = True,  # microphone used as the stream
            frames_per_buffer = self.CHUNK,
            )
        self.thread = threading.Thread(
            target = self._collect_data,
            daemon = True
        )
        self.frames = deque(
            maxlen = self.chunks
        )  # double ended queue
    
    def __call__(self):
        return np.concatenate(self.frames)
    
    def __len__(self):
        return self.CHUNK * self.chunks
    
    def is_full(self):
        return len(self.frames) == self.chunks
    
    def start(self):
        self.thread.start()
        while not self.is_full(): # wait until the buffer is filled
            sleep(0.1)
    
    def _collect_data(self):
        while True:
            raw_data = self.stream.read(self.CHUNK)  # returns bytes data
            decoded = np.frombuffer(raw_data, np.int16) # decoded to integers
            self.frames.append(decoded)  # represents the last chunks of the recorded signal

if __name__ == "__main__":
    audio_buffer = AudioBuffer()
    audio_buffer.start()
    sleep(0.5) # wait until the buffer is not empty
    print(audio_buffer.audio.shape)