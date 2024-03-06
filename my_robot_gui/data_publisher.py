#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class DataPublisher(Node):
    def __init__(self, gui=None):
        super().__init__("data_publisher")
        self.gui = gui
        self.publisher_ = self.create_publisher(Int32, '/number_topic', 10)
        self.timer_ = self.create_timer(1.0, self.publish_number)
        self.counter = 0

    def publish_number(self):
        msg = Int32()
        msg.data = self.counter
        # self.publisher_.publish(msg)
        # print("Publish Number: ", msg.data)
        self.counter += 1
        # if self.counter > 3:
        #     self.counter = 1       # reset counter if it exceeds 3
        
        if self.gui is not None:
            if self.gui.cw:
                if self.counter > 3:
                    self.counter = 1
            else:
                if self.counter > 6:
                    self.counter = 4
                    
        self.publisher_.publish(msg)
        print("Publish Number: ", msg.data)
                     
def main(args=None):
    rclpy.init(args=args)
    node = DataPublisher()
    rclpy.spin(node)
    rclpy.shutdown()