# import rclpy
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
import sys
import pandas as pd
import bag_converter
import matplotlib.pyplot as plt

if __name__ == "__main__":
    bag_converter = bag_converter.BagConverter()
    args = sys.argv
    if len(args) < 2:
        print("Usage: python3 bag_converter.py <bag_file>")
        exit(1)
    else:
        bag_file = args[1]

    bag_converter.connectDB(bag_file)
    res = bag_converter.getTopicDataWithPandas("/sg/pressure")
    print(res)
    plt.plot(res['msec'], res['data'])
    plt.show()
    res = bag_converter.getTopicDataWithPandas("/sg/wrench")
    print(res)
    plt.plot(res['msec'], res['wrench_force_z'])
    plt.show()

    bag_converter.closeDB()


        
        