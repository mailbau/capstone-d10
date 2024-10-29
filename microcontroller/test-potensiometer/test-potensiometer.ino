const int potentiometerPins[2] = {32, 33}; // Pin connected to the potentiometer
const int ledPins[2] = {5, 19}; // Pin connected to the LED

void setup() {
  // Initialize Serial communication
  Serial.begin(9600);

  // Set the LED pin as an output
  for (int i = 0; i<2; i++){
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i<2; i++) {
    // Read the analog input from the potentiometer
    int potValue = analogRead(potentiometerPins[i]);

    // Map the potentiometer values to LED intensity levels
    int ledIntensity = map(potValue, 0, 4095, 0, 255);

    // Control the LED intensity using analogWrite
    analogWrite(ledPins[i], ledIntensity);

    // Print potentiometer values and LED intensity to Serial Monitor
    Serial.print("Potentiometer: ");
    Serial.print(potValue);
    Serial.print(" | LED Intensity: ");
    Serial.println(ledIntensity);
  }
  delay(100); // Add a small delay to avoid flickering in the Serial Monitor
}