import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from tqdm import tqdm

# Some parts of the code refer to shared posts on the internet. The current code retains the main process while removing token-related information.
# For research and educational purposes only. Any use for commercial purposes or cyberattacks is strictly prohibited.
# 仅供研究学习使用，禁止用于任何商业或者网络攻击行为！

# music_lyris
def extract_id(url):
    match = re.search(r"id=(\d+)", url)
    if match:
        return match.group(1)
    return None

city_list = pd.read_csv('./data/city-music-list.csv')

exist_links = pd.read_csv('./data/lyrics.csv', names=['city', 'link', 'lyric'])['link'].tolist()
for index, row in tqdm(city_list.iterrows(), total=len(city_list)):
    if row['link'] in exist_links:
        pass
    else:
        songid = extract_id(row['link'])
        url = 'https://music.163.com/api/song/media?id='
        url += songid
        response = requests.get(url)
        res = response.json()
        row['lyric'] = res.get('lyric') or ''
    
        temp = pd.DataFrame([row])
        temp.to_csv('./data/lyrics.csv', mode='a', index=None, header=None)
        time.sleep(1)
    
print('====done====')

# music_audio
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import time
# import re
# from tqdm import tqdm

# with open('./data/cookie.txt', 'r', encoding='utf-8') as file:
#     cookie = [file.readline().strip() for _ in range(1)][0]


# def extract_id(url):
#     match = re.search(r'id=(\d+)', url)
#     if match:
#         return match.group(1)
#     return None

# def is_mp3_file(response):
#     content_type = response.headers.get('Content-Type', '')
#     return 'audio/mpeg' in content_type or 'audio/mp3' in content_type

# def download_mp3(url, save_path):
#     try:
#         response = requests.get(url, stream=True)
#         if response.status_code == 200:
#             if not is_mp3_file(response):
#                 print('该文件不是有效的MP3文件')
#                 return
                
#             with open(save_path, 'wb') as file:
#                 for chunk in response.iter_content(chunk_size=1024):
#                     if chunk:
#                         file.write(chunk)
#         else:
#             print(f'下载失败，HTTP 状态码: {response.status_code}')
#     except Exception as e:
#         print(f'发生错误: {e}')


# city_list = pd.read_csv('./data/city-music-list.csv')

# for index, row in tqdm(city_list.iterrows(), total=len(city_list)):
#     songid = extract_id(row['link'])
#     url = 'https://music.163.com/song/media/outer/url?id=' + songid + '.mp3'
#     save_path = './clean_data/music_audio/' + row['city'] + '.mp3'
#     download_mp3(url, save_path)
#     time.sleep(2)
    
