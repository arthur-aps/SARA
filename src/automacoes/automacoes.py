import time
import threading


class Automacoes:
    
    def __init__(self, fila, situacao, situacao_manager, dispositivos):
        self.fila = fila
        self.situacao = situacao
        self.situacao_manager = situacao_manager
        self.dispositivos = dispositivos


    def tick(self):
        self.situacao.logica["ambiente"]["periodo_anterior"] = self.situacao.logica["ambiente"]["periodo"]
        self.situacao_manager.atualizar_periodo()

        try:
            self.dispositivos.status()
        except Exception as e:
            print(f"[AUTOMAÇÃO] Erro ao atualizar situação: {e}")
            return

        self.verificar_presenca()
        self.verificar_ausencia()
        self.verificar_periodo()


    def verificar_presenca(self):
        agora = time.time()

        if self.situacao.fisica["presenca"]:
            self.situacao.logica["usuario"]["ultima_presenca"] = agora
            self.situacao.logica["automacao"]["modo_sono_automatico"] = False

            if not self.situacao.logica["usuario"]["usuario_presente"]:
                print(
                    f"[AUTOMAÇÃO] Usuário presente."
                )
                self.situacao.logica["usuario"]["usuario_presente"] = True

                if (
                    self.situacao.logica["ambiente"]["modo"] == "sono" or
                    self.situacao.logica["ambiente"]["modo"] == "circadiano"
                ):
                    print(
                        "[AUTOMAÇÃO] "
                        "Ativando modo circadiano"
                    )
                    self.dispositivos.modo_circadiano()
                if agora - self.situacao.logica["automacao"]["ultima_saudacao"] > 600: # 10 min desde a última saudação
                    
                    threading.Thread(
                        target=self.audio.tts.falar,
                        args=("Bem vindo de volta, Arthur.",),
                        daemon=True
                    ).start()
                    self.situacao.logica["automacao"]["ultima_saudacao"] = agora


    def verificar_ausencia(self):
        tempo_ausente = time.time() - self.situacao.logica["usuario"]["ultima_presenca"]
        self.situacao.logica["usuario"]["tempo_sem_presenca"] = tempo_ausente

        if tempo_ausente > 300 and self.situacao.logica["usuario"]["usuario_presente"]: # 5 min de ausência dá como usuário ausente
            print("[AUTOMAÇÃO] Usuário ausente")
            self.situacao.logica["usuario"]["usuario_presente"] = False

        if (
            tempo_ausente > 900 and
            not self.situacao.logica["automacao"]["modo_sono_automatico"] and
            not self.situacao.logica["modo"]["cinema"]
        ): # 15 min de ausência entra no modo sono, exceto se estava no modo cinema
            print("[AUTOMAÇÃO] Sem presença há mais de 15 minutos, ativando modo sono...")
            self.dispositivos.modo_sono()
            self.situacao.logica["automacao"]["modo_sono_automatico"] = True


    def verificar_periodo(self):
        ambiente = self.situacao.logica["ambiente"]

        if ambiente["periodo"] == ambiente["periodo_anterior"]:
            return

        print(
            f"[AUTOMAÇÃO] Mudança de período: "
            f"{ambiente['periodo_anterior']} -> {ambiente['periodo']}"
        )

        if ambiente["modo"] == "circadiano":
            self.dispositivos.modo_circadiano()

        ambiente["periodo_anterior"] = ambiente["periodo"]


    def _loop(self):
        while True:
            try:
                self.tick()
            except Exception as e:
                print(f"[AUTOMAÇÃO] {e}")

            time.sleep(2)

    def iniciar(self):
        threading.Thread(
            target=self._loop,
            daemon=True
        ).start()