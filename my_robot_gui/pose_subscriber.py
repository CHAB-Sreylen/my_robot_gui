import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import String
import rclpy
from rclpy.node import Node

class MyGUI:
    def __init__(self):
        # self.node = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title('Tkinter Frame Example')

        # Set the window size
        window_width, window_height = 1366, 768
        self.root.geometry(f'{window_width}x{window_height}')
        self.root.configure(bg='lightgrey')

        # Create and display frames with random sizes and positions
        self.create_frame(323, 230, 30, 100, 25, "Location")
        # self.text_label("x (mm):","white", 50, 150)
        
        self.lbl_x_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_x_val.place(x=50, y=150)
        # self.text_label("mm", 260, 150)
        # self.text_label("y (mm):","white", 50, 200)
        self.lbl_y_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_y_val.place(x=50, y=200)
        # self.text_label("mm", 260, 200)
        # self.text_label("yaw angle (degree):","white", 50, 250)
        # self.text_label("degree", 260, 250)
        self.lbl_theta_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_theta_val.place(x=50, y=250)

        self.create_frame(946, 228, 390, 100, 25, "Sensor Camera:")
        self.text_label("Gyro rate wz","white", 480, 180)
        self.text_label("Magnetometer Mx","white", 750, 180)
        self.text_label("Magnetometer My","white", 1050, 180)

        self.text_label("Proximity 2","white", 480, 230)
        self.text_label("Proximity 2","white", 750, 230)
        self.text_label("Proximity 3","white", 1050, 230)

        self.create_frame(1301, 248, 30, 378, 25, "Area1")
        self.text_label("Current task","white", 50, 410)

        self.text_label("Forward","white", 50, 460)
        self.text_label("Pick up","white", 240, 460)
        self.text_label("Forward","white", 430, 460)
        self.text_label("Forward","white", 620, 460)
        self.text_label("Pick up","white", 810, 460)
        self.text_label("Forward","white", 1000, 460)
        self.text_label("Pick up","white", 1190, 460)

        self.text_label("Next task","white", 50, 510)
        self.text_label("Forward","white", 50, 560)
        self.text_label("Pick up","white", 240, 560)
        self.text_label("Forward","white", 430, 560)
        self.text_label("Forward","white", 620, 560)
        self.text_label("Pick up","white", 810, 560)
        self.text_label("Forward","white", 1000, 560)
        self.text_label("Pick up","white", 1190, 560)

        self.button_retry = tk.Button(self.root, text='Retry', font=('Times 15'))
        self.button_retry.place(x=190, y=676, width=120, height=40)
        self.button_retry.configure(bg='white')
        self.button_retry["state"] = "normal"

        self.button_connected = tk.Button(self.root, text="Connected", command=self.toggle_button1, bg="blue", font=('Times 15'))
        self.button_connected.pack(side=tk.LEFT, padx=5)
        self.button_connected.place(x=30, y=30, width=120, height=40)
        self.button_connected["state"] = "normal"

        # Create the second button
        self.button_blue = tk.Button(self.root, text="Blue", command=self.toggle_button2, bg="blue", font=('Times 15'))
        self.button_blue.pack(side=tk.LEFT, padx=5)
        self.button_blue.place(x=1220, y=30, width=120, height=40)
        self.button_blue["state"] = "normal"

        self.button_start = tk.Button(self.root, text="Start", command=self.toggle_button4, bg="white", font=('Times 15'))
        self.button_start.pack(side=tk.LEFT, padx=5)
        self.button_start.place(x=30, y=676, width=120, height=40)
        self.button_start["state"] = "normal"

    def run(self):
        self.root.mainloop()

    def create_frame(self, width, height, x, y, border_radius, title):
        frame = tk.Frame(self.root, width=width, height=height, bg='white')
        frame.pack_propagate(False)  # Prevents the frame from adjusting to its content
        frame.place(x=x, y=y, width=width, height=height)

        label = tk.Label(frame, text=title, font=('Times 20'), bg='white')
        label.pack(pady=10)

    def text_label(self, text, bg, x, y):
        label = tk.Label(text=text, bg=bg)
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

    def toggle_button4(self):
        if self.button_start["text"] == "Start":
            self.button_start["text"] = "Started"
            self.button_start["bg"] = "blue"
        else:
            self.button_start["text"] = "Start"
            self.button_start["bg"] = "white"


class ROSNode(Node):
    def __init__(self, gui):
        super().__init__("ros_node")
        self.gui = gui
        self.publisher = self.create_publisher(String, 'control_topic', 10)

        # Create a subscriber to receive data from turtlesim
        self.subscription = self.create_subscription(
            Pose,'/turtle1/pose', self.pose_callback,1
        )

    def pose_callback(self, msg):
        # Update GUI with received pose data
        self.gui.lbl_x_val.config(text=f"x: {msg.x:.1f} mm")
        # self.gui.lbl_x_val.config(text=f"{msg.x:.2f}")
        self.gui.lbl_y_val.config(text=f"y : {msg.y:.1f} mm")
        self.gui.lbl_theta_val.config(text=f"yaw angle : {msg.theta:.1f} degree")

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)


def start_ros_node(gui):
    rclpy.init(args=None)
    node = ROSNode(gui)
    rclpy.spin(node)
    rclpy.shutdown()


def main():
    gui = MyGUI()
    gui.node = threading.Thread(target=start_ros_node, args=(gui,))
    gui.node.start()
    gui.run()


if __name__ == "__main__":
    main()
