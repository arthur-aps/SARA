import threading
import time


class LedSpeechSync:

    def __init__(self, situacao, dispositivos, intensidade_maxima=0.55, intervalo=0.08):
        self.situacao = situacao
        self.dispositivos = dispositivos
        self.intensidade_maxima = intensidade_maxima
        self.intervalo = intervalo

        self._lock = threading.Lock()
        self._ativo = False
        self._cor_original = None
        self._cor_alvo = None
        self._thread = None

    def iniciar(self):
        with self._lock:
            self._cor_original = self._cor_atual()
            self._cor_alvo = self._cor_original
            self._ativo = True

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True
        )
        self._thread.start()

    def atualizar_volume(self, rms):
        with self._lock:
            if not self._ativo or not self._cor_original:
                return

            nivel = max(0.0, min(float(rms), 1.0))
            fator = 1.0 - (nivel * self.intensidade_maxima)

            self._cor_alvo = {
                canal: self._limitar_cor(valor * fator)
                for canal, valor in self._cor_original.items()
            }

    def finalizar(self):
        with self._lock:
            cor_original = self._cor_original
            self._ativo = False
            self._cor_alvo = None
            self._cor_original = None

        if cor_original:
            self._aplicar_cor(cor_original)

    def _loop(self):
        ultima_cor = None

        while True:
            with self._lock:
                if not self._ativo:
                    return

                cor_alvo = self._cor_alvo

            if cor_alvo and cor_alvo != ultima_cor:
                self._aplicar_cor(cor_alvo)
                ultima_cor = cor_alvo

            time.sleep(self.intervalo)

    def _cor_atual(self):
        cor = self.situacao.fisica.get("corLEDs", {})

        return {
            "red": int(cor.get("red", 0)),
            "green": int(cor.get("green", 0)),
            "blue": int(cor.get("blue", 0)),
        }

    def _aplicar_cor(self, cor):
        try:
            self.dispositivos.definir_cor_temporaria(
                cor["red"],
                cor["green"],
                cor["blue"]
            )
        except Exception as e:
            print(f"[LedSpeechSync] Erro ao sincronizar LEDs: {e}")

    def _limitar_cor(self, valor):
        return max(0, min(int(valor), 255))
