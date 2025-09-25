#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 Sensor Ready!");
  dht.begin();
}

void loop() {
  delay(2000);

  float h = dht.readHumidity();

  if (isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print("humidity:");
  Serial.println(h);
}
