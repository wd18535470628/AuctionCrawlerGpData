#coding=utf-8
'''
Created on 2018-4-9

@author: Administrator
'''
from bs4 import BeautifulSoup
from lxml import etree
import re
import urllib2
import random
from mysql import Mysql
import httplib
import ssl
import socket
import time,datetime
import sys
reload(sys) 
#print 'code:'+sys.getdefaultencoding()
sys.setdefaultencoding('utf8')

class CrawlerData:
    circleList = ['1','2','3','4']
    def getPage(self,url):
        user_agent = '"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(req).read()
        return html
    def getPageNum(self,url):
        page = self.getPage(url)
        pattern = re.compile(r'class="page-infos"><label>(.*?)</label>')
        item = re.findall(pattern, page.decode('utf8'))
        if item.__len__() != 0:
            pageNum = item[0][1:2]
        else:
            pageNum = 1
        return pageNum
    def getLabel(self,url):
        page = self.getPage(url)
        labelList = re.findall(re.compile(r'<label>(.*?)</label>'), page.decode('utf8'))
        return labelList
    def getDataList(self,url,court_id,kind):
        jsonData = {}
        html = self.getPage(url)
        et = etree.HTML(html)
        #拍卖模式
        paimaiModel = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[1]/td[1]/text()')
        jsonData['paimai_model'] = ""
        if paimaiModel.__len__()!=0:
            paimai_model = paimaiModel[0]
            len = paimai_model.__len__()
            if len>7:
                jsonData['paimai_model'] = paimai_model[7:]
                #print 'paimai_model:'+jsonData['paimai_model']
            else:
                jsonData['paimai_model'] = paimai_model[5:]
                #print 'paimai_model:'+jsonData['paimai_model']  
        #拍卖次数或者是变卖期
        paimaiTimes = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[1]/td[2]/text()')
        jsonData['selling_period'] = ""
        jsonData['paimai_times'] = ""
        if paimaiTimes.__len__()!=0:
            paimai_times = paimaiTimes[0]
            if str(jsonData['paimai_model'].encode('utf-8')) == '变卖':
                jsonData['selling_period'] = paimai_times[4:]
                #print 'selling_period:' + jsonData['selling_period']
            else:
                jsonData['paimai_times'] = paimai_times[5:]
                #print 'paimai_times:'+jsonData['paimai_times']
        #拍卖方式
        paimaiType = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[1]/td[3]/text()')
        jsonData['paimai_type'] = ""
        if paimaiType.__len__()!=0:
            paimai_type = paimaiType[0]
            jsonData['paimai_type'] = paimai_type[5:]
            #print 'paimai_type:'+jsonData['paimai_type']
        #在线拍周期或者是竞价期
        onlineCycle = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[2]/td[1]/text()')
        jsonData['online_cycle'] = ""
        if onlineCycle.__len__()!=0:
            online_cycle = onlineCycle[0]
            len = online_cycle.__len__()
            if len>8:
                jsonData['online_cycle'] = online_cycle[6:]
                #print 'online_cycle:'+jsonData['online_cycle']
            else:
                jsonData['online_cycle'] = online_cycle[4:]
                #print 'online_cycle:'+jsonData['online_cycle']
        #延时周期
        delayCycle = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[2]/td[2]/text()')
        jsonData['delay_cycle'] = ""
        if delayCycle.__len__()!=0:
            delay_cycle = delayCycle[0]
            jsonData['delay_cycle'] = delay_cycle[5:]
            #print 'delay_cycle:'+jsonData['delay_cycle']
        #加价幅度
        fareIncrease = re.findall(re.compile(r'<span id="Price_Step">(.*?)</span>', re.S), html.decode('utf-8'))
        jsonData['fare_increase'] = ""
        if fareIncrease.__len__()!=0:
            fare_increase = fareIncrease[0]
            jsonData['fare_increase'] = fare_increase
            #print 'fare_increase:'+jsonData['fare_increase']
        #起拍价
        startPrice = re.findall(re.compile(r'<span id="Price_Start">(.*?)</span>', re.S), html.decode('utf-8'))
        jsonData['start_price'] = ""
        if startPrice.__len__()!=0:
            start_price = startPrice[0]
            jsonData['start_price'] = start_price
            #print 'start_price:'+jsonData['start_price']
        jsonData['cash_deposit'] = ""
        jsonData['payment_advance'] = ""
        if str(jsonData['paimai_model'].encode('utf-8')) == '变卖':
            #变卖预缴款
            paymentAdvance = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[3]/td[2]/text()')
            #保证金
            cashDeposit = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[3]/td[3]/text()')
            if paymentAdvance.__len__() !=0:
                payment_advance = paymentAdvance[0]
                cash_deposit = cashDeposit[0]
                jsonData['cash_deposit'] = cash_deposit[4:].replace(",","")
                jsonData['payment_advance'] = payment_advance[6:].replace(",","")
                #print 'payment_advance:'+jsonData['payment_advance']
                #print 'cash_deposit:'+jsonData['cash_deposit']           
        else:
            #保证金
            cashDeposit = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[3]/td[2]/text()')
            if cashDeposit.__len__()!=0:
                cash_deposit = cashDeposit[0]
                jsonData['cash_deposit'] = cash_deposit[4:].replace(",","")
                #print 'cash_deposit:'+jsonData['cash_deposit']
        #评估价
        accessPrice = et.xpath('//div[@class="d-m-tb"]/table[1]/tr[4]/td[1]/text()')
        jsonData['access_price'] = ""
        if accessPrice.__len__()!=0:
            access_price = accessPrice[0]
            jsonData['access_price'] = access_price[4:].replace(",","")
            #print 'access_price:'+jsonData['access_price']
        #标的物名称
        titleList = re.findall(re.compile(r'class="d-m-title"><b>(.*?)</b>', re.S), html.decode('utf-8'))
        jsonData['title'] = ""
        if titleList.__len__()!=0:
            title = titleList[0]
            jsonData['title'] = title
            #print 'title:'+jsonData['title']
        #报名人数
        enrollMment = et.xpath('//div[@class="peoples-infos"]/span[1]/b[1]/text()')
        jsonData['enrollment'] = ""
        if enrollMment.__len__()!=0:
            enrollment = enrollMment[0]
            jsonData['enrollment'] = enrollment
            #print 'enrollment:' +jsonData['enrollment']
        #提醒人数
        setReminders = et.xpath('//div[@class="peoples-infos"]/span[2]/b[1]/text()')
        jsonData['set_reminders'] = ""
        if setReminders.__len__()!=0:
            set_reminders = setReminders[0]
            jsonData['set_reminders'] = set_reminders
            #print 'set_reminders:'+jsonData['set_reminders']
        #围观人数
        onLookers = et.xpath('//div[@class="peoples-infos"]/span[3]/b[1]/text()')
        jsonData['onlookers'] = ""
        if onLookers.__len__()!=0:
            onlookers = onLookers[0]
            jsonData['onlookers'] = onlookers
            #print 'onlookers:'+jsonData['onlookers']
        #处置法院
        courtName = re.findall(re.compile(r"<td nowrap class='pr7'>(.*?)</td>", re.S), html.decode('utf-8'))
        jsonData['court_name'] = ""
        if courtName.__len__()!=0:
            court_name = courtName[0]
            jsonData['court_name'] = court_name[5:]
            #print 'court_name:'+jsonData['court_name']
        #联系人
        corporateAgent = re.findall(re.compile(r"<td valign='top'>(.*?)</td>", re.S), html.decode('utf-8'))
        jsonData['corporate_agent'] = ""
        if corporateAgent.__len__()!=0:
            corporate_agent = corporateAgent[0]
            jsonData['corporate_agent'] = corporate_agent[4:]
            #print 'corporate_agent:'+jsonData['corporate_agent']
        #联系电话
        Phone = re.findall(re.compile(r"<td colspan='2'>(.*?)</td>", re.S), html.decode('utf-8'))
        jsonData['phone'] = ""
        if Phone.__len__()!=0:
            phone = Phone[0]
            jsonData['phone'] = phone[5:]
            #print 'phone:'+jsonData['phone']
        #竞买记录
        biddingRecord = re.findall(re.compile(r"id='html_Bid_Shu'>(.*?)</span>", re.S), html.decode('utf-8'))
        jsonData['bidding_record'] = ""
        if biddingRecord.__len__()!=0:
            bidding_record = biddingRecord[0]
            if bidding_record == "":
                jsonData['bidding_record'] = '0'
                #print 'bidding_record:'+jsonData['bidding_record']
            else:
                jsonData['bidding_record'] = bidding_record
                #print 'bidding_record:'+jsonData['bidding_record']
        #成交价或当前价
        currentPrice = re.findall(re.compile(r"<b class='price-red'>(.*?)</b>", re.S), html.decode('utf-8'))
        jsonData['current_price'] = ""
        if currentPrice.__len__()!=0:
            current_price = currentPrice[0]
            jsonData['current_price'] = current_price
            #print 'current_price:'+jsonData['current_price']
        #标的物地址
        jsonData['url'] = url
        #更新时间
        jsonData['data_time'] = dataTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #标的物id
        jsonData['auction_id'] = url[44:]
        #法院id
        jsonData['court_id'] = court_id
        #标的物类型
        jsonData['kind_id'] = kind
        return jsonData
    def getItemHtml(self,url,court_id,kind):
        Itemhtml = self.getPage(url)
        urlList = re.findall(re.compile(r'<a href="(.*?)item2.do?(.*?)"><img'), Itemhtml.decode('utf8'))
        for urls in urlList:
            url = 'http://www.gpai.net/sf/item2.do'+urls[1]
            jsonData = self.getDataList(url,court_id,kind)
            mysql.insertData(jsonData)
            #print url
            #print jsonData
    def getData(self):
        for court in mysql.getCourtList():
            print court[2] + "开始爬取"
            for kind in mysql.getKindList():
                for circle in self.circleList:
                    urlForPageNum = 'http://www.gpai.net/sf/court.do?id=' + court[1] + '&at=' + kind[1] + '&restate=' + circle
                    label = self.getLabel(urlForPageNum)
                    if int(label[0])>0:
                        for i in range(1, int(self.getPageNum(urlForPageNum)) + 1):
                         url = urlForPageNum+'&page=' + str(i)
                         #print url
                         itemUrlList = self.getItemHtml(url,court[1],kind[1])
                print court[2] + "抓取完成"
crawlerData = CrawlerData()    
mysql = Mysql()
crawlerData.getData()  
        
        
        
        
        
        