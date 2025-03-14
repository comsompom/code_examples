# pylint: disable=E0401
# pylint: disable=W0718
# pylint: disable=R0914
# pylint: disable=R1732
"""Dowloader module for download images"""
import os
import time
import urllib
from urllib.parse import quote
import requests
from constants import TIME_SLEEP_AFTER_EACH_DOWNLOAD


class Downloader:
    """Main Downloader class"""
    def __init__(self, main_dir_name):
        self.main_dir_name = main_dir_name

    def urls(self, keywords, limit):
        """Process for preparing urls to download"""
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        i = 0
        links = []
        while i < len(keyword_to_search):
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode(
                    'utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=' \
                                'ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:' \
                                '1581168823770&source=lnms&sa=X&ved=' \
                                '0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)
            end_object = -1
            j = 0
            while j < limit:
                while True:
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffer = raw_html.find('\\', new_line + 1, end_object)
                        if buffer != -1:
                            object_raw = raw_html[new_line + 1:buffer]
                        else:
                            object_raw = raw_html[new_line + 1:end_object]

                        if '.jpg' in object_raw \
                                or 'png' in object_raw \
                                or '.ico' in object_raw \
                                or '.gif' in object_raw \
                                or '.jpeg' in object_raw:
                            break
                    except Exception as e:
                        print(e)
                        break

                links.append(object_raw)
                j += 1
            i += 1
        return links

    def download(self, keywords, limit):
        """downloader method"""
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        main_directory = f"{self.main_dir_name}/"
        i = 0

        while i < len(keyword_to_search):
            self._create_directories(main_directory, keyword_to_search[i])
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode('utf-8')) + '&biw=1536&bih=674&tbm' \
                                                        '=isch&sxsrf=ACYBGNSXXpS6' \
                                                        'YmAKUiLKKBs6xWb4uUY5gA:1581' \
                                                        '168823770&source=lnms&sa=' \
                                                        'X&ved=0ahUKEwioj8jwiMLnAh' \
                                                        'W9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)
            end_object = -1
            j = 0
            while j < limit:
                while True:
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffer = raw_html.find('\\', new_line + 1, end_object)
                        if buffer != -1:
                            object_raw = raw_html[new_line+1:buffer]
                        else:
                            object_raw = raw_html[new_line+1:end_object]

                        if '.jpg' in object_raw \
                                or 'png' in object_raw \
                                or '.ico' in object_raw \
                                or '.gif' in object_raw \
                                or '.jpeg' in object_raw:
                            break
                    except Exception as e:
                        print(e)
                        break

                path = main_directory + keyword_to_search[i]

                if not os.path.exists(path):
                    os.makedirs(path)
                # change the file name for right labels
                filename = str(keyword_to_search[i]).replace(" ", "_") + "_" + str(j + 1) + ".jpg"

                try:
                    r = requests.get(object_raw, allow_redirects=True)
                    with open(os.path.join(path, filename), 'wb') as obj_img_file:
                        obj_img_file.write(r.content)
                    time.sleep(TIME_SLEEP_AFTER_EACH_DOWNLOAD)
                except Exception as e:
                    print(e)
                    j -= 1
                j += 1
            i += 1

    def _create_directories(self, main_directory, path):
        """private method for creating the directories for images"""
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
        except OSError as e:
            if e.errno != 17:
                raise

    def _download_page(self, url):
        """private method to download the one page"""
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 " \
                                    "(KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            resp_data = str(resp.read())
            return resp_data
        except Exception as e:
            print(e)
            exit(0)
