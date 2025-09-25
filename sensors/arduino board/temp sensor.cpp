const int tempPin = A0;

void setup() {
  Serial.begin(9600);
  Serial.println("TMP36 Sensor Ready!");
}

void loop() {
  int sensorValue = analogRead(tempPin);

  float voltage = sensorValue * (5.0 / 1023.0);

  float temperatureC = (voltage - 0.5) * 100;

  float temperatureF = (temperatureC * 9/5) + 32;

  Serial.print("temp_C:");
  Serial.print(temperatureC);
  Serial.print(",temp_F:");
  Serial.println(temperatureF);

  delay(2000);
}
