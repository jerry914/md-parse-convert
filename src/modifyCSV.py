import csv
import re
import exportCSV
import os

with open('src/data/junyi_question0 (2).csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    # if(os.path.isfile('./output/output.csv')):
    #     os.remove('./output/output.csv')
    #     with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(["qid","is_hidden","subject","source","cover_range","level","question","related_video","related_exercise"])
    #         csvfile.close()

    for row in rows:
        if(row[4].find("cs-webdev")<0):
            continue
        content = row[6]
        if(content.find("iframe 1]]")<0):
            print("d")
            content = content.replace("[[☃ article-block 1]]","[[☃ iframe 1]]\\n[[☃ article-block 1]]\\n[[☃ iframe 2]]",1)
            content = content.replace('"widgets": {',r'''"widgets": {"iframe 1": {"type": "iframe","graded": true,"options": {"height": 80,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/bulbTop.html","width": 560},"version": {"major": 0,"minor": 0}},"iframe 2": {"type": "iframe","graded": true,"options": {"height": 50,"settings": [{"name": "","value": ""}],"url": "https://ys-fang.github.io/Code-Club-Learning-Resources/banFrame/bulbBot.html","width": 560},"version": {"major": 0,"minor": 0}},''',1)

            with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],content,row[7],row[8]])
                csvfile.close()
    csvfile2.close()
