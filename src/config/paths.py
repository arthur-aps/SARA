from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

# assets
ASSETS = ROOT / "assets"
WWMODELS = ASSETS / "wwmodels"
SOUNDS = ASSETS / "sounds"

# data
DATA = ROOT / "data"
RECORDINGS = DATA / "recordings"
SITUACAO_SAVE = DATA / "situacao_save"


def criar_diretorios():
    for diretorio in (
        DATA,
        RECORDINGS,
        SITUACAO_SAVE,
    ):
        diretorio.mkdir(parents=True, exist_ok=True)