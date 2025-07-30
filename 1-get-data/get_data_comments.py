import collections
import datetime
import requests, json
import time
import numpy as np 
import pandas as pd
from urllib.parse import urlparse, parse_qs
import math


# Some parts of the code refer to shared posts on the internet. The current code retains the main process while removing token-related information.
# For research and educational purposes only. Any use for commercial purposes or cyberattacks is strictly prohibited.
# 仅供研究学习使用，禁止用于任何商业或者网络攻击行为！

def get_comments_count(song_id): 
    # Use your data.
    headers = {}
    # Use your data (token). 
    pdata = {}
    response = requests.post('https://music.163.com/weapi/comment/resource/comments/get', headers=headers,data=pdata)
    data = json.loads(response.text)['data']
    return data['totalCount']


def get_comments(city, link, cursor, pagesize=1): 
    parsed_url = urlparse(link)
    fragment = parsed_url.fragment
    query_params = parse_qs(fragment.split('?')[-1])
    song_id = query_params.get('id', [None])[0]
    
    # Use your data.
    headers = {}
    # Use your data (token). 
    response = requests.post('https://music.163.com/weapi/comment/resource/comments/get', headers=headers,data=pdata)
    data = json.loads(response.text)['data']
    current_comments = data['comments']
    

    for i in current_comments:
        # user
        user = i['user']
        userId = user['userId']
        userType = user['userType']
        avatarUrl = user['avatarUrl']
        followed = user['followed']
        nickname = user['nickname']
         
        # content
        user_content = (i['content'] or '' ).replace('\n', ' ').replace('\r', ' ')
        time = i['time']
        timeStr = i['timeStr']
        likedCount = i['likedCount']
        ip = i['ipLocation']['location']
        is_main = 1
        parentCommentId = i['parentCommentId']

        main_row = [city, link, userId, userType, avatarUrl, followed, nickname,
                   user_content, time, timeStr, likedCount, ip, is_main, parentCommentId]

        pd.DataFrame([main_row]).to_csv('./comments.csv', index=None, mode='a', header=None)

       
    return data['cursor']

df = pd.read_csv('../../../clean_data/lyrics_clean.csv')
temp = pd.read_csv('../../../clean_data/comment_count.csv')

def get_done_cities():
    names = ['city', 'link', 'userId', 'userType', 'avatarUrl', 'followed', 'nickname',
                   'user_content', 'time', 'timeStr', 'likedCount', 'ip', 'is_main', 'parentCommentId']
    cities = list(set(pd.read_csv('./comments.csv', names=names,low_memory=True)['city'].tolist()))
    return cities

cities = get_done_cities()

for i, r in temp.iterrows():
    city = r['city']
    if city not in cities:
        cursor = '-1'
        psize = 100
        total_count = r['comment_count']
        total_pages = math.ceil(total_count / psize)
        link = r['link']
        for p in range(total_pages):
            try:
                cursor = get_comments(city, link, cursor, pagesize=psize)
                print(city, total_count, cursor)
                time.sleep(0.5)
            except Exception as e:
                print(f"发生异常：停10s......")
                time.sleep(10)


names = ['city', 'link', 'userId', 'userType', 'avatarUrl', 'followed', 'nickname',
                   'user_content', 'time', 'timeStr', 'likedCount', 'ip', 'is_main', 'parentCommentId']
df = pd.read_csv('./comments.csv', names=names,low_memory=True)

temp = df.drop_duplicates(subset=['link', 'userId', 'user_content', 'timeStr', 'parentCommentId', 'time'])
temp.to_csv('./comments.csv', index=None)