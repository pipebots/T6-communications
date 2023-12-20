import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import csv
import os
import time
import serial

class LoRaDataSubscriber(Node):
    def __init__(self):
        super().__init__('lora_data_subscriber')
        self.get_logger().info("LoRa Data Subscriber is initializing...")
        # Specify the path on the SD card where you want to save the CSV file
        #sd_card_path = '~/data'
         # Use os.path.expanduser to expand the tilde to the home directory
        home_directory = os.path.expanduser('~')
        self.csv_file_path = os.path.join(home_directory, 'data/pi_data.csv')
        #self.csv_file_path = os.path.join(sd_card_path, 'pi_data.csv')

        # Create a subscriber to the 'lora_data' topic
        self.subscription = self.create_subscription(
            String,
            'lora_data',
            self.lora_data_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        # Create the CSV file path on the SD card
       

        # Get the directory of the current script
        #script_directory = os.path.dirname(os.path.realpath(__file__))

        # Create the CSV file path in the same directory as the script
        #self.csv_file_path = os.path.join(script_directory, 'lora_data1.csv')

        # Open CSV file for writing
        self.csv_file = open(self.csv_file_path, 'a', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'CPU Temperature', 'Battery Status', 'Blockage Status'])
        #Open serial port for communication with Pycom LoPy4
        #self.serial_port = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

        
    def lora_data_callback(self, msg):
        lora_data = msg.data

        # Example parsing of lora_data (replace this with your actual parsing logic)
        data_parts = lora_data.split(',')
        
        if len(data_parts) >= 3:
            battery_status= data_parts[1]
            cpu_temp = data_parts[0]
            blockage_status=data_parts[2]
            timestamp  = 'Unknown' if len(data_parts) < 4 else data_parts[3]
            
            # Write data to CSV file
            self.csv_writer.writerow([timestamp, cpu_temp, battery_status, blockage_status])
            self.get_logger().info("Data saved to CSV: Timestamp=%s, CPU Temp=%s, Battery Status=%s, Blockage Status=%s" %
                                   (timestamp, cpu_temp, battery_status, blockage_status))

            # Send data to Pycom LoPy4 over serial
            data_to_send = f"{timestamp},{cpu_temp},{battery_status},{blockage_status}\n"
            # Open serial port for communication with Pycom LoPy4
            with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as serial_port:
                serial_port.write(data_to_send.encode('utf-8'))
           # self.serial_port.write(data_to_send.encode('utf-8'))
           # self.serial_port.close()
        else:
            self.get_logger().warning("Received invalid lora_data: %s" % lora_data)

def main(args=None):
    rclpy.init(args=args)
    node = LoRaDataSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()