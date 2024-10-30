#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

// WiFi and Firebase credentials
const char *ssid = "Joho";
const char *password = "joanda1234";
const char *serverUrl = "https://smart-bin-capstone-d10-default-rtdb.asia-southeast1.firebasedatabase.app/logv3.json"; // Firebase project ID

const int potensiometerPins[] = {35, 32, 33, 25, 26, 27, 14, 12, 13}; // ADC pins for potentiometers
const int ledPins[] = {23, 22, 21, 19, 18, 5, 4, 2, 15};              // PWM pins for LEDs
const int numPins = 9;                                                // Number of potentiometers and LEDs

int tpsPercentage[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0}; // Array to store the percentage of each potentiometer


void sendRequest(const char *url, String tpsId, int percentage)
{
  // Get the current Unix time (seconds since Jan 1, 1970)
  time_t now = time(nullptr);
  // Round to the previous minute
  now = now - (now % 60);

  // Construct the JSON data with the specified structure
  String jsonData = "{" + tpsId + "/" + String(now) + "/percentage\": " + String(percentage) + "}";

  // Create an HTTPClient instance
  HTTPClient http;

  http.setTimeout(1000000);

  // Specify the URL and begin the connection
  http.begin(url);

  // Specify the content type and send the PUT request
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.PATCH(jsonData);

  // Check the response code and print the result
  if (httpResponseCode > 0)
  {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    // Get the response payload
    String response = http.getString();
    Serial.println("Response: ");
    Serial.println(response);
  }
  else
  {
    Serial.print("Error on sending PATCH: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  // Free resources
  http.end();

}


void connectWifi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void setup()
{
    Serial.begin(9600); // Initialize serial communication at 9600 baud rate

    // Connect to WiFi
    connectWifi();

    for (int i = 0; i < numPins; i++)
    {
        pinMode(ledPins[i], OUTPUT); // Set LED pins as output
    }
}

void loop()
{
    for (int i = 0; i < numPins; i++)
    {
        // Read voltage value from each potentiometer (0-4095)
        int voltageValue = analogRead(potensiometerPins[i]);

        // Map voltage value to PWM duty cycle (0-255)
        int dutyCycle = map(voltageValue, 0, 4095, 0, 255);

        // Calculate percentage for duty cycle (0-100%)
        float dutyCyclePercentage = (voltageValue / 4095.0) * 100;

        // Set LED brightness using PWM
        analogWrite(ledPins[i], dutyCycle);

        // Print the values to the Serial Monitor
        Serial.print("Potentiometer ");
        Serial.print(i);
        Serial.print(" (Pin ");
        Serial.print(potensiometerPins[i]);
        Serial.print("): ");
        Serial.print(nilaiTegangan);
        Serial.print(" -> LED ");
        Serial.print(i);
        Serial.print(" (Pin ");
        Serial.print(ledPins[i]);
        Serial.print("): Duty Cycle = ");
        Serial.print(dutyCyclePercentage, 2);
        Serial.println("%");

        String tpsId = "tps_" + String(i + 1);
        sendRequest(serverUrl, tpsId, dutyCyclePercentage);
    }

    delay(500); // Delay to reduce the number of serial prints
}