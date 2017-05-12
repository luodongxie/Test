#-*- coding: utf-8 -*-
# from urllib.request import urlopen
# html = urlopen("http://www.baidu.com")
# print(html.read())
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# html = urlopen("http://www.baidu.com")
# bsobj = BeautifulSoup(html.read())
# print(bsobj.html)

# from urllib.request import urlopen
# from urllib.error import HTTPError
# from bs4 import BeautifulSoup


# def getTitle(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         return None
#     try:
#         bsobj = BeautifulSoup(html.read(), "lxml")
#         title = bsobj.body.h1
#     except AttributeError as e:
#         return None
#     return title
# title = getTitle("http://www.pythonscraping.com/pages/page1.html")
# if title == None:
#     print("title could not be found")
# else:
#     print(title)

"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsobj = BeautifulSoup(html, "lxml")
namelist = bsobj.findAll("span", {"class": "green"})
for name in namelist:
    print(name.get_text())
"""
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsobj = BeautifulSoup(html, "lxml")
images = bsobj.findAll(
    "img", {"src": re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for image in images:
    print(image["src"])
"""
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

random.seed(datetime.datetime.now())

pages = set()


def getLinks(articleUrl):
    global pages
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsobj = BeautifulSoup(html, "lxml")
    for link in bsobj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                newPage = link.attrs["href"]
                pages.add(newPage)
                print(newPage)
                getLinks(newPage)
getLinks("/wiki/kevin_Bacon")
"""
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()


def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org" + pageUrl)
    bsobj = BeautifulSoup(html, 'lxml')
    try:
        print(bsobj.h1.get_text())
        print(bsobj.find(id="mv-content-text").findAll("p")[0])
        print(bsobj.find(id="ca-edit").find("span").find("a").attrs["href"])
    except AttributeError:
        print("lack of some attrs ,don't worry!")

    for link in bsobj.findAll("a", herf=re.compile("^(/wiki/)")):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                newPage = link.attrs["href"]
                print("--------------\n" + newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("/wiki/kevin_Bacon")
'''

# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import re

# def getPicLinks(url):
#     html = urlopen(url)
#     bsobj = BeautifulSoup(html, "lxml")
#     links = bsobj.findAll("img", {"src": re.compile("(movie_poster_cover)")})
#     return links
# links = getPicLinks("https://movie.douban.com/")
# path = "./DBPIC/"
# for link in links:
#     # print(".............\n" + link.attrs["src"]+"...."+link.attrs["alt"])
#     web = urlopen(link.attrs["src"])
#     jpg = web.read()
#     filename = link.attrs["alt"] + ".jpg"
#     File = open(path + filename, "wb")
#     File.write(jpg)
#     File.close()

# print(html.read().decode(encoding='utf-8'))

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import os


def getHtml(url):
    try:
        html = urlopen(url).read().decode(encoding='utf-8')
    except HTTPError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(baseurl):
    findTitle = re.compile(r'<span class="title">(.*)</span>')
    findRating = re.compile(
        r'<span class="rating_num" property="v:average">(.*)</span>')
    findImgSrc = re.compile(r'<img.*src="(.*jpg)"', re.S)
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = getHtml(url)
        soup = BeautifulSoup(html, "lxml")
        for item in soup.find_all('div', class_='item'):  # 找到每一个影片项
            data = []
            item = str(item)  # 转换成字符串
            titles = re.findall(findTitle, item)
            # 片名可能只有一个中文名，没有外国名
            # if(len(titles) == 2):
            #     ctitle = titles[0]
            #     data.append(ctitle)  # 添加中文片名
            #     otitle = titles[1].replace(" / ", "")  # 去掉无关符号
            #     data.append(otitle)  # 添加外国片名
            # else:
            #     data.append(titles[0])  # 添加中文片名
            #     data.append(' ')  # 留空
            data.append(titles[0])  # 添加中文片名
            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片链接
            if(len(data) != 3):
                data.insert(8, ' ')  # 留空
            datalist.append(data)
    return datalist


def imgDonload(data):
    FolderName = "./DBTOP250/"
    if os.path.exists(FolderName):
        pass
    else:
        os.mkdir(FolderName)
    for i in range(len(data)):
        picWeb = urlopen(str(data[i][2]))
        jpg = picWeb.read()
        fileName = str(data[i][0]) + "" + str(data[i][1]) + ".jpg"
        File = open(FolderName + fileName, "wb")
        File.write(jpg)
        File.close()

baseurl = 'https://movie.douban.com/top250?start='
datalist = getData(baseurl)
imgDonload(datalist)
