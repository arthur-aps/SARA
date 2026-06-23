from queue import Queue, Empty


class AudioBus:

    def __init__(self):
        self.listeners = []


    def subscribe(self) -> Queue[AudioChunk]:
        fila = Queue()

        self.listeners.append(fila)

        print("[AudioBus] Subscribe no bus realizado com sucesso.")

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