#include <ArduinoJson.h>

#define SOIL A0
#define LDR A4



void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

void loop() {
  DynamicJsonBuffer jBuffer;
  
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
//    DynamicJsonBuffer jBuffer;
    JsonObject& root = jBuffer.createObject();
    // read the input on analog pin 0:
    float sensorValue = analogRead(SOIL) * (5.0 / 1023.0);
    int ldrValue = analogRead(LDR) * (5.0 / 1023.0);
    // print out the value you read:
    root["soil"] = sensorValue;
    root["ldr"] = ldrValue;
    root.printTo(Serial);
    Serial.println();
  }
}
