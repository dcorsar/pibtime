 # pibtime

Project for RPis using the RPi camera and MQTT broker to make annimated gifs


# Pi Bullet Time


## User Profiles


##### Developers


The developers wanted to make creating bullet time style effects (as seen in the Matrix movie) accessible to all. They benefit from the system being able to be setup for full remote operation (reducing their costs) or using their services for communication between devices and gif generation (at a small charge to the consumer). Their main interaction with a system is to sell it to users, then periodically update the software, making updates available via a private code distribution platform, which users with a subscription can download. 


##### Amateur Film Makers

Amateur Film Makers would utilise this product as a cheap way to include a bullet time sequence into their movie. They benefit from having all the code already provided, easy setup and use, along with the ability to customise the quality of the images taken by using different camera modules. They purchase the system, follow the instructions on physically setting up the system, load the first RPi which involves providing subscription details if using the developer provided services. Then they load every other device, entering its number (position) in the sequence. When ready to start, they run a script on the first RPi, then wait for the final gif to appear in their mailbox.


## System Design 


The system uses a fog paradigm. Each deployed system is setup as a star topology – with camera devices acting as sensor/actuator nodes, a RPi acting as a gateway node that collects data from the others, uses it, and forwards it via the interent. 


##### Equipment:

**Camera devices nodes**: acting as sensor / actuator nodes at the edge, these can be implemented using a RPi Zero W (https://www.raspberrypi.com/products/raspberry-pi-zero-w/) running the latest Raspberry OS (released Feb 21st 2023). Requires a camera – the RPi Camera Module 2 (https://www.raspberrypi.com/products/camera-module-v2/) is sufficient as it has 8-megapixel sensor, has suitable image resolution (can take high-definition pictures (3280 x 2464 pixel)) for inclusion in HD movies; frequency of taking images is expected to be low (less than 1 per second) which the camera can handle. Will also require a RPi Zero Camera Adapter (https://thepihut.com/products/raspberry-pi-zero-camera-adapter), case, and power supply. 

Each camera device will run a script that asks the user to provide the sequence number of the device, take a picture after the camera device immediately before it has, and upload that image to the sink node. 

**Sink node**: recommended to use a RPi 3B, running Python. This will run a script that asks the user to provide the number of camera devices, receive images from each camera device each of which is stored on the sink node. Once all images have been received, they will be used to generate an animated gif, of each image in sequence. This will then be emailed to the user at an email address the provide.

The sink node broadcasts a wireless network for the Camera Device nodes to connect to. These camera devices are preconfigured to connect to that wireless network. The sink node also runs the MQTT broker (mosquitto) meaning that the camera nodes don’t need access to the Internet. This improves the security of the system. 


WiFi was chosen because, while its very expensive in terms of power resources consumed the devices are plugged in, and the camera devices will likely be close enough to all be able to connect to the same network. However, it does add an extra setup step for users; using Bluetooth Low Energy could be a better solution, and could also make it easier to use battery powerpacks, but makes the programming a bit more complicated. LoRaWAN could be used, but would add too much costs (because those bits are expensive).

Each camera device will communicate with each other and the sink node via MQTT. MQTT is used rather than, for example web sockets because we like MQTT.


MQTT messages containing the picture details will be published to the “picture” topic. Messages containing details of which camera device just took a picture will be published on the “camera” topic.

Messages on the “picture” topic will include a JSON string containing keys: “camera” (value the sequency number of the camera), “picture” (value the base64 encoding of the jpeg image), “timestamp” (timestamp of the date and time the picture was taken). 

The main data collected in the system is the images; these are collected by the sink node, processed, then deleted once the final video (gif) has been generated.

The user has control over the system in terms of defining the sequence number of the camera devices, and email address to send the generated image to.

[todo: insert image of the system design]

## Setup Guide

First setup the sink node (if the node has been setup before you can skip steps 1-6)

**Sink node**

1. Follow instructions at https://www.raspberrypi.com/software/ to install Raspberry Pi OS on to device.
2. Then connect device to monitor, keyboard, mouse, then power.
3. Go through setup wizard to setup the operating system
4. Open a terminal window
5. Install imagemagick following the guide at https://projects.raspberrypi.org/en/projects/timelapse-setup/1
6. Install mosquitto following the guide at https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/
7. Type `git clone https://github.com/dcorsar/pibtime`
8. Type `cd pibtime`
9. Install Paho MQTT library – type `pip install paho-mqtt`
10. Once that is complete, type `python sink_node.py`
11. Provide the requested information

Once the sink node is up and running, you can then setup each camera node. If the node has been setup before, you can skip steps 1-6

**Camera Device**
The camera devices should be deployed similar to the following image - i.e. multiple devices around the thing they are taking pictures of.

![MicrosoftTeams-image (2)](https://user-images.githubusercontent.com/1210289/223456782-33e52b44-d593-41ed-a2b7-b650b09339e4.png)


1. Install camera module following instructions at https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/2
2. Follow instructions at https://www.raspberrypi.com/software/ to install Raspberry Pi OS on to device. 
3. Connect device to a monitor, keyboard, mouse, and power supply
4. Go through setup wizard to setup the operating system
5. Open a terminal window
6. Type git clone https://github.com/dcorsar/pibtime
7. Type cd pibtime
8. Install Paho MQTT library – type `pip install paho-mqtt`
9. Setup all the camera device that are not the first one 
10. Position the camera device so that the camera is pointing at the thing that will be photographed
11. type python `camera_device.py` 
12. Provide the requested information

#### Once all of the cameras have taken all the pictures, go back to the sink node
1.	Press 'ctrl+c' to stop running the script
2.	Then type 'convert -delay 10 -loop 1 i_*.jpg animation.gif' 
3.	After a few moments, the animation.gif will be created containing the gif of all of the files.  
4.	Once its been created type, `rm i_*.jpg` to delete all of the images.

