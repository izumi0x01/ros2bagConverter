# how to use
bagファイルのデータを取り出して，pandasのデータフレーム型で取りだすユーティリティです．

```converter.py
# bag_converterクラスをインポート
import bag_converter

# bag_fileには記録したバグファイルを指定してください
bag_converter.connectDB(bag_file)
# .bagファイルから"/topicname"で指定したバグデータを取得
#　dfで取り出される．
df = bag_converter.getTopicDataWithPandas("/topicname")
bag_converter.closeDB()
```

# refer from
https://github.com/fishros/ros2bag_convert
