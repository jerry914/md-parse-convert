import os
import requests
import mdconvert

f = open("src/data/pathList.txt", "r",encoding = 'utf8')
for x in f:
    print(x)
    projectName = x.replace("\n",'')
    if not os.path.isdir("output/raspberrypilearning/"+projectName):
        os.mkdir("output/raspberrypilearning/"+projectName)
    stepIdx = 1
    while 1:
        # projectName = 'happy-birthday'
        step = str(stepIdx)
        url = 'https://raw.githubusercontent.com/ys-fang/Code-Club-Learning-Resources/master/'+projectName+'/zh-TW/step_'+step+'.md'
        resp = requests.get(url)
        # print(resp.text)
        if resp.status_code == 200:
            try:
                # mdconvert.md_convert(projectName,stepIdx)
                mdconvert.exportCSV.add_csv(projectName,step)
            except Exception as e:
                print(e)
            stepIdx+=1
        else:
            break