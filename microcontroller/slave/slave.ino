#include <esp_now.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

typedef struct struct_message
{
  int id;
  long sensor[4];
} struct_message;

typedef struct wall_data
{
  int id;
  int filled[4] = {0, 0, 0, 0};
} wall_data;

typedef struct level_message
{
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
const char *ssid = "Joho";
const char *password = "joanda1234";
const char *serverUrl = "https://smart-bin-capstone-d10-default-rtdb.asia-southeast1.firebasedatabase.app/logv3.json"; // Firebase project ID

void sendRequest(const char *url, String tpsId, int wallId, int sensorId, int filled)
{

  // connectWifi();

  // Get the current Unix time (seconds since Jan 1, 1970)
  time_t now = time(nullptr);
  // Round to the previous minute
  now = now - (now % 60);

  // Construct the JSON data with the specified structure
  String jsonData = "{" + tpsId + "/" + String(wallId) + "/" + sensorId + "/" + String(now) + "/filled\": " + String(filled) + "}";

  // Create an HTTPClient instance
  HTTPClient http;

  // Specify the URL and begin the connection
  http.begin(url);

  // Specify the content type and send the PUT request
  http.addHeader("Content-Type", "application/json");
  int httpResponseCode = http.PUT(jsonData);

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
    Serial.println(httpResponseCode);
  }

  // Free resources
  http.end();

  // disconnectWifi();
}

// callback function that will be executed when data is received
void OnDataRecv(const uint8_t *mac_addr, const uint8_t *incomingData, int len)
{
  char macStr[18];
  Serial.print("Packet received from: ");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.println(macStr);
  memcpy(&myData, incomingData, sizeof(myData));

  // Update the structures with the new incoming data
  memcpy(boardsStruct[myData[0].id - 1].sensor, myData[0].sensor, sizeof(myData[0].sensor));
  memcpy(boardsStruct[myData[1].id - 1].sensor, myData[1].sensor, sizeof(myData[1].sensor));

  boardsStruct[myData[0].id - 1].id = myData[0].id;
  boardsStruct[myData[1].id - 1].id = myData[1].id;

  int ids[2] = {myData[0].id - 1, myData[1].id - 1};

  Serial.printf("Board ID %u: \n", myData[0].id);
  for (int i = 0; i < sizeof(boardsStruct[myData[0].id - 1].sensor) / sizeof(boardsStruct[myData[0].id - 1].sensor[0]); i++)
  {
    Serial.printf("Sensor %d value: %d\n", i, boardsStruct[myData[0].id - 1].sensor[i]);
  }
  Serial.printf("Board ID %u: \n", myData[1].id);
  for (int i = 0; i < sizeof(boardsStruct[myData[0].id - 1].sensor) / sizeof(boardsStruct[myData[0].id - 1].sensor[0]); i++)
  {
    Serial.printf("Sensor %d value: %d\n", i, boardsStruct[myData[1].id - 1].sensor[i]);
  }
  Serial.println();

  wallData.tpsId = 1;
  Serial.printf("TPS:\ntpsId: %d\n", wallData.tpsId);
  for (int i = 0; i < 2; i++)
  {
    for (int j = 0; j < 4; j++)
    {
      if (boardsStruct[ids[i]].id == 1)
      {
        if (boardsStruct[ids[i]].sensor[j] < longThreshold)
        {
          wallData.wallStatus[i].filled[j] = 1;
        }
        else
        {
          wallData.wallStatus[i].filled[j] = 0;
        }
      }
      else
      {
        if (boardsStruct[i].sensor[j] < threshold)
        {
          wallData.wallStatus[i].filled[j] = 1;
        }
        else
        {
          wallData.wallStatus[i].filled[j] = 0;
        }
      }
      Serial.printf("Wall Status for wall %d at sensor %d: %d\n", boardsStruct[ids[i]].id, j, wallData.wallStatus[i].filled[j]);
      // sendRequest(serverUrl, String(wallData.tpsId), boardsStruct[ids[i]].id, j, wallData.wallStatus[i].filled[j]);
    }
  }
}

int32_t getWifiChannel(const char *ssid)
{
  if (int32_t n = WiFi.scanNetworks())
  {
    for (int32_t i = 0; i < n; i++)
    {
      if (!strcmp(ssid, WiFi.SSID(i).c_str()))
      {
        return WiFi.channel(i);
      }
    }
  }
}

void connectWifi()
{
  // Connect to Wi-Fi with provided SSID and password
  WiFi.begin(ssid, password, 1);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void disconnectWifi()
{
  WiFi.disconnect();
}

void setup()
{
  Serial.begin(9600);
  delay(1000);

  WiFi.mode(WIFI_STA);

  // wifi_config_t wifi_config;
  // wifi_config.ap.channel =

  int channel = WiFi.channel();

  Serial.println(channel);

  // Print the MAC address in hexadecimal format
  Serial.println(WiFi.macAddress()); // Print MAC address directly

  // disconnectWifi();

  // Initialize ESP-NOW
  Serial.println("\nInitialize ESP-NOW");
  if (esp_now_init() != ESP_OK)
  {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  Serial.println("\nSucessfully Initialize ESP-NOW");

  connectWifi();
  // Synchronize time using NTP server
  configTime(0, 0, "pool.ntp.org", "time.nist.gov"); // Set time server
  Serial.print("Waiting for time synchronization");
  while (!time(nullptr))
  {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("\nTime synchronized");

  channel = WiFi.channel();

  Serial.println(channel);

  Serial.println(WiFi.macAddress()); // Print MAC address directly

  // Register for ESP-NOW receive callback to handle incoming data
  esp_now_register_recv_cb(OnDataRecv);
}

void loop()
{
  delay(1000);
}