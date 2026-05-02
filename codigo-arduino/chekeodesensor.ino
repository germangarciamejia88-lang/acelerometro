#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ========= CONFIGURACIÓN ADXL345 =========
#define ADXL345_ADDRESS 0x53
#define ADXL345_REG_DEVID 0x00
#define ADXL345_REG_POWER_CTL 0x2D
#define ADXL345_REG_DATAX0 0x32

// ========= CONFIGURACIÓN WiFi =========
const char* ssid = "xxxxx";
const char* password = "xxxx";

// ========= CONFIGURACIÓN MQTT =========
const char* mqtt_server = "ip";
const int mqtt_port = 1883;
const char* mqtt_topic = "sensor/acelerometro";

// ========= OBJETOS =========
WiFiClient espClient;
PubSubClient client(espClient);

float accel_x, accel_y, accel_z;

// ========= SETUP =========
void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println("\n🚀 Iniciando sistema ADXL345...");
  
  // 1. Inicializar ADXL345
  Wire.begin(21, 22); // SDA=21, SCL=22
  
  if (!initADXL345()) {
    Serial.println("❌ ERROR: ADXL345 no encontrado");
    Serial.println("Verifica conexiones:");
    Serial.println("  VCC → 3.3V o 5V");
    Serial.println("  GND → GND");
    Serial.println("  SCL → GPIO 22");
    Serial.println("  SDA → GPIO 21");
    while (1) delay(100);
  }
  Serial.println("✅ ADXL345 conectado");
  
  // 2. Conectar WiFi
  connectWiFi();
  
  // 3. Conectar MQTT
  client.setServer(mqtt_server, mqtt_port);
  connectMQTT();
  
  Serial.println("\n✅ Sistema listo! Enviando datos...\n");
}

// ========= INICIALIZAR ADXL345 =========
bool initADXL345() {
  // Verificar Device ID
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(ADXL345_REG_DEVID);
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345_ADDRESS, (uint8_t)1);
  
  if (!Wire.available()) return false;
  
  byte deviceId = Wire.read();
  if (deviceId != 0xE5) return false;
  
  // Configurar modo medición
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(ADXL345_REG_POWER_CTL);
  Wire.write(0x08); // Modo medición
  Wire.endTransmission();
  
  // Configurar rango ±16g
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(0x31); // Registro DATA_FORMAT
  Wire.write(0x0B); // ±16g, full resolution
  Wire.endTransmission();
  
  return true;
}

// ========= LEER ADXL345 =========
void readADXL345() {
  Wire.beginTransmission(ADXL345_ADDRESS);
  Wire.write(ADXL345_REG_DATAX0);
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345_ADDRESS, (uint8_t)6);
  
  if (Wire.available() >= 6) {
    int16_t x = Wire.read() | (Wire.read() << 8);
    int16_t y = Wire.read() | (Wire.read() << 8);
    int16_t z = Wire.read() | (Wire.read() << 8);
    
    // Convertir a g (escala 256 LSB/g para ±16g)
    accel_x = x / 256.0;
    accel_y = y / 256.0;
    accel_z = z / 256.0;
  }
}

// ========= ENVIAR DATOS POR MQTT =========
void sendData() {
  StaticJsonDocument<200> doc;
  doc["accel_x"] = accel_x;
  doc["accel_y"] = accel_y;
  doc["accel_z"] = accel_z;
  
  // Calcular magnitud
  float magnitud = sqrt(accel_x*accel_x + accel_y*accel_y + accel_z*accel_z);
  doc["magnitud"] = magnitud;
  
  char buffer[256];
  serializeJson(doc, buffer);
  
  if (client.connected()) {
    if (client.publish(mqtt_topic, buffer)) {
      Serial.printf("📤 X:%.2f Y:%.2f Z:%.2f | Mag:%.2f ✅\n", 
                    accel_x, accel_y, accel_z, magnitud);
    } else {
      Serial.println("❌ Error MQTT");
    }
  } else {
    Serial.println("⚠️ MQTT desconectado");
  }
}

// ========= CONEXIÓN WiFi =========
void connectWiFi() {
  Serial.print("📡 Conectando a WiFi...");
  WiFi.begin(ssid, password);
  
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("✅ WiFi conectada - IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("❌ Error WiFi");
    while(1) delay(100);
  }
}

// ========= CONEXIÓN MQTT =========
void connectMQTT() {
  Serial.print("🔌 Conectando a MQTT...");
  int intentos = 0;
  
  while (!client.connected() && intentos < 10) {
    String clientId = "ESP32_ADXL345_" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("✅ Conectado");
    } else {
      Serial.print(".");
      delay(1000);
      intentos++;
    }
  }
  
  if (!client.connected()) {
    Serial.println("\n⚠️ MQTT no disponible, enviando solo por serial");
  }
}

// ========= LOOP PRINCIPAL =========
void loop() {
  if (!client.connected() && WiFi.status() == WL_CONNECTED) {
    connectMQTT();
  }
  if (client.connected()) {
    client.loop();
  }
  
  readADXL345();
  sendData();
  
  delay(1000); // Enviar cada 1 segundo
}