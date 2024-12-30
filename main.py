# import rclpy
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
import sys
import pandas as pd
import bag_converter
import matplotlib.pyplot as plt

if __name__ == "__main__":
    bag_converter = bag_converter.BagConverter()

    path = "./bag/sg_exp/sg_exp_0.db3"
    bag_converter.connectDB(path)
    res = bag_converter.getTopicDataWithPandas("/sg/pressure")
    print(res)
    plt.plot(res['msec'], res['data'])
    plt.show()
    res = bag_converter.getTopicDataWithPandas("/sg/wrench")
    print(res)
    plt.plot(res['msec'], res['wrench_force_z'])
    plt.show()

    bag_converter.closeDB()

