from groq import Groq
import dispositivos
from dotenv import load_dotenv
import os
import json

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_AI_MODEL")

client = Groq(api_key=groq_key)

available_functions = {
    'ligar_luz': dispositivos.ligar_luz,
    'desligar_luz': dispositivos.desligar_luz,
    'status': dispositivos.status,
    'definir_cor': dispositivos.definir_cor,
    'modo_cinema': dispositivos.modo_cinema,
    'modo_gaming': dispositivos.modo_gaming,
    'modo_leitura': dispositivos.modo_leitura,
    'granada_de_luz': dispositivos.granada_de_luz,
}

messages = [
    {
        'role': 'system',
        'content': f"""
        Você é SARA, Sistema de Automação Residencial Autônoma. Controla dispositivos do quarto do Arthur via comandos de voz.

        PERSONALIDADE
        - Respostas curtas, diretas e amigáveis, sempre em português
        - Senso de humor ocasional, sem exageros
        - Sem emojis

        REGRAS DE AÇÃO
        - Só execute ações quando o pedido for explícito ("acende a luz", "apaga a luz", "liga o ar")
        - Antes de agir, chame status() para verificar o estado atual e evitar ações desnecessárias
        - Se algo já estiver no estado pedido, informe em vez de agir
        - Em caso de dúvida sobre a intenção, pergunte antes de executar

        REGRAS DE CONSULTA
        - Chame status() sempre que o usuário perguntar sobre temperatura, umidade, presença ou estado dos dispositivos
        - Não chame status() em saudações ou mensagens casuais

        CONVERSAS CASUAIS
        - Responda brevemente
        - Não ofereça informações não solicitadas
        - Pode fazer uma piada leve se o contexto permitir
        """
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
            'name': 'status',
            'description': 'Obtém o estado atual do quarto, com informações sobre a luz (do quarto, não da fita LED), temperatura e umidade',
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
            'name': 'modo_cinema',
            'description': 'Muda a cor das fitas LED para um tom mais cinema (255, 80, 20) e desliga a luz do quarto.',
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
            'description': 'Muda a cor das fitas LED para vermelho (255, 0, 0) e desliga a luz do quarto.',
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
            'description': 'Muda a cor das fitas LED para um branco quente (255, 255, 200) e desliga a luz do quarto.',
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
            'name': 'granada_de_luz',
            'description': 'Flashbang. Liga a luz do quarto e LEDs no branco total (255, 255, 255).',
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