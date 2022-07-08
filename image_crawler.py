import os
import sys
import time
import socket
import argparse
from PIL import Image
from urllib import error
from urllib import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CrawlSelenium():
    def __init__(self, explorer="Chrome", url="https://www.google.com"):
        self.url = url
        self.explorer = explorer
        self.options = Options()

    def set_loading_strategy(self, strategy="none"):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
        self.options.add_argument('--user-agent=%s' % user_agent)
        # self.options.add_argument('--headless')     #在背景執行
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.page_load_strategy = strategy

    def scrollTobottom(self):
        """Scrolling to the page bottom.
           To loading more images as many as possible.
        """
        self.driver.set_page_load_timeout(100)
        last_height = self.driver.execute_script('return document.body.scrollHeight')
        while True:
            self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)
            new_height = self.driver.execute_script('return document.body.scrollHeight')
            try:
                self.driver.find_elements_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            except Exception as err:
                print(err)
                pass
            if new_height == last_height:
                # 點擊顯示更多結果
                try:
                    self.driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
                except Exception as e:
                    print(e)
                    break
            last_height = new_height

    def collect_and_download_images(self, img, imgs_dir, img_count):
        """To get the url of an image, than download image from it.
           Count the number of images and check the image format.
        Args:
            img (selenium.webdriver.remote.webelement.WebElement):  Each thumbnail.
            imgs_dir (str): The image save folder.
            img_count (int): The image number.

        Returns:
            int: The image number.
        """
        img_url = self.find_img_url(img, img_count)
        if img_url is not None:
            path = os.path.join(imgs_dir, str(img_count) + "_img.jpg")
            # save each image to specified path
            self.downloaded_image(img_url, path)
            img_count = self.check_image_format(path, img_count)
        else:
           return img_count

        return img_count

    def find_img_url(self, img, img_count):
        """Click thumbnail to find the image url.
        Args:
            img (selenium.webdriver.remote.webelement.WebElement): Each thumbnail.
            img_count (int): The image number.
        Returns:
            string: The image url.
        """
        # click thumbnail
        self.driver.execute_script("arguments[0].click();", img)
        time.sleep(1)
        print('\ndownloading image ' + str(img_count) + ': ')
        # navigate to real image
        img_real = self.driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
        img_url = img_real.get_attribute("src")

        return img_url

    def downloaded_image(self, img_url, path):
        """To download image. Set timeout for urllib urlretrieve download file.
        Args:
            img_url (str): The image url to download.
            path (str): The image save path.
        """
        # set timeout time
        socket.setdefaulttimeout(60)
        # 解決下載不完全的問題且避免陷入死循環
        try:
            request.urlretrieve(url = img_url, filename = path, reporthook = progress_callback, data = None)
        except socket.timeout:
            count = 1
            while count <= 5:
                try:
                    request.urlretrieve(url = img_url, filename = path, reporthook = progress_callback, data = None)
                    break
                except socket.timeout:
                    err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                    print(err_info)
                    count += 1
            if count > 5:
                print('downloading image failed!')

    def check_image_format(self, path, img_count):
        """To check whether the image format is supported.
        Args:
            path (str): The image save path.
            img_count (int): The image number.
        Returns:
            string: The image number.
        """
        img = Image.open(path)
        img_format = img.format
        if img_format in ['JPG','JPEG']:
            print(f'\nThe "{path}" format is "{img_format}".')
            img_count = img_count + 1
        elif img_format == 'PNG':
            print(f'\nThe "{path}" format is "{img_format}". So convert it to "{img_format}"')
            os.remove(path)
            new = path.rsplit('.', 1)[0] + '.png'
            img.save(new)
            img_count = img_count + 1
        else:
            print(f'\nThe "{path}" format is "{img_format}". It would deleted.')
            os.remove(path)
            img_count = img_count - 1

        return img_count

    def crawl(self, keyword, imgs_dir):
        """Crawler flow.
        Args:
            keyword (str): Keyword for crawl.
            imgs_dir (str): The path to the download images directory.
        """
        # instantiate driver according to corresponding explorer
        if self.explorer == "Chrome":
            self.driver = webdriver.Chrome(options=self.options)
        
        # search on google and navigate to url
        self.driver.get(self.url)
        # self.driver.maximize_window()
        
        # locate input field
        # search_input = self.driver.find_element(By.NAME, 'q')
        locator = (By.NAME, 'q')
        search_input = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(locator), "找不到指定的元素")
        
        # emulate user input and enter to search
        webdriver.ActionChains(self.driver).move_to_element(search_input).send_keys(keyword + Keys.ENTER).perform()
        time.sleep(2)

        # navigate to google image and find navigation buttons to click
        self.driver.find_element(By.LINK_TEXT, '圖片').click()

        time.sleep(1)
        # Browser the original window and scroll to the page bottom
        self.scrollTobottom()
        
        # find all image elements in google image result page and download its
        imgs = self.driver.find_elements_by_class_name('rg_i')
        img_count = 0
        for img in imgs:
            try:
                img_count = self.collect_and_download_images(img, imgs_dir, img_count)
            except error.HTTPError as http_err:
                print(http_err)
            except Exception as err:
                print(err)

        print("\n============================================================")

        # collect the suggest links
        # switch the tabs to collect more images
        suggest_keys = self.driver.find_elements_by_class_name('ZZ7G7b')
        suggest_links = []
        for key in suggest_keys:
            url = key.get_attribute('href')
            suggest_links.append(url)
            # open the new tab
            self.driver.execute_script("window.open('');")
            time.sleep(1)
            # switch to the new tab
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(url)

            time.sleep(1)
            self.scrollTobottom()

            # find all image elements in google image result page
            imgs = self.driver.find_elements_by_class_name('rg_i')
            for img in imgs:
                try:
                    img_count = self.collect_and_download_images(img, imgs_dir, img_count)
                except error.HTTPError as http_err:
                    print(http_err)
                except Exception as err:
                    print(err)

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        print("Finished loading images.")


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
    crawl_s.set_loading_strategy("none")

    # make directory
    imgs_dir = os.path.join(imgs_dir, keyword)
    if not os.path.exists(imgs_dir):
        os.makedirs(imgs_dir)

    # crawling
    crawl_s.crawl(keyword, imgs_dir)


if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default="https://www.google.com", type=str)
    parser.add_argument('--explorer', default="Chrome", type=str)
    parser.add_argument('--save_path', default="./images", type=str)#, required=True)
    parser.add_argument('--keyword', default="google", type=str)#, required=True)
    args = parser.parse_args()

    main(args.url, args.explorer, args.save_path, args.keyword)