import paho.mqtt.client as mqtt
import base64
import json
import time

# Define MQTT parameters
broker_address = "localhost"
picture_topic = "picture"

# Define MQTT callback function
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    try:
        # Parse JSON object from payload
        data = json.loads(payload)
        camera_id = data["camera"]
        picture_data = data["picture"]
        timestamp = int(data["timestamp"])

        # Convert image data from base64
        image_data = base64.b64decode(picture_data)

        # Save image data to file
        filename = f"{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(image_data)

        print(f"Received picture from camera {camera_id} at {time.ctime(timestamp)}")

    except (ValueError, KeyError):
        print(f"Received invalid JSON message: {payload}")

# Set up MQTT client and subscribe to topic
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address)
client.subscribe(picture_topic)

# Start the MQTT client loop
client.loop_forever()
