import subprocess
import threading

import numpy as np
import sounddevice as sd


class AudioPlayer:

    def __init__(self, sample_rate=24000, channels=1, chunk_ms=50):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_frames = int(sample_rate * chunk_ms / 1000)
        self._parar = threading.Event()
        self._processo = None
        self._lock = threading.Lock()

    def parar(self):
        self._parar.set()

        with self._lock:
            processo = self._processo

        if processo and processo.poll() is None:
            processo.terminate()

    def tocar(self, arquivo, on_volume=None):
        self._parar.clear()

        bytes_por_frame = np.dtype(np.float32).itemsize * self.channels
        bytes_por_chunk = self.chunk_frames * bytes_por_frame

        processo = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "quiet",
                "-i",
                str(arquivo),
                "-f",
                "f32le",
                "-acodec",
                "pcm_f32le",
                "-ac",
                str(self.channels),
                "-ar",
                str(self.sample_rate),
                "pipe:1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        with self._lock:
            self._processo = processo

        try:
            with sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
            ) as stream:
                while not self._parar.is_set():
                    dados = processo.stdout.read(bytes_por_chunk)

                    if not dados:
                        break

                    audio = np.frombuffer(dados, dtype=np.float32)

                    if audio.size == 0:
                        break

                    audio = audio.reshape(-1, self.channels)

                    if on_volume:
                        rms = float(np.sqrt(np.mean(np.square(audio))))
                        on_volume(min(rms, 1.0))

                    stream.write(audio)

        finally:
            if on_volume:
                on_volume(0.0)

            if processo.poll() is None:
                processo.terminate()

            processo.wait()

            with self._lock:
                if self._processo is processo:
                    self._processo = None
