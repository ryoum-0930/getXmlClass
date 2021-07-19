# ImageSetsに追加した画像分を書き込む
# ランダム抽出のプログラム適当に書くかなぁ
# trainval.txt=train.txt
# val.txt=test.txt
import glob,random,os

class SplitData:
    def __init__(self,_rootPath,_perTrain):
        self.rootPath=_rootPath
        self.xmlPath=f"{_rootPath}Annotations/"
        self.imagePath=f"{_rootPath}JPEGImages/"
        self.perTrain = _perTrain
    
    def GetFileName(self,_listPath):
        _nameList = []
        for path in _listPath:
            _imName = os.path.splitext(os.path.basename(path))[0]
            _nameList.append(_imName)        
        return _nameList
    
    def JoinPath(self,_nameList,_basePath):
        _pathList = []
        for name in _nameList:
            _joinPath = f"{_basePath}{name}.jpg"
            # print(_joinPath)
            _pathList.append(_joinPath)
        
        return _pathList
    
    def SplitList(self,_list,_perTrain):
        # listを8:2に分割（train:test)
        MaxSize = len(_list)
        size = int(MaxSize*_perTrain)
        train = _list[:size]
        test = _list[size+1:]
        return train,test
        
    def WriteTxt(self,_dataList,_file):
        path=f"{self.rootPath}ImageSets/Main/{_file}"
        with open(path,'wt') as f:
            for data in _dataList:
                f.write("%s\n" %data)
    
    def Main(self):
        # xmlフォルダリストの取得
        _xmlList = glob.glob(f"{self.xmlPath}*.xml")
        # xmlフォルダリストをランダムに並び替える
        random.shuffle(_xmlList)
        # xmlのnameのみ取得
        _nameList = self.GetFileName(_xmlList)
        # 同様のimgフォルダリストを作成(たぶんいらん)
        _imgList = self.JoinPath(_nameList,self.imagePath)
        # train : test = trainval : val = 8 : 2 でImageSetsにファイル名を追記
        train,test = self.SplitList(_nameList,self.perTrain)
        # print(len(_nameList))
        print(f"{len(train)},{len(test)}")
        # print(f"{train},{test}")
        # txtに追記
        self.WriteTxt(train,"train.txt")
        self.WriteTxt(test,"test.txt")
        
        print("complete!!")

if __name__=='__main__':
    # trainデータの割合
    perTrain = 0.9
    perTest = 0.1
    # ----------------------
    _rootPath = "./person/"
    a = SplitData(_rootPath,perTrain)
    a.Main()