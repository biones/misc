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


def search(search_query):

    tweet=tweepy.Cursor(api.search, q =search_query,  include_entities = True, tweet_mode = 'extended', lang = 'ja').items(1000)    

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
    cnt=0
    print(d)
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
        
        if "pickup" in d:     
            ptweet=search_query+"を利用中の"+locstr+u.name[:20]+" @"+u.screen_name[:20]+"さん "+d["tweet"]
        else:
            ptweet=d["tweet"]
        ptweet=ptweet[:140]
        print(ptweet)
        print("strlength",len(ptweet))
        ptweet+=" "+urls        


        try:
            #print(1)
            api.update_status(ptweet)
        except:
            continue
        cnt+=1
        if "ntry" not in d:
            print("retun")
            return
        elif cnt>=d["ntry"]:
            return True
         
        time.sleep(int(ST*0.1))
    

ST=600

    
cm="それは税金の無駄ですね #A型事業所 #B型事業所 #就労移行支援 などの悪質事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。自宅で自習や内職をしましょう"
settai="厚労省と福祉の業者団体でも絶対こういうのありますね、全国社会就労センター協議会,きょうされん,全国就労移行支援事業所連絡協議会全国就業センターとか　"+"https://fukusiprob.blogspot.com/2021/03/blog-post_8.html #接待 #福祉ビジネス"

dat={
    "放課後デイサービス":{"tweet":"LINEで体温の報告を聞いりアンパンマンを見せるだけで1万数千円も出るヤツですね、税金の無駄です。利用を控えてください　#放課後デイサービス #福祉ビジネス ",
                 "pickup":True},
    
    "A型事業所":{
        "tweet":"それは税金の無駄ですね掃除や家事の報告で１万円の報酬が出る #A型事業所 #B型事業所などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になりアホになります。自習や内職をしましょう",
        "pickup":True        
    },
    "就労移行支援":{
        "tweet":"エクセルやUdemyでの自習で1.5万円/日の報酬が出る #就労移行支援 などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。ハロワの基金訓練などを探しましょう",
        "pickup":True 
        
    },
    "接待":{
        "tweet":settai,
        "min_retweet":True,
        "ntry":1
    }    
}

run_bot(dat)

