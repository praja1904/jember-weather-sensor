from flask import Flask, render_template, jsonify
from datetime import datetime
import random
import os
import psycopg2

app = Flask(__name__)

def get_db_connection():
    """Membuat koneksi ke database PostgreSQL menggunakan environment variables."""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "database"),
        database=os.environ.get("DB_NAME", "jember_db"),
        user=os.environ.get("DB_USER", "admin"),
        password=os.environ.get("DB_PASS", "admin123")
    )

def get_sensor_data():
    """Mengambil data sensor simulasi dan data mahasiswa dari database."""
    nim_mhs = "NIM Belum Terhubung"
    nama_mhs = "Nama Belum Terhubung"
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT nama, nim FROM log_sensor ORDER BY id DESC LIMIT 1;")
        row = cur.fetchone()
        if row:
            nama_mhs, nim_mhs = row
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

    return {
        "suhu": round(random.uniform(24.0, 33.0), 1),
        "kelembapan": round(random.uniform(60.0, 90.0), 1),
        "lokasi": "Pemkab Jember",
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S WIB"),
        "status": "ONLINE",
        "nama_mahasiswa": nama_mhs,
        "nim_mahasiswa": nim_mhs
    }

@app.route("/")
def index():
    data = get_sensor_data()
    return render_template("index.html", data=data)

@app.route("/api/sensor")
def api_sensor():
    """Endpoint JSON untuk konsumsi dashboard / IoT gateway."""
    return jsonify(get_sensor_data())

@app.route("/health")
def health():
    """Healthcheck untuk Docker."""
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)