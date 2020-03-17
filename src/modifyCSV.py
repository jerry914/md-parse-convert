import csv
import re
import exportCSV
# import getWeb

with open('./output/junyi_question0 (1).csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    for row in rows:
        
        # with open("./temp/JSONSpe.txt", 'r',encoding = 'utf8') as f: 
        #     content = f.read()
        # f.close()
        # content = content.replace("PUBID",row[4])
        # content = content.replace("PROJECT",row[2])
        # content = content.replace("SCRIPTID",row[3])
        # content = content.replace("SCRIPTID",row[3])
        # content = content.replace("BLOCKHEIGHT",row[7])
        # content = content.replace("SCRIPTHEIHT",row[10])
        # with open("temp/"+row[2]+"-"+row[3]+".txt", 'w',encoding = 'utf8') as f: 
        #     f.write(content)
        # f.close()
        RC = row[6]
        # try:
        #     if(RC.find("#eafaec")>=0):
        #         RC = RC.replace("[[☃ article-block 1]]","[[☃ iframe 1]]\\n[[☃ article-block 1]]\\n[[☃ iframe 2]]",1)
        #         RC = RC.replace('"widgets": {',r'''"widgets": {"iframe 1": {"type": "iframe","graded": true,"options": {"height": 80,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/learnTop.html","width": 560},"version": {"major": 0,"minor": 0}},"iframe 2": {"type": "iframe","graded": true,"options": {"height": 50,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/learnBot.html","width": 560},"version": {"major": 0,"minor": 0}},''',1)
        #     elif(RC.find("挑戰")>=0):
        #         RC = RC.replace("[[☃ article-block 1]]","[[☃ iframe 1]]\\n[[☃ article-block 1]]\\n[[☃ iframe 2]]",1)
        #         RC = RC.replace('"widgets": {',r'''"widgets": {"iframe 1": {"type": "iframe","graded": true,"options": {"height": 80,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/challangeTop.html","width": 560},"version": {"major": 0,"minor": 0}},"iframe 2": {"type": "iframe","graded": true,"options": {"height": 50,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/challangeBot.html","width": 560},"version": {"major": 0,"minor": 0}},''',1)
        # except Exception as e:
        #     print(e)
        RC = RC.replace("[[☃ article-block 1]]","[[☃ article-block 1]]\\n\\n\\n#### **#致謝與授權**\\n####本課程採用[創用 CC 姓名標示-非商業性-相同方式分享 2.5 台灣](https://creativecommons.org/licenses/by-nc-sa/2.5/tw/ \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 授權條款釋出。內容源自CC授權課程：[資訊安全與倫理（新北市政府教育局）](https://code.ntpc.edu.tw/infosense \\\"\\\"\\\"\\\" \\\"\\\"_blank\\\"\\\") 。\\n\\n[[☃ image 1]]",1)
        RC = RC.replace('"widgets": {','''"widgets": {"image 1": {
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
                        "url": "https://github.com/ys-fang/ys-fang.github.io/blob/master/cc_logos/by-nc-sa.png?raw=true",
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
        RC = RC.replace("/jerry914.github.io","")
        RC = RC.replace("\n","")
        with open("temp/"+row[4]+row[0]+".txt", 'w',encoding = 'utf8') as f: 
            f.write(RC)
        f.close()
        with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],RC,row[7],row[8]])
        csvfile.close()
    csvfile2.close()
