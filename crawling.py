import time
import csv
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd


## CHECK START TIME
start = time.time()       # 시작 시간 (전체 수행시간을 구하기 위함)

driver = wd.Chrome(executable_path="/Users/jiyeonhwang/Downloads/chromedriver")

# INPUT YOUTUBE URL
url = "https://www.youtube.com/watch?v=AWd8VNd0l_Y"       # 댓글 수집할 Youtube URL입력
driver.get(url)

last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.0)       # 인터발 1이상으로 줘야 데이터 취득가능(롤링시 데이터 로딩 시간 때문)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height

html_source = driver.page_source
driver.close()

# HTML 태크 크롤링 작업
soup = BeautifulSoup(html_source, "lxml")

youtube_user_IDs = soup.select("div#header-author > a > span")
youtube_comments = soup.select("yt-formatted-string#content-text")

str_youtube_userIDs = []   # USER ID 배열
str_youtube_comments = []  # USER 댓글 내용 배열

# REPLACE DATA
for i in range(len(youtube_user_IDs)):
    str_tmp = str(youtube_user_IDs[i].text)
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace('   ','')
    str_youtube_userIDs.append(str_tmp)

    str_tmp = str(youtube_comments[i].text)
    str_tmp = str_tmp.replace('\n', '')
    str_tmp = str_tmp.replace('\t', '')
    str_tmp = str_tmp.replace('   ','')
    str_youtube_comments.append(str_tmp)

    ## MODIFY VIEW FORMAT
    pd_data = {"ID": str_youtube_userIDs, "comment": str_youtube_comments}
    youtube_pd = pd.DataFrame(pd_data)

    ## WRITE TO EXCEL
    youtube_pd.to_excel("~/Documents/crawling/data1.csv", sheet_name="sheet1", index=True)
    print("Running Time : ", time.time() - start)  # 전체 수행 시킨 출력