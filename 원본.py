#초기 변수 설정 
import sys, os
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib, urllib.request
import requests
import random
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

###initial set

folder = "./image/"
webDriver = "./chromedriver.exe"
searchItems = ["아이디어 유모차","자전거 유모차","페도라 유모차","컨셉 유모차","클래식 유모차","전동 유모차"]
size = 300

for item in searchItems:
    params ={
    "q":item
    ,"tbm":"isch"
    ,"sa":"1"
    ,"source":"lnms&tbm=isch"
    }

    print(params)

    url = "https://www.google.com/search"
    #브라우저 구동
    url = url+"?"+urllib.parse.urlencode(params)

    print(url)

    browser = webdriver.Chrome(webDriver)
    time.sleep(0.5)
    browser.get(url)
    html = browser.page_source
    time.sleep(0.5)


    #Page Down
    ### get number of image for a page
    soup_temp = BeautifulSoup(html,'html.parser')
    img4page = len(soup_temp.findAll("img"))

    ### page down 
    elem = browser.find_element_by_tag_name("body")
    imgCnt =0


    while imgCnt < size*10:
        # elem.send_keys(Keys.PAGE_DOWN)

        More_Results = browser.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input')
        try:
            elem.send_keys(Keys.PAGE_DOWN)
            More_Results.click()
        except :
            elem.send_keys(Keys.PAGE_DOWN)

        rnd = random.random()
        # print(imgCnt)
        time.sleep(rnd)
        imgCnt+=img4page



    # html 가공, src 추출
    html = browser.page_source
    soup = BeautifulSoup(html,'html.parser')
    img = soup.findAll("img")

    browser.find_elements_by_tag_name('img')

    fileNum=0
    srcURL=[]

    for line in img:
        if str(line).find('data-src') != -1 and str(line).find('http')<100:  
            # print(fileNum, " : ", line['data-src'])  
            srcURL.append(line['data-src'])
            fileNum+=1



    #폴더 생성, 파일 저장
    ### make folder and save picture in that directory
    saveDir = folder+item

    try:
        if not(os.path.isdir(saveDir)):
            os.makedirs(os.path.join(saveDir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

    for i,src in zip(range(fileNum),srcURL):
        try:
            urllib.request.urlretrieve(src, saveDir+"/"+str(i)+".png")
            # print(i,"saved")
        except :
            print("이미지를 찾을수 없습니다.")
    
    browser.quit()
