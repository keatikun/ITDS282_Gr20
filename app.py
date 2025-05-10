from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ตัวแปรเก็บค่าจาก Node-RED
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "light": 0.0
}

# หน้า Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html', data=sensor_data)

# รับข้อมูลจาก Node-RED
@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    if data:
        sensor_data.update(data)
        return jsonify({"message": "Data updated"}), 200
    return jsonify({"message": "No data received"}), 400

# Dashboard ขอข้อมูล (ใช้กรณี AJAX ดึง)
@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)
