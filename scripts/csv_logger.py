import csv
import os
import json
from datetime import datetime
import pandas as pd
from config import CSV_FILE, COLUMNAS, BUFFER_SIZE, DATA_DIR

class CSVLogger:
    def __init__(self, filename=CSV_FILE):
        self.filename = filename
        self.buffer = []
        self.buffer_size = BUFFER_SIZE
        self.init_csv()
    
    def init_csv(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(COLUMNAS)
            print(f"✅ Archivo CSV creado: {self.filename}")
    
    def save_data(self, accel_x, accel_y, accel_z, magnitud):
        record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'accel_x': accel_x,
            'accel_y': accel_y,
            'accel_z': accel_z,
            'magnitud': magnitud
        }
        
        self.buffer.append(record)
        
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def save_from_mqtt(self, payload):
        try:
            if isinstance(payload, str):
                data = json.loads(payload)
            else:
                data = payload
            
            magnitud = data.get('magnitud', 0)
            
            self.save_data(
                data.get('accel_x', 0),
                data.get('accel_y', 0),
                data.get('accel_z', 0),
                magnitud
            )
            return True
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return False
    
    def flush(self):
        if not self.buffer:
            return
        
        try:
            with open(self.filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for record in self.buffer:
                    row = [record[col] for col in COLUMNAS]
                    writer.writerow(row)
            
            print(f"💾 Guardados {len(self.buffer)} registros")
            self.buffer = []
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def force_save(self):
        self.flush()
    
    def get_last_n(self, n=10):
        try:
            df = pd.read_csv(self.filename)
            return df.tail(n)
        except:
            return pd.DataFrame(columns=COLUMNAS)
    
    def get_stats(self):
        try:
            df = pd.read_csv(self.filename)
            return {
                "total": len(df),
                "size_kb": os.path.getsize(self.filename) / 1024
            }
        except:
            return {"total": 0, "size_kb": 0}