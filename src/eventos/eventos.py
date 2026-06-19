from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class MicGravacaoIniciada:
    pass

@dataclass
class MicGravacaoEncerrada:
    pass



@dataclass
class Wakeword:
    pass



@dataclass
class FalaUsuarioIniciada:
    pass

@dataclass
class FalaUsuarioFinalizada:
    caminho: Path

@dataclass
class FalaUsuarioArquivada:
    caminho: Path

@dataclass
class FalaUsuarioTranscrita:
    transcricao: str



@dataclass
class IaRespondeu:
    resposta: str



@dataclass
class TTSArquivando:
    pass

@dataclass
class TTSArquivado:
    pass

@dataclass
class TTSRodando:
    pass

@dataclass
class TTSRodado:
    pass



@dataclass
class PeriodoAtualizado:
    periodo: str