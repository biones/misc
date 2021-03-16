import tweepy
import json
from requests_oauthlib import OAuth1Session
import time
import numpy as np


def getApiInstance():
    # 認証キーの設定
    consumer_key = "IuNdbReQk4sxdjzSR0HZVPQNn"
    consumer_secret = "vmf1b20uj7n3WYbDpP0M8q2Wi7s3zhOmDQ4drOMuCFlPqvNFU5"
    bear_token = "AAAAAAAAAAAAAAAAAAAAADMSNAEAAAAA%2FFaIeFxZpFsBoWHklqISSrqkyHM%3D5x03MFuYuFsShUJ6IveoNahLGToQ1O8PbYTfpomSmOBFHyfvCo"
    access_token="1288065283219832834-YE7ynNgeX6JK06NDsyngnZYxTHyJOO"
    access_token_secret = "t5xuiQHZKY2HlzxExm4ZnFbZVgD051Xrd4cQlqmdO3lRS"


    # OAuth認証
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # APIのインスタンスを生成
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api



def search(search_query):

    tweet=tweepy.Cursor(api.search, q =search_query,  include_entities = True, tweet_mode = 'extended', lang = 'ja').items(300)    

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


def run_bot(querys,tweets,n_try,min_retweet,pickup):
    while True:
        k=np.random.choice(len(querys),1)[0]
        print(k)
        dfb,texts=search(querys[k])                
        retweetWithComment(querys[k],tweets[k],dfb,
                           min_retweet=min_retweet[k],pickup=pickup[k],texts=texts,ntry=n_try[k])
        
        time.sleep(1200)

def retweetWithComment(search_query,tweet,tweets,ntry=1,min_retweet=0,pickup=False,random=True,texts=[]):
    cnt=0
    for i in range(len(tweets)):
        if random:
            #tw=np.random.choice(tweets,1)[0]
            k=np.random.choice(range(len(tweets)),1)[0]
            tw=tweets[k]
        else:
            #print(notrand)
            tw=df[i]
        print("text",texts[k])

        if tw.retweet_count<=min_retweet:
            continue
        #print(tw)
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
        
        if pickup:            
            ptweet=search_query+"を利用中の"+locstr+u.name+" @"+u.screen_name[:20]+"さん "+tweet
        else:
            ptweet=tweet
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
        if cnt>=ntry:
            return True
        
        time.sleep(300)
    

ST=1000

    
cm="それは税金の無駄ですね #A型事業所 #B型事業所 #就労移行支援 などの悪質事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。自宅で自習や内職をしましょう"
settai="厚労省と福祉の業者団体でも絶対こういうのありますね、全国社会就労センター協議会,きょうされん,全国就労移行支援事業所連絡協議会全国就業センターとか　"+"https://fukusiprob.blogspot.com/2021/03/blog-post_8.html #接待 #福祉ビジネス"

run_bot(["A型事業所","就労移行支援","接待"],
       ["それは税金の無駄ですね掃除や家事の報告で１万円の報酬が出る #A型事業所 #B型事業所などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になりアホになります。自習や内職をしましょう",
        "エクセルやUdemyでの自習で1.5万円/日の報酬が出る #就労移行支援 などの茶番事業の利用は控えてくださいマトモな事に税金が使われなくなり障害者の迷惑になります。ハロワの基金訓練などを探しましょう",
        settai
       ],
       [1,1,2],
       [0,0,20],
       [1,1,0])

    