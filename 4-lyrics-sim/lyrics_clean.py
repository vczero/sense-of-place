import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from openai import OpenAI
from tqdm import tqdm

lyrics = pd.read_csv('../clean_data/lyrics.csv')

def clean_lyrics(text):
    text = text.replace('\n', ' ')  
    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\d+', '', text) 
    text = re.sub(r'词曲\w+', '', text)
    text = re.sub(r'演唱\w+', '', text)
    text = re.sub(r'编曲\w+', '', text)
    text = re.sub(r'制作人\w+', '', text)
    text = re.sub(r'监制\w+', '', text)
    text = re.sub(r'伴奏\w+', '', text)
    text = re.sub(r'作词\w+', '', text)
    text = re.sub(r'混音/母带\w+', '', text)
    text = re.sub(r'发行\w+', '', text)
    text = re.sub(r'封面\w+', '', text)
    text = re.sub(r'特别鸣谢\w+', '', text)
    text = re.sub(r'唢呐：\w+', '', text)
    text = re.sub(r'大提琴\w+', '', text)
    text = re.sub(r'特别鸣谢\w+', '', text)
    text = re.sub(r'单簧管\w+', '', text)
    text = re.sub(r'录音\w+', '', text)
    text = re.sub(r'混音\w+', '', text)
    text = re.sub(r'吉他\w+', '', text)
    text = re.sub(r'录音\w+', '', text)
    text = re.sub(r'作曲\w+', '', text)
    text = re.sub(r'业务联系\w+', '', text)
    text = re.sub(r'版权合作\w+', '', text)
    text = re.sub(r'歌手合作\w+', '', text)
    text = re.sub(r'打击乐\w+', '', text)
    text = re.sub(r'监制\w+', '', text)
    text = re.sub(r'制作人\w+', '', text)
    text = re.sub(r'钢琴\w+', '', text)
    text = re.sub(r'bass\w+', '', text)
    text = re.sub(r'和声\w+', '', text)
    text = re.sub(r'后期\w+', '', text)
    text = re.sub(r'发行\w+', '', text)
    text = re.sub(r'mix by\w+', '', text)
    text = re.sub(r'词\w+', '', text)
    text = re.sub(r'曲\w+', '', text)
    text = re.sub(r'音乐制作人\w+', '', text)
    text = text.replace('\r', ' ')
    return text.lower()

client = OpenAI(
    api_key='YOUR KEY', 
    base_url="YOUR URL",
)

def clean_lyrics_llm(text):
    ROLE = '你是优秀的数据清洗工程师，需要从歌词文件中提取歌词的正文，去掉演唱、编曲之类的文字。'    
    USER_CONTENT = '下面是一个音乐的歌词，请进行数据清洗。直接给出清洗后的结果，不需要任何解释说明。' 
    USER_CONTENT += text

    completion = client.chat.completions.create(
        model="model-name", 
        messages = [
            {'role': 'system', 'content': ROLE},
            {'role': 'user', 'content': USER_CONTENT},
        ],
        stream=False
    )
    return completion.choices[0].message.content


for index, row in tqdm(lyrics.iterrows(), total=lyrics.shape[0]):
    ly = row['content']
    text = clean_lyrics_llm(ly)
    text = clean_lyrics(text)
    rows.append([row['city'], row['link'], text])

temp_lys = pd.DataFrame(rows, columns=['city', 'link', 'content'])


for i, r in temp_lys.iterrows():
    if len(r['content']) < 45:
        print(r['content'])

lyrics_new = temp_lys[~temp_lys['content'].str.contains('纯音乐|轻音乐', na=False) & (temp_lys['content'].str.len() >= 45)]
lyrics_new.to_csv('../clean_data/lyrics_clean.csv', index=None)