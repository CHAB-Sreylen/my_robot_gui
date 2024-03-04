#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import tkinter as tk
import threading

class MyGUI():
    def __init__(self):
        self.window_ = tk.Tk()
        self.window_.title("Turtlesim Pose Viewer")

        self.lbl_x = tk.Label(self.window_, text="X:", font=("Arial", 12))
        self.lbl_x.grid(row=0, column=0)
        self.lbl_x_val = tk.Label(self.window_, text="", font=("Arial", 12))
        self.lbl_x_val.grid(row=0, column=1)

        self.lbl_y = tk.Label(self.window_, text="Y:", font=("Arial", 12))
        self.lbl_y.grid(row=1, column=0)
        self.lbl_y_val = tk.Label(self.window_, text="", font=("Arial", 12))
        self.lbl_y_val.grid(row=1, column=1)

        self.lbl_theta = tk.Label(self.window_, text="Theta:", font=("Arial", 12))
        self.lbl_theta.grid(row=2, column=0)
        self.lbl_theta_val = tk.Label(self.window_, text="", font=("Arial", 12))
        self.lbl_theta_val.grid(row=2, column=1)

    def run(self):
        self.window_.mainloop()

class Test(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("pose_subscriber")
        self.gui = gui
        self.pose_sub_ = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )

    def pose_callback(self, msg: Pose):
        self.gui.lbl_x_val.config(text=f"{msg.x:.2f}")
        self.gui.lbl_y_val.config(text=f"{msg.y:.2f}")
        self.gui.lbl_theta_val.config(text=f"{msg.theta:.2f}")

def start_node(gui):
    rclpy.init(args=None)
    node = Test(gui)
    rclpy.spin(node)
    rclpy.shutdown()

def main():
    gui = MyGUI()
    t = threading.Thread(target=start_node, args=(gui,))
    t.start()
    gui.run()

if __name__ == "__main__":
    main()
