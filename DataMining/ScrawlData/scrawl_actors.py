from Config import DB
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import time
#below is for Pain
CONSUMER_KEY ='i1R5zHZKUzhgfPwVY7nug'
CONSUMER_SECRET ='srml6tGIG5Y2txxQj3hAQuTepj9a7t9369tNrttzuU'
ACCESS_KEY='593462483-3dye3ZhVfMQOpTSyDHafNnp4g2jSW358FdoJlz3g'
ACCESS_SECRET = 'ZsnSnw4miZMyl0JbwOfUCrbZk1kQssvxW0hOSY3xtjrRd'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# for i in api.followers(screen_name="AshBenzo"):
#     print i.screen_name
#     time.sleep(1)


# user = api.get_user(screen_name="AshBenzo")
# #Display basic details for twitter user name
# print user.screen_name
# print user.followers_count
# for friend in user.followers():
# #   # print friend.screen_name
#     print friend.name

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

    for status in tweepy.Cursor(api.user_timeline,id=screen_name).items(maxnumtweets):
       print status.text+"\n"
#twitter_fetch('AshBenzo',100)

def start_scrawling_actors():
    CONSUMER_KEY ='i1R5zHZKUzhgfPwVY7nug'
    CONSUMER_SECRET ='srml6tGIG5Y2txxQj3hAQuTepj9a7t9369tNrttzuU'
    ACCESS_KEY='593462483-3dye3ZhVfMQOpTSyDHafNnp4g2jSW358FdoJlz3g'
    ACCESS_SECRET = 'ZsnSnw4miZMyl0JbwOfUCrbZk1kQssvxW0hOSY3xtjrRd'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    conn=DB.get_dbconn_obj()
    cur=DB.get_dbcur(conn)
    for i in api.friends(count=10000):
        cur.execute("insert into actors_and_directors (full_name,screen_name,user_id) values ('"+str(i.name)+"','"+str(i.screen_name)+"','"+str(i.id)+"')")
        conn.commit()
        #print i.name
start_scrawling_actors()