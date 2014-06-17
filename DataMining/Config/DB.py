from __future__ import print_function
#import MySQLdb
thread_constant=0
total_constant=0
base=2 #the base doesn't matter so we randomly choose 5, this base is for calculating tf-idf
import pymysql
# def get_dbconn_obj():
#     try:
#        conn=MySQLdb.connect(host='localhost',user='root',passwd='admin',db='datamining',port=3306)
#        # cur=conn.cursor()
#        # cur.close()
#        return conn
#     except MySQLdb.Error,e:
#        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
# def get_dbcur(conn):
#     cur=conn.cursor()
#     #cur.execute('select * from user')
#     return cur


def get_dbconn_obj():
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='datamining')
        return conn
    except:
        print ("error connection!")

def get_dbcur(conn):
    cur=conn.cursor()
    return cur
