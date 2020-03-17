from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import csv

Options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webdriver_path = 'C:\\chromedriver.exe'
options = Options()


def getHeight(url,tag):
    browser = webdriver.Chrome(executable_path=webdriver_path, options=options)
    browser.get(url)
    delay = 20 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,tag)))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
    
    browser.maximize_window()
    height = browser.execute_script("return document.body.offsetHeight")
    browser.close()
    print(height)
    return height

def test_fullpage_screenshot(url):#not work
    browser = webdriver.Chrome(executable_path=webdriver_path, options=options)
    browser.get(url)
    height = browser.execute_script("return document.body.offsetHeight")

    browser.set_window_size(1920, height+1000)
    browser.save_screenshot(r"D:\scrrenshot\baidu.png")
    browser.close()

def getWebScreenShot(url):
    browser = webdriver.Chrome(executable_path=webdriver_path, options=options)
    browser.get(url)
    browser.get_screenshot_as_file(r"D:\scrrenshot\baidu.png")

def judgeEle(url,tag):
    browser = webdriver.Chrome(executable_path=webdriver_path, options=options)
    browser.get(url)
    try:
        block = browser.find_element_by_class_name(tag)
        print(block)
        browser.close()
        return True
    except Exception as e:
        print(e)
    browser.close()
    return False

for i in range(12,43):
    if(judgeEle("https://www.junyiacademy.org/SNAPSHOT/se/SNAPSHOT_701"+str(i),"sb3-obsolete")):
        with open("D:/scrrenshot/errorList.csv", 'a+', newline='',encoding = 'utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["https://www.junyiacademy.org/SNAPSHOT/se/SNAPSHOT_701"+str(i),'sb3-obsolete'])
        csvfile.close()