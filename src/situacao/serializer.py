import json
from config.paths import SITUACAO_SAVE


class Serializer:

    def __init__(self, situacao):
        self.SAVE_PATH = SITUACAO_SAVE / "situacao_logica_save.json"
        self.situacao = situacao


    def salvar(self):
        with self.SAVE_PATH.open("w", encoding="utf-8") as f:
            json.dump(
                self.exportar(),
                f,
                indent=4,
                ensure_ascii=False
            )


    def carregar(self):
        if not self.SAVE_PATH.exists():
            return

        with self.SAVE_PATH.open("r", encoding="utf-8") as f:
            dados = json.load(f)

        self.situacao.logica["ambiente"].update(dados["ambiente"])


    def exportar(self):
        return {
            "ambiente": {
                "modo": self.situacao.logica["ambiente"]["modo"],
            }
        }