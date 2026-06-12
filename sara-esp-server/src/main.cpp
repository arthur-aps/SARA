#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DHTesp.h>
#include <secrets.h> // onde ficam ssid e senha da rede wifi

#define DHT 25
#define RELE 26
#define PRESENCA 27
#define PIN_R 18
#define PIN_G 19
#define PIN_B 21

const int canalR = 0;
const int canalG = 1;
const int canalB = 2;

DHTesp dhtSensor;

void fadeParaCor(int rAlvo, int gAlvo, int bAlvo, int duracao) {
    int passos = 50;  // quantidade de passos da transição
    int intervalo = duracao / passos;

    // lê os valores atuais
    int rAtual = ledcRead(canalR);
    int gAtual = ledcRead(canalG);
    int bAtual = ledcRead(canalB);

    for (int i = 1; i <= passos; i++) {
        int r = rAtual + (rAlvo - rAtual) * i / passos;
        int g = gAtual + (gAlvo - gAtual) * i / passos;
        int b = bAtual + (bAlvo - bAtual) * i / passos;

        ledcWrite(canalR, r);
        ledcWrite(canalG, g);
        ledcWrite(canalB, b);

        delay(intervalo);
    }
}

WebServer server(80);


void handleRoot() {
  server.send(200, "text/plain", "Opa, seja bem-vindo ao módulo de controle da SARA!");
}

void handleNotFound() {
  server.send(404, "text/plain", "Página não encontrada");
}

void handleLigarLuz() {
  digitalWrite(RELE, LOW);
  server.send(200, "text/plain", "Luz ligada");
}

void handleDesligarLuz() {
  digitalWrite(RELE, HIGH);
  server.send(200, "text/plain", "Luz desligada");
}

void handleStatus() {
  // Temperatura e umidade
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  bool presenca = digitalRead(PRESENCA) == HIGH;
  bool releStatus = digitalRead(RELE) == LOW; // LOW = ligado

  String json = "{";
  json += "\"temperatura\": " + String(data.temperature, 1) + ",";
  json += "\"umidade\": " + String(data.humidity, 1) + ",";
  json += "\"presenca\": " + String(presenca ? "true" : "false") + ",";
  json += "\"luz\": \"" + String(releStatus ? "ligada" : "desligada") + "\"";
  json += "}";
  
  server.send(200, "application/json", json);
}

void handleDefinirCor() {
  if (!server.hasArg("r") ||
        !server.hasArg("g") ||
        !server.hasArg("b")) {

        server.send(400, "text/plain", "Parâmetros r, g e b obrigatórios");
        return;
    }

    int r = constrain(server.arg("r").toInt(), 0, 255);
    int g = constrain(server.arg("g").toInt(), 0, 255);
    int b = constrain(server.arg("b").toInt(), 0, 255);

    Serial.printf("R=%d G=%d B=%d\n", r, g, b);

    fadeParaCor(r, g, b, 1500);

    server.send(200, "text/plain", "Cor alterada com sucesso!");
}

void setup() {
  Serial.begin(115200);

  ledcSetup(canalR, 5000, 8); // canal, frequência, resolução
  ledcSetup(canalG, 5000, 8);
  ledcSetup(canalB, 5000, 8);

  ledcAttachPin(PIN_R, canalR);
  ledcAttachPin(PIN_G, canalG);
  ledcAttachPin(PIN_B, canalB);

  ledcWrite(canalR, 255);

  dhtSensor.setup(DHT, DHTesp::DHT22);

  pinMode(RELE, OUTPUT);
  digitalWrite(RELE, HIGH); // relé começa desligado

  pinMode(PRESENCA, INPUT);

  IPAddress ip(192, 168, 15, 100); // IP estático para o ESP32
  IPAddress gateway(192, 168, 15, 1); // IP do roteador
  IPAddress subnet(255, 255, 255, 0);

  WiFi.config(ip, gateway, subnet);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/ligar_luz", handleLigarLuz);
  server.on("/desligar_luz", handleDesligarLuz);
  server.on("/status", handleStatus);
  server.on("/cor", handleDefinirCor);
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}