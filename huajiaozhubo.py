# __author__ = 'Administrator'
#coding:utf-8
from bs4 import BeautifulSoup
import re
import urllib2
import sys
def filterLiveIds(url):
     html = urllib2.urlopen(url)
     liveIds = set()
     bsObj = BeautifulSoup(html, "html.parser")
     for link in bsObj.findAll("a", href=re.compile("^(/l/)")):
         if 'href' in link.attrs:
             newPage = link.attrs['href']
             liveId = re.findall("[0-9]+", newPage)
             liveIds.add(liveId[0])
     return liveIds
 # get user id from live page
 def getUserId(liveId):
     html = urllib2.urlopen("http://www.huajiao.com/" + "l/" + str(liveId))
     bsObj = BeautifulSoup(html, "html.parser")
     text = bsObj.title.get_text()
     res = re.findall("[0-9]+", text)
     return res[0]
 #  get user data from user page

def getUserData(userId):
     html = urllib2.urlopen("http://www.huajiao.com/user/" + str(userId))
     bsObj = BeautifulSoup(html, "html.parser")
     data = dict()
     try:
         userInfoObj = bsObj.find("div", {"id":"userInfo"})
         data['FAvatar'] = userInfoObj.find("div", {"class": "avatar"}).img.attrs['src']
         userId = userInfoObj.find("p", {"class":"user_id"}).get_text()
         data['FUserId'] = re.findall("[0-9]+", userId)[0]
         tmp = userInfoObj.h3.get_text('|', strip=True).split('|')
         #print(tmp[0].encode("utf-8"))
         data['FUserName'] = tmp[0]
         data['FLevel'] = tmp[1]
         tmp = userInfoObj.find("ul", {"class":"clearfix"}).get_text('|', strip=True).split('|')
         data['FFollow'] = tmp[0]
         data['FFollowed'] = tmp[2]
         data['FSupported'] = tmp[4]
         data['FExperience'] = tmp[6]
         return data
     except AttributeError:
         #traceback.print_exc()
         print(str(userId) + ":html parse error in getUserData()")
         return 0
# get user history lives

def getUserLives(userId):
     try:
         url = "http://webh.huajiao.com/User/getUserFeeds?fmt=json&amp;uid=" + str(userId)
         html = urllib2.urlopen(url).read().decode('utf-8')
         jsonData = json.loads(html)
         if jsonData['errno'] != 0:
             print(str(userId) + "error occured in getUserFeeds for: " + jsonData['msg'])
             return 0
         return jsonData['data']['feeds']
     except Exception as e:
         print(e)
         return 0

# spider user ids

def spiderUserDatas():
    for liveId in getLiveIdsFromRecommendPage():
        userId = getUserId(liveId)
        userData = getUserData(userId)
        if userData:
            replaceUserData(userData)
    return 1

# spider user lives

def spiderUserLives():
    userIds = selectUserIds(100)
    for userId in userIds:
        liveDatas = getUserLives(userId[0])
        for liveData in liveDatas:
            liveData['feed']['FUserId'] = userId[0]
            replaceUserLive(liveData['feed'])
    return 1

def main(argv):
    if len(argv) < 2:
        print("Usage: python3 huajiao.py [spiderUserDatas|spiderUserLives]")
        exit()
    if (argv[1] == 'spiderUserDatas'):
        spiderUserDatas()
    elif (argv[1] == 'spiderUserLives'):
        spiderUserLives()
    elif (argv[1] == 'getUserCount'):
        print(getUserCount())
    elif (argv[1] == 'getLiveCount'):
        print(getLiveCount())
    else:
        print("Usage: python3 huajiao.py [spiderUserDatas|spiderUserLives|getUserCount|getLiveCount]")
if __name__ == '__main__':
    main(sys.argv)