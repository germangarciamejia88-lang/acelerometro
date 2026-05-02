import os
import sys
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

# Agregar el directorio actual y el directorio scripts al path
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)  # Agrega el directorio raíz
sys.path.append(os.path.join(current_dir, 'scripts1'))  # Agrega scripts

from config import CSV_FILE
from mqtt_receiver import MQTTReceiver
from csv_logger import CSVLogger
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    print("="*50)
    print("   SISTEMA ACELERÓMETRO ADXL345")
    print("   MQTT + CSV")
    print("="*50)
    print(f"📁 Datos: {CSV_FILE}")
    print("="*50)

def ver_ultimos_datos():
    """Muestra los últimos 10 datos guardados"""
    logger = CSVLogger()
    df = logger.get_last_n(10)
    
    if len(df) == 0:
        print("\n⚠️ No hay datos guardados aún")
        return
    
    print("\n📊 ÚLTIMOS 10 REGISTROS")
    print("-"*70)
    print(df.to_string(index=False))
    
    stats = logger.get_stats()
    print(f"\n📈 Total registros: {stats['total']}")
    print(f"💾 Tamaño archivo: {stats['size_kb']:.2f} KB")

def main():
    while True:
        clear_screen()
        show_header()
        
        print("\n📋 MENÚ")
        print("-"*30)
        print("1. 📡 INICIAR RECEPTOR MQTT")
        print("2. 📊 VER ÚLTIMOS 10 DATOS")
        print("3. ❌ SALIR")
        print("-"*30)
        
        opcion = input("\n👉 Opción (1-3): ").strip()
        
        if opcion == '1':
            clear_screen()
            receptor = MQTTReceiver()
            receptor.start()
            
        elif opcion == '2':
            clear_screen()
            ver_ultimos_datos()
            input("\nPresiona Enter para continuar...")
            
        elif opcion == '3':
            print("\n👋 Saliendo...")
            break
        else:
            print("\n❌ Opción inválida")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()