#!/usr/bin/env python

import rclpy
import time
import numpy as np
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
    self.ref_time_axis = []
    self.ref_ang_axis = []
    self.ref_ang = 0
    self.ref_subs
    self.ref_flag = True
    self.fig = plt.figure()

  def str_callback(self, data):
    arrive_time = time.time()
    time_index = arrive_time - self.start_time
    #print(time_index)
    curr_ang = 0
    curr_ang = -data.data
    # self.str_ang_axis.append(curr_ang / 13.3)
    self.str_ang_axis.append(curr_ang)
    self.str_time_axis.append(time_index)
    if self.ref_flag == True:
        # self.ref_ang_axis.append(self.ref_ang / 13.3)
        self.ref_ang_axis.append(self.ref_ang)
        self.ref_time_axis.append(time_index)
        self.ref_flag = False

    plt.xlabel("Time (Seconds)", fontsize=14)
    plt.ylabel("Steer Angle", fontsize=14)
    # plt.plot(self.str_time_axis, self.ref_ang_axis, color="red", label="Ref")
    marker, stemlines, baseline = plt.stem(np.array(self.ref_time_axis), np.array(self.ref_ang_axis), use_line_collection=True)
    plt.plot(np.array(self.ref_time_axis), np.array(self.ref_ang_axis), color='red')
    plt.plot(np.array(self.str_time_axis), np.array(self.str_ang_axis), color="black", label="Vel")
    marker.set_color('red')
    #stemlines.set_color('red')
    stemlines.set_visible(False)
    baseline.set_visible(False)
    plt.setp(marker, markersize = 3)
    plt.draw()
    plt.pause(0.2)
    self.fig.clear()

  def ref_callback(self, data):
    if int(self.ref_ang) != -int(data.data):
        self.ref_flag = True
    #if self.ref_flag == True:
    #    print(self.ref_ang)
    #    print(-data.data)
    self.ref_ang = -data.data


def main(args=None):
  rclpy.init(args=args)
  steer_graph = Steer_graph()

  rclpy.spin(steer_graph)

  steer_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
