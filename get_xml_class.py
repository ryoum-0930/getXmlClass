import xml.etree.ElementTree as ET
import shutil
import glob
import os

# PASCALVOCからpersonを抜き出したい


class GetXml:
    def __init__(self, _rootPath, _targetList):
        self.rootPath = _rootPath
        self.targetList = _targetList

    # 操作するフォルダを選択後、取得したいファイル群を取得
    def GetFileList(self, _tarDir, _extend="xml"):
        _targetPath = f"{self.rootPath}/{_tarDir}"
        _fileList = glob.glob(f"{_targetPath}/*.{_extend}")
        print(_targetPath)
        print("GetFileList")
        return _fileList

    # XMLファイルの解析と取得
    def ParseXml(self, _path):
        # XMLファイルを解析
        TREE = ET.parse(_path)
        # XMLを取得
        _rootXml = TREE.getroot()
        return _rootXml

    # 目的オブジェクトのがある画像とアノテーションデータを取り出す
    def FindTarget(self, _xmlName):
        _root = self.ParseXml(_xmlName)
        for tag in _root.iter("object"):
            for name in tag.iter("name"):
                if name.text in self.targetList:
                    for dif in tag.iter("difficult"):
                        # print(f"\rdiff: {dif.text}, name: {name.text}",end="")
                        if dif.text == "0":
                            return 1
        # ターゲットのタグが見つからなかった時
        return 0

    # 対象のタグを含むxmlPathリストを取得
    def SearchXml(self, _xmlList):
        _targetListPath = []
        _no = 1
        print("SearchXml IN")
        for xml in _xmlList:
            # リストで取得して、target別フォルダを作成後、保存
            _result = self.FindTarget(xml)
            print("\r"+"No.{:5}: {:2}".format(_no, _result), end="")
            # targetがあればpathが返ってくる
            if _result == 1:
                _targetListPath.append([xml])
                _no += 1
        print(f"\nFound Number of Data {_no}")
        return _targetListPath, _no

    def GetImg(self, xmlPath):
        _imName = os.path.splitext(os.path.basename(xmlPath))[0]
        _imPath = f"{self.rootPath}/JPEGImages/{_imName}.jpg"
        return _imPath

    # 移動先のパスのみ指定
    def Main(self, path, type):
        _xmlList = self.GetFileList("Annotations", "xml")
        # print(_xmlList)
        _targets, _no = self.SearchXml(_xmlList)
        # _targetsをpathにコピー
        # print(_targets)
        num = 1
        outPath = f"{path}{type}"
        for targetFile in _targets:
            strPath = ''.join(targetFile)
            print("\r"+"No.{:5}/{:5}: {}".format(num, _no, strPath), end="")
            shutil.copyfile(strPath, f"{path}{type}/{num:06}.xml")
            _imPath = self.GetImg(strPath)
            shutil.copyfile(_imPath, f"{path}JPEGImages/{num:06}.jpg")
            num += 1
        print(f"\n{self.targetList}の取り出しに成功しました。")

    def GarbageCollect(self):
        checkPath = "./person_0/"
        _xmlList = self.GetFileList("Annotations", "xml")
        Garbages = []

        for xml in _xmlList:
            rootXml = self.ParseXml(xml)
            fname = rootXml.find("filename").text
            for xmlObject in rootXml.iter("object"):
                for name in xmlObject.iter("name"):
                    if name.text in self.targetList:
                        for point in xmlObject.iter("bndbox"):
                            xmin = float(point.find("xmin").text)
                            xmax = float(point.find("xmax").text)
                            ymin = float(point.find("ymin").text)
                            ymax = float(point.find("ymax").text)
                            x = xmax-xmin
                            y = ymax-ymin
                            # print(fname,x,y)
                            if x <= 0 or y <= 0:
                                Garbages.append(fname)
                                print(fname, xmin, xmax, ymin, ymax)
        print(Garbages)


if __name__ == '__main__':

    targetList = ["Bear"]
    outputPath = "./Bear_Ver-1/"
    getDataPath = "H:/dataset/BearVer2_VOC/"
    data = GetXml(getDataPath, targetList)
    # data.Main(outputPath,"Annotations")
    data.GarbageCollect()
