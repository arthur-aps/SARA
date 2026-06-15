import time
import estado
import dispositivos
import audio

estado.logico["ambiente"]["periodo_anterior"] = estado.logico["ambiente"]["periodo"]

def tick():
    try:
        dispositivos.status()
    except Exception as e:
        print(f"[AUTOMAÇÃO] Erro ao atualizar estado: {e}")
        return

    verificar_presenca()
    verificar_ausencia()
    verificar_periodo()


def verificar_presenca():
    agora = time.time()

    if estado.fisico["presenca"]:
        estado.logico["usuario"]["ultima_presenca"] = agora
        estado.logico["automacao"]["modo_sono_automatico"] = False

        if not estado.logico["usuario"]["usuario_presente"]:
            print(
                f"[AUTOMAÇÃO] Usuário presente, ativando modo circadiano..."
            )
            estado.logico["usuario"]["usuario_presente"] = True
            if estado.logico["ambiente"]["modo"] == "sono":
                print(
                    "[AUTOMAÇÃO] "
                    "Saindo do modo sono devido à presença"
                )
                dispositivos.modo_circadiano()
            if agora - estado.logico["automacao"]["ultima_saudacao"] > 300:
                
                threading.Thread(
                    target=audio.falar,
                    args=("Bem vindo de volta, Arthur.",),
                    daemon=True
                ).start()
                estado.logico["automacao"]["ultima_saudacao"] = agora


def verificar_ausencia():
    tempo_ausente = time.time() - estado.logico["usuario"]["ultima_presenca"]
    estado.logico["usuario"]["tempo_sem_presenca"] = tempo_ausente

    if tempo_ausente > 60 and estado.logico["usuario"]["usuario_presente"]:
        print("[AUTOMAÇÃO] Usuário ausente")
        estado.logico["usuario"]["usuario_presente"] = False

    if tempo_ausente > 900 and not estado.logico["automacao"]["modo_sono_automatico"]: # 15 min de ausência
        print("[AUTOMAÇÃO] Sem presença há mais de 15 minutos, ativando modo sono...")
        dispositivos.modo_sono()
        estado.logico["automacao"]["modo_sono_automatico"] = True


def verificar_periodo():
    periodo_atual = estado.logico["ambiente"]["periodo"]
    periodo_anterior = estado.logico["ambiente"]["periodo_anterior"]
    if (
        estado.logico["ambiente"]["modo"] == "circadiano" and
        periodo_anterior != periodo_atual
    ):
        dispositivos.modo_circadiano()
        estado.logico["ambiente"]["periodo_anterior"] = periodo_atual