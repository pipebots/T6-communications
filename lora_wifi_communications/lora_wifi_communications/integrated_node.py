import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from flask import Flask, render_template, send_from_directory, redirect, url_for
import os
import subprocess
import threading
import csv
import serial

app = Flask(__name__, template_folder='/home/pi/ros2_ws/src/lora_wifi_communications/lora_wifi_communications/templates', static_folder='static')

class IntegratedNode(Node):
    def __init__(self):
        super().__init__('integrated_node')
        qos_profile = rclpy.qos.qos_profile_sensor_data
        self.lora_subscription = self.create_subscription(
            String,
            'lora_data', # from publisher lora_node.py
            self.lora_data_callback,
            qos_profile
        )
        self.wifi_subscription = self.create_subscription(
            String,
            'location_topic', #from publisher file_publisher.py
            self.location_callback,
            qos_profile
        )
        self.wifi_subscription = self.create_subscription(
            String,
            'folder_path_topic', #from publisher file_publisher.py
            self.folder_path_callback,
            qos_profile
        )
        self.wifi_connected = False  # Flag to track WiFi connection status
        self.locations = ['manhole']

        # Thread for running Flask app
        self.flask_thread = threading.Thread(target=self.run_flask_app, daemon=True)

        # Open CSV file for writing
        home_directory = os.path.expanduser('~')
        self.csv_file_path = os.path.join(home_directory, '/home/pi/Documents/wifi_data/pi_data.csv')
        self.csv_file = open(self.csv_file_path, 'a', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'CPU Temperature', 'Battery Status', 'Blockage Status', 'Location Status'])

#     def run_flask_app(self):
#         app.run(host='0.0.0.0', port=8000)

    def run_flask_app(self):
        self.get_logger().info("Flask thread starting...")
        app.run(host='0.0.0.0', port=8000, threaded=True)
        self.get_logger().info("Flask thread terminated.")


    def location_callback(self, msg):
        location = msg.data
        self.get_logger().info(f"Received location: {location}")
        app.config['location'] = location  # Store location in Flask app config
        
#         if app.config.get('location') == 'manhole' and self.wifi_connected:
#                 if not self.flask_thread.is_alive():
#                     self.flask_thread.start()

        if location in self.locations and not self.wifi_connected:
            # Connect to WiFi (replace 'Hina Nasir GP' and 'hinahina' with actual values of available wifi login and password)
            subprocess.run(['sudo', 'nmcli', 'd', 'wifi', 'connect', 'Hina Nasir GP', 'password', 'hinahina'])
            self.wifi_connected = True
        elif location not in self.locations and self.wifi_connected:
            # Disconnect from WiFi if location is not in 'manhole' and WiFi is connected
            subprocess.run(['sudo', 'nmcli', 'd', 'disconnect'])
            self.wifi_connected = False

    
    def folder_path_callback(self, msg):
        folder_path = msg.data
        self.get_logger().info(f"Received folder path: {folder_path}")

        # Store file list and folder path in Flask app config
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            app.config['files'] = files
            app.config['folder_path'] = folder_path
            # Only run the server if the location is 'manhole' and WiFi is connected
            if app.config.get('location') == 'manhole' and self.wifi_connected:
                if not self.flask_thread.is_alive():
                    self.flask_thread.start()
    def lora_data_callback(self, msg):
        lora_data = msg.data

        data_parts = lora_data.split(',')

        if len(data_parts) >= 4:
            battery_status = data_parts[1]
            cpu_temp = data_parts[0]
            blockage_status = data_parts[2]
            location_status = data_parts[3]
            timestamp = 'Unknown' if len(data_parts) < 5 else data_parts[4]

            # Write data to CSV file
            self.csv_writer.writerow([timestamp, cpu_temp, battery_status, blockage_status, location_status])
            self.get_logger().info(
                "Data saved to CSV: Timestamp=%s, CPU Temp=%s, Battery Status=%s, Blockage Status=%s, Location Status=%s" %
                (timestamp, cpu_temp, battery_status, blockage_status, location_status))

            # Send data to Pycom LoPy4 over serial
            data_to_send = f"{timestamp},{cpu_temp},{battery_status},{blockage_status}, {location_status}\n"
            # Open serial port for communication with Pycom LoPy4
            with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as serial_port:
                serial_port.write(data_to_send.encode('utf-8'))

    def get_flask_data(self):
        return {
            'files': app.config.get('files', []),
            'location': app.config.get('location', 'unknown')
        }

@app.route('/')
def serve_index():
    files = app.config.get('files', [])
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    folder_path = app.config.get('folder_path', '/home/pi/Documents/wifi_data') #default folder ppath
    return send_from_directory(folder_path, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    folder_path = app.config.get('folder_path', '')
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        # After deleting the file, update the file list
        files = os.listdir(folder_path)
        app.config['files'] = files

    return redirect(url_for('serve_index'))

def main(args=None):
    rclpy.init(args=args)
    node = IntegratedNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
