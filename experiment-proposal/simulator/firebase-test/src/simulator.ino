#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>


// WiFi and Firebase credentials
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// DHT sensor pin and type
#define DHTPIN 13
#define DHTTYPE DHT22

// Define LED pin
#define led 2

const char* serverUrl = "https://smart-bin-capstone-d10-default-rtdb.asia-southeast1.firebasedatabase.app/test-log.json";  // Firebase project ID


void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}


void sendPostRequest(const char* url, String sensorId, float temperature) {
  // Construct the JSON data
  String jsonData = String("{\"sensorId\":\"") + sensorId + "\", \"temp-value\":" + String(temperature, 2) + "}";

  // Create an HTTPClient instance
  HTTPClient http;

  // Specify the URL and begin the connection
  http.begin(url);

  // Specify the content type and send the POST request
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonData);

  // Check the response code and print the result
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Get the response payload
    String response = http.getString();
    Serial.println("Response: ");
    Serial.println(response);
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
  }

  // Free resources
  http.end();
}

DHT dht(DHTPIN, DHTTYPE);

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  // Sensor data
  String sensorId = "DHT22_Sensor__1";

  // Send the sensor data as a POST request
  sendPostRequest(serverUrl, sensorId, t);


  delay(2000); // Send data every 2 seconds
}
