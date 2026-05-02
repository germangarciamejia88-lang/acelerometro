import paho.mqtt.client as mqtt
import json
import signal
import sys
import time
from csv_logger import CSVLogger
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

class MQTTReceiver:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.logger = CSVLogger()
        self.running = True
        
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print("\n🛑 Deteniendo...")
        self.logger.force_save()
        self.running = False
        self.client.disconnect()
        sys.exit(0)
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"✅ Conectado a {MQTT_BROKER}:{MQTT_PORT}")
            client.subscribe(MQTT_TOPIC)
            print(f"📡 Suscrito a: {MQTT_TOPIC}")
        else:
            print(f"❌ Error de conexión. Código: {rc}")
            print("   Posibles causas:")
            print("   1. Mosquitto no está corriendo")
            print("   2. IP incorrecta en config.py")
            print("   3. Puerto 1883 bloqueado por firewall")
    
    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode('utf-8')
            print(f"📨 Recibido: {payload}")
            self.logger.save_from_mqtt(payload)
        except Exception as e:
            print(f"⚠️ Error: {e}")
    
    def start(self):
        print("="*50)
        print("🚀 RECEPTOR MQTT - ADXL345")
        print("="*50)
        print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"Tópico: {MQTT_TOPIC}")
        print(f"Archivo: {self.logger.filename}")
        print("="*50)
        
        # Verificar que Mosquitto esté corriendo ANTES de intentar conectar
        print("\n🔍 Verificando conexión...")
        
        try:
            # Intentar conectar con timeout
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("✅ Conectado al broker MQTT")
            print("📡 Esperando datos... (Presiona Ctrl+C para detener)\n")
            self.client.loop_forever()
        except ConnectionRefusedError:
            print("\n❌ ERROR: No se pudo conectar al broker MQTT")
            print("="*50)
            print("🔧 SOLUCIÓN:")
            print("1. Abre una terminal y ejecuta:")
            print("   cd 'C:\\Program Files\\mosquitto'")
            print("   mosquitto -v")
            print("\n2. Verifica tu IP en config.py:")
            print(f"   Actual: {MQTT_BROKER}")
            print("   Ejecuta 'ipconfig' y verifica que coincida")
            print("\n3. Revisa que el firewall no bloquee el puerto 1883")
            print("="*50)
            input("\nPresiona Enter para volver al menú...")
            return
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("\nPresiona Enter para volver al menú...")
            return

if __name__ == "__main__":
    receiver = MQTTReceiver()
    receiver.start()