from dataclasses import dataclass
from queue import Empty, Queue

import numpy as np


@dataclass(slots=True)
class AudioChunk:
    samples: np.ndarray
    rms: float


class AudioBus:

    def __init__(self):
        self.listeners = []


    def subscribe(self):
        fila = Queue()
        self.listeners.append(fila)
        return fila


    def unsubscribe(self, fila):
        if fila in self.listeners:
            self.listeners.remove(fila)


    def publish(self, chunk: AudioChunk):
        for fila in list(self.listeners):
            fila.put(chunk)


    def flush(self, fila):
        while True:
            try:
                fila.get_nowait()
            except Empty:
                break
