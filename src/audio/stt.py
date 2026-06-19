import subprocess

import numpy as np
import pyaudio
import soundfile as sf
import webrtcvad
import threading

from config.paths import SOUNDS
from config.paths import RECORDINGS

from faster_whisper import WhisperModel

from eventos import (
    FalaUsuarioIniciada,
    FalaUsuarioFinalizada,
    FalaUsuarioArquivada,
    FalaUsuarioTranscrita
)


class STT:

    def __init__(self, fila, audio_bus, request_path=(RECORDINGS / "request.wav")):
        self.fs = 16000
        self.modelo = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )
        self.vad = webrtcvad.Vad(2)
        self.audio = pyaudio.PyAudio()
        self.fila_eventos = fila
        self.audio_bus = audio_bus
        self.REQUEST_PATH = request_path

    def _gravar(self):
        path = self.REQUEST_PATH
        frames = []

        silencio = 0
        falando = False

        fila_audio = self.audio_bus.subscribe()

        try:
            subprocess.run([
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(SOUNDS / "start-stream.mp3")
            ])

            self.audio_bus.flush(fila_audio)

            print("[STT] Gravando...")

            self.fila_eventos.put(FalaUsuarioIniciada())

            while True:

                chunk = fila_audio.get()

                is_speech = self.vad.is_speech(chunk, self.fs)

                if is_speech:
                    falando = True
                    silencio = 0
                    frames.append(chunk)

                elif falando:

                    silencio += 1
                    frames.append(chunk)

                    if silencio > 80:
                        break

            subprocess.run([
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel",
                "quiet",
                str(SOUNDS / "end-stream.mp3")
            ])

            print("[STT] Fim da gravação.")
            self.fila_eventos.put(FalaUsuarioFinalizada(path))

            recording = np.frombuffer(
                b"".join(frames),
                dtype=np.int16
            )

            recording = recording.astype(np.float32) / 32768.0

            sf.write(path, recording, self.fs)
            self.fila_eventos.put(FalaUsuarioArquivada(path))

        finally:
            self.audio_bus.unsubscribe(fila_audio)


    def gravar_async(self):
        self.thread_gravar = threading.Thread(
            target=self._gravar,
            daemon=True
        ).start()


    def _transcrever(self):
        audio = self.REQUEST_PATH

        segments, info = self.modelo.transcribe(
            audio,
            language="pt",
            vad_filter=True
        )

        texto = " ".join(segment.text for segment in segments)

        self.fila_eventos.put(FalaUsuarioTranscrita(texto))

    def transcrever_async(self):
        self.thread_transcrever = threading.Thread(
            target=self._transcrever,
            daemon=True
        )
        self.thread_transcrever.start()