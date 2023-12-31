import rclpy
from std_msgs.msg import String
from rclpy.node import Node

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_folder_path = self.create_publisher(String, 'folder_path_topic', 10)
        self.publisher_location = self.create_publisher(String, 'location_topic', 10)
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        # Publish the file path to folder_path_topic
        folder_path_msg = String()
        folder_path_msg.data = '/home/pi/Documents/wifi_data'
        self.publisher_folder_path.publish(folder_path_msg)

        # Publish the location to location_topic
        location_msg = String()
        location_msg.data = 'manhole'  # You can change this value based on your requirements
        self.publisher_location.publish(location_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
