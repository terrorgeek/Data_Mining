#import MySQLdb
import re
import math
from Config import DB
import pymysql

def get_single_fans_tweets(fans_user_id):
    if fans_user_id=="" or len(fans_user_id)==0: return
    conn=DB.get_dbconn_obj()
    cursor=DB.get_dbcur(conn)
    sql="select * from tweets where fans_user_id='"+str(fans_user_id)+"'"
    count=cursor.execute(sql)
    res=cursor.fetchall()
    result_list=[]
    for r in res:
        tup=(r[4],r[6],r[3]) #fan's screen_name, fan's user_id and fan's tweet
        result_list.append(tup)
    return result_list
def Calculate_SingleUser_Tf_Idf(user_id):
    if len(user_id)==0: return
    result_list=get_single_fans_tweets(user_id)
    hash={}
    for fan in result_list:
        tweet_arr=re.split('[\s\.\,]',fan[2])
        for token in tweet_arr:
            token=re.sub('[\!\?\.\#\&\,]*',"",token)#remove trvial chars
            if hash.get(token,None)==None and len(token)!=0: hash[token]=1
            else:
                if len(token)!=0: hash[token]+=1
    #Tf calculation already finished
    #now let's calculate Idf
    #this hash is for storing the Idf count
    idf_hash={}
    for key,value in hash.items():
        for fan in result_list:
            tweet_arr=re.split('[\s\.\,]',fan[2])
            tweet_arr=[re.sub('[\!\?\.\#\&\,]*',"",x) for x in tweet_arr]
            if key in tweet_arr:
                if idf_hash.get(key,None)==None: idf_hash[key]=1
                else: idf_hash[key]+=1
    N=len(result_list)
    tf_idf_hash={}
    result={}
    for key,value in hash.items():
        idf_value=math.log(float(N/idf_hash[key]),float(DB.base))
        tf_idf_value=hash[key]*idf_value
        tf_idf_hash[key]=tf_idf_value
    #print tf_idf_hash
    #now we need to pick the top 5 words based on the count
    new_tf_idf_hash={}
    sorted_hash=sorted(tf_idf_hash,key=tf_idf_hash.get,reverse=False)
    if len(sorted_hash)>5:
        for index in range(5):
            new_tf_idf_hash[sorted_hash[index]]=tf_idf_hash[sorted_hash[index]]
    else:
        for index in range(len(sorted_hash)):
            new_tf_idf_hash[sorted_hash[index]]=tf_idf_hash[sorted_hash[index]]
   # print new_tf_idf_hash
    return new_tf_idf_hash
def get_all_fans_list():
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    cur.execute("select * from tweets group by fans_full_name")
    res=[]
    out=cur.fetchall()
    for row in out:
        tup=(row[5],row[6],row[1])
        res.append(tup)
    return res

def construct_vector_old(result):
    sample_hash={}
    for single_list in result:
        for k,v in single_list[1].items():
            if sample_hash.get(k,None)==None:
                sample_hash[k]=1
    keys_list=sample_hash.keys()
    #rehandle the result set again
    for single_list in result:
        #find the difference between 2 lists
        diff=[i for i in keys_list if i not in single_list[1]]
        #make them all have the same dimension
        for d in diff:
            single_list[1][d]=0
        single_list[1]=sorted(single_list[1].items(),key=lambda e:e[0],reverse=False)
        print single_list
    return result
def prepare_for_kmeans():
    res=[]
    fans_tuple_list=get_all_fans_list()
    for fan in fans_tuple_list:
        hash=Calculate_SingleUser_Tf_Idf(fan[1])
        res.append([fan[0].strip(),hash,fan[2]])
        print [fan[0].strip(),hash,fan[2]]
    #print res
    return res