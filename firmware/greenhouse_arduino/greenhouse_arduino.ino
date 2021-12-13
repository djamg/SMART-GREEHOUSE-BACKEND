#include "DHT.h"
#include <ArduinoJson.h>

#define SOIL A0
#define LDR A4
#define WATER A1
#define DHTPIN 2 
#define DHTTYPE DHT11 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  DynamicJsonBuffer jBuffer;
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //    DynamicJsonBuffer jBuffer;
    JsonObject& root = jBuffer.createObject();
    float h = dht.readHumidity();
    // Read temperature as Celsius
    float t = dht.readTemperature();
    // read the input on analog pin 0:
    float sensorValue = analogRead(SOIL) * (5.0 / 1023.0);
    int ldrValue = analogRead(LDR) * (5.0 / 1023.0);
    // print out the value you read:
    float sensorValue1 = map(sensorValue, 0,5,100,0);
    root["soil"] = sensorValue1;
    root["water"] = ldrValue;
    root["temperature"] = t;
    root["humidity"] = h;
    root.printTo(Serial);
    Serial.println();
  }
}
