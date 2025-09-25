#include <DHT.h>

const int moisturePin = A0;

void setup() {
  Serial.begin(9600);
  Serial.println("Soil Moisture Sensor Ready!");
}

void loop() {
  delay(2000);

  int sensorValue = analogRead(moisturePin);

  float moisturePercentage = map(sensorValue, 0, 1023, 0, 100);

  Serial.print("moisture:");
  Serial.println(moisturePercentage);
}

