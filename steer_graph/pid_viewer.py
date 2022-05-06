#!/usr/bin/env python

import rclpy
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
      Float64MultiArray, "SAS11", self.whl_callback, 10)
    self.whl_ang_axis = []
    self.whl_index_axis = []
    self.whl_index = 0
    self.ref_ang = 0
    self.ref_subs
    self.fig = plt.figure()

  def whl_callback(self, data): 
    curr_ang = 0
    idx = 0
    self.whl_index = self.whl_index + 1
    for idx in range (1):
      curr_ang = data.data[idx]
    self.whl_ang_axis.append(curr_ang)
    self.whl_index_axis.append(self.whl_index)

    #plt.yscale('linear')
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Wheel Angle", fontsize=14)
    plt.axhline(self.ref_ang, color="red", linestyle="-", label="Ref")
    plt.legend()
    plt.plot(self.whl_index_axis, self.whl_ang_axis, color="black")
    plt.draw()
    plt.pause(0.2)
    self.fig.clear()

  def ref_callback(self, data):
    self.ref_ang = data.data


def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
