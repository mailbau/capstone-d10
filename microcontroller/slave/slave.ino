#include <esp_now.h>
#include <WiFi.h>



typedef struct struct_message {
    int id;
    long sensor[4];
} struct_message;

typedef struct wall_data {
    int id;
    int filled[4] =  {0, 0, 0, 0};
} wall_data;


typedef struct level_message {
  int tpsId;
  wall_data wallStatus[2];
} level_message;

// Create a struct_message called myData
struct_message myData[2];

// Create an array with all the structures
struct_message boardsStruct[4];

level_message wallData;

const long threshold = 3;
const long longThreshold = 20;


// callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac_addr, const uint8_t *incomingData, int len) {
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));

  // Update the structures with the new incoming data
  memcpy(boardsStruct[myData[0].id-1].sensor, myData[0].sensor, sizeof(myData[0].sensor));
  memcpy(boardsStruct[myData[1].id-1].sensor, myData[1].sensor, sizeof(myData[1].sensor));

  boardsStruct[myData[0].id-1].id = myData[0].id;
  boardsStruct[myData[1].id-1].id = myData[1].id;


  Serial.printf("Board ID %u: \n", myData[0].id);
  for (int i = 0; i < sizeof(boardsStruct[myData[0].id-1].sensor) / sizeof(boardsStruct[myData[0].id-1].sensor[0]); i++) {
    Serial.printf("Sensor %d value: %d\n", i, boardsStruct[myData[0].id-1].sensor[i]);
  }
  Serial.printf("Board ID %u: \n", myData[1].id);
  for (int i = 0; i < sizeof(boardsStruct[myData[0].id-1].sensor) / sizeof(boardsStruct[myData[0].id-1].sensor[0]); i++) {
    Serial.printf("Sensor %d value: %d\n", i, boardsStruct[myData[1].id-1].sensor[i]);
  }
  Serial.println();

  wallData.tpsId = 1;
  Serial.printf("TPS:\ntpsId: %d\n", wallData.tpsId);
  for (int i = 0; i < 2; i++) {
    for (int j = 0; j < 4; j++) {
      if (boardsStruct[i].id == 1) {
        if (boardsStruct[i].sensor[j] < longThreshold) {
          wallData.wallStatus[i].filled[j] = 1;
        } else {
          wallData.wallStatus[i].filled[j] = 0;
        }
      } else {
        if (boardsStruct[i].sensor[j] < threshold) {
          wallData.wallStatus[i].filled[j] = 1;
        } else {
          wallData.wallStatus[i].filled[j] = 0;
        }
      }
      Serial.printf("Wall Status for wall %d at sensor %d: %d\n", boardsStruct[i].id, j, wallData.wallStatus[i].filled[j]);
    }
  }

}

 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(9600);
  
  //Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  
  // Once ESPNow is successfully Init, we will register for recv CB to
  // get recv packer info
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
}
 
void loop() {
  delay(1000);  
}