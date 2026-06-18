from .micinput import Microfone
from .wakeword import WakeWord
from .stt import STT
from .tts import TTS


class AudioManager:

    def __init__(self, fila):
        self.fila = fila
        self.microfone = Microfone(self.fila)
        self.wakeword = WakeWord(self.fila, self.microfone)
        self.stt = STT(self.fila, self.microfone)
        self.tts = TTS(self.fila)