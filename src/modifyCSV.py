import csv
import re
import exportCSV
import os

with open('src/data/junyi_question0.csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    os.remove('./output/output.csv')
    for row in rows:
        RC = row[6]
        RC = RC.replace("?src=../","?src=..//")
        
        with open('./output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([row[0],row[1],row[2],row[3],row[4],row[5],RC,row[7],row[8]])
        csvfile.close()
    csvfile2.close()
