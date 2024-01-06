# #!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from turtlesim.msg import Pose
# import tkinter as tk
# import threading

# class MyGUI():
#     def __init__(self):
#         self.window_ = tk.Tk()
#         self.lbl_ = tk.Label(self.window_, text="", font=("Arial", 48))
#         self.lbl_.pack()
    
#     def run(self):
#         self.window_.mainloop()

# class PoseSubscriberNode(Node):
#     def __init__(self, gui: MyGUI):
#         super().__init__("pose_subscriber")
#         self.gui = gui
#         self.pose_sub_ = self.create_subscription(
#             Pose, "/turtle1/pose", self.pose_callback, 10
#         )
#         self.get_logger().info("Draw Circle Node has been started!")
            
#     def pose_callback(self, msg: Pose):
#         msg_str = "x:%.2f\ny: %.2f" % (msg.x, msg.y)
#         msg_str1 = "a:%.2f\nb: %.2f" % (msg.x, msg.y)
#         #self.get_logger().info(msg_str)
#         self.gui.lbl_.config(text=msg_str)
#         self.gui.lbl_.config(text=msg_str1)
#         print(msg_str1)
# def start_node(gui):
#     rclpy.init(args=None)
#     node = PoseSubscriberNode(gui)
#     rclpy.spin(node)
#     rclpy.shutdown()

# def main():
#     gui = MyGUI()
#     t = threading.Thread(target=start_node, args=(gui,))
#     t.start()
#     gui.run()



import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from tkinter import *
import tkinter as tk
import threading

class MyGUI():
    def __init__(self):
        # self.window_ = tk.Tk()
        # self.window_.title("Turtlesim Pose Viewer")

        # self.lbl_x = tk.Label(self.window_, text="X:", font=("Arial", 12))
        # self.lbl_x.grid(row=0, column=0)
        # self.lbl_x_val = tk.Label(self.window_, text="", font=("Arial", 12))
        # self.lbl_x_val.grid(row=0, column=1)

        # self.lbl_y = tk.Label(self.window_, text="Y:", font=("Arial", 12))
        # self.lbl_y.grid(row=1, column=0)
        # self.lbl_y_val = tk.Label(self.window_, text="", font=("Arial", 12))
        # self.lbl_y_val.grid(row=1, column=1)

        # self.lbl_theta = tk.Label(self.window_, text="Theta:", font=("Arial", 12))
        # self.lbl_theta.grid(row=2, column=0)
        # self.lbl_theta_val = tk.Label(self.window_, text="", font=("Arial", 12))
        # self.lbl_theta_val.grid(row=2, column=1)
        def create_frame(root, width, height, x, y, border_radius, title):
            self.frame = tk.Frame(root, width=width, height=height, bg='white')
            self.frame.pack_propagate(False)  # Prevents the frame from adjusting to its content
            self.frame.place(x=x, y=y, width=width,height=height)
            #frame.size(width=width,height=height)

            self.label = tk.Label(self.frame, text=title,font=('Times 20'),bg='white')
            self.label.pack(pady=10)
    
        #label
        def text_label(text,x,y):
            text_label = tk.Label(text=text,)
            text_label.place(x=x, y=x)
            
        # def toggle_button():
        #     if button["text"] == "Blue":
        #         button["text"] = "Red"
        #         button["bg"] = "blue"
        #     else:
        #         button["text"] = "Blue"
        #         button["bg"] = "red"

        # Create the main window
        self.root = tk.Tk()
        self.canvas = Canvas()
        self.root.title('Tkinter Frame Example')

        # Set the window size
        self.window_width, self.window_height = 1366, 768
        self.root.geometry(f'{self.window_width}x{self.window_height}')
        self.root.configure(bg='lightgrey')

        # Create and display frames with random sizes and positions
        create_frame(self.root, 323, 230, 30, 100, 25, "Location")
        # self.text=tk.Label(text = "x:",font=('Times 16'),bg='white').place(x = 50,y = 150)
        # self.lbl_x_val = tk.Label(self.root, text="", font=("Arial", 12))
        # self.lbl_x_val.place(x=70, y=150)
        # self.text=tk.Label(text = "mm",font=('Times 16'),bg='white').place(x = 260,y = 150)  
        # self.text=tk.Label(text = "y:",font=('Times 16'),bg='white').place(x = 50,y = 200) 
        # self.lbl_y_val = tk.Label(self.root, text="", font=("Arial", 12))
        # self.lbl_y_val.place(x=70, y=200)
        # self.lbl_y_val=tk.Label(self.root, text="").place(x=70, y=150)
        # self.text=tk.Label(text = "mm",font=('Times 16'),bg='white').place(x = 260,y = 200)
        # self.text=tk.Label(text = "yaw angle:",font=('Times 16'),bg='white').place(x = 50,y = 250)
        # self.lbl_theta_val = tk.Label(self.root, text="", font=("Arial", 12))
        # self.lbl_theta_val.place(x=70, y=250)
        # self.text=tk.Label(text = "degree",font=('Times 16'),bg='white').place(x = 260,y = 250)

        self.lbl_x_text = tk.Label(self.root, text="x:", font=('Times 16'), bg='white')
        self.lbl_x_text.place(x=50, y=150)
        
        self.lbl_x_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_x_val.place(x=150, y=150)
        #-----
        self.lbl_y_text = tk.Label(self.root, text="y:", font=('Times 16'), bg='white')
        self.lbl_y_text.place(x=50, y=200)
        
        self.lbl_y_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_y_val.place(x=150, y=200)
        
        
        #-----
        self.lbl_yaw_text = tk.Label(self.root, text="yaw angle:", font=('Times 16'), bg='white')
        self.lbl_yaw_text.place(x=50, y=250)
        self.lbl_theta_val = tk.Label(self.root, text="", font=("Times 16"), bg='white' )
        self.lbl_theta_val.place(x=150, y=250)
        

        create_frame(self.root, 946, 228, 390, 100, 25, "Sensor Camera:")
        self.text=tk.Label(text = "Gyro rate wz",font=('Times 16'),bg='white').place(x = 480,y = 180)
        self.text=tk.Label(text = "Magnetometer Mx",font=('Times 16'),bg='white').place(x = 750,y = 180)
        self.text=tk.Label(text = "Magnetometer My",font=('Times 16'),bg='white').place(x = 1050,y = 180)

        self.text=tk.Label(text = "Proximity 2",font=('Times 16'),bg='white').place(x = 480,y = 230)
        self.text=tk.Label(text = "Proximity 2",font=('Times 16'),bg='white').place(x = 750,y = 230)
        self.text=tk.Label(text = "Proximity 3",font=('Times 16'),bg='white').place(x = 1050,y = 230)


        create_frame(self.root, 407, 248, 30, 378, 25, "Area1")
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 100,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 100,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 100,y = 550)

        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 300,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 300,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 300,y = 550)





        create_frame(self.root, 407, 248, 477, 378, 25, "Area2")
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 550,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 550,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 550,y = 550)

        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 750,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 750,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 750,y = 550)

        create_frame(self.root, 407, 252, 924, 378, 25, "Area3")
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 1000,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 1000,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 1000,y = 550)

        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 1200,y = 450)
        self.text=tk.Label(text = "Pick up",font=('Times 16'),bg='white').place(x = 1200,y = 500)
        self.text=tk.Label(text = "Forward",font=('Times 16'),bg='white').place(x = 1200,y = 550)


        # Create a button at specific coordinates
        self.button = tk.Button(self.root, text='Start',fg='white',font=('Times 15'))
        self.button.place(x=30, y=676, width=120,height=40)
        self.button.configure(bg='dodgerblue3')

        self.button = tk.Button(self.root, text='Retry',font=('Times 15'))
        self.button.place(x=190, y=676, width=120,height=40)
        self.button.configure(bg='white')

        # button = tk.Button(root, text="Blue", bg="red", command=toggle_button,)
        button = tk.Button(self.root, text="Blue", bg="red")
        self.button.pack(pady=10)
        self.button.place(x=1220, y=30, width=120,height=40)
        # root.mainloop()

    def run(self):
        self.root.mainloop()
    


class PoseSubscriberNode(Node):
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
    node = PoseSubscriberNode(gui)
    rclpy.spin(node)
    rclpy.shutdown()

def main():
    gui = MyGUI()
    t = threading.Thread(target=start_node, args=(gui,))
    t.start()
    gui.run()

if __name__ == "__main__":
    main()
