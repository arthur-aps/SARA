from audio import gravar, transcrever, falar
from ia import processar
from wakeword import aguardar_ativacao
import time
import threading
import automacoes


def loop_automacoes():
    while True:
        try:
            automacoes.tick()
        except Exception as e:
            print(f"[AUTOMAÇÃO] {e}")

        time.sleep(2)


threading.Thread(
    target=loop_automacoes,
    daemon=True
).start()


def main():
    while True:
        aguardar_ativacao()
        
        while True:
            time.sleep(0.2)
            texto = transcrever(gravar())
            if not texto.strip():
                break
            print(f"Pergunta: {texto}")
            resposta = processar(texto)
            if resposta:
                threading.Thread(
                    target=falar,
                    args=(resposta,),
                    daemon=True
                ).start()
                print(f"Resposta: {resposta}")
                # só volta pra wakeword se não terminou com pergunta
                if not resposta.strip().endswith("?"):
                    break


main()