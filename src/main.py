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
    criar_diretorios()

    fila = Queue()

    audio = AudioManager(fila)

    situacao = Situacao(fila)

    situacao_manager = SituacaoManager(fila, situacao)

    serializer = Serializer(situacao)

    dispositivos = Dispositivos(fila, situacao)

    ia = Ia(fila, situacao, dispositivos)

    automacoes = Automacoes(fila, situacao, situacao_manager, dispositivos)

    conversation = ConversationManager(
        fila,
        audio,
        ia,
    )

    automacoes.iniciar()

    serializer.carregar()

    conversation.executar()


main()