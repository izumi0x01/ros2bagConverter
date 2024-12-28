# how to use
bagファイルのデータを取り出して，pandasのデータフレーム型で取りだすユーティリティです．

```converter.py
# bagファイルをインポート
import bag_converter

# .bagファイルから"/topicname"で指定したバグデータを取得
bag_converter.connectDB(bag_file)
#　dfで取り出される．
df = bag_converter.getTopicDataWithPandas("/topicname")
bag_converter.closeDB()
```

# refer from
https://github.com/fishros/ros2bag_convert
