#include <WiFi.h>

#define SSID "Joho"
#define pw "Joanda1234"

const int potensiometerPins[] = {35, 32, 33, 25, 26, 27, 14, 12, 13}; // ADC pins for potentiometers
const int ledPins[] = {23, 22, 21, 19, 18, 5, 4, 2, 15};              // PWM pins for LEDs
const int numPins = 9;                                                // Number of potentiometers and LEDs

void setup()
{
    Serial.begin(9600); // Initialize serial communication at 9600 baud rate

    // Connect to WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");

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
        int nilaiTegangan = analogRead(potensiometerPins[i]);

        // Map voltage value to PWM duty cycle (0-255)
        int dutyCycle = map(nilaiTegangan, 0, 4095, 0, 255);

        // Calculate percentage for duty cycle (0-100%)
        float dutyCyclePercentage = (nilaiTegangan / 4095.0) * 100;

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
        Serial.print(dutyCyclePercentage, 1); // Print percentage with 1 decimal place
        Serial.println("%");
    }

    delay(500); // Delay to reduce the number of serial prints
}