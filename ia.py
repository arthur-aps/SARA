from groq import Groq
import dispositivos
import estado
from dotenv import load_dotenv
import os
import json

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_AI_MODEL")

client = Groq(api_key=groq_key)

SYSTEM_PROMPT = f"""
    Você é SARA, Sistema de Automação Residencial Autônoma. Controla dispositivos do quarto do Arthur via comandos de voz.

    PERSONALIDADE
    - Respostas curtas e amigáveis, sempre em português
    - Senso de humor ocasional, sem exageros
    - Sem emojis

    REGRAS DE AÇÃO
    - Se o pedido do usuário for explícito, faça
    - Se algo já estiver no estado pedido, informe em vez de agir
    - Você pode decidir a melhor ação para o contexto, pois é autônoma
    - Em caso de dúvida sobre a intenção, pergunte antes de executar

    REGRAS DE CONSULTA
    O estado físico e lógico fornecidos no contexto são a fonte principal da verdade.
    Use essas informações para decidir suas ações.
    Quando o modo atual estiver definido no estado lógico,
    considere-o confiável. Não utilize RGB para inferir modos.
    Só chame status() quando:
    - algum valor necessário estiver ausente;
    - houver suspeita de dessincronização;
    - o usuário pedir explicitamente uma atualização dos sensores.

    CONVERSAS CASUAIS
    - Responda brevemente
    - Não ofereça informações não solicitadas
    - Pode fazer uma piada leve se o contexto permitir

    Existem dois tipos de modos:
    - Modos automáticos:
    - modo_circadiano

    - Modos manuais:
    - modo_cinema
    - modo_gaming
    - modo_leitura
    - modo_sono
    - modo_trabalho
    - modo_relaxar

    Quando o usuário pedir uma iluminação adequada ao horário, conforto ou ambiente sem especificar um modo, utilize modo_circadiano.

    Quando o usuário pedir explicitamente um modo, utilize o modo solicitado.
"""

dispositivos.status()
estado.atualizar_estado_logico()
estado.atualizar_periodo()
print('Estado do quarto sincronizado.')

available_functions = {
    'ligar_luz': dispositivos.ligar_luz,
    'desligar_luz': dispositivos.desligar_luz,
    'obter_estado': dispositivos.obter_estado,
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

messages = [
    {
        'role': 'system',
        'content': SYSTEM_PROMPT + "\n\n" +
        estado.gerar_contexto_tempo() + "\n\n" +
        estado.gerar_prompt_estado()
    }
]

tools=[
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

def processar(texto):
    global messages
    print(estado.gerar_contexto_tempo())
    
    if len(messages) > 11:
        messages = messages[:1] + messages[-10:] # memória de no máximo 10 mensagens (e o system prompt), pra não viajar demais na maionese
    
    messages.append({'role': 'user', 'content': texto})
    
    tentativas = 0
    while True:
        try:
            response = client.chat.completions.create(
                model=groq_model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            tentativas = 0
        except Exception as e:
            print(f"Erro: {e}")
            tentativas += 1
            if tentativas >= 3:
                return "Desculpe, tive um problema. Pode repetir?"
            continue

        print(response.choices[0].message)
        messages.append(response.choices[0].message)
        content = response.choices[0].message.content

        # detecta se o modelo gerou function call como texto
        if content and "<function=" in content:
            tentativas += 1
            if tentativas >= 3:
                return "Desculpe, tive um problema na chamada de funções. Pode repetir?"
            messages.pop()  # remove a mensagem mal formatada do histórico
            continue

        if response.choices[0].message.tool_calls:
            for tc in response.choices[0].message.tool_calls:
                if tc.function.name in available_functions:
                    args = json.loads(tc.function.arguments)

                    print("TOOL CALL:")
                    print(tc.id)
                    print(tc.function.name)
                    print(tc.function.arguments)

                    result = available_functions[tc.function.name](**args)

                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tc.id,
                        'name': tc.function.name,
                        'content': str(result)
                    })
        else:
            return content  # retorna o texto final pro SARA.py falar