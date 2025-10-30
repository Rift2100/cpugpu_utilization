import sqlite3

connection = sqlite3.connect('metrics.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu_utilization REAL NOT NULL,
        gpu_utilization REAL,
        gpu_memory_used REAL
    )
''')

print("Database table 'metrics' is ready.")

connection.commit()
connection.close()
