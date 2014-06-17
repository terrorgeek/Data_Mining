from Config import DB
import pymysql
import re
import math
def get_num_of_documents():
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    count=cur.execute("select * from tweets group by actor_full_name")
    return count
def build_base_tfidf_table():
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    cur.execute("select tweet from tweets")
    res=cur.fetchall()
    hash={}
    for r in res:
        tweet_arr=re.split('[\s\.\,]',r[0])
        for token in tweet_arr:
            token=re.sub('[\!\?\.\#\&\,]*',"",token)#remove trvial chars
            if hash.get(token,None)==None and len(token)!=0: hash[token]=1
            else:
                if len(token)!=0: hash[token]+=1
    return hash #the hash of all teh tweets in tweets table
def get_single_actor_tweets(actor_full_name):
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    cur.execute("select * from tweets where actor_full_name='"+str(actor_full_name)+"'")
    res=cur.fetchall()
    data_structure=[]
    for r in res:
        tmp=(r[3],r[5],r[6])
        data_structure.append(tmp)
    return data_structure

def get_tfidf_for_singleActor(actor_full_name,base_hash,N):#N is the number of documents, that is, the number of users
    tweets=get_single_actor_tweets(actor_full_name)
    hash={}
    result={}
    for r in tweets:
        tweet_arr=re.split('[\s\.\,]',r[0])
        for token in tweet_arr:
            token=re.sub('[\!\?\.\#\&\,]*',"",token)#remove trvial chars
            if hash.get(token,None)==None and len(token)!=0: hash[token]=1
            else:
                if len(token)!=0: hash[token]+=1
    for k,v in hash.items():
        tf_idf=hash[k]*math.log(float(N)/float(base_hash[k]),float(DB.base))
        result[k]=tf_idf
    result=sorted(result.items(),key=lambda e:e[1],reverse=True)
    #pick the top 5
    if len(result)<5: return [actor_full_name,result]
    else:
        tmp=[]
        for i in range(5):
            tmp.append(result[i])
        return [actor_full_name,tmp]

def getAll_Actor_tfidf(base_hash,N):
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    cur.execute("select actor_full_name from tweets group by actor_full_name")
    res=cur.fetchall()
    user_res_list=[]
    for r in res:
        tf_idf=get_tfidf_for_singleActor(r[0],base_hash,N)
        user_res_list.append(tf_idf)
        print tf_idf
    return user_res_list

def store_into_database(answer):
    for actor in answer:
        sql="insert into actor_tfidf (actor_full_name, keywords) values ('"+str(actor[0])+"','"
        append_sql=""
        for tuple in actor[1]:
            append_sql+=tuple[0]+","
        sql+=append_sql[0:len(append_sql)-1].replace('"','\\"').replace("'","\\'")
        sql+="')"
        print sql
        conn=DB.get_dbconn_obj()
        cur=DB.get_dbcur(conn)
        cur.execute(sql)
        conn.commit()



base_hash=build_base_tfidf_table() # this function must be executed first in this file!
N=get_num_of_documents() #so does this
answer=getAll_Actor_tfidf(base_hash,N)
store_into_database(answer)
