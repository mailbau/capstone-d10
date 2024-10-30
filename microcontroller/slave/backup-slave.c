#include <esp_now.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
// #include <WiFiClientSecure.h>

const char* rootCA = \
"-----BEGIN CERTIFICATE-----\n" \
"MIIFVzCCBD+gAwIBAgIQfR+V4jASgIoNfoPQ/u6aDjANBgkqhkiG9w0BAQsFADA7\n" \
"MQswCQYDVQQGEwJVUzEeMBwGA1UEChMVR29vZ2xlIFRydXN0IFNlcnZpY2VzMQww\n" \
"CgYDVQQDEwNXUjEwHhcNMjQxMDAxMTczODQzWhcNMjQxMjMwMTczODQyWjAxMS8w\n" \
"LQYDVQQDDCYqLmFzaWEtc291dGhlYXN0MS5maXJlYmFzZWRhdGFiYXNlLmFwcDCC\n" \
"ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALjrgimWpAj7aQt/qPUp7cuq\n" \
"8neQBarUGCWxhvE/sCjgg6xdqtt/OsDF5oOo7726NNLS6jIY3Fsha1zCevAdFjxP\n" \
"VhgMY9ZVzufTkrbXJRMnUxR0lD5fQfXAtj/3gIT3JurhL6/gXzUdxz44BUTC6S0L\n" \
"12/DcNtsd6SXhia/TcW62Q1ViU2x3aYTxTNPRC7FN1J63iPxzeznoZTC6QdnMzEA\n" \
"qfemYc9M9OOPtbDrClsnHp8zMat2szt6ALlzw32wSQnA1m6C2xI3ryY5ZUi1Rud8\n" \
"32xBVPLKaUkmtdvY1QBBzDSuAmwt7gF/KHIsgSNRt73p3l5YH9FUJkmgsQnkjKsC\n" \
"AwEAAaOCAl8wggJbMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcD\n" \
"ATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBTxqJQY0aGJQ7fV/KwGlP08eYcvjTAf\n" \
"BgNVHSMEGDAWgBRmaUnU3iqckQPPiQ4kuA4wA26ILjBeBggrBgEFBQcBAQRSMFAw\n" \
"JwYIKwYBBQUHMAGGG2h0dHA6Ly9vLnBraS5nb29nL3Mvd3IxL2ZSODAlBggrBgEF\n" \
"BQcwAoYZaHR0cDovL2kucGtpLmdvb2cvd3IxLmNydDAxBgNVHREEKjAogiYqLmFz\n" \
"aWEtc291dGhlYXN0MS5maXJlYmFzZWRhdGFiYXNlLmFwcDATBgNVHSAEDDAKMAgG\n" \
"BmeBDAECATA2BgNVHR8ELzAtMCugKaAnhiVodHRwOi8vYy5wa2kuZ29vZy93cjEv\n" \
"dXE4NktKd18ydFEuY3JsMIIBBAYKKwYBBAHWeQIEAgSB9QSB8gDwAHYA2ra/az+1\n" \
"tiKfm8K7XGvocJFxbLtRhIU0vaQ9MEjX+6sAAAGSSWCnfAAABAMARzBFAiBdsNJR\n" \
"ijSs1puY2OH9VkMRzmmC3YQXyJBjAg8qECOSuwIhAI+j7hPqDCMTEJRnxkD3Ctoo\n" \
"ETuzioHPFEsRRqNojcPoAHYAdv+IPwq2+5VRwmHM9Ye6NLSkzbsp3GhCCp/mZ0xa\n" \
"OnQAAAGSSWCncQAABAMARzBFAiEArD7Tw+3BSwh4Wk0DnRGjAjh88GRL8CGDmVZw\n" \
"TQQRjMwCID4DRPi2WKmDuYtWgqIkz/7pVVbncshrt1yaZhVRPBYtMA0GCSqGSIb3\n" \
"DQEBCwUAA4IBAQCvJEAzSIzADkb6vEXHMca1FR1SkS2vo6+rinmPWXuh6kVs8N3h\n" \
"G6jcTnr4xnbcucZPmnVWUTBg/Q38vtMuIjz+6k3OemTCC8FtfbeM2CPafDAgJF58\n" \
"6zuhL+8qNBgQDR/EWOFgP36pDy6uU4f4rR5LJJ8/wYBlq/B7v3H7Ueseog0lUia3\n" \
"LneZSgmCx38Wu66aUbRMTbIeTbF4LJrCRU+a91PllNDxdjwrLJ9VhbcrzBbIkdD9\n" \
"TiVHnBVizZPZxGOBiP4mTiSO9DjKAmHIs6J1Fgoq9ThK3JRug9SUA70An6JoNxsQ\n" \
"5jHkEILCYvfrAJbqsjX3jL+0ciaFMEmr8glS\n" \
"-----END CERTIFICATE-----\n";

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

// WiFi and Firebase credentials
const char* ssid = "Joho";
const char* password = "joanda1234";
const char* serverUrl = "https://smart-bin-capstone-d10-default-rtdb.asia-southeast1.firebasedatabase.app/logv3.json";  // Firebase project ID
const char* url = "http://128.199.138.69:5001";
IPAddress dns(8,8,8,8);

bool sendHttp = false;
int idToSend[2];

void sendRequest(const char* url, String tpsId, int wallId, int sensorId, int filled) {

  // connectWifi();

  // Get the current Unix time (seconds since Jan 1, 1970)
  time_t now = time(nullptr);
  // Round to the previous minute
  now = now - (now % 60);

  // Construct the JSON data with the specified structure
  // String jsonData = "{" + tpsId + "/" + String(wallId) + "/" + sensorId + "/" + String(now) + "/filled\": " + String(filled) + "}";
  String jsonData = "{\"destination_url\": \"" + String(serverUrl) + "\", \"method\": \"" + "POST" + "\", \"" + tpsId + "/" + String(wallId) + "/" + sensorId + "/" + String(now) + "/filled\": " + String(filled) + "}";

  // Create an HTTPClient instance
  HTTPClient http;
  http.setTimeout(1000000);
  // http.setReuse(false);
  WiFiClientSecure *client = new WiFiClientSecure;
  client -> setCACert(rootCA);
  // client.setInsecure();

  // Specify the URL and begin the connection
  http.begin(url);
  // http.begin(*client, url);


  // Specify the content type and send the PUT request
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
    Serial.print("Error on sending PATCH: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  // Free resources
  http.end();

  // disconnectWifi();
}


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
  
  for (int i = 0; i < 2; i++) {
    idToSend[i] = myData[i].id-1;
  } 
  


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
      if (boardsStruct[idToSend[i]].id == 1) {
        if (boardsStruct[idToSend[i]].sensor[j] < longThreshold) {
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
      Serial.printf("Wall Status for wall %d at sensor %d: %d\n", boardsStruct[idToSend[i]].id, j, wallData.wallStatus[i].filled[j]);
      // sendRequest(url, String(wallData.tpsId), boardsStruct[idToSend[i]].id, j, wallData.wallStatus[i].filled[j]);
    }
  }
  sendHttp = true;

}

int32_t getWifiChannel(const char *ssid) {
  if (int32_t n = WiFi.scanNetworks()) {
    for (int32_t i = 0; i < n; i++) {
      if (!strcmp(ssid, WiFi.SSID(i).c_str())) {
        return WiFi.channel(i);
      }
    }
  }
}

void connectWifi() {

  // if (!WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE, dns)) {
  //   Serial.println("Failed to set DNS");
  // }
  // Connect to Wi-Fi with provided SSID and password
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void disconnectWifi() {
  WiFi.disconnect();
}
 
void setup() {
  Serial.begin(9600);
  delay(1000);

  WiFi.mode(WIFI_STA);

  // wifi_config_t wifi_config;
  // wifi_config.ap.channel = 

  connectWifi();

  int channel = WiFi.channel();

  // Synchronize time using NTP server
  configTime(0, 0, "pool.ntp.org", "time.nist.gov"); // Set time server
  Serial.print("Waiting for time synchronization");
  while (!time(nullptr)) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nTime synchronized");

  // disconnectWifi();

  // Initialize ESP-NOW
  Serial.println("\nInitialize ESP-NOW");
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  Serial.println("\nSucessfully Initialize ESP-NOW");


  // wifi_config_t wifiConfig;
  // wifiConfig.ap.channel = WiFi.channel();

  // // Set the AP configuration
  // esp_wifi_set_config(ESP_IF_WIFI_AP, &wifiConfig);

  // Register for ESP-NOW receive callback to handle incoming data
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {
  if (sendHttp) {
    for (int i = 0; i < 2; i++) {
      for (int j = 0; j < 4; j++) {
        sendRequest(url, String(wallData.tpsId), boardsStruct[idToSend[i]].id, j, wallData.wallStatus[i].filled[j]);
      }
    sendHttp = false;
  }
  }
  delay(1000);  
}