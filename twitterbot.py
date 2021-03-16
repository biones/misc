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

import numpy as np
import numpy as np

import numpy as np
import re

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
        print(key)
        retweetWithComment(key,dat[key],tweets,
                           texts=texts)
        
        time.sleep(ST)

def retweetWithComment(search_query,d,tweets,texts=[]):
    global gtest
    cnt=0
    #print(d)
    for i in range(len(tweets)):
        if "notrandom" in d:
            print(notrand)
            tw=df[i]            
            k=i
        else:            
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
            locstr=u.location+"の"
            locstr=locstr.replace("日本","")
            locstr=locstr[:12]
        else:
            locstr=""
        
        
        try:
            tweet=np.random.choice(d["tweet"],1)[0]
        except:
            tweet=d["tweet"]
            
        if "pickup" in d:     
            ptweet=search_query+"を利用中の"+locstr+u.name[:20]+" @"+u.screen_name[:20]+"さん "+tweet
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
        
        print("NNNNoret",test,i,s)
        input()
        
        if cnt>=d["ntry"]:
            return True
        
        
         
        time.sleep(int(ST*0.1))


        
gtest=False


if gtest:
    ST=10
else:
    ST=30

Ntweet=int(ST*3)
    
cm="それは税金の無駄ですね #A型事業所 #B型事業所 #就労移行支援 などの悪質事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。自宅で自習や内職をしましょう"
settai="厚労省と福祉の業者団体でも絶対こういうのありますね、全国社会就労センター協議会,きょうされん,全国就労移行支援事業所連絡協議会全国就業センターとか　"+"https://fukusiprob.blogspot.com/2021/03/blog-post_8.html #接待 #福祉ビジネス"

dat={
    "放課後デイサービス":{"tweet":"LINEで体温の報告を聞いりアンパンマンを見せるだけで1万数千円も出るヤツですね、税金の無駄です。利用を控えてくださいhttps://bit.ly/2OSOlWV　#放課後デイサービス #福祉ビジネス ",
                 "pickup":True},
    
    "A型事業所":{
        "tweet":[
            "それは税金の無駄ですね掃除や家事の報告で１万円の報酬が出る #A型事業所 #B型事業所などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になりアホになります。自習や内職をしましょう",
            "それは税金の無駄ですね掃除や家事の報告で１万円の報酬が出る #A型事業所 #B型事業所などの茶番事業の利用は控えてください  https://bit.ly/3tte9HZ"],
        "pickup":True        
    },
    "就労移行支援":{
        "tweet":
            ["エクセルやUdemyの自習で1.5万円/日の報酬が出る #就労移行支援 などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。ハロワの基金訓練などを探しましょう",
            s2],
        "pickup":True 
        
    },
    "接待":{
        "tweet":settai,
        "min_retweet":True,
        "ntry":1
    }    
}

run_bot(dat)

