# CPU and GPU Performance Monitor

This is a simple, Python web application built with Flask that monitors and displays your system's CPU and GPU performance in real-time.

## Features

*   **CPU Utilization**: Captures and charts the overall CPU usage percentage.
*   **GPU Utilization**: Captures and charts NVIDIA GPU usage and memory consumption (if an NVIDIA GPU and the `pynvml` library are available).
*   **Real-time Dashboard**: Uses Chart.js to display auto-refreshing line charts.
*   **Data Persistence**: Stores up to one hour of performance metrics in a local SQLite database.

## How It Works

The application consists of a few key parts:

*   **`app.py`**: The main Flask backend. It runs two background threads:
    1.  A **collector thread** that fetches CPU and GPU metrics every second and saves them to the database.
    2.  A **cleanup thread** that periodically removes data older than one hour from the database.
    It also serves the main web page and a JSON API endpoint (`/api/metrics`) that the frontend uses to get data.

*   **`db_setup.py`**: A one-time script to create the `metrics.db` SQLite database and the `metrics` table.

*   **`templates/index.html`**: The HTML page that structures the dashboard.

*   **`static/js/main.js`**: The frontend JavaScript that fetches data from the `/api/metrics` endpoint every second and updates the charts.


Follow these steps to get the application running on your local machine.

Set up the database by executing the setup script once to create `metrics.db` database file.

```bash
python db_setup.py
```

Start the Flask server.

```bash
python app.py
```

Application is set to use 8080 port which can be changed in app.py.
