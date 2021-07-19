import xml.etree.ElementTree as ET
import shutil,glob,os

# PASCALVOCからpersonを抜き出したい
class GetXml:
    def __init__(self,_rootPath,_targetList):
        self.rootPath = _rootPath
        self.targetList = _targetList
    
    # 操作するフォルダを選択後、取得したいファイル群を取得
    def GetFileList(self,_tarDir,_extend="xml"):
        _targetPath = f"{self.rootPath}/{_tarDir}"
        # _fileList = glob.glob(f"{_targetPath}/000001.xml")
        _fileList = glob.glob(f"{_targetPath}/*.{_extend}")
        print("GetFileList")
        return _fileList
    
    # XMLファイルの解析と取得
    def ParseXml(self,_path):
        # XMLファイルを解析
        TREE = ET.parse(_path)
        # XMLを取得
        _rootXml = TREE.getroot()
        return _rootXml
    
    # 目的オブジェクトのがある画像とアノテーションデータを取り出す
    def FindTarget(self,_xmlName):
        _root = self.ParseXml(_xmlName)
        for tag in _root.iter("name"):
            # print(tag.text)
            # ターゲットが見つかった時
            # if tag.text == "person":
            if tag.text in self.targetList:
                return 1
        # ターゲットのタグが見つからなかった時
        return 0

    # 対象のタグを含むxmlPathリストを取得
    def SearchXml(self,_xmlList):
        _targetListPath=[]
        _no = 1
        print("SearchXml IN")
        for xml in _xmlList:
            # リストで取得して、target別フォルダを作成後、保存
            _result = self.FindTarget(xml)
            print("\r"+"No.{:5}: {:2}".format(_no,_result),end="")
            # targetがあればpathが返ってくる
            if _result == 1:
                _targetListPath.append([xml])
                _no+=1
        print(f"\nFound Number of Data {_no}")
        return _targetListPath,_no
    
    def GetImg(self,xmlPath):
        _imName = os.path.splitext(os.path.basename(xmlPath))[0]
        _imPath = f"{self.rootPath}/JPEGImages/{_imName}.jpg"
        return _imPath
        
    # 移動先のパスのみ指定
    def Main(self,path,type):
        _xmlList = self.GetFileList("Annotations","xml")
        # print(_xmlList)
        _targets,_no = self.SearchXml(_xmlList)
        # _targetsをpathにコピー
        # print(_targets)
        num = 1
        outPath = f"{path}{type}"
        for targetFile in _targets:
            strPath=''.join(targetFile)
            print("\r"+"No.{:5}/{:5}: {}".format(num,_no,strPath),end="")
            shutil.copyfile(strPath,f"{path}{type}/{num:06}.xml")
            _imPath=self.GetImg(strPath)
            shutil.copyfile(_imPath,f"{path}JPEGImages/{num:06}.jpg")
            num+=1
        print(f"\n{self.targetList}の取り出しに成功しました。")
        

if __name__=='__main__':
    
    targetList = ["person"]
    outputPath="./person/"
    wantDataPath = "H:/dataset/VOC2007"
    data = GetXml(wantDataPath,targetList)
    data.Main(outputPath,"Annotations")
