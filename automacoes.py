import time
import estado
import dispositivos
import audio


def tick():
    try:
        dispositivos.status()
    except Exception as e:
        print(f"[AUTOMAÇÃO] Erro ao atualizar estado: {e}")
        return

    verificar_presenca()
    verificar_ausencia()


def verificar_presenca():
    agora = time.time()

    if estado.fisico["presenca"]:
        estado.logico["ultima_presenca"] = agora
        estado.logico["modo_sono_automatico"] = False

        if not estado.logico["usuario_presente"]:
            print(
                f"[AUTOMAÇÃO] Usuário presente. Modo={estado.logico['modo']}"
            )
            estado.logico["usuario_presente"] = True

            if agora - estado.logico["ultima_saudacao"] > 300:
                
                audio.falar("Oi, Arthur.")
                estado.logico["ultima_saudacao"] = agora


def verificar_ausencia():
    tempo_ausente = time.time() - estado.logico["ultima_presenca"]
    estado.logico["tempo_sem_presenca"] = tempo_ausente

    if tempo_ausente > 60 and estado.logico["usuario_presente"]:
        print("[AUTOMAÇÃO] Usuário ausente")
        estado.logico["usuario_presente"] = False

    if tempo_ausente > 900 and not estado.logico["modo_sono_automatico"]: # 15 min de ausência
        print("[AUTOMAÇÃO] Sem presença há mais de 15 minutos, ativando modo sono...")
        dispositivos.modo_sono()
        estado.logico["modo_sono_automatico"] = True