
#BS code to be executed on lopy4 connected at the BS
from network import LoRa
import socket
import time
import pycom

# Initialize LoRa in LORA mode
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, sf=7, tx_power=14)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)


# Define destination and relay addresses
src_addr = b'\x01'
dst_addr = b'\x02'

# Function to send data
def send_data(data):
    sent = s.send(dst_addr + data)
    print("Sent data:", data)
    while sent < len(dst_addr + data):
        sent += s.send(dst_addr[sent:])

# Function to receive data
def receive_data():
    try:
        rx_data, rx_port = s.recvfrom(256)
        print("Received data:", rx_data)
        decoded_data = rx_data[len(dst_addr):].decode('utf-8')
        print("Decoded data:", decoded_data)
    except socket.timeout:
        print("Timeout")

# Main loop
while True:
    # Keep LoRa receiver on all the time
    print("LoRa mode - Continuous communication")
    while True:
        # Receive a message
        receive_data()
        
        # Wait before receiving the next message
        time.sleep(5)

    

