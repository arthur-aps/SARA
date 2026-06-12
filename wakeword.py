import pyaudio
import numpy as np
from openwakeword.model import Model

def aguardar_ativacao():
    modelo_ww = Model(["wwmodels/sarah.onnx", "wwmodels/hey_sarah.onnx"])
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1280
    )

    print('Aguardando palavra de ativação ("SARA" ou "hey SARA", em sotaque norte-americano)...')
    while True:
        chunk = stream.read(1280, exception_on_overflow=False)
        audio_np = np.frombuffer(chunk, dtype=np.int16)
        prediction = modelo_ww.predict(audio_np)
        if prediction["sarah"] > 0.4 or prediction["hey_sarah"] > 0.4:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print("Ativada!")
            return