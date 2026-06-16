import time
import estado
import dispositivos
import audio
import threading

def tick():
    estado.logico["ambiente"]["periodo_anterior"] = estado.logico["ambiente"]["periodo"]
    estado.atualizar_periodo()

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
                f"[AUTOMAÇÃO] Usuário presente."
            )
            estado.logico["usuario"]["usuario_presente"] = True

            if (
                estado.logico["ambiente"]["modo"] == "sono" or
                estado.logico["ambiente"]["modo"] == "circadiano"
            ):
                print(
                    "[AUTOMAÇÃO] "
                    "Ativando modo circadiano"
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

    if tempo_ausente > 300 and estado.logico["usuario"]["usuario_presente"]:
        print("[AUTOMAÇÃO] Usuário ausente")
        estado.logico["usuario"]["usuario_presente"] = False

    if (
        tempo_ausente > 900 and
        not estado.logico["automacao"]["modo_sono_automatico"] and
        not estado.logico["modo"]["cinema"]
    ): # 15 min de ausência entra no modo sono, exceto se estava no modo cinema
        print("[AUTOMAÇÃO] Sem presença há mais de 15 minutos, ativando modo sono...")
        dispositivos.modo_sono()
        estado.logico["automacao"]["modo_sono_automatico"] = True


def verificar_periodo():
    ambiente = estado.logico["ambiente"]

    if ambiente["modo"] != "circadiano":
        return

    if ambiente["periodo"] == ambiente["periodo_anterior"]:
        return

    print(
        f"[AUTOMAÇÃO] Mudança de período: "
        f"{ambiente['periodo_anterior']} -> {ambiente['periodo']}"
    )

    dispositivos.modo_circadiano()

    ambiente["periodo_anterior"] = ambiente["periodo"]