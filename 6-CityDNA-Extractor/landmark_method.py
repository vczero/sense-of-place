import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm

sa = pd.read_csv('../../data/sa340.csv')

toponym = pd.read_csv('./results/landmark/DNA_landmark_study.csv')

def get_word_list():
    lds = toponym['DNA_landmark'].tolist()
    lds_arr = []
    for i in lds:
        lds_arr += i.split(',')
    return lds_arr

def get_word_count(word_list, num=20):
    word_counts = Counter(word_list)
    top_keywords = word_counts.most_common(num)
    return top_keywords

def single_color_func(word=None, font_size=None, position=None, orientation=None,
                      font_path=None, random_state=None, color=None):
    return color
    
def show_word_cloud(word_freq, type, color='#398A1D', size=(700, 100), max_font_size=100):
    def custom_color_func(word=None, font_size=None, position=None, orientation=None,
                          font_path=None, random_state=None):
        return single_color_func(word, font_size, position, orientation, font_path, random_state, color=color)
        
    wc = WordCloud(font_path="/System/Library/fonts/PingFang.ttc",
                   collocations=False,
                   background_color='#ffffff',
                   color_func=custom_color_func,
                   scale=4,
                   width=size[0],
                   height=size[1],
                   max_font_size = max_font_size,
                   random_state=2025,
                  ).generate_from_frequencies(word_freq)
    plt.imshow(wc)  
    plt.axis('off')
    plt.savefig('./results/landmark/landmark-' + type + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.show()

# 1.Landmarks 规则解析
stopwords = pd.read_csv('./stopwords.csv')
# 去掉超大区域:省市区，以及stopwords
def gen_stopwords():
    pros = sa['pro_shortname'].tolist()
    cities = sa['city_shortname'].tolist()
    cities = [i.split('+')[0] for i in cities]
    sts = stopwords['words'].tolist() + cities + pros
    return sts

# 解析出local place name
def get_word_list_toponym(city_name=None):
    ws = []
    lds = get_word_list()
    stopwrds = gen_stopwords()
    for i in lds:
        if i not in stopwrds:
            ws.append(i)
    return ws

def get_landmarks_poi_name():
    res = []
    stopws = gen_stopwords()
    for i, r in toponym.iterrows():
        landmark_row = r['DNA_landmark'].split(',')
        city = r['city']
        for ld in landmark_row:
            if ld not in stopws and '区' not in ld:
                res.append([city, city + ld, ld])

    temp = pd.DataFrame(res, columns=['city', 'poi_name', 'landmark'])
    temp.to_csv('./results/landmark/landmarks_temp_poi_names.csv', index=None)

get_landmarks_poi_name()


# 2 POI 地理编码
# 使用python 异步代码执行数据，提高请求效率 (执行poi2lnglat.py)
# 只能保证模糊地名是存在的
# 需要过滤重复解析的数据，
pois = pd.read_csv('./results/landmark/landmarks_temp_pois_lnglat.csv')
pois = pois.drop_duplicates(subset=['city', 'poi_name'])
pois.to_csv('../QGIS/CityDNA/landmarks.csv', index=None)


# 3.正则统计
pois = pd.read_csv('./results/landmark/landmarks_temp_pois_lnglat.csv')
pois['poi_name'] = pois.apply(lambda row: row['poi_name'].replace(row['city'], ''), axis=1)
pois = pd.DataFrame(pois)

# 关键字查询
# 包含：include_keywords
# 排除：exclude_keywords
def get_landmarks_num_by_keywords(include_keywords, exclude_keywords):
    include_condition = pois['poi_name'].str.contains('|'.join(include_keywords))
    exclude_condition = ~pois['poi_name'].str.contains('|'.join(exclude_keywords))
    filtered_pois = pois[include_condition & exclude_condition]
    return len(filtered_pois), filtered_pois


# 后缀
# 包含：include_keywords
# 排除：exclude_keywords
def get_landmarks_num_by_suffix(include_keywords, exclude_keywords):
    keyword_pattern = f"(?:{'|'.join(include_keywords)})$"
    include_condition = pois['poi_name'].str.contains(keyword_pattern, regex=True)
    exclude_condition = ~pois['poi_name'].str.contains('|'.join(exclude_keywords))
    filtered_pois = pois[include_condition & exclude_condition]
    return len(filtered_pois), filtered_pois

# 后缀
def get_landmarks_num_by_suffix2(include_keywords):
    keyword_pattern = f"(?:{'|'.join(include_keywords)})$"
    include_condition = pois['poi_name'].str.contains(keyword_pattern, regex=True)
    filtered_pois = pois[include_condition]
    return len(filtered_pois), filtered_pois

# 4.城市分析
def df2freq_dict(city):
    df = pois[pois.city==city]
    poi_counter = Counter(df['poi_name'].tolist())
    poi_count_df = pd.DataFrame(poi_counter.items(), columns=['poi_name', 'count'])
    poi_count_df = poi_count_df.sort_values(by='count', ascending=False).reset_index(drop=True)
    poi_count_df.to_csv('./results/landmark/POI-' + city + '.csv', index=None)
    return poi_counter
    
def get_landmarks_by_topN(city, topk):
    df = pois[pois.city==city]
    poi_counter = Counter(df['poi_name'].tolist())
    return poi_counter.most_common(topk)

def get_category_topk(df, topk):
    temp = df[['city', 'poi_name']]
    grouped_df = temp.groupby(['city', 'poi_name']).size().reset_index(name='count')
    grouped_df = grouped_df.sort_values(by='count', ascending=False).reset_index(drop=True)
    return grouped_df.head(topk)

show_word_cloud(df2freq_dict('杭州市'), '杭州市', color='#312AFA', size=(350, 350))