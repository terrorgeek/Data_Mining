from Config import DB
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import cgi
import re
import sys
import time
import tweepy


def get_single_users_tweets(screen_name,api,actor_full_name,actor_screen_name):
    if screen_name=="" or api=="" or screen_name==None or api==None: return
    else:
        try:
           for tweet in tweepy.Cursor(api.user_timeline,id=screen_name).items(50):
               if DB.thread_constant>=700:
                   DB.thread_constant=0
                   time.sleep(360)
               print tweet.text
               DB.thread_constant+=1
               DB.total_constant+=1
               #start to insert into database
               conn=DB.get_dbconn_obj()
               cur=DB.get_dbcur(conn)
             #  sql='''insert into actors_tweets (actor_full_name,actor_screen_name,tweet,fans_screen_name,fans_full_name) values ('"+actor_full_name+"','"+actor_screen_name+"','"+tweet.text+"','"+str(tweet.user.screen_name)+"','"+str(tweet.user.name)+"')'''
               sql='insert into tweets (actor_full_name,actor_screen_name,tweet,fans_screen_name,fans_full_name,fans_user_id) values (%s,%s,%s,%s,%s,%s)'
             #  print sql % (actor_full_name,actor_screen_name,tweet.text.encode('utf-8'),str(tweet.user.screen_name),str(tweet.user.name),str(tweet.user.id))
             #  sql=sql.replace("'","\\'")
             #  sql=sql.replace("\"","");
             #  sql=re.sub("[<>\\\/]*","",sql)
             #  print sql
               sql=sql.encode('utf-8')
               cur.execute(sql,(actor_full_name,actor_screen_name,tweet.text.encode('utf-8'),str(tweet.user.screen_name),str(tweet.user.name),str(tweet.user.id)))
               conn.commit()
               #insert db finished!
           print "Now it's: "+str(DB.thread_constant)
        except:
            print "Unexpected error:", sys.exc_info()
            if sys.exc_info(): pass
            else: raise
        print DB.total_constant

#get_single_users_tweets("AshBenzo",api,"","")

def start_scrawling_actors_fans_tweets():
    # CONSUMER_KEY ='i1R5zHZKUzhgfPwVY7nug'
    # CONSUMER_SECRET ='srml6tGIG5Y2txxQj3hAQuTepj9a7t9369tNrttzuU'
    # ACCESS_KEY='593462483-3dye3ZhVfMQOpTSyDHafNnp4g2jSW358FdoJlz3g'
    # ACCESS_SECRET = 'ZsnSnw4miZMyl0JbwOfUCrbZk1kQssvxW0hOSY3xtjrRd'

    CONSUMER_KEY ='3dP9mmZpYy3ihQdVSID6RQ'
    CONSUMER_SECRET ='mXvDbCAmzhPSvw2JK5267CXCIZPwRkrqUB44BPOFrc'
    ACCESS_KEY='1542481423-8qcKHktRzXp9iM5Xg2Iw0cKlZTEFWJdbLcM4Xns'
    ACCESS_SECRET = 'HnclC1BalwvzsL6SijIq48s0SjBAoKCb3MzjgJgr8xPHC'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    for friend in api.friends(count=200):
        for fan in api.followers(screen_name=friend.screen_name,count=50):
            #print fan.screen_name, friend.name, friend.screen_name
            get_single_users_tweets(fan.screen_name, api ,friend.name,friend.screen_name)
start_scrawling_actors_fans_tweets()
print "scrawling finished!!!!!!"

