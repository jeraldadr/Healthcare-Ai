#include "BioSensor.h"

void initBioSensor(SparkFun_Bio_Sensor_Hub &bioHub) {
  int result = bioHub.begin();
  if (result == 0) // Zero errors!
    Serial.println("BioSensor started!");
  else
    Serial.println("Could not communicate with the BioSensor!");
 
  Serial.println("Configuring BioSensor...."); 
  int error = bioHub.configBpm(MODE_ONE); // Configuring just the BPM settings. 
  if(error == 0){ 
    Serial.println("BioSensor configured.");
  }
  else {
    Serial.println("Error configuring sensor.");
    Serial.print("Error: "); 
    Serial.println(error); 
  }

  Serial.println("Loading up the buffer with data....");
  delay(4000); 
}

bioData readBioData(SparkFun_Bio_Sensor_Hub &bioHub) {
    bioData body = bioHub.readBpm();
    return body; 
}

bool receiveValidData(bioData &body) {
  if (body.status == 3) {
    // These constraints set arbitrary based on the test data received
    if (body.heartRate > 50 && body.confidence > 90 && body.oxygen > 90)
      Serial.println("Received Valid Bio Data!");
      return true;
  }
  return false;
}

