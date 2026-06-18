from enum import Enum, auto


class Evento(Enum):

    MIC_GRAVACAO_INICIADA = auto()
    MIC_GRAVACAO_ENCERRADA = auto()

    WAKEWORD = auto()

    FALA_USUARIO_INICIADA = auto()
    FALA_USUARIO_FINALIZADA = auto()
    FALA_USUARIO_ARQUIVADA = auto()
    FALA_USUARIO_TRANSCRITA = auto()

    IA_RESPONDEU = auto()

    TTS_ARQUIVANDO = auto()
    TTS_ARQUIVADO = auto()
    TTS_RODANDO = auto()
    TTS_RODADO = auto()