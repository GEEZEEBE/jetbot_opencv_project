# Scraping_google.py

from google_images_download import google_images_download as google
from selenium import webdriver
import ssl, os
ssl._create_default_https_context = ssl._create_unverified_context


def google_image(keyword, dir):
    response = google.googleimagesdownload()
    arguments = {'keywords': keyword,
                 'limit': 500,
                 'print_urls': False,
                 'no_directory' : True,
                 'output_directory': dir,
                 'chromedriver':'/home/cloudera/Documents/Develop/chromedriver' # chromedriver 위치
                 }
    response.download(arguments)


def test(keywords):
    cwd = os.getcwd()
    for keyword in keywords:
        dir = cwd + f"/{keyword}" #파일 저장 폴더명

        if not os.path.exists(dir):
            os.mkdir(dir)
        google_image(keyword, dir)


def main():
    keywords = ['circle red sign', 'crosswalk'] #검색할 이미지 (구글 검색어), 변경/단독 혹은 나열 가능
    test(keywords)

main()
