import paho.mqtt.client as mqtt

# MQTT broker details (must match the broker on the Raspberry Pi)
broker = "172.17.0.1"  # Replace with the IP address of your Raspberry Pi or MQTT broker
port = 1883               # Default MQTT port
topic = "sensor/heart_rate"  # The topic to subscribe to

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")

# Create an MQTT client instance
client = mqtt.Client()

# Set callback function for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Subscribe to the topic
client.subscribe(topic)

# Start the loop to listen for incoming messages
client.loop_forever()  # Keeps the script running to wait for messages