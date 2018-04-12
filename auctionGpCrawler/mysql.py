#coding=utf-8
import MySQLdb
import time
from __builtin__ import str
from _ast import Str

class Mysql:
    # 数据库初始化
    def __init__(self):
        try:
            self.db = MySQLdb.connect('localhost', 'root', 'root', 'gp_info')
            self.cur = self.db.cursor()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "连接数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def insertAuctionCourtName(self,sql):
        try:
            self.db.set_character_set('utf8')
            result = self.cur.execute(sql)
            insert_id = self.db.insert_id()
            self.db.commit()
            print sql
            # 判断是否执行成功
            if result:
                return insert_id
            else:
                return 0
        except MySQLdb.Error, e:
            # 发生错误时回滚
            self.db.rollback()
            # 主键唯一，无法插入
            if "key 'PRIMARY'" in e.args[1]:
                print sql
                print self.getCurrentTime(), "数据已存在，未插入数据"
            else:
                print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
    def getCourtList(self):
        try:
            self.db.set_character_set('utf8')
            #sqlGetData = "select id,court_id,court_name from gp_court_info where id>='3327' and id<='3484'"
            sqlGetData = "select id,court_id,court_name from gp_court_info"
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
    def getKindList(self):
        try:
            self.db.set_character_set('utf8')
            sqlGetData = "select id,auction_type from gp_auction_kind "
            self.cur.execute(sqlGetData)
            return list(self.cur._rows)
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
            exit()
    def insertData(self,jsonDatas):
        try:
            self.db.set_character_set('utf8')
            sqlCheck = 'select count(*) from gp_auction_info where auction_id =' + jsonDatas['auction_id']
            self.cur.execute(sqlCheck) 
            if self.cur._rows[0][0] == 0:
                insertInfo = "insert into %s (%s) VALUES (%s)" % ('gp_auction_info', "auction_id,court_id,title,kind_id,url,start_price,current_price,cash_deposit,payment_advance,access_price,fare_increase,paimai_times,paimai_type,delay_cycle,corporate_agent,phone,selling_period,online_cycle,bidding_record,paimai_model,enrollment,set_reminders,onlookers,data_time",str(jsonDatas['auction_id'])+",'"+str(jsonDatas['court_id'])+"','"+ str(jsonDatas['title'])+"','"+ str(jsonDatas['kind_id'])+"','"+str(jsonDatas['url'])+"','"+str(jsonDatas['start_price'])+"','"+str(jsonDatas['current_price'])+"','"+str(jsonDatas['cash_deposit'])+"','"+str(jsonDatas['payment_advance'])+"','"+str(jsonDatas['access_price'])+"','"+str(jsonDatas['fare_increase'])+"','"+str(jsonDatas['paimai_times'])+"','"+str(jsonDatas['paimai_type'])+"','"+str(jsonDatas['delay_cycle'])+"','"+str(jsonDatas['corporate_agent'])+"','"+str(jsonDatas['phone'])+"','"+str(jsonDatas['selling_period'])+"','"+str(jsonDatas['online_cycle'])+"','"+str(jsonDatas['bidding_record'])+"','"+str(jsonDatas['paimai_model'])+"','"+str(jsonDatas['enrollment'])+"','"+str(jsonDatas['set_reminders'])+"','"+str(jsonDatas['onlookers'])+"','"+str(jsonDatas['data_time'])+"'")
                print insertInfo
                try:
                    result = self.cur.execute(insertInfo)
                    insert_id = self.db.insert_id()
                    self.db.commit()
                    # 判断是否执行成功
                    if result:
                        return insert_id
                    else:
                        return 0
                except MySQLdb.Error, e:
                    # 发生错误时回滚
                    self.db.rollback()
                    # 主键唯一，无法插入
                    if "key 'PRIMARY'" in e.args[1]:
                        print self.getCurrentTime(), "数据已存在，未插入数据"
                    else:
                        print self.getCurrentTime(), "插入数据失败，原因 %d: %s" % (e.args[0], e.args[1])
                        exit()
            else:
                updateInfo = 'update gp_auction_info set ' + 'auction_id="' + str(jsonDatas['auction_id']) + '",court_id="'+str(jsonDatas['court_id'])+'",title="'+ jsonDatas['title'] + '",kind_id="'+str(jsonDatas['kind_id'])+'",url="'+ str(jsonDatas['url'])+'",start_price="'+str(jsonDatas['start_price'])+'",current_price="'+str(jsonDatas['current_price'])+'",cash_deposit="'+str(jsonDatas['cash_deposit'])+'",payment_advance="'+str(jsonDatas['payment_advance'])+'",access_price="'+str(jsonDatas['access_price'])+'",fare_increase="'+str(jsonDatas['fare_increase'])+'",paimai_times="'+str(jsonDatas['paimai_times'])+'",paimai_type="'+str(jsonDatas['paimai_type'])+'",delay_cycle="'+str(jsonDatas['delay_cycle'])+'",corporate_agent="'+str(jsonDatas['corporate_agent'])+'",phone="'+str(jsonDatas['phone'])+'",selling_period="'+str(jsonDatas['selling_period'])+'",set_reminders="'+str(jsonDatas['set_reminders'])+'",online_cycle="'+str(jsonDatas['online_cycle'])+'",bidding_record="'+str(jsonDatas['bidding_record'])+'",paimai_model="'+str(jsonDatas['paimai_model'])+'",enrollment="'+str(jsonDatas['enrollment'])+'",set_reminders="'+str(jsonDatas['set_reminders'])+'",onlookers="'+jsonDatas['onlookers']+'",data_time="'+str(jsonDatas['data_time'])+'" where auction_id='+str(jsonDatas['auction_id'])
                print updateInfo
                result = self.cur.execute(updateInfo)
                insert_id = self.db.insert_id()
                self.db.commit()
                # 判断是否执行成功
                if result:
                    return insert_id
                else:
                    return 0
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
            exit()
        except MySQLdb.Error, e:
            print self.getCurrentTime(), "数据库错误，原因%d: %s" % (e.args[0], e.args[1])
if __name__ == '__main__':
    mysql = Mysql()
    court_list = mysql.getCourtList()
    for court in court_list:
        print court[2] + "," + str(court[0]) + "," + str(court[1])
    
    
    
    
    