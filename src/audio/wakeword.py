import numpy as np
from openwakeword.model import Model

from config.paths import WWMODELS

from eventos import Evento


class WakeWord:

    def __init__(self, fila, mic):
        self.modelo = Model([
            str(WWMODELS / "sarah.onnx"),
            str(WWMODELS / "hey_sarah.onnx")
        ])
        self.fila = fila
        self.mic = mic

    def aguardar(self):
        while True:
            
            chunk = self.mic.ler(self.mic.chunk_wakeword)

            audio = np.frombuffer(
                chunk,
                dtype=np.int16
            )

            pred = self.modelo.predict(audio)

            if (
                pred["sarah"] > 0.4 or
                pred["hey_sarah"] > 0.4
            ):
                self.fila.put(Evento.WAKEWORD)