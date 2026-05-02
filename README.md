# 📡 Recepción de datos de un acelerómetro por vía MQTT

Proyecto para recibir y visualizar datos de un acelerómetro en tiempo real usando el protocolo MQTT. Ideal para monitorear movimientos, vibraciones o inclinación desde cualquier dispositivo conectado a la misma red.

## 📖 Descripción del proyecto

Este proyecto permite conectar un acelerómetro a una tarjeta ESP32, la cual envía los datos de aceleración (ejes X, Y, Z y Magnitud) a través del protocolo MQTT. Cualquier cliente MQTT puede suscribirse al tema correspondiente y recibir los datos en tiempo real y guardalos en archivo csv.

## 🧩 Piezas del proyecto

- Acelerómetro (ADXL345)
- Proto board 
- Cables para protoboard 
- ESP32 

## 📸 Diagrama del proyecto

<img width="523" height="583" alt="Captura de pantalla 2026-05-02 120723" src="https://github.com/user-attachments/assets/6a20a121-2e4f-4075-8369-5698cd3bd069" />


## 🚀 ¿Cómo funciona?

1. El acelerómetro se conecta a la ESP32 mediante comunicación I2C.
2. La ESP32 lee los valores del acelerómetro.
3. La ESP32 publica esos valores en un tema MQTT.
4. Un cliente MQTT se suscribe a ese tema y recibe los datos para guardalos en csv.

## ⚙️ Requisitos

- Arduino IDE o PlatformIO instalado
- Librerías necesarias:
  - `PubSubClient` (para MQTT)
  - `Wire` (para I2C)
  - Librería específica del acelerómetro (`Adafruit_ADXL345`)
