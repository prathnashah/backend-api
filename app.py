from flask import Flask, request, jsonify
import pandas as pd
import datetime
import os

app = Flask(__name__)

FILE_NAME = "sensor_data.csv"

# Ensure CSV file exists with proper headers
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["id", "Date", "Time", "Ignition", "Photodiode", "SeatBelt", 
                               "CO", "PIR", "Speed", "Alcohol", "Brake", "Temperature", 
                               "Accident", "Towed", "Location"])
    df.to_csv(FILE_NAME, index=False)

def append_data(data_row):
    """ Append sensor data to CSV """
    try:
        df = pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id", "Date", "Time", "Ignition", "Photodiode", "SeatBelt", 
                                   "CO", "PIR", "Speed", "Alcohol", "Brake", "Temperature", 
                                   "Accident", "Towed", "Location"])
    
    new_df = pd.DataFrame([data_row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)

@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    """ Receive and store sensor data from POST request """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        data_row = {
            "id": len(pd.read_csv(FILE_NAME)) + 1,
            "Date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Ignition": data.get("ignition"),
            "Photodiode": data.get("photodiode"),
            "SeatBelt": data.get("seatbelt"),
            "CO": data.get("co"),
            "PIR": data.get("pir"),
            "Speed": data.get("speed"),
            "Alcohol": data.get("alcohol"),
            "Brake": data.get("brake"),
            "Temperature": data.get("temperature"),
            "Accident": data.get("accident"),
            "Towed": data.get("towed"),
            "Location": data.get("location")
        }

        append_data(data_row)
        return jsonify({"message": "Data stored successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/sensor-data", methods=["GET"])
def get_sensor_data():
    """ Fetch stored sensor data """
    try:
        df = pd.read_csv(FILE_NAME)
        return df.to_json(orient="records"), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
