from enum import Enum, auto


class Estado(Enum):

    ESPERA = auto()
    OUVINDO = auto()
    RESPOSTA = auto()
    