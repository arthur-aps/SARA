from groq import Groq
from dotenv import load_dotenv
import os
import json
import threading

from .tool_registry import ToolRegistry
from .prompts import Prompts

from eventos import IaRespondeu


load_dotenv()

class Ia:
    def __init__(self, fila_eventos, situacao, dispositivos):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_AI_MODEL")
        self.client = Groq(api_key=self.groq_key)

        self.situacao = situacao
        self.dispositivos = dispositivos
        
        self.tool_registry = ToolRegistry(self.dispositivos)
        self.prompts = Prompts(fila_eventos, self.situacao)

        self.messages = [
            {
                "role": "system",
                "content": self.prompts.gerar_system_prompt()
            }
        ]

        self.fila_eventos = fila_eventos

    def adicionar_mensagem(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def _limitar_memoria(self):
        if len(self.messages) > 11:
            self.messages = (
                self.messages[:1]
                + self.messages[-10:]
            )

    def _processar(self, texto):
        self.messages[0]["content"] = self.prompts.gerar_system_prompt()
        
        self._limitar_memoria()

        self.adicionar_mensagem('user', texto)

        tools = self.tool_registry.TOOLS
        available_functions = self.tool_registry.AVAILABLE_FUNCTIONS
        
        tentativas = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.groq_model,
                    messages=self.messages,
                    tools=tools,
                    tool_choice="auto"
                )
                tentativas = 0

            except Exception as e:
                print(f"[IA] Erro: {e}")
                tentativas += 1
                if tentativas >= 3:
                    return "Desculpe, tive um problema. Pode repetir?"
                continue

            print(response.choices[0].message)
            self.messages.append(response.choices[0].message)
            content = response.choices[0].message.content

            # detecta se o modelo gerou function call como texto
            if content and "<function=" in content:
                tentativas += 1
                if tentativas >= 3:
                    return "Desculpe, tive um problema na chamada de funções. Pode repetir?"
                self.messages.pop()  # remove a mensagem mal formatada do histórico
                continue

            if response.choices[0].message.tool_calls:
                for tc in response.choices[0].message.tool_calls:
                    if tc.function.name in available_functions:
                        args = json.loads(tc.function.arguments)

                        print("[IA] TOOL CALL:")
                        print(tc.id)
                        print(tc.function.name)
                        print(tc.function.arguments)

                        result = available_functions[tc.function.name](**args)

                        self.messages.append({
                            'role': 'tool',
                            'tool_call_id': tc.id,
                            'name': tc.function.name,
                            'content': str(result)
                        })
            else:
                self.fila_eventos.put(
                    IaRespondeu(content)
                )
                return

    def processar_async(self, texto):
        self.thread_processar = threading.Thread(
            target=self._processar,
            args=(texto,),
            daemon=True
        )
        self.thread_processar.start()