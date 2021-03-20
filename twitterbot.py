import tweepy
import json
from requests_oauthlib import OAuth1Session
import time
import numpy as np


def getApiInstance():
    # 認証キーの設定
    consumer_key 
    consumer_secret
    bear_token
    access_token
    access_token_secret 
    # OAuth認証
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # APIのインスタンスを生成
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api


import re
import numpy as np
import re
import sqlite3

def search(search_query):
    global Ntweet
    print(Ntweet)
    tweet=tweepy.Cursor(api.search, q =search_query,  include_entities = True, tweet_mode = 'extended', lang = 'ja').items(Ntweet)    
    #tweet=api.search(search_query,count=5000)

    texts=[]
    profile=[]

    df=[]
    for r in tweet:
        df.append(r)    
        texts.append(r.user.name+r.user.description+"  "+r.full_text)
        #df.append({"name":r.user.name,"location":r.user.location,"description":r.user.description})        

    #print(len(texts))
    return df,texts


def run_bot(dat):
    while True:
        key=np.random.choice(list(dat.keys()),1)[0]
        tweets,texts=search(key)          
        #print(key)
        retweetWithComment(key,dat[key],tweets,
                           texts=texts)        
        time.sleep(ST)

def insertusertable(r):
    u=r.user
    dd=[u.id,u.screen_name,u.name,search_query,u.description,r.full_text,u.location]    
    cur.execute("insert into users(id,screen_name,name,search_query,description,tweet,location) values(?,?,?,?,?,?,?)",dd)
    
def inserttweet(tw):
    tw=[r.id,r.full_text,r.user.screen_name,r.user.name,r.user.description,search_query,r.created_at,r.user.location,r.retweet_count]
    cur.execute("insert into tweets(id,tweet,screen_name,name,description,search_query,created_at,location,retweet_count) values(?,?,?,?,?,?,?,?,?)",tw)
    

def retweetWithComment(search_query,d,tweets,texts=[]):
    global gtest,cur
    cnt=0
    #print(d)
    for i in range(len(tweets)):
        #if "notrandom" in d:
          #  print(notrand)
           # tw=df[i]            
            #k=i
        #else:            
            #tw=np.random.choice(tweets,1)[0]
        k=np.random.choice(range(len(tweets)),1)[0]
        tw=tweets[k]
            
        print("text",texts[k])
        print(i,gtest)
        #m.min_retweet
        try:
            if tw.retweet_count<=d["min_retweet"]:
                continue
        except:
            pass

        u=tw.user
        print(u.screen_name)
        #print(u)
        urls="https://twitter.com/"+u.screen_name+"/status/"+str(tw.id)    
        
        if len(u.location)>0:            
            locstr=u.location.replace("日本","")
            locstr=locstr[:12]
            locstr=locstr+"の"
        else:
            locstr=""
        
        #q="insert into users(screen_name,name,profile,location) values"+blacket([u.screen_name,u.name,u.description,u.location])
        #print(q)
        #dd=(u.screen_name,u.name,u.description,u.location)
        #dd=[r.user.id,r.user.screen_name,r.user.name,search_query,r.user.description,r.full_text,r.user.location]
        #print(dd)
        try:
            insertusertable(u)
            #cur.execute("insert into users(screen_name,name,description,location) values(?,?,?,?)",dd)            
            conn.commit()            
        except:
            pass
        try:
            inserttweet(tw)
        except:
            pass
            

        try:
            tweet=np.random.choice(d["tweet"],1)[0]
        except:
            tweet=d["tweet"]
            
        if "pickup" in d:     
            ptweet="#"+search_query+" を利用中の"+locstr+u.name[:20]+" @"+u.screen_name[:20]+"さん "+tweet
        else:
            ptweet=tweet            
        
        if re.match("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",ptweet):            
            ptweet=ptweet[:135]
        else:
            ptweet=ptweet[:140]
        
        print(ptweet)
        print("strlength",len(ptweet))
        
        ptweet+=" "+urls        

        try:
            if gtest:
                print(1)
            else:          
                print("bpost")
                api.update_status(ptweet)
                print("posted")
            cnt+=1
        except:
            continue
        try:
            s=d["ntry"]
        except:
            return
        
        print("NNNNoret",cnt,gtest,i,d["ntry"])
        #input()
        
        if cnt>=d["ntry"]:
            return True
        
        
         
        time.sleep(int(ST*0.1))


        
gtest=False


if gtest:
    ST=10
else:
    ST=1200

Ntweet=int(ST)
    
cm="それは税金の無駄ですね #A型事業所 #B型事業所 #就労移行支援 などの悪質事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。自宅で自習や内職をしましょう"
settai="厚労省と福祉の業者団体でも絶対こういうのありますね、全国社会就労センター協議会,きょうされん,全国就労移行支援事業所連絡協議会全国就業センターとか　"+"https://fukusiprob.blogspot.com/2021/03/blog-post_8.html #接待 #福祉ビジネス"

stop='''【悪質な事業所は許せません】
ここの事業所はどうなんだろう？アンケートご協力お願いします(匿名可) → http://bit.ly/3vIZ9HW 
    STOP！税金の無駄・不正 #就労移行支援　#A型事業所　#放課後デイ　#福祉ビジネス'''

dat={
    "放課後デイサービス":{"tweet":["LINEで体温の報告を受けたり,アンパンマンを見せるだけで1.5万円も出る茶番事業ですね、税金の無駄です。利用を控えてくださいhttps://bit.ly/2OSOlWV　#放課後デイ #福祉ビジネス",
                          stop,
                         "税金ジャブジャブ障害福祉サービスの利用は控えましょう　https://bit.ly/2OSOlWV　放課後デイ #福祉ビジネス"],
                 "pickup":True},
    
    "A型事業所":{
        "tweet":[
            "税金の無駄ですね掃除や家事の報告で１万円の報酬が出る茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になりアホになります。自習や内職をしましょう https://bit.ly/3tte9HZ",
            "それは税金の無駄ですね掃除や家事の報告で１万円の報酬が出る茶番事業の利用は控えてください  https://bit.ly/3tte9HZ #B型事業所",
            stop],
        "pickup":True        
    },
    "就労移行支援":{
        "tweet":
            ["エクセルやUdemyの自習で1.5万円/日の報酬が出る茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。ハロワの基金訓練などを探しましょうhttps://bit.ly/3bUqaQR",
             "エクセルやUdemyの自習で1.5万円/日の報酬が出る茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります　https://bit.ly/3bUqaQR ",
             stop
            ],
        "pickup":True 
        
    },
    "接待":{
        "tweet":settai,
        "min_retweet":True,
        "ntry":1
    }    
}

dbname = 'fukusi.db'
conn = sqlite3.connect(dbname)
cur= conn.cursor()
#cur.execute(
#    'CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,        
#     screen_name STRING unique)')

run_bot(dat)

conn.close()
            