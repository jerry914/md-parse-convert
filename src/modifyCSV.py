import csv
import re
import exportCSV
import os

with open('C:/Users/joyce/Downloads/junyi_question0.csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    if(os.path.isfile('./output/output.csv')):
        os.remove('./output/output.csv')

    for row in rows:
        content = row[6]
        content = content.replace("#f9e79f","#fff2cf")
        content = content.replace("#d5f5e3","#e6f5e4")
        content = content.replace("#CCCCFF","#fee")
        cv="cover_range"
        if(row[4]!="cover_range"):
            cv= "picoboard-osep-9"
        with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([row[0],row[1],row[2],row[3],cv,row[5],content,row[7],row[8]])
            csvfile.close()
    csvfile2.close()
