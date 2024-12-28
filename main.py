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
    res = bag_converter.extractDataFromDB()
    bag_converter.closeDB()

# 行数、列数の表示制限を解除
    res.set_option('display.max_rows', None)  # 行数制限を解除
    res.set_option('display.max_columns', None)  # 列数制限を解除
    print(res[1])
    plt.plot(res[1]['header_stamp_secs'], res[1]['wrench_force_z'])
    plt.grid(True)
    plt.show()
    



        
        