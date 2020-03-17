import junyiJSONgenerate
import json
import sqlite3
import imgDownload
fileRootPath = str('D:/workspace/HtmlParseBot/Linkit7697Learning Resources/')

def titleSplit(section,subtitle):
    title = section.split("|")
    mdtitle = title[1]+" "+title[2].replace(subtitle,'')
    return mdtitle

def artBlk_generate(num,Type):
    string = ''
    blockType = ''
    if(Type == 'a'):
        blockType = "article-block"
    elif(Type == 'm'):
        blockType = "image"
    else:
        blockType = "iframe"
    for n in range(num):
        string+="[[☃ "+blockType+" "+str(n+1)+"]]\\n\\n"
    return string

def artBlk_wigit_generate(num,Type,route,idx):
    resuleString = ''
    if(Type == 'm'):
        for n in range(num):
            templete = junyiJSONgenerate.JSON_open('src\Templete\JSONimage')
            string = templete.replace("IMGBLOCKINDEX",str(n+1))
            string = string.replace("ROUTE",route)
            string = string.replace("IMGIDX",str(idx+n))
            imgfilePath = fileRootPath+'img/'+route+'/'
            string = string.replace("IMAGEWIDTH",str(imgDownload.search_img_width(imgfilePath+str(idx+n)+".gif").width))
            string = string.replace("IMAGEHEIGHT",str(imgDownload.search_img_width(imgfilePath+str(idx+n)+".gif").height))
            resuleString+=string
        return resuleString[:-1]
    else:
        a=0
        if(Type == 'vf'):
            templete = junyiJSONgenerate.JSON_open('src\Templete\JSONiframe')
            string = templete.replace("IFRAMEIDX",str(1))
            string = string.replace("https://ys-fang.github.io/Linkit7697Learning-Resources/bubble/ROUTE/BUBBLEIDX.html",videoLL[videoIdx])
            resuleString+=string
            a=1
        for n in range(num-1):
            templete = junyiJSONgenerate.JSON_open('src\Templete\JSONiframe')
            string = templete.replace("IFRAMEIDX",str(n+1+a))
            string = string.replace("ROUTE",route)
            string = string.replace("BUBBLEIDX",str(idx+n))
            resuleString+=string
        return resuleString

def cont_wiget_generate(sectionText,sectionImgCount,sectionBubbleCount,route,sectionVideoCount,videoLink):
    templete = junyiJSONgenerate.JSON_open('src\Templete\JSONartblo')
    bubbleIdx = 1
    imgIdx = 1
    global videoLL,videoIdx
    videoIdx = 0
    videoLL = videoLink
    result =  ''
    for a in range(1,len(sectionText)-2):
        articleBlock = ''
        articleBlock = templete.replace("ARTICLEIDX",str(a+1))
        articleBlock = articleBlock.replace("ARTICLETEXT",sectionText[a+1])
        if(sectionVideoCount[a+1]>0):
            articleBlock = articleBlock.replace("IFRAMEBLOCK",artBlk_wigit_generate(sectionBubbleCount[a+1]+sectionVideoCount[a+1],'vf',route,bubbleIdx))
        else:
            articleBlock = articleBlock.replace("IFRAMEBLOCK",artBlk_wigit_generate(sectionBubbleCount[a+1],'f',route,bubbleIdx))
        articleBlock = articleBlock.replace("[[☃ iframe 1]]",artBlk_generate(sectionBubbleCount[a+1]+sectionVideoCount[a+1],'f'))
        if(imgDownload.search_img_width(fileRootPath+'img/'+route+'/'+str(imgIdx)+".gif").width!=70):
            articleBlock = articleBlock.replace("IMGBLOCK",artBlk_wigit_generate(sectionImgCount[a+1],'m',route,imgIdx))
            articleBlock = articleBlock.replace("[[☃ image 1]]",artBlk_generate(sectionImgCount[a+1],'m'))
            articleBlock = articleBlock.replace("ARTICLESTYLE",'')
        else:
            if(articleBlock.find(",IMGBLOCK")>0):
                articleBlock = articleBlock.replace(",IMGBLOCK",'')
            else:
                articleBlock = articleBlock.replace("IMGBLOCK",'')
            articleBlock = articleBlock.replace("[[☃ image 1]]",'')
            articleBlock = articleBlock.replace("#fff",'')
            articleBlock = articleBlock.replace("ARTICLESTYLE",'# ')
        bubbleIdx+=sectionBubbleCount[a]
        imgIdx+=sectionImgCount[a+1]
        videoIdx+=sectionVideoCount[a+1]
        result+=articleBlock

    return result[:-1]