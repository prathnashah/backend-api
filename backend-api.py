import datetime
import requests

def append_data(file_name, data_row):
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["id", "Date", "Time", "Ignition", "Photodiode", "SeatBelt", "CO", "PIR", "Speed", "Alcohol", "Brake", "Temperature", "Accident", "Towed"])
    
    new_df = pd.DataFrame([data_row], columns=df.columns)
    df = pd.concat([new_df, df]).reset_index(drop=True)
    df.to_csv(file_name, index=False)

file_name = "sensor_data.csv"
append_data(file_name, sensor_data)

url = "http://localhost:5000/api/sensor-data"
params = {
    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    "time": datetime.datetime.now().strftime("%H:%M:%S"),
    "ignition": sen_ignn,
    "photodiode": sen_ldr,
    "seatbelt": sen_blt,
    "co": sen_co,
    "pir": sen_pir,
    "speed": sen_spd,
    "alcohol": sen_alc,
    "brake": sen_brk,
    "temperature": sen_tem,
    "accident": sen_acc,
    "towed": sen_tow,
    "location": location_1
}
response = requests.post(url, json=params)
print(response.text)
