#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import curses

class TeleopTurtlesim(Node):
    def __init__(self):
        super().__init__('teleop_turtlesim')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.get_logger().info('Teleop Turtlesim Node has been started!')

    def publish_twist(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.publisher_.publish(twist)

def main(stdscr):
    rclpy.init()
    node = TeleopTurtlesim()

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "Use arrow keys to control turtles. Press 'q' to quit.")

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            node.publish_twist(2.0, 0.0)
        elif key == curses.KEY_DOWN:
            node.publish_twist(-2.0, 0.0)
        elif key == curses.KEY_LEFT:
            node.publish_twist(0.0, 2.0)
        elif key == curses.KEY_RIGHT:
            node.publish_twist(0.0, -2.0)
        else:
            node.publish_twist(0.0, 0.0)

    rclpy.shutdown()

if __name__ == '__main__':
    curses.wrapper(main)
