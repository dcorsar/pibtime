import paho.mqtt.client as mqtt
import base64
import json
import time
import ssl

# Define MQTT parameters
broker_address = "soc-broker.rgu.ac.uk"
broker_port = 8883
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
        filename = f"i_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(image_data)

        print(f"Received picture from camera {camera_id} at {time.ctime(timestamp)}")

    except (ValueError, KeyError):
        print(f"Received invalid JSON message: {payload}")

# Set up MQTT client and subscribe to topic
client = mqtt.Client()
client.on_message = on_message
client.username_pw_set("sociot", password="s7ci7tRGU")
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(False)
client.connect(broker_address, port=broker_port)
client.subscribe(picture_topic)

# Start the MQTT client loop
client.loop_forever()
