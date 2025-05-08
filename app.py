from flask import Flask, request, jsonify
from flask_cors import CORS

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

# ESP32 ส่งข้อมูลมาที่นี่
@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        sensor_data.update(data)
        return jsonify({"message": "Data updated"}), 200
    return jsonify({"message": "No data received"}), 400

# Dashboard เรียกข้อมูลจาก ESP32
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "sensor": sensor_data,
        "control": device_control
    })

# Dashboard ส่งคำสั่งควบคุมมา
@app.route('/control', methods=['POST'])
def control_devices():
    data = request.get_json()
    if data:
        device_control.update(data)
        return jsonify({"message": "Control updated"}), 200
    return jsonify({"message": "No data received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
