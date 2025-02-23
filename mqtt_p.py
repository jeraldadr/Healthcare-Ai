import paho.mqtt.client as mqtt
import time
import random  # Simulating sensor data (replace with actual sensor code)
import serial

# MQTT broker details
broker = "localhost"  # IP address of the broker or cloud MQTT broker URL
port = 1883           # Default MQTT port
topic = "sensor/heart_rate"  # The topic to publish to

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)  # Subscribe to the topic after connection (optional)

# Create an MQTT client instance
client = mqtt.Client()

# Set callback function for connection
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Start the loop to handle incoming/outgoing messages
client.loop_start()

ser = serial.Serial('/dev/tty/ACM0', 9600, timeout=1)
# Simulating sensor data (replace with actual data from Raspberry Pi sensor)
while True:
    heart_rate = ser.readline().decode('utf-8').strip()
    
    # Publish the sensor data to the topic
    print(f"Publishing data: {heart_rate}")
    client.publish(topic, heart_rate)

    time.sleep(5)  # Wait for 5 seconds before publishing again