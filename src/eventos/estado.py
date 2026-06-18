from enum import Enum, auto


class Estado(Enum):

    ESPERA = auto()
    PERGUNTA = auto()
    RESPOSTA = auto()
    