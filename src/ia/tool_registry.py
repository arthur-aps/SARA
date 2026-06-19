class ToolRegistry:
    def __init__(self, dispositivos):
        self.AVAILABLE_FUNCTIONS = {
            'ligar_luz': dispositivos.ligar_luz,
            'desligar_luz': dispositivos.desligar_luz,
            'obter_estado': dispositivos.obter_situacao,
            'status': dispositivos.status,
            'definir_cor': dispositivos.definir_cor,
            'modo_circadiano': dispositivos.modo_circadiano,
            'modo_cinema': dispositivos.modo_cinema,
            'modo_gaming': dispositivos.modo_gaming,
            'modo_leitura': dispositivos.modo_leitura,
            'modo_sono': dispositivos.modo_sono,
            'modo_trabalho': dispositivos.modo_trabalho,
            'modo_relaxar': dispositivos.modo_relaxar
        }

        self.TOOLS = [
            {
                'type': 'function',
                'function': {
                    'name': 'ligar_luz',
                    'description': 'Liga a luz do quarto',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'desligar_luz',
                    'description': 'Desliga a luz do quarto',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'obter_estado',
                    'description': 'Obtém o estado atual do quarto, com informações sobre a luz (do quarto e da fita LED), temperatura, umidade e presença.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'status',
                    'description': 'Obtém o estado atual do quarto atualizado em tempo real, com uma requisição HTTP. Demora mais que obter_estado, mas é atualizado em tempo real.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'definir_cor',
                    'description': 'Muda a cor das fitas LED no quarto.',
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'red': {
                                'type': 'number',
                                'description': 'valor a ser definido da cor vermelha (0 a 255).'
                            },
                            'green': {
                                'type': 'number',
                                'description': 'valor a ser definido da cor verde (0 a 255).'
                            },
                            'blue': {
                                'type': 'number',
                                'description': 'valor a ser definido da cor azul (0 a 255).'
                            }
                        },
                        'required': ['red', 'green', 'blue']
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_circadiano',
                    'description': 'Muda a luz do quarto e cor das fitas LED para um tom confortável específico para o período atual.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_cinema',
                    'description': 'Muda a cor das fitas LED para um tom mais cinema e desliga a luz do quarto.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_gaming',
                    'description': 'Muda a cor das fitas LED para vermelho e desliga a luz do quarto.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_leitura',
                    'description': 'Muda a cor das fitas LED para um branco quente e desliga a luz do quarto.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_sono',
                    'description': 'Muda a cor das fitas LED para tudo apagado e desliga a luz do quarto.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_trabalho',
                    'description': 'Liga a luz do quarto e deixa os LEDs no branco total.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'type': 'function',
                'function': {
                    'name': 'modo_relaxar',
                    'description': 'desliga a luz do quarto e deixa os LEDs num tom quente relaxante.',
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            }
        ]