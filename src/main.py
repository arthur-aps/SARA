import time
import threading

from audio import AudioManager
from ia import Ia
from situacao import Situacao, SituacaoManager, Serializer
from automacoes import Automacoes, Dispositivos
from conversa import ConversationManager
from config.paths import criar_diretorios 

from queue import Queue


def main():
    print("[main] Criando diretórios...")
    criar_diretorios()
    
    print("[main] Criando fila de eventos...")
    fila = Queue()

    print("[main] Criando instância de AudioManager...")
    audio = AudioManager(fila)

    print("[main] Criando instância de Situacao...")
    situacao = Situacao(fila)

    print("[main] Criando instância de SituacaoManager...")
    situacao_manager = SituacaoManager(fila, situacao)

    print("[main] Criando instância de Serializer...")
    serializer = Serializer(situacao)

    print("[main] Criando instância de Dispositivos...")
    dispositivos = Dispositivos(fila, situacao)

    print("[main] Criando instância de Ia...")
    ia = Ia(fila, situacao, dispositivos)

    print("[main] Criando instância de Automacoes...")
    automacoes = Automacoes(fila, situacao, situacao_manager, dispositivos)

    print("[main] Criando instância de ConversationManager...")
    conversation = ConversationManager(
        fila,
        audio,
        ia,
    )

    print("[main] Iniciando automacoes...")
    automacoes.iniciar()

    print("[main] Carregando estado do quarto anterior com serializer...")
    serializer.carregar()

    print("[main] Executando módulo orquestrador de conversação...")
    conversation.executar()


main()