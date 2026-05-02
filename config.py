import os

# ========== RUTAS ==========
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "acelerometro.csv")

# ========== MQTT ==========
MQTT_BROKER = "xxxxx"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/acelerometro"

# ========== CSV ==========
COLUMNAS = ["timestamp", "accel_x", "accel_y", "accel_z", "magnitud"]
BUFFER_SIZE = 5

print(f"📁 Datos guardados en: {CSV_FILE}")
