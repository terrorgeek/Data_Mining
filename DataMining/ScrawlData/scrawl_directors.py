from Config import DB
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

#user id: 1542481423
#below is for terrorgeek
CONSUMER_KEY ='3dP9mmZpYy3ihQdVSID6RQ'
CONSUMER_SECRET ='mXvDbCAmzhPSvw2JK5267CXCIZPwRkrqUB44BPOFrc'
ACCESS_KEY='1542481423-8qcKHktRzXp9iM5Xg2Iw0cKlZTEFWJdbLcM4Xns'
ACCESS_SECRET = 'HnclC1BalwvzsL6SijIq48s0SjBAoKCb3MzjgJgr8xPHC'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



#user = api.get_user(screen_name="AshBenzo")
# Display basic details for twitter user name
#print user.screen_name
#print user.followers_count
# for friend in user.friends():
#   # print friend.screen_name
#    print friend.name

#search user example
# user=api.search_users(q="Ashley Benson",per_page=5,page=10)
# for i in user:
#     print i.name


# timeline = api.home_timeline(screen_name="AshBenzo", include_rts=True, count=10)
# for tweet in timeline:
#     print ("ID:", tweet.id)
#     print ("User ID:", tweet.user.id)
#     print ("Text:", tweet.text)
#     print  "Screen name:"+str(tweet.screen_name)


#for follower in api.home_timeline(include_rts=True, count=1000):
#    print follower.text


# user = api.me()
#
# print('Name: ' + user.name)
# print('Location: ' + user.location)
# print('Friends: ' + str(user.friends_count))

def twitter_fetch(screen_name = "BBCNews",maxnumtweets=10):
    'Fetch tweets from @BBCNews'
    # API described at https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline

    CONSUMER_KEY ='3dP9mmZpYy3ihQdVSID6RQ'
    CONSUMER_SECRET ='mXvDbCAmzhPSvw2JK5267CXCIZPwRkrqUB44BPOFrc'
    ACCESS_KEY='1542481423-8qcKHktRzXp9iM5Xg2Iw0cKlZTEFWJdbLcM4Xns'
    ACCESS_SECRET = 'HnclC1BalwvzsL6SijIq48s0SjBAoKCb3MzjgJgr8xPHC'

    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)

    api  = tweepy.API(auth)
    #print api.me().name
    #api.update_status('Hello -tweepy + oauth!')

    for status in tweepy.Cursor(api.user_timeline,id=screen_name).items(10):
       print status.text+"\n"
#twitter_fetch('AshBenzo',10)

def get_all_actors_screen_name_list():
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    cur.execute("select * from actors_and_directors")
    result=cur.fetchall()
    res=[]
    for row in result:
        res.append(row[2])
    return res

def start_scrawling_directors():
    CONSUMER_KEY ='3dP9mmZpYy3ihQdVSID6RQ'
    CONSUMER_SECRET ='mXvDbCAmzhPSvw2JK5267CXCIZPwRkrqUB44BPOFrc'
    ACCESS_KEY='1542481423-8qcKHktRzXp9iM5Xg2Iw0cKlZTEFWJdbLcM4Xns'
    ACCESS_SECRET = 'HnclC1BalwvzsL6SijIq48s0SjBAoKCb3MzjgJgr8xPHC'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    all_actors_list=get_all_actors_screen_name_list()
    for i in api.friends(count=1000):
        if i.screen_name in all_actors_list:
            pass
        else:
            cur.execute("insert into actors_and_directors (full_name,screen_name,user_id) values ('"+str(i.name)+"','"+str(i.screen_name)+"','"+str(i.id)+"')")
            conn.commit()
start_scrawling_directors()