#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from my_robot_gui.msg import Data  # Import your custom message type

class DataPublisher(Node):
    def __init__(self, gui=None):
        super().__init__("data_publisher")
        self.gui = gui
        self.publisher_ = self.create_publisher(Data, '/number_topic', 10)
        self.timer_ = self.create_timer(1.0, self.publish_number)
        self.counter = 0

    def publish_number(self):
        msg = Data()
        
        # You can modify the attributes here as needed
        msg.start = True
        msg.retry = False
        msg.team_color = "blue"  # Example modification
        
        self.publisher_.publish(msg)
        self.get_logger().info("Publish Number: %s %s %s" % (msg.start, msg.retry, msg.team_color))
                     
def main(args=None):
    rclpy.init(args=args)
    node = DataPublisher()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
