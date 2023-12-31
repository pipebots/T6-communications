**Overview**
This lora_communications contains a ROS2 node designed to facilitate communication over LoRa 868 MHz. The node subscribes to various pieces of information, including sensor data, battery status, and blockage information. This information is then transmitted to a ground station. The LoRa communication is established using a Pycom LoPy4 device connected to a Raspberry Pi 4 via a USB port.

**Requirements**
To set up the communication system, you will need the following hardware components:

2 Pycom LoPy4 or FiPy devices
2 pycom Expansion Boards 3.0
Raspberry Pi 4 with ROS2 installed
1 PC for base station monitoring

**Setup Instructions**
Connect the Raspberry Pi 4 to the LoPy4 device using a USB cable. Ensure that the correct port (in this code, it is assumed to be ttyACM0) is used.

Connect the LoPy4 device to the PC or laptop located at the ground station.

Save the code in the file mainSender.py to the main.py file of the LoPy4 connected to the Raspberry Pi 4.

Save the code in the file mainBS.py to the main.py file of the LoPy4 connected to the laptop or PC, which functions as the base station.

**Running the System**
The ROS2 package lora_communications includes two nodes:

lora_node: This node is responsible for publishing information.
lora_receiver_node: This node subscribes to the information published by the lora_node.
Follow these steps to run the system:

Execute both the lora_node and lora_receiver_node.
The LoPy4 attached to the Raspberry Pi will start receiving data on the serial port and send it to another LoPy4 connected to the PC.

**Notes**
Make sure that the appropriate COM port is configured in the code (e.g., ttyACM0). Adjust this value if necessary.
Ensure that the ROS2 setup on the Raspberry Pi is properly configured.
Monitor the communication system using a PC connected as the base station.
Feel free to reach out for any issues or improvements. 
