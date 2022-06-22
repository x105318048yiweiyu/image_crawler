from ast import keyword
from tkinter import N
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib import error
from urllib import request
import os
import time
import sys
import argparse


class CrawlSelenium():
    def __init__(self, explorer="Chrome", url="https://www.google.com"):
        self.url = url
        self.explorer = explorer

    def set_loading_strategy(self, strategy="normal"):
        self.options = Options()
        self.options.page_load_strategy = strategy

    def crawl(self, keyword, imgs_dir):
        # instantiate driver according to corresponding explorer
        if self.explorer == "Chrome":
            self.driver = webdriver.Chrome(options=self.options)
        if self.explorer == "Opera":
            self.driver = webdriver.Opera(options=self.options)
        if self.explorer == "Firefox":
            self.driver = webdriver.Firefox(options=self.options)
        if self.explorer == "Edge":
            self.driver = webdriver.Edge(options=self.options)
        
        # search on google
        # navigate to url
        self.driver.get(self.url)
        
        # locate input field
        search_input = self.driver.find_element(By.NAME, 'q')
        
        # emulate user input and enter to search
        webdriver.ActionChains(self.driver).move_to_element(search_input).send_keys(keyword + Keys.ENTER).perform()
#         webdriver.ActionChains(self.driver).move_to_element(search_input).send_keys("吉娃娃" + Keys.ENTER).perform()
        
        # navigate to google image
        # find navigation buttons
        self.driver.find_element(By.LINK_TEXT, '圖片').click()

        # 滾動頁面
        last_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            try:
                self.driver.find_elements_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            except:
                pass
            if new_height == last_height:
                # 點擊顯示更多結果
                try:
                    box = self.driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
                except:
                    break
            last_height = new_height

#         # load more images as many as possible
#         # scrolling to bottom
#         self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        
#         # get button
#         show_more_button = self.driver.find_element(By.CSS_SELECTOR, "input[value='顯示更多搜索結果']")
#         try:
#             while True:
#                 # do according to message
#                 message = self.driver.find_element(By.CSS_SELECTOR, 'div.OuJzKb.Bqq24e').get_attribute('textContent')
#                 # print(message)
#                 if message == '正在加載更多內容，請稍後':
#                     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#                 elif message == '新內容已成功加載。向下滾動即可查看更多內容。':
#                     # scrolling to bottom
#                     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

#                 if show_more_button.is_displayed():
#                     show_more_button.click()
#                 elif message == '看來您已經看完了所有內容':
#                     break
#                 elif message == '無法加載更多內容，點擊即可重試。':
#                     show_more_button.click()
#                 else:
#                     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#         except Exception as err:
#             print(err)
        
        # find all image elements in google image result page
        imgs = self.driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")
        img_count = 0
        for img in imgs:
            try:
                # image per second
                time.sleep(1)
                print('\ndownloading image ' + str(img_count) + ': ')
                img_url = img.get_attribute("src")
                if img_url == None:
                    continue
                path = os.path.join(imgs_dir, str(img_count) + "_img.jpg")
                request.urlretrieve(url = img_url, filename = path, reporthook = progress_callback, data = None)
                img_count = img_count + 1
            except error.HTTPError as http_err:
                print(http_err)
            except Exception as err:
                print(err)


# report hook with three parameters passed
# count_of_blocks The number of blocks transferred
# block_size The size of block
# total_size Total size of the file
def progress_callback(count_of_blocks, block_size, total_size):
    # determine current progress
    progress = int(50 * (count_of_blocks * block_size) / total_size)
    if progress > 50:
        progress = 50
    
    # update progress bar
    sys.stdout.write("\r[%s%s] %d%%" % ('█' * progress, ' ' * (50 - progress), progress * 2))
    sys.stdout.flush()


def main(url, explorer, imgs_dir, keyword):
    # setting
    crawl_s = CrawlSelenium(explorer, url)
    crawl_s.set_loading_strategy("normal")
    
    # make directory
    imgs_dir = os.path.join(imgs_dir, keyword)
    if not os.path.exists(imgs_dir):
        os.makedirs(imgs_dir)

    # crawling
    crawl_s.crawl(keyword, imgs_dir)


if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default="https://www.google.com", type=str)
    parser.add_argument('--exploer', default="Chrome", type=str)
    parser.add_argument('--save_path', default="./images", type=str)#, required=True)
    parser.add_argument('--keyword', default="吉娃娃", type=str)#, required=True)
    args = parser.parse_args()

    main(args.url, args.exploer, args.save_path, args.keyword)