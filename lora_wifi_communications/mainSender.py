#pycom lopy4 code to be executed on the sender attached to the Rasberrypi4 
import machine
from machine import UART
from network import LoRa
import socket
import time

# Configure the UART
uart = machine.UART(0, baudrate=9600)

# Configure LoRa
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


while True:
    # Read data from serial
    serial_data = uart.readline()

    if serial_data:
        # Parse the received data 
        data_parts = serial_data.decode('utf-8').strip().split(',')
        
        if len(data_parts) >= 5:
            timestamp, cpu_temp, battery_status, blockage_status, location_status = data_parts
            
            # Print received data 
            print("Received Data: Timestamp={}, CPU Temp={}, Battery Status={}, Blockage Status={}, Location Status={}".format(
                timestamp, cpu_temp, battery_status, blockage_status, location_status))

            # Send data over LoRa
            lora_data = "{},{},{},{},{}".format(timestamp, cpu_temp, battery_status, blockage_status, location_status)
            s.send(lora_data)
            print(lora_data)

    time.sleep(1)  # Adjust sleep duration as needed
