#coding=utf-8
'''
Created on 2018-3-26

@author: Administrator
'''
import re
import urllib2
class auctionGpDrawler:
    def getData(self):
        url = 'http://www.gpai.net/sf/courtList.do'
        html = self.getPage(url)
        dataList = re.findall(re.compile(r'<a href="court.do?(.*?)" target="_blank">', re.S), html.decode('utf-8'))
        data = dataList[0]
        court_id = data[12:]
        return dataList
    def getPage(self,url):
      req = urllib2.Request(url)
      html = urllib2.urlopen(req).read()
      return html
    def getCourt(self):
        dataList = self.getData()
        for datas in dataList:
            print datas
        print dataList
        print dataList[0]
        print '--------'
        print dataList[1]
        print '+++++++++'
        print dataList[2]
        #url = "http://www.gpai.net/sf/court.do" + data
        #html = self.getPage(url)
        #courtName = re.findall(re.compile(r"<span class='searchtitle'>(.*?)</span>", re.S), html.decode('utf-8'))
#str1='<a href="court.do?id=4154" target="_blank">新疆维吾尔自治区伊犁哈萨克自治州阿勒泰地区中级人民法院  (2)</a></dt>'
#url = "http://www.gpai.net/sf/" + data
#req = urllib2.Request(url)
#html = urllib2.urlopen(req).read()
#courtName = re.findall(re.compile(r"<span class='searchtitle'>(.*?)</span>", re.S), html.decode('utf-8'))
#print data
#print court_id
#print courtName[0]
#print html
if __name__ == '__main__':
    auction = auctionGpDrawler()
    auction.getCourt()
    









