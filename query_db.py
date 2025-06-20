import sqlite3
import json

DB_PATH = 'trackiq.db'

def print_all_audio_features():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM audio_features')
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        record = dict(zip(columns, row))
        print(json.dumps(record, indent=2))
    conn.close()

if __name__ == '__main__':
    print_all_audio_features() 