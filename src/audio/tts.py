import asyncio
import subprocess
import threading

import edge_tts

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
        self.response_path = RECORDINGS / "response.mp3"

    def _tocar_arquivo(self, arquivo):
        subprocess.run([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            str(arquivo)
        ])

    async def _falar_async(self, texto):
        arquivo = self.response_path

        self.fila_eventos.put(TTSArquivando())
        communicate = edge_tts.Communicate(
            texto,
            voice="pt-BR-FranciscaNeural"
        )

        await communicate.save(arquivo)

        self.fila_eventos.put(TTSArquivado())

        self.fila_eventos.put(TTSRodando())
        self._tocar_arquivo(arquivo)
        
        self.fila_eventos.put(TTSRodado())


    def _falar(self, texto):
        asyncio.run(self._falar_async(texto))


    def falar_async(self, texto):
        self.thread_falar = threading.Thread(
            target=self._falar,
            args=(texto,),
            daemon=True
        )
        self.thread_falar.start()
