import sqlite3
import uuid
from datetime import datetime
from typing import List, Dict

class Database:
    def __init__(self, db_name="IoTDB.db"):
        self.db_name = db_name
        self.create_table()
        
    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TempLog2 (
                    GUID TEXT(36) PRIMARY KEY,
                    TEMP TEXT(10),
                    HUMI TEXT(10),
                    Time TEXT(30)
                )
            ''')
            conn.commit()
    
    def insert_temp_log(self, temp: str, humi: str) -> Dict:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            guid = str(uuid.uuid4())
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                'INSERT INTO TempLog2 (GUID, TEMP, HUMI, Time) VALUES (?, ?, ?, ?)',
                (guid, temp, humi, current_time)
            )
            conn.commit()
            
            return {
                "guid": guid,
                "temp": temp,
                "humi": humi,
                "time": current_time
            }
    
    def get_all_records(self) -> List[Dict]:
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM TempLog2 ORDER BY Time DESC')
            records = cursor.fetchall()
            
            return [{
                "guid": record[0],
                "temp": record[1],
                "humi": record[2],
                "time": record[3]
            } for record in records] 