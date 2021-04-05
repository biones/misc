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
    client = NotionClient(token_v2="8f3ff0a1f8ee1758ce8d1ad19741cff2dac2197f520c382b76dd3652723f68e8d889d717ea8c0f134d0da8fc18497a6abfc071e1e93242e7a181768d100c419cd6704def7cf59c22f65944504943")
    url="https://www.notion.so/ede84dc00e8c42c1bcff78751313c82e?v=3ad69769c83148f5aaf02d1313387f1a"

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

tdf=notion_to_pandas()
api=lib.getApiInstance()

#res=client.get_collection_view(url)



def search(search_query):
    global Ntweet,api
    print(Ntweet)
    tweet=tweepy.Cursor(api.search, q =search_query,  include_entities = True, tweet_mode = 'extended', lang = 'ja').items(Ntweet)    
    #tweet=api.search(search_query,count=5000)
    texts=[]
    profile=[]

    df=[]
    for r in tweet:        
        #print(r)
        df.append(r)    
        texts.append(r.user.name+r.user.description+"  "+r.full_text)
        #df.append({"name":r.user.name,"location":r.user.location,"description":r.user.description})        

    #print(len(texts))
    return df,texts


def run_bot(dat):
    while True:
        d=tdf.iloc[np.random.choice(tdf.shape[0],1)[0]]
        key=d.search_word
        
        #tweepy.Cursor(api.search_users, q ="社会福祉士", lang = 'ja').items(100) 
        #if d.tweettype!="tweet":
        #    continue
        if d.tweettype=="tweet":
            tweets=d["tweet"]
            #print(np.random.choice(tweets,1)[0])
            try:
                api.update_status(np.random.choice(tweets,1)[0])
            except:
                pass
            time.sleep(600)
            continue            
        elif d.tweettype=="search":            
            try:
                tweets,texts=search(key)
            except:
                time.sleep(ST)
                continue
        elif d.tweettype=="search_profile":
            try:
                tweets,texts=search(key)
            except:
                time.sleep(ST)
                continue
        else:
            continue
            
        #print(tweets)
        print(d)
        retweetWithComment(d,tweets,
                           texts=texts)        
        time.sleep(ST)

def insertusertable(r):
    u=r.user
    dd=[u.id,u.screen_name,u.name,search_query,u.description,r.full_text,u.location]    
    cur.execute("insert into users(id,screen_name,name,search_query,description,tweet,location) values(?,?,?,?,?,?,?)",dd)
    
def inserttweet(tw):
    tw=[r.id,r.full_text,r.user.screen_name,r.user.name,r.user.description,search_query,r.created_at,r.user.location,r.retweet_count]
    cur.execute("insert into tweets(id,tweet,screen_name,name,description,search_query,created_at,location,retweet_count) values(?,?,?,?,?,?,?,?,?)",tw)
    

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

        u=tw.user
        #print(u)
        urls="https://twitter.com/"+u.screen_name+"/status/"+str(tw.id)    
        
        if len(u.location)>0:            
            locstr=u.location.replace("日本","")
            locstr=locstr[:12]
            locstr=locstr+"の"
        else:
            locstr=""
        
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
            
        if len(d.condition_profile)>0 and not(d.condition_profile in u.description):
            continue            
            
        
        tweet=d["tweet"]
        '''
        try:
            tweet=np.random.choice(d["tweet"],1)[0]
        except:
            tweet=d["tweet"]
        '''
        print(d["pickup"],type(d["pickup"]),bool(["pickup"]))
        if bool(d["pickup"]):     
            nname=15
            if "士" in search_query:
                ptweet=locstr+u.name[:15]+" @"+u.screen_name[:15]+"さん "+tweet
            else:
                ptweet="#"+search_query+" を利用中の"+locstr+u.name[:nname]+" @"+u.screen_name[:nname]+"さん "+tweet
        else:
            ptweet=tweet            
        m=re.search("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+",ptweet)
        #l=len(m.group())
        if m.start()+11>140:
            ptweet=ptweet[:m.start()]
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
    ST=3600
    Ntweet=int(1000)


dat=tdf
#discord https://discord.com/invite/HpNBWw7KYt
dbname = 'fukusi.db'
conn = sqlite3.connect(dbname)
cur= conn.cursor()
#cur.execute(
#    'CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,        
#     screen_name STRING unique)')

run_bot(dat)
conn.close()
            