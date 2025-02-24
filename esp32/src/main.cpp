#include <Arduino.h>
#include <stdio.h>
#include <ArduinoJson.h>

// // Sensors

#include "BioSensor.h"


// Cloud Connection



// Reset pin, MFIO pin, Buzzer pin
const int resPin = 37;
const int mfioPin = 38;
const int ledPin = 25;

// Sensors
SparkFun_Bio_Sensor_Hub bioHub(resPin, mfioPin); // Biosensor


// cloud 
// variable for logic control and calibration
bool calibrated = false;
unsigned long sittingTime = 0;
unsigned long heartRateSum = 0;
unsigned long oxygenSum = 0;
unsigned int heartRateCount = 0;
float averageHeartRate = 0; 
float averageOxygen = 0;
bool valid = false;
float min_X = 0;
float max_X = 0;

void setup(){
  
  int trigger = 0;
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);  

  Wire.begin();

  initBioSensor(bioHub);

  sittingTime = millis(); // initialize the timestamp
 
}

void loop(){ 
 


    if (Serial.available() > 0) {  // Check if data is available
        String receivedData = Serial.readString();  // Read full incoming strin
        if (receivedData == "ready"){
        trigger = 1
    digitalWrite(ledPin, HIGH);}}

    bioData body = readBioData(bioHub); // biosensor needs 5-10s to start updating   
    if (trigger == 1) {
    // These constraints set arbitrary based on the test data received
      if (body.heartRate > 40 && body.confidence > 40 && body.oxygen > 70){
        if (body.status == 3){
        // Create JSON
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["Heartrate"] = body.heartRate;
        jsonDoc["Oxygen"] = body.oxygen;

        String json_str;
        serializeJson(jsonDoc, json_str); 
        Serial.print(json_str);
        digitalWrite(ledPin, LOW);
        trigger = 0;
        }
      }
    }
    unsigned long elapsedTime = (millis() - sittingTime) / 1000;

    // display the sitting time on the screen
    // once the user is not on the object

      // averageHeartRate = (heartRateCount > 0) ? (float)heartRateSum / heartRateCount : 0;
      // averageOxygen = (heartRateCount > 0) ? (float)oxygenSum / heartRateCount : 0;
      // Serial.print("Average Heart Rate: ");
      // Serial.print(averageHeartRate, 2); 
      // Serial.println(" bpm");
      // Serial.print("Average Oxygen: ");
      // Serial.print(averageOxygen, 2); 
      // Serial.println(" lpm");
      // Serial.print("Sitting Time: ");
      // Serial.print(elapsedTime);
      // Serial.println(" s");


      // Publish the averages to MQTT

      delay(1000);

      // Reset for next session
      heartRateSum = 0;
      oxygenSum = 0;
      heartRateCount = 0;
    }
  

