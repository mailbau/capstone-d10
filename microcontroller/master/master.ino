#include <esp_now.h>
#include <WiFi.h>

// REPLACE WITH THE RECEIVER'S MAC Address
// 34:5F:45:A9:47:54
uint8_t broadcastAddress[] = {0x34, 0x5F, 0x45, 0xA9, 0x47, 0x54};


const int TRIGGER_PINS[4] = {26, 25, 33, 32};
const int ECHO_PINS[4] = {13, 12, 14, 27};

long distances[4];

typedef struct struct_message {
    int id;
    long sensor[4];
} struct_message;


struct_message myData;


esp_now_peer_info_t peerInfo;


void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nLast Packet Send Status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
 
void setup() {
  Serial.begin(9600);

  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);

  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Failed to add peer");
    return;
  }

  // Initialize the pins for all 4 sensors
  for (int i = 0; i < 4; i++) {
    pinMode(TRIGGER_PINS[i], OUTPUT);
    pinMode(ECHO_PINS[i], INPUT);
  }

}
 
void loop() {
  // Set values to send
  myData.id = 2;
  for (int i = 0; i < 4; i++) {
    distances[i] = measureDistance(TRIGGER_PINS[i], ECHO_PINS[i]);
    
    // Print the measured distance
    Serial.print("Sensor ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(distances[i]);
    Serial.println(" cm");

    myData.sensor[i] = distances[i];
    
    delay(100); // Small delay to avoid flooding the serial output
  }

  // Send message via ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &myData, sizeof(myData));
   
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }
  delay(1000);
}

long measureDistance(int triggerPin, int echoPin) {
  // Send a 10µs pulse to trigger the sensor
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  
  // Measure the echo pulse duration
  long duration = pulseIn(echoPin, HIGH);
  
  // Convert the duration to distance in cm
  long distance = duration * 0.0343 / 2;
  
  return distance;
}