#include <DHT.h>

// Define the pin connected to the DHT sensor
#define DHTPIN 2
// Define the type of DHT sensor you are using
#define DHTTYPE DHT11

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 Sensor Ready!");
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Read humidity from the sensor.
  float h = dht.readHumidity();

  // Check if read failed
  if (isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Format the data into a single string for your Python script.
  Serial.print("humidity:");
  Serial.println(h);
}
