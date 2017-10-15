import pymysql
import os
import time

TOP_YEAR = 2017
BOTTOM_YEAR = 2012

HOST = '172.31.238.141'
PORT = 3306
USER = 'wise_r'
PASSWD = 'wise_r'
CHARSET = 'UTF8'
DB = 'wise'

ROOT = os.path.join('..','d2v-data')

REST = 60*5 # 停歇时间，否则连接数据库会出问题

def fetchNews(cmd):
    conn = pymysql.connect(host = HOST,port = PORT, user = USER,passwd = PASSWD,db = DB,charset = CHARSET)
    cursor = conn.cursor()
    cursor.execute(cmd)
    all_news = cursor.fetchall()
    cursor.close()
    conn.close()
    return all_news

def writeNews(news_in_year,year = 0):
    if not os.path.exists(ROOT):
        os.mkdir(ROOT)
    print("Start writting news in %d" % year)
    for _id,pub_date,news_content in news_in_year:
        nodir = os.path.join(ROOT,'%d_%s.txt'%(_id,pub_date))
        with open(nodir,'w',encoding='utf-8',errors='ignore') as fout:
            fout.write(news_content)
    print("Finish writting in %d" % year)

if __name__=='__main__':
    all_year = [year for year in range(BOTTOM_YEAR,TOP_YEAR+1)]

    for year in all_year:
        cmd = r"select id,pub_date,news_content from wise_news where pub_date>='%d-01-01' and pub_date<='%d-12-31';" % (year,year)
        news_in_year = fetchNews(cmd)
        writeNews(news_in_year=news_in_year,year = year)
        time.sleep(REST)
    print("\nOver\n")