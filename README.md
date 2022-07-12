# image_crawler

## Getting started
### Dependencies
1. Ubuntu 20.04
2. **Google-Chrome** or your browser (ex: Firefox, Opera, etc.)
3. The driver of browser 
    - The table of each driver
        - 一個適用於不同語言的**API**以及**協議(protocol)**，用於處理`selenium`和瀏覽器之間的交流，進而控制瀏覽器的行為。幾乎所有的瀏覽器都有對應的driver，如下表
            
            
            |          Browser |                Maintainer | Versions Supported |
            | --- | --- | --- |
            |          Chrome |                 Chromium |         All versions |
            |           Firefox |                    Mozilla |       54 and newer |
            |            Opera | Opera Chromium / Presto |     10.5 and newer |
            |            Safari |                      Apple |      10 and newer |
4. python 3.8
    1. selenium
    2. urllib
    3. PIL
        - Python Image Library
            
            [https://yungyuc.github.io/oldtech/python/python_imaging.html](https://yungyuc.github.io/oldtech/python/python_imaging.html)
            
            [https://ithelp.ithome.com.tw/articles/10226578](https://ithelp.ithome.com.tw/articles/10226578)
            
    4. socket
### Installation Web-Driver

**Chrome-driver** is the driver of browser google-chrome, the version must be the same with your browser

1. Download Google-Chrome browser：
    
    ```powershell
    $ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    $ dpkg -i google-chrome-stable_current_amd64.deb
    $ apt-get -f install
    ```
    
2. Check Google-Chrome browser version
    
    ```powershell
    $ google-chrome --version
    ```
    
3. Install Chrome-driver with the same browser version
    - [Download site of chrome-driver](https://chromedriver.chromium.org/downloads)
    
    ```powershell
    $ wget http://chromedriver.storage.googleapis.com/ `version` /chromedriver_linux64.zip
    $ unzip chromedriver_linux64.zip
    $ chmod +x chromedriver
    $ mv chromedriver /usr/local/bin/ -> set your enviornment path
    ```
    
## Process

The direct logic of image crawler was: 

1. Open the browser. 
   ![178393327-1f951b5f-0081-4bac-b8ef-9ffabdab33f9](https://user-images.githubusercontent.com/32357364/178393958-f6afb280-3b1c-453b-812c-c18271002f86.png)
2. Navigate to specific URL and search on it.
   ![2022-07-12 10-16-03 的螢幕擷圖](https://user-images.githubusercontent.com/32357364/178394172-8da15782-3837-454a-b02f-7e263d749ad7.png)
3. Locate input field, emulate user input and enter to search.
   ![image](https://user-images.githubusercontent.com/32357364/178394217-b61a4f42-f54d-4fd2-abcf-cac7360cdf99.png)
4. Find button「圖片」and navigate to google image.
   ![image](https://user-images.githubusercontent.com/32357364/178394251-de2dba3e-3962-4515-b96c-ac97a73ced47.png)
5. Scrolling to the bottom of web-page and load more images as many as possible.
   ![image](https://user-images.githubusercontent.com/32357364/178394318-4c4ec61d-6fc2-4227-878d-418ede1757ec.png)
6. Find all image elements in result web-page. And click each thumbnail to get the URL to download it.
   ![image](https://user-images.githubusercontent.com/32357364/178394383-bd4d7da7-479a-47da-a62a-c7cc716de403.png)
7. Collect the suggest links and click each link to collect more images.
   ![image](https://user-images.githubusercontent.com/32357364/178394438-df562b96-2a1c-44c0-bc7d-361a06345e46.png)
8. Then finish it.

## Usage

```python
python image_crawler.py --save_path "./images" --keyword "吉娃娃"
```

### Main code

```python
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
    parser.add_argument('--explorer', default="Chrome", type=str)
    parser.add_argument('--save_path', default="./images", type=str, required=True)
    parser.add_argument('--keyword', default="柴犬", type=str, required=True)
    args = parser.parse_args()

    main(args.url, args.explorer, args.save_path, args.keyword)
```

#### Input

- `url`：The specific URL to search on it
- `explorer`：The explorer classes
- `save_path`：The download path
- `keyword`：Search keyword



## [Solved] Bug of selenium：

### ****Message: element click intercepted: Element is not clickable at point(xx, xx). Other element would receive the click****

#### Problem

- **Click** the thumbnail to image is not work

```python
imgs = self.driver.find_elements_by_class_name('rg_i')
img_count = 0
for img in imgs:
    try:
        img.click() # 點開大圖
```

- Error message

```python
selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element is not clickable at point(xx, xx). Other element would receive the click
```

#### Solution

- 使用execute_script()功能，程式碼如下。並注意在find_elements_by_xpath(”path”).click()的.click()需要去掉，否則仍會報錯。

```python
imgs = self.driver.find_elements_by_class_name('rg_i')
img_count = 0
for img in imgs:
    try:
        self.driver.execute_script("arguments[0].click();", img) # 點選大圖
```

## Reference

- [https://yanwei-liu.medium.com/python爬蟲學習筆記-二-selenium自動化-ab0a27a94ff2](https://yanwei-liu.medium.com/python%E7%88%AC%E8%9F%B2%E5%AD%B8%E7%BF%92%E7%AD%86%E8%A8%98-%E4%BA%8C-selenium%E8%87%AA%E5%8B%95%E5%8C%96-ab0a27a94ff2)
- [https://linyencheng.github.io/2021/10/05/python-crawler/](https://linyencheng.github.io/2021/10/05/python-crawler/)
- [https://pythonmana.com/2021/12/202112182358440092.html](https://pythonmana.com/2021/12/202112182358440092.html)
- [https://blog.csdn.net/qq_34687559/article/details/106340929](https://blog.csdn.net/qq_34687559/article/details/106340929)
- [https://www.cnblogs.com/lh4217/p/15181934.html](https://www.cnblogs.com/lh4217/p/15181934.html)
- [https://medium.com/企鵝也懂程式設計/python爬蟲-python-selenium-自動化爬取大量圖片-a35d3c89c6d1](https://medium.com/%E4%BC%81%E9%B5%9D%E4%B9%9F%E6%87%82%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88/python%E7%88%AC%E8%9F%B2-python-selenium-%E8%87%AA%E5%8B%95%E5%8C%96%E7%88%AC%E5%8F%96%E5%A4%A7%E9%87%8F%E5%9C%96%E7%89%87-a35d3c89c6d1)
- [https://jason-chen-1992.weebly.com/home/python](https://jason-chen-1992.weebly.com/home/python)
- [https://python-bloggers.com/2022/05/automating-and-downloading-google-chrome-images-with-selenium/](https://python-bloggers.com/2022/05/automating-and-downloading-google-chrome-images-with-selenium/)
- [https://medium.com/analytics-vidhya/a-simple-selenium-image-scrape-from-an-interactive-google-image-search-on-mac-45d403e60d9a](https://medium.com/analytics-vidhya/a-simple-selenium-image-scrape-from-an-interactive-google-image-search-on-mac-45d403e60d9a)
- [https://ladvien.com/scraping-internet-for-magic-symbols/](https://ladvien.com/scraping-internet-for-magic-symbols/)
- [https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d](https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d)
- [https://medium.com/geekculture/scrape-google-images-with-python-f9a20cda1355](https://medium.com/geekculture/scrape-google-images-with-python-f9a20cda1355)
