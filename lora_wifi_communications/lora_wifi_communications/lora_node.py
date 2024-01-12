import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random

class LoRaNode(Node):
    def __init__(self):
        super().__init__('lora_node')
        self.get_logger().info("LoRa Node is initializing...")

        # publisher to send LoRa data
        self.lora_pub = self.create_publisher(String, 'lora_data', 10)  # publishes on 'lora_data' topic

        # timer for sending CPU temperature every 10 seconds
        self.timer = self.create_timer(10.0, self.send_sensor_data)
        self.get_logger().info("Sending sensor data every 10 seconds...")

    def get_cpu_temp(self):
        # Replace this with code to get the CPU temperature from your system
        cpu_temp = random.uniform(30.0, 80.0)  # Example random CPU temperature
        self.get_logger().info("CPU temperature is {:.2f} C".format(cpu_temp))
        return cpu_temp

    def generate_random_battery_status(self):
        # Generate a random battery status (you can customize this based on your needs)
        battery_statuses = ['Full', 'Charging', 'Discharging']
        return random.choice(battery_statuses)
    def generate_random_blockage_status(self):
        # Generate a random battery status (you can customize this based on your needs)
        blockage_statuses = ['Clear', 'Blockage']
        return random.choice(blockage_statuses)
    def generate_random_location_status(self):
        # Generate a random battery status (you can customize this based on your needs)
        location_statuses = ['Manhole', 'Junction']
        return random.choice(location_statuses)

    def send_sensor_data(self):
        cpu_temp = self.get_cpu_temp()
        battery_status = self.generate_random_battery_status()
        blockage_status = self.generate_random_blockage_status()
        location_status = self.generate_random_location_status()

        message = "{:.2f} C, {}, {}, {}".format(cpu_temp, battery_status,blockage_status,location_status)

        # Log CPU temperature and battery status
        self.get_logger().info(message)

        msg = String()
        msg.data = message
        self.lora_pub.publish(msg)  # Publish the message on the 'lora_data' topic

def main(args=None):
    rclpy.init(args=args)
    node = LoRaNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
