#include "Adafruit_MAX31855.h"

// Define your pin connections
int8_t thermoDO = 12;
int8_t thermoCS = 10;
int8_t thermoCLK = 13;

// Create the thermocouple object
Adafruit_MAX31855 thermocouple(thermoCLK, thermoCS, thermoDO);

void setup() {
  Serial.begin(9600);

  // Ensure the chip is working
  if (!thermocouple.begin()) {
    Serial.println("Could not initialize MAX31855. Check your wiring.");
    while (1);
  }
}

void loop() {
  // Read temperature values
  float tempC = thermocouple.readCelsius();

  // Check for errors
  Serial.println(tempC);
  
  delay(100); // Wait 1 second between readings
}
