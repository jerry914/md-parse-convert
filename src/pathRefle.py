import os
import sys
import csv
import base64
import imgDownload
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

with open('data/junyi_question0.csv', newline='',encoding = 'utf8') as csvfile2:
    rows = csv.reader(csvfile2)
    if(os.path.isfile('../output/output.csv')):
        os.remove('../output/output.csv')

    for row in rows:
        content = row[6]
        cv = row[4]
        if(row[4]!="cover_range"):
            cv = "osep-test"
        while(content.find("https://drive.google.com/uc?export=view&id=")!=-1):
            glinkStart = content.find("https://drive.google.com/uc?export=view&id=")
            glinkEnd=content.find('"',glinkStart)
            imgURL = content[glinkStart:glinkEnd]
            imgID = imgURL.replace("https://drive.google.com/uc?export=view&id=",'')
            print(imgID)
            with open('data/googleDrive.csv', newline='',encoding = 'utf8') as nameList:
                datas = csv.reader(nameList)
                isFind=False
                for data in datas:
                    rawData = data[3].split("/")
                    if len(rawData)>5:
                        gid = rawData[5]
                        if gid == imgID:
                            content = content.replace("https://drive.google.com/uc?export=view&id=","https://raw.githubusercontent.com/jerry914/Arduino-Learning-Resources/master/",1)
                            content = content.replace(imgID,data[0].replace("Arduino2to3/",""))
                            print(data[0].replace("Arduino2to3/",""))
                            isFind=True
                            break
                if(isFind==False):
                    content = content.replace("https://drive.google.com/uc?export=view&id=","IMETHEDEE",1)
            nameList.close()
        if(content.find("IMETHEDEE")):
            content = content.replace("IMETHEDEE","https://drive.google.com/uc?export=view&id=")
        if(content.find("base64")!=-1):
            while(content.find("base64")!=-1):
                #data:image/png;base64,
                baseStart = content.find("data:image/")
                baseEnd=content.find('"',baseStart)
                imgstring = content[baseStart:baseEnd]
                fileType = imgstring.split(";")[0]
                fileType = fileType.replace("data:image/","")
                print(fileType)
                
                # missing_padding = len(imgstring) % 4
                # dkt = imgstring
                # if missing_padding != 0:
                #     dkt += '='* (4 - missing_padding)
                # imgdata = base64.b64decode(dkt)
                # filename = 'some_image.png'  # I assume you have a way of picking unique filenames
                # with open(filename, 'wb') as f:
                #     f.write(imgdata)
                # with open('data/googleDrive.csv', newline='',encoding = 'utf8') as nameList:
                #     datas = csv.reader(nameList)
                #     isFind=False
                #     for data in datas:
                #         imgURL = data[3]
                #         if(imgURL.find("http")==-1):
                #             continue
                #         tempBase = imgDownload.getImg_base64(imgURL)
                #         print(data[0])
                #         if tempBase == base64_code:
                #             content = content.replace(imgstring,"",1)
                #             print(data[0].replace("Arduino2to3/",""))
                #             isFind=True
                #             break
                #     if(isFind==False):
                #         print("no corrspondence")
                #         content = content.replace(imgstring,"",1)
                # nameList.close()
                content = content.replace(imgstring,"",1)
                print(row[0],"goes wroung! , because of base64")
                logFile = open("../output/data.txt",'a+')
                logFile.write(row[0]+" base64 issue\n")
                logFile.close()
        with open('../output/output.csv','a', newline='',encoding = 'utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([row[0],row[1],row[2],row[3],cv,row[5],content,row[7],row[8]])
            csvfile.close()
    csvfile2.close()
