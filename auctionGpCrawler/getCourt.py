#coding=utf-8
'''
Created on 2018-3-26

@author: Administrator
'''
import re
import urllib2
from mysql import Mysql
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
    def getCountName(self,id):
        url = 'http://www.gpai.net/sf/court.do' + id
        html = self.getPage(url)
        courtName = re.findall(re.compile(r"<span class='searchtitle'>(.*?)</span>", re.S), html.decode('utf-8'))
        return courtName
    def getCourt(self):
        dataList = self.getData()
        for datas in dataList:
            if datas.__len__()>4:
                count_name = self.getCountName(datas)
                court_id = datas[4:]
                court_name = count_name[0]
                sql = 'insert into gp_court_info (court_id,court_name) values ("'+court_id+'","'+court_name+'")'
                #mysql.insertAuctionCourtName(sql)
if __name__ == '__main__':
    mysql = Mysql()
    auction = auctionGpDrawler()
    auction.getCourt()
    court_list = mysql.getCourtList()
    print court_list









