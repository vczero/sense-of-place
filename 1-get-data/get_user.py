import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from tqdm import tqdm
import asyncio
from tqdm.asyncio import tqdm_asyncio

# Some parts of the code refer to shared posts on the internet. The current code retains the main process while removing token-related information.
# For research and educational purposes only. Any use for commercial purposes or cyberattacks is strictly prohibited.
# 仅供研究学习使用，禁止用于任何商业或者网络攻击行为！

all_userid = pd.read_csv('./userids.csv')['userid'].tolist()
def extract_user_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if soup.find(string="很抱歉，你要查找的网页找不到"):
        return {'is_ok': 0}
    
    user_info = {'is_ok': 1}
    
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    if meta_keywords and 'content' in meta_keywords.attrs:
        content = meta_keywords['content']
        user_info['nickname'] = content.split('，')[0]
    else:
        return {} 

    age_span = soup.find('span', class_='sep', id='age')
    if age_span and 'data-age' in age_span.attrs:
        timestamp = int(age_span['data-age']) / 1000  
        user_info['birthday'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    else:
        user_info['birthday'] = None
    
    location_div = soup.find('div', class_='inf s-fc3')
    if location_div:
        location_span = location_div.find('span')
        if location_span:
            user_info['location'] = location_span.text.split('：')[-1].strip()
        else:
            user_info['location'] = None
    else:
        user_info['location'] = None
    
    listen_h4 = soup.find('h4')
    if listen_h4 and '累积听歌' in listen_h4.text:
        user_info['listen_song_num'] = int(''.join(filter(str.isdigit, listen_h4.text)))
    else:
        user_info['listen_song_num'] = None
    

    fan_strong = soup.find('strong', id='fan_count')
    if fan_strong:
        user_info['fan_count'] = int(fan_strong.text.strip())
    else:
        user_info['fan_count'] = None
    

    event_strong = soup.find('strong', id='event_count')
    if event_strong:
        user_info['event_count'] = int(event_strong.text.strip())
    else:
        user_info['event_count'] = None
    
    # 7. follow_count
    follow_strong = soup.find('strong', id='follow_count')
    if follow_strong:
        user_info['follow_count'] = int(follow_strong.text.strip())
    else:
        user_info['follow_count'] = None
    
    return user_info


def get_userinfo(userid):
    url = "https://music.163.com/user/home?id=" + str(userid)
    # Use your data.
    headers = {}
    cookies = {}
    
    response = requests.get(url, headers=headers, cookies=cookies)
    user_data = extract_user_info(response.text)
    return user_data


def format_userinfo(i):
    user = get_userinfo(i)
    userid = i
    if user.get('is_ok') == 1:
        nickname = user.get('nickname') or ''
        birthday = user.get('birthday') or ''
        location = user.get('location') or ''
        province = location
        city = location
        if ' - ' in location:
            temp = location.split(' - ' )
            province = temp[0]
            city = temp[1]
            
        listen_song_num = user.get('listen_song_num') or ''
        fan_count = user.get('fan_count') or ''
        event_count = user.get('event_count') or ''
        follow_count = user.get('follow_count') or ''
    
        uinfo = [[userid, nickname, birthday, location, province, city, listen_song_num, fan_count, event_count, follow_count]]
        pd.DataFrame(uinfo).to_csv('./userinfo.csv', index=None, header=None, mode='a')

    else:
        pd.DataFrame([[userid]]).to_csv('./no_userinfo.csv', index=None, header=None, mode='a')


USERS = all_userid
for uid in tqdm(USERS, desc="Processing Users"):
    format_userinfo(uid)