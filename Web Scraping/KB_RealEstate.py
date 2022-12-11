import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import pandas as pd
import bs4 as bs
import re
import requests
import time

def CollectData (i):
    time.sleep(1)
    flag_b = []
    box8 = driver.find_elements(By.CLASS_NAME,'listcon')
    box8_1 = box8[0].find_element(By.TAG_NAME,'strong').text
    box8_2 = box8[1].find_element(By.TAG_NAME,'strong').text
    box8_3 = box8[3].find_element(By.TAG_NAME,'strong').text

    flag_b.append(box8_1)
    flag_b.append(box8_2)
    flag_b.append(box8_3)

    box9 = driver.find_element(By.CLASS_NAME,'detail-top')
    box9_1 = box9.find_element(By.CLASS_NAME,'dt-text.top-layer').text
    box9_2 = box9.find_element(By.CLASS_NAME,'dt-text.top-point').text
    box9_3 = box9.find_element(By.CLASS_NAME,'dt-text.top-width').text
    flag_b.append(box9_1)
    flag_b.append(box9_2)
    flag_b.append(box9_3)

    box10 = driver.find_element(By.ID,'property-accordion-3').find_element(By.CLASS_NAME,'groupDetail-txt').find_elements(By.TAG_NAME,'div')
    start = time.time()

    if i==0:
        for i in range(len(box10)):
            try:
                flag_a = box10[i].find_element(By.TAG_NAME,'strong')
            except NoSuchElementException:
                flag_a = False

            if flag_a == False:
                flag_b.append(box10[i].get_attribute('innerText'))
            else:
                flag_b.append(flag_a.get_attribute('innerText'))
            
    return(pd.DataFrame(flag_b).T)

def MaximizeScroll(box7):
    
    scroll = driver.find_element(By.CLASS_NAME,'scrollbar-inner.scroll-content.scroll-scrolly_visible')
    past = box7.find_element(By.CLASS_NAME, 'buylistWrap')
    
    while True:
        flag_a = 1
        driver.execute_script("arguments[0].scrollBy(0,10000);", scroll)
        time.sleep(1.2)
        current = box7.find_elements(By.CLASS_NAME,'buylistWrap')
        if current == past:
            for i in range(flag_a):
                driver.execute_script("arguments[0].scrollBy(0,-10000);", scroll)
                time.sleep(1.2)
            break
        else:
            past = current
            flag_a += 1

# headers는 user agent string 이거 구글에 쳐서 나오는 것으로 가져옴
#headers = {"User-Agnet":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}
url = "https://kbland.kr/"
# DriverPath = "C:\\PythonWorkspace\\Lab_code\\chromedriver.exe"
Target_Region = "서울 서초구"

options = webdriver.ChromeOptions()
#options.add_argument("headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get(url)
driver.implicitly_wait(5)
driver.maximize_window()
Data = pd.DataFrame()

box = driver.find_element(By.XPATH,"//*[@id='app']/div[4]/div[1]/div/div/div/button[3]")
box.click()

box1 = driver.find_element(By.TAG_NAME,'input')
box1.send_keys(Target_Region)
box1.send_keys(Keys.RETURN)


box2 = driver.find_element(By.CLASS_NAME,'text')
box2.click()

time.sleep(1)
box3 = driver.find_element(By.CLASS_NAME,'btn.btn-addrSearch')
box3.click()

# 동 선택
box4 = driver.find_element(By.CLASS_NAME,'btn-group-toggle.btn-group.bv-no-focus-ring').find_elements(By.CLASS_NAME,'btn.btn-secondary')
box4[0].click()
time.sleep(1)

# 아파트 단지 선택
box5= driver.find_element(By.CLASS_NAME,'tab-pane.active').find_elements(By.CLASS_NAME,'item-search-poi')
for j in range(len(box5)):
    print(len(box5))
    time.sleep(1)
    box5[j].click()
    time.sleep(1)

    box_test2 = driver.find_element(By.CLASS_NAME,'btn.btn-addrSearch')
    box_test2.click()
    time.sleep(1)

    if j != len(box5):
        box_flag_dong = driver.find_element(By.CLASS_NAME,'btn.btn-secondary.active')
        box_flag_dong.click()
        time.sleep(1)


# Data Collect, Final Stage ================================================================================

# box6 = driver.find_element(By.CLASS_NAME,'sale-btn-group').find_elements(By.CLASS_NAME,'btn.btn-sale')[0]
# box6.click()
# time.sleep(1)

# box7 = driver.find_element(By.CLASS_NAME,'conWbg')
# MaximizeScroll(box7)


# box7_1 = box7.find_elements(By.CLASS_NAME,'buylistWrap')
# print(len(box7_1))

# scroll = driver.find_element(By.CLASS_NAME,'scrollbar-inner.scroll-content.scroll-scrolly_visible')
# # driver.execute_script("arguments[0].scrollBy(0,937.2);", scroll)

# for i in range(len(box7_1)):
#     print(i)
    
#     try:
#         element = box7_1[i].find_element(By.CLASS_NAME,"blistbox.collapsed")
#     except NoSuchElementException:
#         element = False

#     if element == False:
#         box7_1[i].click()
#         flag_c = CollectData(i)
#         Data = pd.concat([Data,flag_c],ignore_index=True)
#         driver.find_element(By.XPATH,'//*[@id="contents"]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[1]/button').click()
#     else : 
#         box_flag0 = box7_1[i].find_element(By.CLASS_NAME,"blistbox.collapsed")
#         box_flag0.click()
#         box_flag1 = box7.find_element(By.CLASS_NAME,"dubbleadd.collapse.show")
#         box_flag1.find_elements(By.CLASS_NAME,"blistbox")[0].click()
#         flag_c = CollectData(i)
#         Data=pd.concat([Data,flag_c],ignore_index=True)
#         driver.find_element(By.XPATH,'//*[@id="contents"]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[1]/button').click()
#         box7_1[i].click()
    
#     if i!=0 and (i+1)%4 == 0:
#         time.sleep(1.2)
#         driver.execute_script("arguments[0].scrollBy(0,624.812);", scroll)
#         time.sleep(1.2)

box_exit = driver.find_element(By.CLASS_NAME,'btn.btn-pageback')
box_exit.click()
# print(Data)
time.sleep(5)
driver.quit()