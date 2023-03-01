import paho.mqtt.client as mqtt
import picamera
import time
import base64
import json
import ssl

# Define MQTT parameters
broker_address = "soc-broker.rgu.ac.uk"
broker_port = 8883
camera_topic = "camera"
picture_topic = "picture"

# Get the device ID from the user
device_id = input("Enter device ID: ")
while not device_id.isnumeric():
    device_id = input("Invalid input. Enter device ID (must be a number): ")
device_id = int(device_id)

# Define MQTT callback function
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode("utf-8"))
    print(payload)
    camera_number = payload["camera"]
    if isinstance(camera_number, int) and int(camera_number) == device_id - 1:
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
        
                # Publish message to camera_topic without the picture data
        data = {
            "camera": device_id,
            "timestamp": current_time
        }
        client.publish(camera_topic, json.dumps(data))


def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        client.subscribe(camera_topic)
        
# Set up MQTT client and subscribe to topic
client = mqtt.Client()
client.username_pw_set("sociot", password="s7ci7tRGU")
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(False)
client.on_message = on_message
client.on_connect = on_connect

client.connect(broker_address,port=broker_port)


# Start the MQTT client loop
client.loop_forever()
