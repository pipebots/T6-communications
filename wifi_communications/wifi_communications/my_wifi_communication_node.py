#for sharing folder as html page
import rclpy
from std_msgs.msg import String
from rclpy.node import Node
from flask import Flask, render_template, send_from_directory,redirect, url_for
import os
import subprocess
from flask import request

app = Flask(__name__, template_folder='/home/pi/ros2_ws/src/wifi_communications/wifi_communications/templates', static_folder='static')
#app = Flask(__name__, template_folder='/home/pi/ros2_ws/lora_communications/lora_communications/templates', static_folder='static')

class MyNode(Node):
    def __init__(self):
        super().__init__('my_wifi_communication_node')
        qos_profile = rclpy.qos.qos_profile_sensor_data
        self.subscription_folder_path = self.create_subscription(
            String,
            'folder_path_topic',
            self.folder_path_callback,
            qos_profile
        )
        self.subscription_location = self.create_subscription(
            String,
            'location_topic',
            self.location_callback,
            qos_profile
        )
    def location_callback(self, msg):
        location = msg.data
        self.get_logger().info(f"Received location: {location}")

    def folder_path_callback(self, msg):
        folder_path = msg.data
        self.get_logger().info(f"Received folder path: {folder_path}")

        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            app.config['files'] = files  # Store file list in Flask app config
            app.config['folder_path'] = folder_path  # Store folder path in Flask app config
            app.run(host='0.0.0.0', port=8000)
            
     

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
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#for sharing file only
# import rclpy
# from std_msgs.msg import String
# from rclpy.node import Node
# from flask import Flask, send_file
# 
# app = Flask(__name__)
# 
# class MyNode(Node):
#     def __init__(self):
#         super().__init__('my_robot_communication_node')
#         qos_profile = rclpy.qos.qos_profile_sensor_data
#         self.subscription = self.create_subscription(
#             String,
#             'file_path_topic',
#             self.file_path_callback,
#             qos_profile
#         )
# 
#     def file_path_callback(self, msg):
#         file_path = msg.data
#         self.get_logger().info(f"Received file path: {file_path}")
# 
#         if file_path:
#             # Serve the file when requested
#             @app.route('/')
#             def get_file():
#                 return send_file(file_path, as_attachment=True)
# 
#             app.run(host='0.0.0.0', port=8000)
# 
# def main(args=None):
#     rclpy.init(args=args)
#     node = MyNode()
#     rclpy.spin(node)
#     rclpy.shutdown()
# 
# if __name__ == '__main__':
#     main()
# 