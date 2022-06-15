#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from ichthus_can_msgs.msg import Pid
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
import matplotlib.pyplot as plt


class Steer_graph(Node):

  def __init__(self):
    super().__init__("steer_graph")
    self.ref_subs = self.create_subscription(
      Float64, "ref_ang", self.ref_callback, 10)
    self.whl_ang_subs = self.create_subscription(
      Float64MultiArray, "SAS11", self.str_callback, 10)
    self.start_time = time.time()
    self.str_ang_axis = []
    self.str_time_axis = []
    self.ref_ang_axis = []
    self.ref_ang = 0
    self.ref_subs
    self.fig = plt.figure()

  def str_callback(self, data):
    arrive_time = time.time()
    time_index = arrive_time - self.start_time
    print(time_index)
    curr_ang = 0
    idx = 0
    for idx in range (1):
      curr_ang = data.data[idx]
    curr_ang = -curr_ang
    # self.str_ang_axis.append(curr_ang / 13.3)
    self.str_ang_axis.append(curr_ang)
    self.str_time_axis.append(time_index)
    # self.ref_ang_axis.append(self.ref_ang / 13.3)
    self.ref_ang_axis.append(self.ref_ang)

    plt.xlabel("Time (Seconds)", fontsize=14)
    plt.ylabel("Tire Steer Angle", fontsize=14)
    plt.plot(self.str_time_axis, self.ref_ang_axis, color="red", label="Ref")
    plt.plot(self.str_time_axis, self.str_ang_axis, color="black", label="Vel")
    plt.draw()
    plt.pause(0.2)
    self.fig.clear()

  def ref_callback(self, data):
    self.ref_ang = -data.data


def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
