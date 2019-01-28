import errno
import os
import os.path
import time
import urllib.request

import magic
import progressbar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SeleniumScraper:
    def __init__(self, driver='Chromium', path_driver=None, dest='.', quality='min', limit=0, google=True, pexel=False, imgur=False):
        self.driver = driver
        self.path_driver = path_driver

        if dest == "." or dest == "./":
            self.dest = ""
        else:
            if dest.endswith("/") is False:
                dest += "/"
            self.dest = dest

        self.quality = quality

        if limit == 0:
            self.limit = 100000
        else:
            self.limit = limit
        self.google = google
        self.pexel = pexel
        self.imgur = imgur
        self.urls = []
        self.nb_img_scraped = 0
        pass

    @staticmethod
    def init_driver(str_driver, path=None):
        try:
            if str_driver == 'Chromium':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('headless')
                driver = webdriver.Chrome(
                    options=chrome_options,
                    executable_path=path if path is not None else "chromedriver")
            elif str_driver == 'Chrome':
                driver = webdriver.Chrome(executable_path=path if path is not None else "chromedriver")
            elif str_driver == 'Firefox':
                driver = webdriver.Firefox(executable_path=path if path is not None else "geckodriver")
            elif str_driver == 'PhantomJS':
                driver = webdriver.PhantomJS(executable_path=path if path is not None else "phantomjs")
            elif str_driver == 'Safari':
                driver = webdriver.Safari(executable_path=path if path is not None else "/usr/bin/safaridriver")
            else:
                print('Driver not yet supported.')
                raise Exception
        except Exception as e:
            raise e
        return driver

    @staticmethod
    def init_progressbar(title, maxval, min_value=-1):
        bar = progressbar.ProgressBar(maxval=maxval, min_value=min_value,
                                      widgets=[progressbar.Bar('=', title + ' [', ']'), ' ', progressbar.Percentage()])
        return bar

    def scroll_until_limit(self, driver, selector=None):
        # ----------------------------
        # Region scroll to the end
        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
        # ----------------------------
        scroll_limit_pause = 0.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(scroll_limit_pause)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:  # Click on the more result button
                    driver.find_element_by_xpath('//*[@id="smb"]').click()
                except:
                    break
            last_height = new_height

            if selector is not None:
                if len(driver.find_elements_by_css_selector(selector)) > self.limit:
                    break
        # ----------------------------
        # End region
        # ----------------------------

    def download_all(self, directory, my_file):
        # Bug Forbidden 403 for pexel
        # WORKARROUND depreciation AppURLopener()
        # https://code.i-harness.com/en/q/2115ba9
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        # End bug

        self.my_mkdir(directory)
        i = 0
        str_index = 0
        num_lines = sum(1 for line in open(my_file))
        bar = self.init_progressbar(str(num_lines - 1) + ' from all websites to download ...', num_lines)
        bar.start()
        with open(my_file, "r+") as f:
            for ibar, line in enumerate(f):
                file_name = directory + '/' + str(i)
                while os.path.exists(file_name):
                    i += 100
                    file_name = file_name.replace(str(i - 100), str(i))
                try:
                    urllib.request.urlretrieve(line, file_name)
                except Exception:
                    if line.__contains__("Step Done."):
                        pass
                    # else:
                    #     print("Error: ", line)
                    #     print(e)
                    pass
                bar.update(ibar + 1)
                i += 1
            bar.finish()
        # section rename files with right extension
        files = os.listdir(directory)
        nb_files = len(files)
        for i, name in enumerate(files):
            extension = magic.from_file(directory + '/' + name).partition(" ")[0].lower()
            if name.__contains__(extension) is True:
                nb_files -= 1
                continue
            path_file_name = directory + '/' + name + "." + extension
            while os.path.exists(path_file_name) is True:
                path_file_name = directory + '/' + name + str(str_index) + "." + extension
                str_index += 1
            os.rename(directory + '/' + name, path_file_name)
        return nb_files

    @staticmethod
    def check_step_done(step, file_name):
        if step == "url_img" and os.path.exists(file_name) is True:
            with open(file_name, "r") as text_file:
                if text_file.readlines()[-1].__contains__("Step Done."):
                    return True
        if step == "download_img" and os.path.exists(file_name + ".done"):
            return True
        # if step == "resize_img" and os.path.exists("r_" + file_name + ".done"):
        #     return True
        return False

    @staticmethod
    def write_in_file(file_name, dict_data):
        with open(file_name, 'a+') as text_file:
            for data in dict_data:
                print("{}".format(data), file=text_file)
            print("Step Done.", file=text_file)

    @staticmethod
    def my_mkdir(path):
        if path == "":
            return
        try:
            os.makedirs(path)
            print("Directory ", path, " created.")
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def my_append(self, mylist, val):
        try:
            if val not in mylist:
                mylist.append(val)
                self.nb_img_scraped += 1
        except:
            pass
        return mylist

    def google_search(self, driver, category, quality='min'):
        list_url = []
        url = "https://images.google.com/?hl=fr"
        driver.get(url)
        driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[1]/input').send_keys(category)
        driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[1]/input').send_keys(Keys.RETURN)

        self.scroll_until_limit(driver, '.rg_ic.rg_i')

        img_s = driver.find_elements_by_css_selector('.rg_ic.rg_i')

        if len(img_s) <= 0:
            print("No image found. Something wired happened...")
            return []

        if len(img_s) * 7 > self.limit:
            nb_img_to_scrap = self.limit
        else:
            nb_img_to_scrap = len(img_s) * 7
        # ----------------------------
        # Min quality Operation
        # ----------------------------
        if quality == 'min':
            bar = self.init_progressbar("ggsearch : " + str(nb_img_to_scrap) + " elements to scrap ... ", len(img_s) - 1)
            bar.start()
            for i, img in enumerate(img_s):
                try:
                    img.click()
                    card_imgs_s = driver.find_elements_by_css_selector('.irc_rii')
                    for card_img in card_imgs_s:
                        try:
                            if self.nb_img_scraped >= self.limit:
                                break
                            list_url = self.my_append(list_url, card_img.get_attribute('src'))
                        except:
                            pass
                    try:
                        if self.nb_img_scraped >= self.limit:
                            break
                        list_url = self.my_append(list_url, img.get_attribute('src'))
                    except:
                        pass
                except:
                    pass
                bar.update(i)
            bar.finish()
        # ----------------------------
        # End Operation
        # ----------------------------

        # ----------------------------
        # Max quality Operation : long operation
        # ----------------------------
        if quality == 'max':
            bar = self.init_progressbar("ggsearch : " + str(nb_img_to_scrap) + " elements to scrap ... ", len(img_s) - 1)
            bar.start()
            for img in img_s:
                dothis = True
                try:
                    img.click()
                except:
                    dothis = False
                card_imgs_s = driver.find_elements_by_css_selector('.irc_rii')
                for index, card_img in enumerate(card_imgs_s):
                    if index == 7:
                        # card_imgs_s got 8 elements, the last one is "more result"
                        break
                    dothis2 = True
                    try:
                        card_img.click()
                    except:
                        dothis2 = False

                    if dothis2 is True:
                        card_imgs_selected = driver.find_elements_by_css_selector('.irc_mi')
                        for card_img_selected in card_imgs_selected:
                            try:
                                if self.nb_img_scraped >= self.limit:
                                    break
                                list_url = self.my_append(list_url, card_img_selected.get_attribute('src'))
                            except:
                                pass

                # Get the main clicked image
                if dothis is True:
                    selected_imgs = driver.find_elements_by_css_selector('.irc_mi')
                    for selected_img in selected_imgs:
                        try:
                            if self.nb_img_scraped >= self.limit:
                                break
                            list_url = self.my_append(list_url, selected_img.get_attribute('src'))
                        except:
                            pass
            bar.finish()
        # ----------------------------
        # End Operation
        # ----------------------------
        return list(set(list_url))

    def imgur_search(self, driver, category):
        list_url = []
        url = 'https://imgur.com/search?q=' + category
        driver.get(url)

        self.scroll_until_limit(driver, '.image-list-link img')
        images = driver.find_elements_by_css_selector('.image-list-link img')
        if len(images) <= 0:
            print("No image found. Something wired happened...")
            return []
        if len(images) > self.limit:
            nb_img_to_scrap = self.limit
        else:
            nb_img_to_scrap = len(images)
        bar = self.init_progressbar("imgur_search : " + str(nb_img_to_scrap) + " elements to scrap ... ", len(images) - 1)
        bar.start()
        for image in images:
            if self.nb_img_scraped >= self.limit:
                break
            src = image.get_attribute('src')
            src = src[:27] + src[28:]  # miss the b to get the right link
            list_url = self.my_append(list_url, src)
        bar.finish()
        return list(set(list_url))

    def pexel_search(self, driver, category, quality='min'):
        list_url = []
        url = 'https://www.pexels.com/search/' + category
        driver.get(url)
        self.scroll_until_limit(driver, '.photo-item__img')
        images = driver.find_elements_by_css_selector('.photo-item__img')
        if len(images) <= 0:
            print("No image found. Something wired happened...")
            return []
        if len(images) > self.limit:
            nb_img_to_scrap = self.limit
        else:
            nb_img_to_scrap = len(images)
        bar = self.init_progressbar("pexel_search : " + str(nb_img_to_scrap) + " elements to scrap ... ", len(images) - 1)
        bar.start()
        if quality == 'max':
            for image in images:
                if self.nb_img_scraped >= self.limit:
                    break
                list_url = self.my_append(list_url, image.get_attribute('data-big-src'))
        if quality == 'min':
            for image in images:
                if self.nb_img_scraped >= self.limit:
                    break
                list_url = self.my_append(list_url, image.get_attribute('src'))
        bar.finish()
        return list(set(list_url))

    @staticmethod
    def count_files(path):
        files = os.listdir(path)
        return len(files)

    def begin_scrap(self, category):
        self.my_mkdir(self.dest)
        categories = []
        nb_downloads = []
        nb_dl = 0
        if type(category) is not list:
            categories.append(category)
        else:
            categories = category

        driver = self.init_driver(self.driver, self.path_driver)
        for category in categories:
            directory_name = self.dest + category.replace(' ', '_') + "_" + self.quality
            file_name = category.replace(' ', '_') + "_" + self.quality + ".txt"
            if not self.check_step_done("url_img", file_name):
                print("\nCreation of ", file_name, " ... ")

                if self.google is True:
                    self.nb_img_scraped = 0
                    self.urls = self.google_search(driver, category, self.quality)
                if self.pexel is True:
                    self.nb_img_scraped = 0
                    self.urls += self.pexel_search(driver, category, self.quality)
                if self.imgur is True:
                    self.nb_img_scraped = 0
                    self.urls += self.imgur_search(driver, category)
                self.write_in_file(file_name, self.urls)
            else:
                print(file_name, " ... OK")
            nb_dl = self.download_all(directory_name, file_name)

            os.remove(file_name)
            nb_downloads.append(nb_dl)
        driver.close()
        return nb_downloads if len(nb_downloads) > 1 else nb_dl
