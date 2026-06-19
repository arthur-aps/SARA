import asyncio
import subprocess
import edge_tts
import threading

from config.paths import RECORDINGS

from eventos import (
    TTSArquivando,
    TTSArquivado,
    TTSRodando,
    TTSRodado
)


class TTS:

    def __init__(self, fila_eventos):
        self.fila_eventos = fila_eventos
        self.RESPONSE_PATH = (RECORDINGS / "response.mp3")

    async def _falar_async(self, texto):
        arquivo = self.RESPONSE_PATH

        self.fila_eventos.put(TTSArquivando())
        communicate = edge_tts.Communicate(
            texto,
            voice="pt-BR-FranciscaNeural"
        )

        await communicate.save(arquivo)

        self.fila_eventos.put(TTSArquivado())

        self.fila_eventos.put(TTSRodando())
        subprocess.run([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            arquivo
        ])
        
        self.fila_eventos.put(TTSRodado())


    def _falar(self, texto):
        asyncio.run(self._falar_async(texto))


    def falar_async(self, texto):
        self.thread_falar = threading.Thread(
            target=self._falar,
            args=(texto,),
            daemon=True
        ).start()