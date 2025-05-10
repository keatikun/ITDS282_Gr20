from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ตัวแปรสถานะระบบ
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "light": 0.0,
    "system_status": True
}

device_control = {
    "led": False,
    "buzzer": False,
    "system_enabled": True
}

# หน้า Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ESP32 ส่งข้อมูลมา
@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        sensor_data.update(data)
        return jsonify({"message": "Data updated"}), 200
    return jsonify({"message": "No data received"}), 400

# Dashboard ดึงข้อมูล
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "sensor": sensor_data,
        "control": device_control
    })

# Dashboard ควบคุมอุปกรณ์
@app.route('/control', methods=['POST'])
def control_devices():
    data = request.get_json()
    if data:
        # Forward ไปยัง Node-RED แทน
        try:
            r = requests.post("http://192.168.1.54:1880/nodered/control", json=data)
            return jsonify({"message": "Forwarded to Node-RED"}), r.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"message": "No data received"}), 400

@app.route('/sync', methods=['POST'])
def sync_all():
    data = request.get_json()
    if data:
        sensor_data.update(data.get("sensor", {}))
        device_control.update(data.get("control", {}))
        return jsonify({"message": "Synced"}), 200
    return jsonify({"message": "No data received"}), 400



if __name__ == '__main__':
    app.run(debug=True)
