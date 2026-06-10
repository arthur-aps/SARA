#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DHTesp.h>
#include <secrets.h> // onde ficam ssid e senha da rede wifi

#define DHT 25
#define RELE 26
#define PRESENCA 27

DHTesp dhtSensor;

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

void setup() {
  Serial.begin(115200);

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
  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}