import marko
import requests
from bs4 import BeautifulSoup
import junyiJSONgenerate
import exportCSV
import imgDownload
import os
import re

from googletrans import Translator
translator = Translator()
# from opencc import OpenCC
# cc = OpenCC('s2twp')

def get_tag_text(url,tag):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            mark = marko.convert(resp.text)
            soup = BeautifulSoup(mark, 'html.parser')
            return soup.find_all(tag)
    except Exception as e:
        print('Exception: %s' %(e))
        return None
def get_tag(url,tag):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            # mark = marko.convert(resp.text)
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.find(tag)
    except Exception as e:
        print('Exception: %s' %(e))
        return None


def imgAdd(projectName,content):
    imgIdx = 0
    while(content.find("![",0)>0):
        imgIdx+=1
        pre = content.find("![",0)
        content = content.replace("![","",1)
        bac = 0
        bacP = pre
        while(bac<pre):
            bacP += 1
            bac = content.find("]",bacP)
        content = content[:pre]+"[[☃ image "+str(imgIdx)+"]"+content[bac:]
    content = content.replace("(images/","(https://raw.githubusercontent.com/ys-fang/Code-Club-Learning-Resources/master/"+projectName+"/zh-TW/images/")
    imgLink = re.findall(r'[(](https://raw.*?)[)]', content)
    content = re.sub(r'[(](https://raw.*?)[)]', "", content)
    tempBlock = ''
    while(imgIdx>0):
        templete = junyiJSONgenerate.JSON_open(r'src/Templete/JSONimage')
        string = templete.replace("IMGBLOCKINDEX",str(imgIdx))
        string = string.replace("https://ys-fang.github.io/Linkit7697Learning-Resources/img/ROUTE/IMGIDX.gif",imgLink[imgIdx-1])
        try:
            imgWidth = imgDownload.search_img_width(imgLink[imgIdx-1]).width
            imgHeight = imgDownload.search_img_width(imgLink[imgIdx-1]).height
        except Exception:
            print(imgLink[imgIdx-1])
            break
        if(imgWidth>720):
            rad = 720 / imgWidth
            imgWidth = 720
            imgHeight = imgHeight*rad
        string = string.replace("IMAGEWIDTH",str(imgWidth))
        string = string.replace("IMAGEHEIGHT",str(imgHeight))
        imgIdx-=1
        tempBlock += string
    return tempBlock,content

def scratchAdd(wigTemp,artTemp,projectName):
    articleBlockIdx = 1
    while(artTemp.find("--- hints ---",0)>0):
        pre = artTemp.find("--- hints ---")
        artTemp = artTemp.replace("--- hints ---","",1)
        bac = artTemp.find("--- /hints ---")
        artTemp = artTemp.replace("--- /hints ---","",1)
        artContent = artTemp[pre:bac]
        artTemp = artTemp[:pre]+"[[☃ article-block "+str(articleBlockIdx)+"]]"+artTemp[bac:]
        wid,artTemp = imgAdd(projectName,artTemp)
        wid,artContent = scratchAdd(wid,artContent,projectName)
        artTemplete = junyiJSONgenerate.JSON_open(r'src/Templete/JSONartblo')
        articleBlock = artTemplete.replace("CONTENT",artContent)
        articleBlock = articleBlock.replace("TITLE",r"💡 我需要一點提示")
        articleBlock = articleBlock.replace("#fee","#ffe7c9")
        articleBlock = articleBlock.replace("ARTICLEIDX",str(articleBlockIdx))
        articleBlock = articleBlock.replace('"widgets": {','"widgets": {'+wid)
        wigTemp+=articleBlock
        articleBlockIdx +=1
    hintArtIdx = 1
    while(artTemp.find("--- hint ---",0)>0):
        pre = artTemp.find("--- hint ---")
        artTemp = artTemp.replace("--- hint ---","",1)
        bac = artTemp.find("--- /hint ---")
        artTemp = artTemp.replace("--- /hint ---","",1)
        artContent = artTemp[pre:bac]
        artTemp = artTemp[:pre]+"[[☃ article-block "+str(hintArtIdx)+"]]"+artTemp[bac:]
        wid,artTemp = imgAdd(projectName,artTemp)
        wid,artContent = scratchAdd(wid,artContent,projectName)
        artTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONartblo')
        articleBlock = artTemplete.replace("CONTENT",artContent)
        numList = ["一","二","三","四","五"]
        articleBlock = articleBlock.replace("TITLE","提示"+numList[hintArtIdx-1])
        articleBlock = articleBlock.replace("#fee","#fff")
        articleBlock = articleBlock.replace("ARTICLEIDX",str(hintArtIdx))
        articleBlock = articleBlock.replace('"widgets": {','"widgets": {'+wid)
        wigTemp+=articleBlock
        hintArtIdx +=1
    scratchIDX = 1
    while(artTemp.find('```blocks3')>0):
        preIdx = artTemp.index('```blocks3')
        artTemp = artTemp.replace("```blocks3","")
        scratchTemp = (artTemp[preIdx:artTemp.index('```')]).replace('"','\\"')
        artTemp = artTemp[:preIdx]+"[[☃ scratch "+str(scratchIDX)+"]]"+artTemp[artTemp.index('```')+3:]
        artTemp = artTemp.replace("```","")
        scratchTemp = scratchTemp.replace("\n","\\n")
        scratchTemp = scratchTemp.replace("\\(","\\\\(")
        scratchTemp = scratchTemp.replace("\\)","\\\\)")
        shTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONscratch')
        shTemplete = shTemplete.replace("IDX",str(scratchIDX))
        shTemplete = shTemplete.replace("BLOCK",scratchTemp)
        wigTemp+=shTemplete
        scratchIDX+=1
    scratchIDX = 1
    while(artTemp.find("`{",0)>0):
        pre = artTemp.find("`",0)
        artTemp = artTemp.replace("`","",1)
        bac = 0
        bacP = pre
        while(bac<pre):
            bacP += 1
            bac = artTemp.find("`",bacP)
            if(bac==-1):
                break
        if(artTemp[bac+1]!='{'):
            continue
        scratchTemp = (artTemp[pre:bac])
        end = 0
        endp = 0
        while(end<bac):
            endp += 1
            end = artTemp.find('"}',endp)
            if(artTemp.find('"}',endp)<0):
                break
        scratchType = (artTemp[bac+17:end-1])
        artTemp = artTemp[:pre]+"[[☃ inline-scratch "+str(scratchIDX)+"]]"+artTemp[end+2:]
        shTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONinlScratsh')
        shTemplete = shTemplete.replace("IDX",str(scratchIDX))
        shTemplete = shTemplete.replace("BLOCK","("+scratchTemp+" ::"+scratchType)
        wigTemp+=shTemplete
        scratchIDX+=1
    
    while(artTemp.find("[[[",0)>0):
        pre = artTemp.find("[[[")
        artTemp = artTemp.replace("[[[","",1)
        bac = artTemp.find("]]]")
        artTemp = artTemp.replace("]]]","",1)
        genericType = (artTemp[pre:bac])
        
        artTemp = artTemp[:pre]+"[[☃ article-block "+str(articleBlockIdx)+"]]"+artTemp[bac:]
        artTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONartblo')
        articleBlock = artTemplete.replace("CONTENT","[[☃ iframe 1]]")

        ifTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONiframe')
        iframeBlock = ifTemplete.replace("https://ys-fang.github.io/Linkit7697Learning-Resources/bubble/ROUTE/BUBBLEIDX.html","https://ys-fang.github.io/Code-Club-Learning-Resources/"+genericType+"/zh-TW/step_1.html")
        iframeBlock = iframeBlock.replace("IFRAMEIDX",str(1))

        iframeBlock = iframeBlock.replace("320",exportCSV.getdata(genericType).height)
        
        articleBlock = articleBlock.replace("widgets\": {","widgets\": {"+iframeBlock[:-1])

        articleBlock = articleBlock.replace("TITLE","💡 "+exportCSV.getdata(genericType).name)
        articleBlock = articleBlock.replace("#fee","aliceblue")
        articleBlock = articleBlock.replace("ARTICLEIDX",str(articleBlockIdx))
        wigTemp+=articleBlock
        articleBlockIdx +=1
    artTemp = artTemp.replace("\n","\\n")
    return wigTemp[:-1],artTemp

def keyDelet(content):
    keyList = [r"--- no-print ---",r"--- /no-print ---",r"\--- no-print \---",r"\--- /no-print \---",r"--- challenge ---",r"--- /challenge ---",r"\\"]
    for key in keyList:
        content = content.replace(key,"")
    return content



def md_convert(projectName,stepIdx):
    step = str(stepIdx)
    url = 'https://raw.githubusercontent.com/ys-fang/Code-Club-Learning-Resources/master/'+projectName+'/zh-TW/step_'+step+'.md'
    resp = requests.get(url)

    conText = resp.text

    iframeBlock = ""
    try:
        content = conText[:conText.index('<div')]+conText[conText.index('</div'):]
        content = content.replace("</div>","[[☃ iframe 1]]",1)
        content = content.replace("</div>","")
        iframeUrl = get_tag(url,'iframe')['src']
        if(iframeUrl.find("https")==-1):
            iframeUrl = "https:"+iframeUrl 
        
        # micro bit spacail 
        # iframeID = get_tag(url,'iframe')['src'].split("id=")[1]
        # iframeUrl = "https://ys-fang.github.io/msmc/player.html?id="+iframeID

        ifTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONiframe')
        iframeBlock = ifTemplete.replace("https://ys-fang.github.io/Linkit7697Learning-Resources/bubble/ROUTE/BUBBLEIDX.html",iframeUrl)
        iframeBlock = iframeBlock.replace("IFRAMEIDX",str(1))
        iframeBlock = iframeBlock.replace("320",str(480))
    except Exception as e:
        content = conText
        print(e)

    
    while 1:
        if(content.find('<a')>=0):
            try:
                a_link = get_tag(url,'a')
                content = content[:content.index('<a')]+"["+a_link.text+"](\""+a_link["href"]+"\",\" \" \"_blank\")"+content[content.index('</a>')+4:]
            except Exception as e:
                break
        else:
            break
    
    content = keyDelet(content) 
    content = content.replace("){:target=\"_blank\"}"," \"_blank\" \"title\")")
    content = content.replace(r"## \--- collapse \---","--- collapse ---")
    content = content.replace(r"\--- /collapse \---","--- /collapse ---")

    content = content.replace("<kbd>","`")
    content = content.replace("</kbd>","`")
    content = content.replace("(resources","(https://github.com/ys-fang/Code-Club-Learning-Resources/tree/master/"+projectName+"/zh-TW/resources/")
    if(step=='1'):
        content = content.replace(" \"_blank\" \"title\"","")
        content = content.replace(")"," \"_blank\" \"title\")")
    
    content = content.replace("	+","tab&mark")
    content = content.replace("+ ","\\n---\\n$\\\\\\\$\\n\\n+ ✅ ")
    content = content.replace("tab&mark","	+")

    # title modify
    collTitle = []
    try:
        h1Title = get_tag_text(url,'h2')
        for h1 in h1Title:
            if(h1.text.find("collapse")==-1):
                content = content.replace("## "+h1.text,"# **"+h1.text+"**")
                collTitle.append(h1.text)
    except Exception as e:
        print(h1Title)
    try:
        h2Title = get_tag_text(url,'h3')
        for h2 in h2Title:
            content = content.replace("### "+h2.text,"## **"+h2.text+"**")
    except Exception as e:
        print(e)
    try:
        h3Title = get_tag_text(url,'h4')
        for h3 in h3Title:
            content = content.replace("### "+h3.text,"### **"+h3.text+"**")
    except Exception as e:
        print(e)


    articleBlockIdx = 1
    articleBlockContent = ""
    
    titleIdx=1
    
    while 1:
        tempCont = content
        if(tempCont.find('--- collapse ---')>0): 
            content = tempCont[:tempCont.index('--- collapse ---')]+"[[☃ article-block "+str(articleBlockIdx)+"]]"+tempCont[tempCont.index('--- /collapse ---')+17:]
            arTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONartblo')
            artTemp = (tempCont[tempCont.index('--- collapse ---')+19:tempCont.index('--- /collapse ---')]).replace('"','\\"')
            # title = artTemp[artTemp.find("---")+3:artTemp.find("---",1)]
            title = collTitle[titleIdx]
            titleIdx = titleIdx+1

            artTemp = artTemp.replace("\n","\\n")
            title = title.replace("\n","")
            artTemp = artTemp.replace(title,"")
            articleBlock = arTemplete.replace("CONTENT",artTemp)
            articleBlock = articleBlock.replace("TITLE",title.replace("title:","📍"))
            articleBlock = articleBlock.replace("ARTICLEIDX",str(articleBlockIdx))
            articleBlockContent+=articleBlock
            articleBlockIdx+=1
        elif(tempCont.find('--- print-only ---')>0):
            content = tempCont[:tempCont.index('--- print-only ---')]+tempCont[tempCont.index('--- /print-only ---')+19:]
        elif(tempCont.find('--- task ---')>0):
            content = tempCont[:tempCont.index('--- task ---')]+"[[☃ article-block "+str(articleBlockIdx)+"]]"+tempCont[tempCont.index('--- /task ---')+13:]
            arTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONartblo')
            articleBlock = arTemplete.replace("expandable\": true","expandable\": false")
            artTemp = (tempCont[tempCont.index('--- task ---')+13:tempCont.index('--- /task ---')]).replace('"','\\"')
            artTemp = artTemp.replace("\n","\\n")
            artTemp = artTemp.replace("--- task ---","")
            artTemp = artTemp.replace("--- /task ---","")
            wigTemp,artTemp = imgAdd(projectName,artTemp)
            wigTemp,artTemp = scratchAdd(wigTemp,artTemp,projectName)
            articleBlock = articleBlock.replace("CONTENT",artTemp)
            articleBlock = articleBlock.replace("widgets\": {","widgets\": {"+wigTemp)
            articleBlock = articleBlock.replace("TITLE","")
            articleBlock = articleBlock.replace("#fee","#eafaec")
            articleBlock = articleBlock.replace("ARTICLEIDX",str(articleBlockIdx))
            
            articleBlockContent+=articleBlock
            articleBlockIdx+=1
        elif(tempCont.find('--- hints ---')>0):
            content = tempCont[:tempCont.index('--- hints ---')]+"[[☃ article-block "+str(articleBlockIdx)+"]]"+tempCont[tempCont.index('--- /hints ---')+14:]
            arTemplete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONartblo')
            artTemp = (tempCont[tempCont.index('--- hints ---')+14:tempCont.index('--- /hints ---')]).replace('"','\\"')
            # title = artTemp[artTemp.find("---")+3:artTemp.find("---",1)]
            artTemp = artTemp.replace("\n","\\n")
            artTemp = artTemp.replace("--- hint ---","")
            artTemp = artTemp.replace("--- /hint ---","")
            wigTemp,artTemp = imgAdd(projectName,artTemp)
            articleBlock = arTemplete.replace("CONTENT",artTemp)
            articleBlock = articleBlock.replace("widgets\": {","widgets\": {"+wigTemp)
            # title = title.replace("\n","")
            # artTemp = artTemp.replace(title,"")
            articleBlock = articleBlock.replace("TITLE",r"💡 我需要一點提示")
            articleBlock = articleBlock.replace("#fee","#ffe7c9")
            articleBlock = articleBlock.replace("ARTICLEIDX",str(articleBlockIdx))
            articleBlockContent+=articleBlock
            articleBlockIdx+=1
        else:
            break
    
    tempBlock,content = imgAdd(projectName,content)
    tempBlock,content = scratchAdd(tempBlock,content,projectName)
    iframeBlock += tempBlock
    
    templete = junyiJSONgenerate.JSON_open(r'src\Templete\JSONempty')
    content = content.replace("\n","\\n")
    content = content.replace('"','\\"')
    content = content.replace("\\)",")")
    
    output = templete.replace("CONTENT",content)
    output = output.replace("WIDGETS",iframeBlock+articleBlockContent[:-1])
    print(projectName+step+"finish! step- "+step)
    output = output.replace("}\"article-block","},\"article-block")
    output = output.replace("	","")
    output = output.replace("},}","}}")
    if not os.path.isdir("output/raspberrypilearning/"+projectName):
        os.mkdir("output/raspberrypilearning/"+projectName)
    
    junyiJSONgenerate.JSON_write(output,"output/raspberrypilearning/"+projectName+"/"+projectName+"-"+step)
    output = addAuth(projectName,step)
    output = addBanner(output)
    junyiJSONgenerate.JSON_write(output,"output/raspberrypilearning/"+projectName+"/"+projectName+"-"+step)

def addAuth(projectName,step):
    content = junyiJSONgenerate.JSON_open("output/raspberrypilearning/"+projectName+"/"+projectName+"-"+step)
    if(step == str(1)):
        content = content.replace("[[☃ article-block 1]]","[[☃ article-block 1]]\\n---\\n#### **#致謝與授權**\\n####本課程係由均一教育平台(Junyi Academy)進行中文化翻譯與衍生創作，採用[創用 CC 姓名標示 4.0 國際](https://creativecommons.org/licenses/by/4.0/deed.zh_TW \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 授權條款釋出。內容源自CC授權課程：["+exportCSV.getdata(projectName).name+" (CodeClub)](https://projects.raspberrypi.org/en/projects/"+projectName+" \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 。\\n\\n####CodeClub 是由 Raspberry Pi Foundation 主持的一個計畫，也是一個位於英國的非營利組織。CodeClub是正在成長的全球性運動的一部分，目標是將運算思維與數位創作能力帶到世界上每一個人的手中。\\n[[☃ image 1]]",1)
        content = content.replace('"widgets": {','''"widgets": {"image 1": {
                "type": "image",
                "graded": true,
                "options": {
                    "range": [
                        [
                            0,
                            10
                        ],
                        [
                            0,
                            10
                        ]
                    ],
                    "box": [
                        75,
                        26
                    ],
                    "useBoxSize": true,
                    "backgroundImage": {
                        "url": "https://ys-fang.github.io/cc_logos/by-sa.png",
                        "width": 75,
                        "height": 26
                    },
                    "labels": [],
                    "maxImageSize": 435,
                    "aspectRatio": 0.34987593052109184
                },
                "version": {
                    "major": 0,
                    "minor": 0
                }
            },''',1)
    else:
        content = content.replace("[[☃ article-block 1]]","[[☃ article-block 1]]\\n\\n[[☃ explanation 1]]",1)
        content = content.replace('"widgets": {','''"widgets": {"explanation 1": {
                "type": "explanation",
                "graded": false,
                "options": {
                    "showPrompt": "關於課程",
                    "hidePrompt": "隱藏說明",
                    "explanation": "---\\n#### **#致謝與授權**\\n####本課程係由均一教育平台(Junyi Academy)進行中文化翻譯與衍生創作，採用[創用 CC 姓名標示 4.0 國際](https://creativecommons.org/licenses/by/4.0/deed.zh_TW \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 授權條款釋出。內容源自CC授權課程：[%s (CodeClub)](https://projects.raspberrypi.org/en/projects/%s \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 。\\n\\n####CodeClub 是由 Raspberry Pi Foundation 主持的一個計畫，也是一個位於英國的非營利組織。CodeClub是正在成長的全球性運動的一部分，目標是將運算思維與數位創作能力帶到世界上每一個人的手中。\\n[[☃ image 1]]",
                    "widgets": {
                        "image 1": {
                            "id": "image 1",
                            "type": "image",
                            "graded": true,
                            "options": {
                                "range": [
                                    [
                                        0,
                                        10
                                    ],
                                    [
                                        0,
                                        10
                                    ]
                                ],
                                "box": [
                                    75,
                                    26
                                ],
                                "useBoxSize": true,
                                "backgroundImage": {
                                    "url": "https://ys-fang.github.io/cc_logos/by-sa.png",
                                    "width": 75,
                                    "height": 26
                                },
                                "labels": [],
                                "maxImageSize": 435,
                                "aspectRatio": 0.34987593052109184
                            },
                            "version": {
                                "major": 0,
                                "minor": 0
                            }
                        }
                    }
                },
                "version": {
                    "major": 0,
                    "minor": 0
                }
            },'''%(exportCSV.getdata(projectName).name,projectName),1)
    junyiJSONgenerate.JSON_write(content,"output/raspberrypilearning/"+projectName+"/"+projectName+"-"+step)
    return content

def addBanner(content):
    try:
        if(content.find("✅")>=0):
            content = content.replace("[[☃ article-block 1]]","[[☃ iframe 1]]\\n[[☃ article-block 1]]\\n[[☃ iframe 2]]",1)
            content = content.replace('"widgets": {',r'''"widgets": {"iframe 1": {"type": "iframe","graded": true,"options": {"height": 80,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/learnTop.html","width": 560},"version": {"major": 0,"minor": 0}},"iframe 2": {"type": "iframe","graded": true,"options": {"height": 50,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/learnBot.html","width": 560},"version": {"major": 0,"minor": 0}},''',1)
        elif(content.find("挑戰")>=0):
            content = content.replace("[[☃ article-block 1]]","[[☃ iframe 1]]\\n[[☃ article-block 1]]\\n[[☃ iframe 2]]",1)
            content = content.replace('"widgets": {',r'''"widgets": {"iframe 1": {"type": "iframe","graded": true,"options": {"height": 80,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/challangeTop.html","width": 560},"version": {"major": 0,"minor": 0}},"iframe 2": {"type": "iframe","graded": true,"options": {"height": 50,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/challangeBot.html","width": 560},"version": {"major": 0,"minor": 0}},''',1)
    except Exception as e:
        print(e)
    return content
    