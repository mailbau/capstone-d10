import requests
import random
import time
import datetime
import json

# WiFi and Firebase credentials
SSID = "Wokwi-GUEST"
PASSWORD = ""  # Not used in this example as we assume direct internet access

# Define the server URL
server_url = "https://smart-bin-capstone-d10-default-rtdb.asia-southeast1.firebasedatabase.app/logv3.json"  # Firebase project ID

# Define the TPS ID (Unique identifier for the root of the JSON object)
tps_id = "TPS_0001-py-server"  # You can change this to any unique identifier you prefer

def send_put_request(url, tps_id, sensor_id, temperature):
    # Get the current Unix time (seconds since Jan 1, 1970)
    now = int(time.time() // 60 * 60)  # Round to the previous minute

    # Construct the JSON data with the specified structure
    json_data = {
        f"{tps_id}/{sensor_id}/{now}/temp-value": round(temperature, 2)
    }

    try:
        # Send the PUT request
        response = requests.patch(url, json=json_data)
        print(f"HTTP Response code: {response.status_code}")

        if response.status_code == 200:
            print("Response:")
            print(response.json())
        else:
            print("Error on sending PUT:", response.text)
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)

def main():
    sensor_id = "DHT22_Sensor__1"
    
    while True:
        # Generate a random temperature value between 15 and 30 degrees Celsius
        random_temperature = random.uniform(15, 30)

        # Send the sensor data as a PUT request
        send_put_request(server_url, tps_id, sensor_id, random_temperature)

        time.sleep(2)  # Send data every 2 seconds

if __name__ == "__main__":
    main()
