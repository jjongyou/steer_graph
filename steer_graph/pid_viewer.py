#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from ichthus_can_msgs.msg import Pid
from std_msgs.msg import Float64
import matplotlib.pyplot as plt


class Steer_graph(Node):

  def __init__(self):
    super().__init__("steer_graph")
    self.ref_subs = self.create_subscription(
      Float64, "ref_ang", self.ref_callback, 10)
    self.whl_ang_subs = self.create_subscription(
      Float64, "cur_ang", self.str_callback, 10)
    self.start_time = time.time()
    self.str_ang_axis = []
    self.str_time_axis = []
    self.ref_ang_axis = []
    self.ref_ang = 0
    self.curr_ang = 0
    self.flag = 0
    self.ref_subs
    self.fig = plt.figure()

  def str_callback(self, data):
    arrive_time = time.time()
    print(arrive_time - self.start_time)
    if self.flag == 0 and arrive_time - self.start_time > 40:
        self.start_time = time.time()
        self.flag = 1

    if self.flag == 1:
        time_index = arrive_time - self.start_time
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
        plt.pause(0.2)
        self.fig.clear()

  def ref_callback(self, data):
    if self.flag == 1:
        self.ref_ang = -data.data


def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
