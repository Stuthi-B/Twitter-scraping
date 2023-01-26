import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo


def storeInMongo(df):
    client=pymongo.MongoClient("mongodb://StuthiB:Stuthi1999@ac-1bw0xxo-shard-00-00.wp8pxwi.mongodb.net:27017,ac-1bw0xxo-shard-00-01.wp8pxwi.mongodb.net:27017,ac-1bw0xxo-shard-00-02.wp8pxwi.mongodb.net:27017/?ssl=true&replicaSet=atlas-lddb9d-shard-0&authSource=admin&retryWrites=true&w=majority")
    py=client["Twitter"]
    pycollection=py["Tweets"]
    pycollection.insert_one(df)
    print()

st.header("Twitter Scraper")
keyword=st.text_input("Hashtag or Keyword", value="", autocomplete=None, placeholder="Please enter hashtag or keyword", label_visibility="visible")
start_date=st.date_input("Enter start date", value=None, min_value=None, max_value=None, on_change=None,  disabled=False, label_visibility="visible")
end_date=st.date_input("Enter end date", value=None, min_value=None, max_value=None,  on_change=None,  disabled=False, label_visibility="visible")
limit=st.number_input("Enter the limit", step=1, min_value=1)
# print(keyword, start_date,end_date, limit)
if(keyword and start_date and end_date and limit):
    tweets_list= []
    tweets_dict={}
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("{key} since:{start} until:{end}".format(key=keyword,start=start_date,end=end_date)).get_items()):
        if i>=limit:
            break
        tweets_list.append([keyword,tweet.id, tweet.date, tweet.content, tweet.url, tweet.user.username, tweet.replyCount, tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount])
    tweets_dict[keyword]=tweets_list    
    print(tweets_list)
    df=pd.DataFrame(tweets_list, columns=["keyword","id","date","content","url","user","replyCount","retweetCount","lang","source","likeCount"])
    st.table(df)
    csv_data= df.to_csv().encode("utf-8")
    json_data= df.to_json()
    d=df.to_dict()
    dict_data=dict(zip(df['keyword'].astype(str), tweets_dict))
    st.download_button(label="Download as CSV",data= csv_data,file_name="Twitter_csv.csv",mime="text/csv")
    st.download_button(label="Download as json", data= json_data,file_name="Twitter_json.json",mime= "text/json")
    st.button(label="upload", on_click=storeInMongo(tweets_dict), type="secondary", disabled=False)



