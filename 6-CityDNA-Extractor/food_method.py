import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm

sa = pd.read_csv('../../data/sa340.csv')
food = pd.read_csv('./results/food/DNA_food_study.csv')

def single_color_func(word=None, font_size=None, position=None, orientation=None,
                      font_path=None, random_state=None, color=None):
    return color
    
def show_word_cloud(word_freq, type, color='#398A1D', size=(700, 100), max_font_size=100):
    def custom_color_func(word=None, font_size=None, position=None, orientation=None,
                          font_path=None, random_state=None):
        return single_color_func(word, font_size, position, orientation, font_path, random_state, color=color)
        
    wc = WordCloud(font_path='/System/Library/fonts/PingFang.ttc',
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
    plt.savefig('./results/food/food-' + type + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.show()

stopwords = ['加油鸭', '人生一串', '羊', '猪', '牛', '校友鸭', 'zi', '骨', '肉', '嘎腰子', 'N', '呱呱']
def get_food_feq(city=None):
    foods = food.copy()
    if city != None:
         foods = foods[foods.city==city]
    foods = foods['DNA_food'].tolist()
    fds = []
    for f in foods:
        fds += f.split(',')
    cts = Counter(fds)
    for st in stopwords:
        if st in cts:
            del cts[st]
    return cts


def get_food_df():
    food = get_food_feq()
    df = pd.DataFrame(list(food.items()), columns=['food', 'count'])
    df = df.sort_values(by='count', ascending=False)
    return df


def get_food_count(df, keyword):
    temp = df[df.food.str.contains(keyword)]
    return keyword + '', temp['count'].sum()

show_word_cloud(get_food_feq(), '全部', color='#312AFA', size=(1200, 150))
# food_df = get_food_df()
# get_food_count(food_df, '烤')
# get_food_count(food_df, '锅')
# get_food_count(food_df, '面')
# get_food_count(food_df, '粉')
# get_food_count(food_df, '饺')
# get_food_count(food_df, '馍')

# 城市（区域）
def get_city_count_by_keyword(keyword):
    temp = food[food.DNA_food.str.contains(keyword)]
    city_counts = temp['city'].value_counts()
    
    t1 = city_counts.reset_index()
    t1.columns = ['name', 'count']
    t2 = pd.merge(t1, sa[['name', 'en_name', 'center']])
    t2 = t2.sort_values(by='count', ascending=False)
    print('城市数量', len(t2))

show_word_cloud(get_food_feq('安庆市'), '安庆市', color='#312AFA', size=(300, 520))