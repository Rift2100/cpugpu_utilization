# System Performance Monitor

This is a simple, human-written Python web application built with Flask that monitors and displays your system's CPU and GPU performance in real-time.

## Features

*   **CPU Utilization**: Captures and charts the overall CPU usage percentage.
*   **GPU Utilization**: Captures and charts NVIDIA GPU usage and memory consumption (if an NVIDIA GPU and the `pynvml` library are available).
*   **Real-time Charting**: Uses Chart.js to display dynamic, auto-refreshing line charts.
*   **Data Persistence**: Stores up to one hour of performance metrics in a local SQLite database.
*   **Lightweight**: Built with Flask, it's a small and easy-to-understand application.

## How It Works

The application consists of a few key parts:

*   **`app.py`**: The main Flask backend. It runs two background threads:
    1.  A **collector thread** that fetches CPU and GPU metrics every second and saves them to the database.
    2.  A **cleanup thread** that periodically removes data older than one hour from the database.
    It also serves the main web page and a JSON API endpoint (`/api/metrics`) that the frontend uses to get data.

*   **`db_setup.py`**: A one-time script to create the `metrics.db` SQLite database and the `metrics` table.

*   **`templates/index.html`**: The HTML page that structures the dashboard. It uses Jinja2 templating to conditionally show GPU charts.

*   **`static/js/main.js`**: The frontend JavaScript that fetches data from the `/api/metrics` endpoint every second and updates the charts.

## Getting Started

Follow these steps to get the application running on your local machine.

### Prerequisites

*   Python 3.6+
*   `pip` (Python package installer)

### 1. Install Dependencies

Install the required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

Run the setup script once to create the `metrics.db` database file.

```bash
python db_setup.py
```

### 3. Run the Application

Start the Flask server.

```bash
python app.py
```

You can now view the dashboard by opening your web browser and navigating to **http://127.0.0.1:8080**.