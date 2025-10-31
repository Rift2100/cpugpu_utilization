
import sqlite3
import time
import psutil #It will help get the CPU utilization
from threading import Thread, Lock
from flask import Flask, render_template, jsonify

try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetMemoryInfo #For NVIDIA GPUs, For AMD need to get the hardware and test
    nvmlInit()
    MONITOR_GPU = True
    print("GPU monitoring is enabled.")
except Exception as e:
    MONITOR_GPU = False
    print(f"GPU monitoring is disabled. Reason: {e}")


app = Flask(__name__)

db_lock = Lock()

def get_db_connection():
    conn = sqlite3.connect('metrics.db')
    conn.row_factory = sqlite3.Row
    return conn

def collect_metrics():
    print("Starting metrics collection thread...")
    while True:
        cpu_percent = psutil.cpu_percent()

        gpu_percent = None
        gpu_mem_used = None
        if MONITOR_GPU:
            try:
                handle = nvmlDeviceGetHandleByIndex(0)
                util = nvmlDeviceGetUtilizationRates(handle)
                mem = nvmlDeviceGetMemoryInfo(handle)
                gpu_percent = util.gpu
                gpu_mem_used = mem.used / (1024**2)
            except Exception as e:
                print(f"Could not retrieve GPU stats: {e}")

        #making sure we are not using database for anything. 
        with db_lock:
            conn = get_db_connection()
            conn.execute(
                'insert into metrics (cpu_utilization, gpu_utilization, gpu_memory_used) values (?, ?, ?)',
                (cpu_percent, gpu_percent, gpu_mem_used)
            )
            conn.commit()
            conn.close()

        time.sleep(1) #sleep for 1 second before collecting next data

#Clenaing DB every 5 minutes
def cleanup_old_data():
    print("Starting database cleanup thread...")
    while True:
        with db_lock:
            conn = get_db_connection()
            conn.execute("delete from metrics where timestamp <= datetime('now', ?)", ('-' + str(3600) + ' seconds',))
            conn.commit()
            remaining_rows = conn.execute('select count(*) from metrics').fetchone()[0]
            print(f"Database cleanup complete. {remaining_rows} records remaining.")
            conn.close()
        time.sleep(300) # Wait 5 minutes before cleaning old data

@app.route('/')
def index():
    return render_template('index.html', gpu_enabled=MONITOR_GPU) # GPU_enabled indicates if the graph should be shown on UI or not

@app.route('/api/metrics')
def get_metrics():
    conn = get_db_connection()
    metrics = conn.execute('select * from metrics order by timestamp desc limit 60').fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in reversed(metrics)])

if __name__ == '__main__':
    collector_thread = Thread(target=collect_metrics, daemon=True)
    collector_thread.start()

    cleanup_thread = Thread(target=cleanup_old_data, daemon=True)
    cleanup_thread.start()

    print("Starting Flask server on http://127.0.0.1:8080")
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
