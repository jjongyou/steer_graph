#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from ichthus_msgs.msg import Common
from std_msgs.msg import Int32
import matplotlib.pyplot as plt


class Steer_graph(Node):

  def __init__(self):
    super().__init__("steer_graph")
    self.ref_subs = self.create_subscription(
      Common, "ref_ang", self.ref_callback, 10)
    self.whl_ang_subs = self.create_subscription(
      Common, "cur_ang", self.str_callback, 10)
    self.pid_off = self.create_subscription(
      Int32, "external_cmd", self.extern_callback, 10)
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
    curr_ang = -data.data
    # self.str_ang_axis.append(curr_ang / 13.3)
    self.str_ang_axis.append(curr_ang)
    self.str_time_axis.append(time_index)
    # self.ref_ang_axis.append(self.ref_ang / 13.3)
    self.ref_ang_axis.append(self.ref_ang)

    plt.xlabel("Time (Seconds)", fontsize=14)
    plt.ylabel("Steer Angle", fontsize=14)
    plt.plot(self.str_time_axis, self.ref_ang_axis, color="red", label="Ref")
    plt.plot(self.str_time_axis, self.str_ang_axis, color="black", label="Vel")
    plt.draw()
    plt.pause(0.001)
    self.fig.clear()

  def ref_callback(self, data):
    self.ref_ang = -data.data

  def extern_callback(self, data):
    if data.data == 3:
      plt.plot(self.str_time_axis, self.ref_ang_axis, color="red", label="Ref")
      plt.plot(self.str_time_axis, self.str_ang_axis, color="black", label="Vel")
      plt.savefig(str(time.time()) + ".png");
      print("save figure")

def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  # plt.savefig(time.time());
  rclpy.shutdown()


if __name__ == "__main__":
  main()
