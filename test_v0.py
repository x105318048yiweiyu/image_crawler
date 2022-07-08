#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 14:40:09 2022

@author: c95yyw
"""

import os
import bs4
import time
import uuid
import urllib.request
# import urllib
# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def download_pic(url, name, path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    res = urllib.request.urlopen(url, timeout=3).read()
    
    with open(path + name +'.jpg', 'wb') as f:
        f.write(res)
        f.close()

def get_image_url(num, key_word):
    box = driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    box.send_keys(key_word)
    box.send_keys(Keys.ENTER)
    box = driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

    # 滾動頁面
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_elements_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        except:
            pass
        if new_height == last_height:
            # 點擊顯示更多結果
            try:
                box = driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
            except:
                break
        last_height = new_height

    image_urls = []

    for i in range(1, num):
        try:
            image = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img').click()
            # 此選項為下載縮略圖
            # image_src = image.get_attribute("src")
            # image.click() # 點開大圖
            time.sleep(3)  # Google頁面是動態加載的，需要給予頁面加載時間，否則無法得到原圖的url
            # 得到原圖的url
            image_real = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img')
            image_url = image_real.get_attribute("src")
            image_urls.append(image_url)
            print(str(i) + ': ' + image_url)
        except:
            print(str(i) + ': error')
            pass
    
    return image_urls


if __name__ == '__main__':
    url = "https://www.google.com/"
    chromedriver_path = '/home/c95yyw/all_virtualenv/bin/chromedriver'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    os.environ["webdriver.chrome.driver"] = chromedriver_path
    option = webdriver.ChromeOptions()
    option.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option)
#     ch_op = Options()
#     driver = webdriver.Chrome('/home/c95yyw/all_virtualenv/bin/chromedriver', options=ch_op)
    driver.get(url)

    key_word = input('請輸入搜尋關鍵字：')
    num = int(input('請輸入需要下載的圖片數量：'))
    _path = input('圖片儲存路徑：')

    # path = "G:\\google\\images_download\\" + key_word + "\\"  # 圖片儲存路徑改為自己的路徑
#     path = _path + key_word + "\\"
    path = _path + key_word
    print('正在獲取圖片url...')
    image_urls = get_image_url(num, key_word)
    for index, url in enumerate(image_urls):
        try:
            print('第' + str(index) + '張圖片開始下載...')
            download_pic(url, str(uuid.uuid1()), path)
        except Exception as e:
            print(e)
            print('第' + str(index) + '張圖片下載失敗')
            continue
    driver.quit()

                            




# url = 'https://pic.sogou.com/'
# chromedriver_path = '/home/c95yyw/all_virtualenv/bin/chromedriver'
# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
# download_path = './Download'

# keyword = input('Enter the search keyword：')
# limit = 100

# os.environ["webdriver.chrome.driver"] = chromedriver_path                           # to set the environment path
# option = webdriver.ChromeOptions()                                                  # 添加瀏覽器啟動參數
# option.add_argument('--user-agent=%s' % user_agent)
# driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=option) # open the Chrome browser

# driver.get(url)

# submitBtn = driver.find_element_by_css_selector('#submitBtn')
# time.sleep(1)     # 等待1秒
# submitBtn.click()
# time.sleep(0.5)   # 等待0.5秒
# submitBtn.click()
# actions = ActionChains(driver)
# # 滑鼠先移到 submitBtn 上，然後再點擊 submitBtn
# actions.move_to_element(submitBtn).click(submitBtn)
# actions.perform()






