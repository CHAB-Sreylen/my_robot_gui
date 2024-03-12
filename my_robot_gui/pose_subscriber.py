import tkinter as tk
from tkinter import *
import threading
from turtlesim.msg import Pose
from std_msgs.msg import String
import rclpy
from rclpy.node import Node

#=============== Camera ================
import cv2
from PIL import Image, ImageTk


from std_msgs.msg import Int32
from .data_publisher import DataPublisher
from .draw_circle import DrawCircleNode
from rclpy.executors import MultiThreadedExecutor

class MyGUI:
    def __init__(self, data_publisher_node=None, video_source=0):

        # Create the main window
        self.root = tk.Tk()
        self.root.title('Tkinter Frame Example')
        
        #return value to publish
        self.cw = True

        # Set the window size
        window_width, window_height = 1366, 768
        self.root.geometry(f'{window_width}x{window_height}')
        self.root.configure(bg='lightgrey')

        # Create label name Location
        self.frame_location = tk.Frame(self.root, width=323, height=230, bg='white')
        self.frame_location.pack_propagate(False) # Prevents the frame from adjusting to its content
        self.frame_location.place(x=30, y=100)
        self.label_location = tk.Label(self.frame_location, text="Location", bg='white', font=('Times 20'))
        self.label_location.pack(pady=10)
        
        # Set Location of variable x, y and live real value 
        self.lbl_x_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_x_val.place(x=50, y=150)
        
        self.lbl_y_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_y_val.place(x=50, y=200)

        self.lbl_theta_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_theta_val.place(x=50, y=250)
        
        self.lbl_number_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_number_val.place(x=50, y=300)

        # self.create_frame(946, 228, 390, 100, 25, "Sensor Camera:")
        self.frame_sensor = tk.Frame(self.root, width=945, height=228, bg='white')
        self.frame_sensor.pack_propagate(False)
        self.frame_sensor.place(x=390, y=100)
        self.label_sensor = tk.Label(self.frame_sensor, text="Sensor Camera:", bg='white', font=('Times 20'))
        self.label_sensor.pack(pady=10)
        
        # self.Gyro = tk.Label(self.root, text="Gyro rate wz", font=("Times 11"), bg='white' )
        # self.Gyro.place(x=480, y=180)
        
        # self.MagneMx = tk.Label(self.root, text="Magnetometer Mx", font=("Times 11"), bg='white' )
        # self.MagneMx.place(x=750, y=180)
        
        # self.MagneMy = tk.Label(self.root, text="Magnetometer My", font=("Times 11"), bg='white' )
        # self.MagneMy.place(x=1050, y=180)
        
        # self.pro1 = tk.Label(self.root, text="Proximity 1", font=("Times 11"), bg='white' )
        # self.pro1.place(x=480, y=230)
        
        # self.pro2 = tk.Label(self.root, text="Proximity 2", font=("Times 11"), bg='white' )
        # self.pro2.place(x=750, y=230)
        
        # self.pro3 = tk.Label(self.root, text="Proximity 3", font=("Times 11"), bg='white' )
        # self.pro3.place(x=1050, y=230)
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Button to start webcam
        self.btn_start = tk.Button(self.root, text="Start", width=10, command=self.start_webcam)
        self.btn_start.pack(anchor=tk.CENTER, expand=True)

        # Button to stop webcam
        self.btn_stop = tk.Button(self.root, text="Stop", width=10, command=self.stop_webcam)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)

        self.delay = 10
        self.update()
        
        
        #Create frame of area
        self.frame_area = tk.Frame(self.root, width=1301, height=248, bg='white')
        self.frame_area.pack_propagate(False)
        self.frame_area.place(x=30, y=378)
        self.label_area = tk.Label(self.frame_area, text="Area 1", bg='white', font=('Times 20'))
        self.label_area.pack(pady=25)

        #Set label name currennt task in x=50 and y=410
        self.currenttask = tk.Label(self.root, text="Current task", font=("Times 11"), bg='white' )
        self.currenttask.place(x=50, y=410)
        self.x = 50
        x_loc = 50
        z = 0
        for i in range(10):
            self.x = self.x+190
        #if i <=6 it display in y=460 and x=x+190
            if(i <= 6):
                label = tk.Label(text=f"Text {i}", bg='white')
                label.place(x=x_loc, y=460)
                x_loc = x_loc + 190
        #if i > 6 display in y=510 and x=x+190
            else:
                x_loc = 50 + 190*z
                label = tk.Label(text=f"Text {i}", bg='white')
                label.place(x=x_loc, y=510)
                x_loc = x_loc + 190
                z = z + 1
        #Create button retry
        self.button_retry = tk.Button(self.root, text='Retry', font=('Times 15'))
        self.button_retry.place(x=190, y=676, width=120, height=40)
        self.button_retry.configure(bg='white')
        self.button_retry["state"] = "normal"

        #Create button Connected
        self.button_connected = tk.Button(self.root, text="Connected", command=self.toggle_button1, bg="blue", font=('Times 15'))
        self.button_connected.pack(side=tk.LEFT, padx=5)
        self.button_connected.place(x=30, y=30, width=120, height=40)
        self.button_connected["state"] = "normal"

        # Create the second button
        self.button_blue = tk.Button(self.root, text="Blue", command=self.toggle_button2, bg="blue", font=('Times 15'))
        self.button_blue.pack(side=tk.LEFT, padx=5)
        self.button_blue.place(x=1220, y=30, width=120, height=40)
        self.button_blue["state"] = "normal"

        # Create the Start button
        self.button_start = tk.Button(self.root, text="Start", command=self.toggle_button4, bg="white", font=('Times 15'))
        self.button_start.pack(side=tk.LEFT, padx=5)
        self.button_start.place(x=30, y=676, width=120, height=40)
        self.button_start["state"] = "normal"
    
    def start_webcam(self):
        self.vid = cv2.VideoCapture(self.video_source)

    def stop_webcam(self):
        if self.vid.isOpened():
            self.vid.release()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(self.delay, self.update)
    #===end Camera===
    
    def run(self):
        self.root.mainloop()
        
    # Function to trigger text when conndition true
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
        self.cw = not self.cw
        if self.cw:
            self.button_start.config(text="Started")
        else:
            self.button_start.config(text="Start")


class ROSNode(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("ros_node")
        self.gui = gui
        
        self.subscription_num = self.create_subscription(Int32, '/number_topic', self.number_callback, 10)

        # Create a subscriber to receive data from turtlesim
        self.subscription = self.create_subscription(
            Pose,'/turtle1/pose', self.pose_callback,10
        )
    
    def number_callback(self, msg):
        number = msg.data
        def sreylen(number):
            if number == 1:
                self.gui.lbl_number_val.config(text="Hello", bg="blue", fg="white") # Set value to label name=lbl_number_val = Hello , background= "Blue" and text color="white"
            elif number == 2:
                self.gui.lbl_number_val.config(text="Test1", bg="green", fg="white")
            elif number == 3:
                self.gui.lbl_number_val.config(text="Test2", bg="yellow", fg="black")
            elif number == 4:
                self.gui.lbl_number_val.config(text="Test3", bg="green", fg="white")
            elif number == 5:
                self.gui.lbl_number_val.config(text="Test4", bg="red", fg="white")
            elif number == 6:
                self.gui.lbl_number_val.config(text="Test5", bg="green", fg="white")
            else:
                self.gui.lbl_number_val.config(text="Test6")
        #self.gui.lbl_number_val.config(text=f"Number: {msg.data} ")
        sreylen(number)
        self.gui.label_area.config(text=f"Area {number}") # Set value to label_area + value of number

    def pose_callback(self, msg):
        # print(msg)
        
        # Update GUI with received pose data
        self.gui.lbl_x_val.config(text=f"x: {msg.x:.1f} mm")
        # self.gui.lbl_x_val.config(text=f"{msg.x:.2f}")
        self.gui.lbl_y_val.config(text=f"y : {msg.y:.1f} mm")
        self.gui.lbl_theta_val.config(text=f"yaw angle : {msg.theta:.1f} degree")
        
        if (msg.x < 2):
            self.gui.button_blue.config(text='blue', bg="blue")
        elif (msg.x <4):
            self.gui.button_blue.config(text='red', bg='red')
        else:
            self.gui.button_blue.config(text='yellow', bg='yellow')

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.publisher.publish(msg)


def start_ros_node(gui):
    rclpy.init(args=None)
    node1 = ROSNode(gui)
    node2 = DataPublisher(gui)
    node3 = DrawCircleNode(gui)
    
    #create a MultiThreadExecutor
    executor = MultiThreadedExecutor()
    
    #Add nodes to the executor
    executor.add_node(node1)
    executor.add_node(node2)
    executor.add_node(node3)
    
    executor.spin()
    node1.destroy_node()
    node2.destroy_node()
    node3.destroy_node()
    rclpy.shutdown()


def main():
    video_source = 0  # Provide the appropriate video source value
    gui = MyGUI(video_source=video_source)
    gui.node = threading.Thread(target=start_ros_node, args=(gui,))
    gui.node.start()
    gui.run()

if __name__ == "__main__":
    main()