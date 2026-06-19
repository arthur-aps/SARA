from enum import Enum, auto


class Estado(Enum):

    ESPERA = auto()
    OUVINDO = auto()
    TRANSCREVENDO = auto()
    PROCESSANDO_RESPOSTA = auto()
    IA_FALANDO = auto()
    RESPOSTA = auto()
    