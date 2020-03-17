from os import listdir
from os.path import isfile, isdir, join
import os

from opencc import OpenCC
cc = OpenCC('s2twp')

def listRepo():
    projectName = []
    f = open(r"src\data\pathList.txt", "r",encoding = 'utf8')
    for x in f:
        projectName.append(x.replace("\n",''))
    return projectName

projectName = listRepo()

for project in projectName:
    mypath = "D:/workspace/Junyi/Code Club-Learning Resources/"+project+"/zh-CN"
    if not os.path.isdir(mypath):
        continue
    files = listdir(mypath)

    for f in files:
        fullpath = join(mypath, f)
        if isfile(fullpath):
            print("檔案：", f)
            content = ''
            with open(fullpath, 'r',encoding = 'utf8') as f: 
                content = f.read()
            f.close()
            with open(fullpath, 'w',encoding = 'utf8') as f: 
                f.write(cc.convert(content))
            f.close()
        elif isdir(fullpath):
            print("目錄：", f)
    os.rename(mypath,mypath.replace("zh-CN","zh-TW"))