import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import requests as req
import base64

def download_single_img(url,filePath):
    pic=requests.get(url)
    try:
        path = os.path.join(os.getcwd(),filePath+".gif")
    except Exception as e:
        print(e)
    img2 = pic.content
    pic_out = open(path,'wb')
    #encoded_string = base64.b64encode(img2)
    #print(encoded_string)
    pic_out.write(img2)
    pic_out.close()
# https://jerry914.github.io/Linkit7697Learning-Resources/img/DIR/NAME.gif
    print("Image Download !")

def getImg_base64(url):
    pic=requests.get(url)
    img=pic.content
    encoded_string = base64.b64encode(img)
    return str(encoded_string)

def imgDownToPath(path,url):
    pic=requests.get(url)
    try:
        path = os.path.join(os.getcwd(),path)
    except Exception as e:
        print(e)
    img2 = pic.content
    pic_out = open(path,'wb')
    pic_out.write(img2)
    pic_out.close()
    # print("image dowmload!")
    
def search_img_width(path):
    response = req.get(path)
    img = Image.open(BytesIO(response.content))
    # img = Image.open(path)
    imgSize = img.size
    w = img.width
    h = img.height
    f = img.format
    # print(imgSize)
    # print(w, h, f)
# https://jerry914.github.io/Linkit7697Learning-Resources/img/DIR/NAME.gif
    return img

def search_img_type(path):
    img = Image.open(path)
    imgSize = img.size
    w = img.width
    h = img.height
    f = img.format
    print(imgSize)
    print(w, h, f)
    return img.f
