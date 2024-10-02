void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue0 = analogRead(A0);
  int sensorValue1 = analogRead(A1);
  
  float voltage0 = sensorValue0 * (4.8 / 1023.0);
  float voltage1 = sensorValue1 * (4.8 / 1023.0);
  
  Serial.print(voltage0);
  Serial.print(",");
  Serial.println(voltage1);

  delay(1000);
  
}

