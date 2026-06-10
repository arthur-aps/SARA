from groq import Groq
import dispositivos
from dotenv import load_dotenv
import os

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_AI_MODEL")

client = Groq(api_key=groq_key)

available_functions = {
    'ligar_luz': dispositivos.ligar_luz,
    'desligar_luz': dispositivos.desligar_luz,
    'status': dispositivos.status,
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
            'description': 'Obtém o estado atual do quarto, com informações sobre a luz, temperatura e umidade',
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
                    result = available_functions[tc.function.name]()
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tc.function.name,
                        'content': str(result)
                    })
        else:
            return content  # retorna o texto final pro SARA.py falar