#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import tkinter as tk
import threading

class MyGUI():
    def __init__(self):
        self.window_ = tk.Tk()
        self.lbl_ = tk.Label(self.window_, text="", font=("Arial", 48))
        self.lbl_.pack()
    
    def run(self):
        self.window_.mainloop()

class PoseSubscriberNode(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("pose_subscriber")
        self.gui = gui
        self.pose_sub_ = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )
        self.get_logger().info("Draw Circle Node has been started!")
            
    def pose_callback(self, msg: Pose):
        msg_str = "x: %.2f\ny: %.2f" % (msg.x, msg.y)
        #self.get_logger().info(msg_str)
        self.gui.lbl_.config(text=msg_str)
        #print(msg_str)

def start_node(gui):
    rclpy.init(args=None)
    node = PoseSubscriberNode(gui)
    rclpy.spin(node)
    rclpy.shutdown()

def main():
    gui = MyGUI()
    t = threading.Thread(target=start_node, args=(gui,))
    t.start()
    gui.run()
