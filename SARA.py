from audio import gravar, transcrever, falar
from ia import processar
from wakeword import aguardar_ativacao
import time

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
                falar(resposta)
                print(f"Resposta: {resposta}")
                # só volta pra wakeword se não terminou com pergunta
                if not resposta.strip().endswith("?"):
                    break

main()