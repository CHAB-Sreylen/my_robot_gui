import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import String
import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32
# from .data_publisher import DataPublisher
# from .draw_circle import DrawCircleNode
from rclpy.executors import MultiThreadedExecutor

class MyGUI:
    def __init__(self, data_publisher_node=None):
        # self.node = None
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title('Tkinter Frame Example')
        
        self.frame_location = "Location"
        self.create_frame(323, 230, 30, 100, self.frame_location)
        
        self.label = tk.Label()
        self.label.place(x=50, y=150)
        # text_label(self, text, bg, x, y, var):
        self.text = "Hello"
        self.text_label(self.text, "red", 50, 150, "X")
        
        # self.label_text = tk.StringVar()
        # self.label = tk.Label(self.root, textvariable=self.label_text)
        # self.label.pack()

        # self.init_ros()
        # self.location_x_value = 1.04
        # self.location_x_bg = "white"
        # self.text_label(self.location_x_value,self.location_x_bg, 50, 150, "X")
        

    def run(self):
        self.root.mainloop()

    def create_frame(self, width, height, x, y, title):
        frame = tk.Frame(self.root, width=width, height=height, bg='white')
        frame.pack_propagate(False)  # Prevents the frame from adjusting to its content
        frame.place(x=x, y=y, width=width, height=height)

        label = tk.Label(frame, font=('Times 20'), bg='white')
        label.config(text=title)
        label.pack(pady=10)

    def text_label(self,label, text, bg, x, y, var):
        # label = tk.Label()
        label.config(text=f"{var} : {text}")
        label.config(bg=bg)
        label.place(x=x, y=y)
        

    def toggle_button1(self):
        if self.button_connected["text"] == "Connected":
            self.button_connected["text"] = "Disconnected"
            self.button_connected["bg"] = "red"
        else:
            self.button_connected["text"] = "Connected"
            self.button_connected["bg"] = "blue"

    def toggle_button2(self):
        if self.button_blue["text"] == "Blue":
            self.button_blue["text"] = "Red"
            self.button_blue["bg"] = "red"
        else:
            self.button_blue["text"] = "Blue"
            self.button_blue["bg"] = "blue"


class ROSNode(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("ros_node")
        self.gui = gui
        
        # self.subscription_num = self.create_subscription(Int32, '/number_topic', self.number_callback, 10)

        # Create a subscriber to receive data from turtlesim
        self.subscription = self.create_subscription(
            Pose,'/turtle1/pose', self.pose_callback,100
        )
    
    
    def pose_callback(self, msg):
        # print(msg)
        
        # Update GUI with received pose data
        # self.gui.location_x_value.set()
        self.gui.label_text.set(msg.x)
        
        print(msg.x)
        
    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)


def start_ros_node(gui):
    rclpy.init(args=None)
    node1 = ROSNode(gui)
    # node2 = DataPublisher(gui)
    # node3 = DrawCircleNode(gui)
    
    #create a MultiThreadExecutor
    executor = MultiThreadedExecutor()
    
    #Add nodes to the executor
    executor.add_node(node1)
    # executor.add_node(node2)
    # executor.add_node(node3)
    
    executor.spin()
    node1.destroy_node()
    # node2.destroy_node()
    # node3.destroy_node()
    rclpy.shutdown()


def main():
    gui = MyGUI()
    gui.node = threading.Thread(target=start_ros_node, args=(gui,))
    gui.node.start()
    gui.run()


if __name__ == "__main__":
    main()