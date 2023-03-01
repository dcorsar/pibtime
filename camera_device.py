import paho.mqtt.client as mqtt
import picamera
import time
import base64
import json

# Define MQTT parameters
broker_address = "localhost"
camera_topic = "camera"
picture_topic = "picture"

# Get the device ID from the user
device_id = input("Enter device ID: ")
while not device_id.isnumeric():
    device_id = input("Invalid input. Enter device ID (must be a number): ")
device_id = int(device_id)

# Define MQTT callback function
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    if payload.isnumeric() and int(payload) == device_id - 1:
        # Take a picture with the PiCam module
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)  # Wait for camera to warm up
            camera.capture("image.jpg")
            camera.stop_preview()

        # Convert image to base64
        with open("image.jpg", "rb") as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

        # Add current time to data dictionary
        current_time = time.time()
        data = {
            "camera": device_id,
            "picture": base64_image,
            "timestamp": current_time
        }

        # Publish JSON object with camera ID, picture data, and timestamp
        client.publish(picture_topic, json.dumps(data))

# Set up MQTT client and subscribe to topic
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address)
client.subscribe(camera_topic)

# Start the MQTT client loop
client.loop_forever()
