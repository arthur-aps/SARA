# SARA — Sistema de Automação Residencial Autônoma

SARA é uma assistente de automação residencial controlada por voz, construída do zero com ESP32, Python e IA generativa. Fala com ela, ela entende, e o quarto responde.

Foi inspirada no Jarvis do Tony Stark (só não tenho joia da mente sobrando pra transformar no Visão) e roda no meu quarto.

---

## O que ela faz

- Controla iluminação por comando de voz
- Lê temperatura e umidade do ambiente em tempo real
- Detecta presença no quarto via sensor PIR
- Toma decisões contextuais — pode verificar o estado do quarto antes de agir
- Responde em português com voz sintetizada
- Ativa com palavra de ativação ("Sarah")

---

## Como funciona

```
você fala -> Whisper transcreve -> modelo do Groq entende a intenção
-> Function calling decide a ação -> ESP32 executa fisicamente
```

Tudo isso em alguns segundos.

---

## Stack

**Hardware**
- ESP32 DevKit V1
- Módulo relé 1 canal
- Sensor DHT22 (temperatura e umidade)
- Sensor PIR HC-SR501 (presença)
- Receptor IR TSOP1838 (em breve — controle do AC)
- Fita LED RGB 5050 12V + MOSFETs (em breve)

**Software — ESP32**
- Framework Arduino (PlatformIO)
- Servidor HTTP com WebServer.h
- IP estático na rede local

**Software — PC**
- Python 3.14
- [faster-whisper](https://github.com/guillaumekynast/faster-whisper) — transcrição de voz local
- [Groq API](https://groq.com) — inferência rápida com modelos de IA
- [openWakeWord](https://github.com/dscripka/openWakeWord) — detecção de palavra de ativação
- [edge-tts](https://github.com/rany2/edge-tts) — síntese de voz
- FastAPI (em breve — servidor dedicado)

---

## Estrutura do projeto

```
SARA/
├── SARA.py                     # ponto de entrada, loop principal
├── audio.py                    # gravação, transcrição, TTS
├── wakeword.py                 # detecção de palavra de ativação
├── dispositivos.py             # funções que controlam o ESP32
├── ia.py                       # cliente Groq, tools, messages
├── models/                     # modelos de wakeword (.onnx)
├── .env.example                # variáveis de ambiente necessárias
└── sara-esp-server/            # firmware do ESP32 (PlatformIO), controle dos dispositivos
    └── src/
        └── secrets.h.example   # variáveis pro ESP32 conectar com seu roteador
```

---

## Como rodar

### Pré-requisitos

- Python 3.10+
- ESP32 com firmware carregado [sara-esp-server/](sara-esp-server/)
- Conta gratuita no [Groq](https://groq.com)

### Instalação

```bash
git clone https://github.com/arthur-aps/SARA
cd SARA
./scripts/setup.sh
```

### Configuração

Edite os arquivos `.env` e `secrets.h`:

```bash
nano .env
nano sara-esp-server/src/secrets.h
```

### Rodar o programa

```bash
./scripts/run.sh
```

---

## Hardware — diagrama de conexão

```
ESP32
├── Pino 25 → DHT22 (DATA)
├── Pino 26 → Relé (IN)
├── Pino 27 → PIR (OUT)
├── 3.3V    → DHT22 (VCC), PIR (VCC)
├── VIN     → Relé (VCC)
└── GND     → todos os GNDs

Fita LED RGB (em breve)
├── V+  → Fonte 12V (+)
├── R   → MOSFET 1 (OUT-)
├── G   → MOSFET 2 (OUT-)
└── B   → MOSFET 3 (OUT-)

MOSFETs
├── OUT-      → GND compartilhado
└── TRIG/PWM  → ESP32 pinos 18, 19, 21
```

---

## Exemplos de uso

> *"SARA, acende a luz"*
> -> liga a luz e te responde

> *"SARA, como está o quarto?"*
> -> consulta temperatura, umidade e estado da luz -> responde

> *"SARA, modo cinema"*
> -> ajusta as LEDs pra cor quente

---

## Roadmap

- [x] Servidor HTTP no ESP32
- [x] Controle de relé por voz
- [x] Leitura de temperatura e umidade
- [x] Detecção de presença
- [x] Integração com LLM (function calling)
- [x] Transcrição de voz local (Whisper)
- [x] Palavra de ativação
- [x] Síntese de voz
- [x] Controle de fita LED RGB
- [ ] Controle do ar condicionado (IR)
- [ ] Modos de iluminação dos LEDs (cinema, gaming, leitura)
- [ ] Sincronização de LEDs com voz da SARA
- [ ] PCB customizada
- [ ] Case 3D impresso

---

## Por que construí isso

Comecei a estudar programação pelo basicão, frontend, mas sempre quis entender como as coisas funcionam de verdade — hardware, sistemas operacionais, arquitetura. Também sempre curti muito as tecnologias do Tony Stark e, já que eu não consigo fazer a armadura dele ainda, a SARA nasceu como projeto de aprendizado por enquanto.

Do zero: sem experiência prévia em Python, eletrônica ou hardware embarcado.

Tá ficando bem da horinha. Aos poucos, vou melhorando ela, e ideias vão surgindo. Já já ela vai estar controlando quase de tudo no meu quarto.

---

## Licença

MIT — faz o que quiser, só me da os créditos.
