# collect file from raspberrypilearning github

import requests
from bs4 import BeautifulSoup
import marko
import os
import yaml
import junyiJSONgenerate
import imgDownload
import filetype




# list all repo
def listRepo():
    projectName = []
    f = open(r"src\data\pathList.txt", "r",encoding = 'utf8')
    for x in f:
        projectName.append(x.replace("\n",''))
    return projectName

def checkLink(url):
    resp = requests.get(url)
    if resp.status_code == 200:
        return True
    return False

# Download any kind of file from github folder
def getFolder(url,folder):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    pathData = soup.select('td.content a')
    for path in pathData:
        rawPath = "https://github.com"+path["href"]+"?raw=true"
        r = requests.get(rawPath)
        filePath = folder+path["title"]
        with open(filePath, "wb") as code:
            code.write(r.content)
    # kind = filetype.guess(filePath)
    # mypath = filePath
    # if kind != None:
    #     os.rename(mypath,mypath.replace(filePath,filePath+"."+kind.mime.split("/")[1]))
    

def collectMd(project,step,lang):

    url = rootURL+project+'/master/'+lang+'/step_'+str(step)+'.md'
    resp = requests.get(url)

    with open(rootPath+project+"/"+lang+"/step_"+str(step)+".md", 'w',encoding = 'utf8') as f: 
        f.write(resp.text)
        f.close()

def collectImg(project,step,lang):
    url = rootURL+project+'/master/'+lang+'/step_'+str(step)+'.md'
    resp = requests.get(url)
    try:
        mark = marko.convert(resp.text)
        soup = BeautifulSoup(mark, 'html.parser')
        for img in soup.find_all("img"):
            
                imgDownload.imgDownToPath(rootPath+project+"/"+lang+"/"+img["src"],rootURL+project+"/master/"+lang+"/"+img["src"])
    except Exception as e:
        print(e)

def getYaml(project,lang):
    url = rootURL+project+'/master/'+lang+'/meta.yml'
    resp = requests.get(url)

    with open(rootPath+project+"/"+lang+"/meta.yml", 'w',encoding = 'utf8') as f: 
        f.write(resp.text)
        f.close()

def getProjectTitle(project,lang):
    url = rootURL+project+'/master/'+lang+'/meta.yml'
    resp = requests.get(url)
    
    y = yaml.load(resp.text, Loader=yaml.FullLoader)
    title = y["title"]
    return title

def estFolder(project,lang):
    if not os.path.isdir(rootPath+project):
        os.mkdir(rootPath+project)
    if not os.path.isdir(rootPath+project+"/"+lang):
        os.mkdir(rootPath+project+"/"+lang)
        os.mkdir(rootPath+project+"/"+lang+"/images")
        os.mkdir(rootPath+project+"/"+lang+"/resources")

def getFile(url,filePath):
    r = requests.get(url)
    with open(filePath, "wb") as code:
        code.write(r.content)

global rootURL
global rootPath

projectName = listRepo()

for project in projectName:
    rootURL = 'https://raw.githubusercontent.com/raspberrypilearning/'
    rootPath = "D:/workspace/Junyi/Code Club-Learning Resources/"
    try:
        getFile(rootURL+project+'/master/en/images/banner.png',rootPath+project+'/banner.png')
        print(project)
    except Exception as e:
        print(e)
# for project in projectName:
#     step = 1
#     rootURL = 'https://raw.githubusercontent.com/raspberrypilearning/'
#     rootPath = "D:/workspace/Junyi/Code Club-Learning Resources/"
#     getFolder('https://github.com/raspberrypilearning/'+project+'/tree/master/en/resources','D:/workspace/Junyi/Code Club-Learning Resources/'+project+'/zh-TW/resources/')
    
    
#     if checkLink(rootURL+project+'/master/zh-TW/step_'+str(step)+'.md'):
#         estFolder(project,"zh-TW")
#         while(checkLink(rootURL+project+'/master/en/step_'+str(step)+'.md')):
#             collectMd(project,step,"zh-TW")
#             collectImg(project,step,"zh-TW")
#             step+=1

#         getYaml(project,"zh-TW")
#         title = getProjectTitle(project,"zh-TW")
#         print(title)

#     elif checkLink(rootURL+project+'/master/zh-CN/step_'+str(step)+'.md'):
#         estFolder(project,"zh-CN")
#         while(checkLink(rootURL+project+'/master/en/step_'+str(step)+'.md')):
#             collectMd(project,step,"zh-CN")
#             collectImg(project,step,"zh-CN")
#             step+=1

#         getYaml(project,"zh-CN")
#         title = getProjectTitle(project,"zh-CN")
#         print(title)

#     else:
#         estFolder(project,"en")
#         while(checkLink(rootURL+project+'/master/en/step_'+str(step)+'.md')):
#             collectMd(project,step,"en")
#             collectImg(project,step,"en")
#             step+=1

#         getYaml(project,"en")
#         title = getProjectTitle(project,"en")
#         print(title)
        
