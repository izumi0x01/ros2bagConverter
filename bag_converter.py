import sqlite3
import message_converter
import os
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
import pandas as pd


class BagConverter:
    def __init__(self):
        self.cursor = None
        self.conn = None

    def connectDB(self, bag_file):
        if not os.path.exists(bag_file):
            print("Bag file not found")
            return

        self.conn = sqlite3.connect(bag_file)
        self.cursor = self.conn.cursor()

    def closeDB(self):
        if self.conn is not None:
            self.conn.close()

    def __flatten_dict(self, d, parent_key='', sep='_'):
        """
        unfold sub-structs, except struct array
        """
        items = []
        i = 0
        for key, val in d.items(): 
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(val, dict):
                items.extend(self.__flatten_dict(val, new_key, sep=sep).items())
            elif isinstance(val, list):
                for val_i in val:
                    items.append((new_key + '_' + str(i), val_i))
                    i += 1
            else:
                items.append((new_key, val))
            i = 0
        return dict(items) 
    
    def extractDataFromDB(self):

        self.cursor.execute('SELECT * from({})'.format('topics'))
        topicRecords = self.cursor.fetchall()

        self.cursor.execute('SELECT * from({})'.format('messages'))
        messageRecords = self.cursor.fetchall()
        
        topicList = []
        for topic_row in topicRecords:    
            topicName = topic_row[1]
            topicType = topic_row[2]
            print(topicType)

            dataList = []
            for message_row in messageRecords:
                _type = get_message(topicType)
                _msgs = message_row[3]
                try:
                  _dmsg = deserialize_message(_msgs, _type)
                  dic_data = message_converter.convert_ros_message_to_dictionary(_dmsg)
                  _res = self.__flatten_dict(dic_data)
                  dataList.append(_res)
                  _res['topic_name'] = topicName
                  #print(_res)
                except Exception as e:
                  continue
                #print(dic_data)    

            df = pd.DataFrame(dataList)
            last_col = df.columns[-1]
            df.insert(0, last_col, df.pop(last_col))
        #    print(df)
            topicList.append(df)

        print(topicList[1])
        return topicList
