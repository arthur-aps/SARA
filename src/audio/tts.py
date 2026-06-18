import asyncio
import subprocess
import edge_tts

from eventos import Evento


class TTS:

    def __init__(self, fila):
        self.fila = fila

    async def falar_async(self, texto, arquivo):
        fila.put(Evento.TTS_ARQUIVANDO)
        communicate = edge_tts.Communicate(
            texto,
            voice="pt-BR-FranciscaNeural"
        )

        await communicate.save(arquivo)

        fila.put(Evento.TTS_ARQUIVADO)

        fila.put(Evento.TTS_RODANDO)
        subprocess.run([
            "ffplay",
            "-nodisp",
            "-autoexit",
            "-loglevel",
            "quiet",
            arquivo
        ])
        
        fila.put(Evento.TTS_RODADO)

    def falar(self, texto, arquivo):
        asyncio.run(
            self.falar_async(texto, arquivo)
        )