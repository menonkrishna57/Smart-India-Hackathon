#include <DHT.h>

const int moisturePin = A0; // Analog pin connected to the soil moisture sensor

void setup() {
  Serial.begin(9600);
  Serial.println("Soil Moisture Sensor Ready!");
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Read the analog value from the sensor (0-1023)
  int sensorValue = analogRead(moisturePin);

  // Convert the analog value (0-1023) to a percentage (0-100).
  // Note: This is a simple linear mapping for demonstration purposes.
  float moisturePercentage = map(sensorValue, 0, 1023, 0, 100);

  // Format the data into a single string for your Python script.
  Serial.print("moisture:");
  Serial.println(moisturePercentage);
}

