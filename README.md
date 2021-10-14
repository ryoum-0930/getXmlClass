# getXmlClass
XMLデータ群から欲しいタグを含むデータを抜き出す

# Introduction
1. XMLデータ群から欲しいタグを含むデータを抜き出す(get_xml_class.py)
2. trainとtestを任意の割合で分割する(split_train_test.py)

# How to Run
## get_xml_class.py
```python
if __name__=='__main__':
    
    targetList = ["person"]
    outputPath="./person/"
    getDataPath = "H:/dataset/VOC2007"
```
上記のtargetList,outputPath,getDataPathを必要に応じて書き換える
```bash
python get_xml_class.py
```

## split_train_test.py
```python
    # trainデータの割合
    perTrain = 0.9
    perTest = 0.1
    # ----------------------
    _rootPath = "H:/dataset/BearVer2_VOC/"
``` 
parTrain,perTestで割合を設定
_rootPathでデータセットのパスを指定

```bash
python split_train_test.py
```
くそ雑実装（途中から汎用性を無視した）
主にpath周り。他は大丈夫だと思いたい思いたい
