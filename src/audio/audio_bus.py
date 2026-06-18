from queue import Queue


class AudioBus:

    def __init__(self):
        self.listeners = []

    def subscribe(self):

        fila = Queue()

        self.listeners.append(fila)

        return fila

    def publish(self, chunk):

        for fila in self.listeners:
            fila.put(chunk)