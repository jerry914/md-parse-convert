import csv
import re
import exportCSV

with open('./output/資訊安全與倫理 - 工作表1.csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    for row in rows:
        if(row[2].find("http")>=0):
            title = row[0]
            src = row[2]
            with open("src/Templete/securatyTmp.txt", 'r',encoding = 'utf8') as f: 
                content = f.read()
                f.close()
            content = content.replace("TITLE",title)
            content = content.replace("URL",src)
            content = content.replace("\n","")
            with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['0','False','電腦科學','新北市政府教育局-資訊安全與倫理','infoSec','1',content,'',''])
            csvfile.close()
    csvfile2.close()
