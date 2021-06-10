import numpy as np
import re
import sqlite3

import tweepy
import json
from requests_oauthlib import OAuth1Session
import time
import lib
from notion.client import NotionClient
import pandas as pd 

%load_ext autoreload
%autoreload 2


def notion_to_pandas():
    # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so

    # Replace this URL with the URL of the page you want to edit
    #page = client.get_block("https://www.notion.so/myorg/Test-c0d20a71c0944985ae96e661ccc99821")

    #print("The old title is:", page.title)
    res=client.get_collection_view(url)
    tdf=[]
    col=res.collection
    for r in col.get_rows():
        try:
            tdf.append(r.get_all_properties())
        except:
            pass
    
    tdf=pd.DataFrame(tdf)
    #tdf=pd.DataFrame(col.columns[0])
    
    #tdf.columns=col
    import re
    for i,row in tdf.iterrows():        
        text=re.sub("\[|\]", "",row.tweet)
        tdf.tweet[i]=re.sub("\(.+?\)", "", text)

    return tdf
import pandas as pd
import numpy as np
import re
import sqlite3
import tweepy
import json
from requests_oauthlib import OAuth1Session
import time
import lib
from notion_client import Client
import pandas as pd 


def build_tweet(d,user):
    tweet=d["tweet"]
    if len(user.location)>0:            
        locstr=user.location.replace("日本","")
        locstr=locstr[:12]
    else:
         locstr=""
            
    if d["pickup"]:     
        nname=15
        if "士" in d["search_word"]:
            ptweet=locstr+"の"+user.name[:13]+" @"+user.screen_name[:15]+"さん "+tweet
        elif "議" in d["condition_profile"]:            
            ptweet=locstr+"在住という事になっている議員の"+user.name[:nname]+" @"+user.screen_name[:nname]+"さん "+tweet            
        else:
            ptweet="#"+d["search_word"]+" を利用中の"+locstr+user.name[:nname]+" @"+user.screen_name[:nname]+"さん "+tweet
    else:
        ptweet=tweet            
        
    m=re.search("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",ptweet)
    #l=len(m.group())
    if m and m.start()+11>140:
        ptweet=ptweet[:m.start()]
    print(ptweet)
    print("strlength",len(ptweet))
    #ptweet+=" "+urls
    return ptweet


def search_profile(search_query):
    res=tweepy.Cursor(api.search_users, q =search_query,lang = 'ja').items(100)    
    return list(res)


def search(search_query):
    global Ntweet,api
    print(Ntweet,search_query)
    tweet=tweepy.Cursor(api.search, q =search_query+" -filter:retweets",  include_entities = True, tweet_mode = 'extended', lang = 'ja').items(Ntweet)    
    #tweet=api.search(search_query,count=5000)
    texts=[]
    profile=[]
   
    df=[]
    for r in tweet:        
        #print(r)
        #if "RT @" in status.text[0:4]:
        #    continue
            
        df.append(r)    
        texts.append(r.user.name+r.user.description+"  "+r.full_text)
        #df.append({"name":r.user.name,"location":r.user.location,"description":r.user.description})        

    #print(len(texts))
    return df,texts



def run_bot(df):
    global api
    tdf.weight[pd.isna(tdf.weight)]=1
    n=tdf.weight    
    while True:
        #d=df.iloc[np.random.choice(df.shape[0],1)[0]]
        print(np.random.choice(range(df.shape[0]),p=n/np.sum(n)))
        d=df.iloc[np.random.choice(range(df.shape[0]),p=n/np.sum(n))]
        key=d.search_word
        #print(d)
        
        #tweepy.Cursor(api.search_users, q ="社会福祉士", lang = 'ja').items(100) 
        #if d.tweettype!="tweet":
        #    continue
    
        if d.tweettype=="tweet":
            tweets=d["tweet"]
            #print(np.random.choice(tweets,1)[0])
            try:
                api.update_status(d.tweet)
            except:
                pass
            time.sleep(1800)
            continue            
            
        elif d.tweettype=="search":            
            try:
                tweets,texts=search(key)
            except:
                time.sleep(ST)
                continue
        elif d.tweettype=="search_profile":
            users=search_profile(key)                
            reply(d,np.random.choice(users))
            time.sleep(3000)
            continue
                
        else:
            continue
            
        #print(tweets)
        #print("aft",d)
        retweetWithComment(d,tweets,
                           texts=texts)        
        time.sleep(ST)

def insertusertable(r):
    u=r.user
    dd=[u.id,u.screen_name,u.name,search_query,u.description,r.full_text,u.location]    
    cur.execute("insert into users(id,screen_name,name,search_query,description,tweet,location) values(?,?,?,?,?,?,?)",dd)
    
def inserttweet(tw):
    twt=[r.id,r.full_text,r.user.screen_name,r.user.name,r.user.description,search_query,r.created_at,r.user.location,r.retweet_count]
    cur.execute("insert into tweets(id,tweet,screen_name,name,description,search_query,created_at,location,retweet_count) values(?,?,?,?,?,?,?,?,?)",twt)

def reply(d,user):    
    try:
        api.update_status(build_tweet(d,user))
        insertusertable(user)
        inserttweet(tw)
        conn.commit()    
    except:
        pass        
    
    

def retweetWithComment(d,tweets,texts=[]):
    global gtest,cur
    
    search_query=d.search_word
    cnt=0
    for i in range(len(tweets)):
        k=np.random.choice(range(len(tweets)),1)[0]
        tw=tweets[k]
        
        print("minret",d.min_retweet,d["min_retweet"])
        try:
            if tw.retweet_count<=d["min_retweet"]:
                continue
        except:
            pass
        user=False
        try:
            user=res.retweeted_status.user
        except:
            user=tw.user
        print(tw.id,tw.user.screen_name)
        print(user.screen_name)
        
        urls="https://twitter.com/"+user.screen_name+"/status/"+str(tw.id)
        
        if len(user.location)>0:            
            locstr=user.location.replace("日本","")
            locstr=locstr[:12]
            locstr=locstr+"の"
        else:
            locstr=""
        
        
        try:
            insertusertable(user)
            #cur.execute("insert into users(screen_name,name,description,location) values(?,?,?,?)",dd)            
            conn.commit()            
        except:
            pass
        try:
            inserttweet(tw)
            conn.commit()  
        except:
            pass
            
        if not(pd.isna(d.condition_profile)) and not(d.condition_profile in user.description):
            continue            
            
        
        tweet=d["tweet"]
        '''
        try:
            tweet=np.random.choice(d["tweet"],1)[0]
        except:
            tweet=d["tweet"]
        '''
        ptweet=""
        print(d["pickup"],type(d["pickup"]))
        if d["pickup"]:     
            nname=15
            if "士" in search_query:
                ptweet=locstr+user.name[:13]+" @"+user.screen_name[:15]+"さん "+tweet
            else:
                ptweet="#"+search_query+" を利用中の"+locstr+user.name[:nname]+" @"+user.screen_name[:nname]+"さん "+tweet
        else:
            ptweet=tweet            
        m=re.search("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",ptweet)
        #l=len(m.group())
        if m and m.start()+11>140:
            ptweet=ptweet[:m.start()]
        print(ptweet)
        print("strlength",len(ptweet))
        
        ptweet+=" "+urls        
        
        print(ptweet)
        
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
            
        return
        '''
        try:
            s=d["ntry"]
        except:
            return
        
        print("NNNNoret",cnt,gtest,i,int(d["ntry"]))
        #input()
        
        if cnt>=int(d["ntry"]):
            return True
                
        time.sleep(int(ST*0.1))
        '''


        
gtest=False

Ntweet=50
if gtest:
    ST=1000
    Ntweet=int(50)
else:
    ST=7200
    Ntweet=int(100)


api=lib.getApiInstance()
#discord https://discord.com/invite/HpNBWw7KYt
dbname = ''
conn = sqlite3.connect(dbname)
cur= conn.cursor()
#cur.execute(
#    'CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,        
#     screen_name STRING unique)')
tdf=pd.read_csv("")
tdf=tdf.drop_duplicates()
run_bot(tdf)
conn.close()
            