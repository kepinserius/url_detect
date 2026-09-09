import sqlite3
from api.services.db import DB_PATH

class QuotaManager:
    @staticmethod
    def check_and_increment(api_key: str, max_limit: int = 1000) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT requests_count, tier FROM api_keys WHERE key = ?", (api_key,))
        row = cursor.fetchone()
        
        if not row:
            # If not in enterprise db, fallback to pass
            conn.close()
            return True
            
        count, tier = row
        if count >= max_limit:
            conn.close()
            return False
            
        cursor.execute("UPDATE api_keys SET requests_count = requests_count + 1 WHERE key = ?", (api_key,))
        conn.commit()
        conn.close()
        return True
