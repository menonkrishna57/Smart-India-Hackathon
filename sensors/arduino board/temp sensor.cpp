const int tempPin = A0; // Analog pin connected to the TMP36's signal pin

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
  Serial.println("TMP36 Sensor Ready!");
}

void loop() {
  // Read the analog voltage value from the sensor (0-1023)
  int sensorValue = analogRead(tempPin);

  // Convert the analog value (0-1023) to voltage (0-5V)
  float voltage = sensorValue * (5.0 / 1023.0);

  // Convert the voltage to temperature in Celsius
  // The TMP36 outputs 0.75V at 25C and changes by 10mV per degree Celsius
  float temperatureC = (voltage - 0.5) * 100;

  // Convert Celsius to Fahrenheit
  float temperatureF = (temperatureC * 9/5) + 32;

  // Format the data and send it to the serial port
  Serial.print("temp_C:");
  Serial.print(temperatureC);
  Serial.print(",temp_F:");
  Serial.println(temperatureF);

  // Wait 2 seconds before the next reading
  delay(2000);
}
