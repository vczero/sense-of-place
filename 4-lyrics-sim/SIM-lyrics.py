import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.manifold import MDS
from sklearn.metrics import pairwise_distances
from sklearn.cluster import SpectralClustering
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FormatStrFormatter
import cmocean

import re
import jieba

from wordcloud import WordCloud
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('../../clean_data/lyrics_clean.csv')
df['content_length'] = df['content'].str.len()
df['content_length'].describe()

cities = pd.read_csv('../../data/sa340.csv')
data_semantic = pd.read_csv('../../clean_data/city_lyrics_sim.csv', index_col='Unnamed: 0')


def show_heatmap(data):
    temp = data.values.ravel().tolist()
    plt.figure(figsize=(4, 4))  
    sns.heatmap(
        data,
        cmap='coolwarm',  
        square=True,      
        cbar_kws={
            'shrink': 0.8
        },  
        xticklabels=False,  
        yticklabels=False  
    )
    plt.tight_layout()
    plt.show()

def df2heatmap(df, name):
    plt.figure(figsize=(4, 4))
    colors = ['blue', 'white', 'red']  
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=20)

    heatmap = plt.imshow(df, cmap=custom_cmap, aspect='equal')
    
    cbar = plt.colorbar(heatmap)
    temp = df.values.ravel().tolist()
    _max = max(temp)
    _min = min(temp)
    cbar.set_ticks(np.linspace(_max, _min, 6))
    cbar.ax.set_position([0.8, 0.1, 0.03, 0.8])  
    cbar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  

    cbar.outline.set_edgecolor('#fff')
    ax = plt.gca()  
    for spine in ax.spines.values():
        spine.set_edgecolor('#fff')
    
    plt.savefig('../../Figs/similarity/sim_heatmap_' + name + '.pdf', format='pdf', bbox_inches='tight') 
    plt.show()


# 平均相似度
def get_avg_sim(data):
    city_names = data.columns
    similarity_matrix = data.values
    upper_triangle = similarity_matrix[np.triu_indices(similarity_matrix.shape[0], k=1)]
    average_similarity = upper_triangle.mean()
    print(f'平均相似度（忽略对角线）：{average_similarity}')
    print('相似度中位数', np.median(upper_triangle))


# 相似度 TOP10 city pair
def get_sim_top10_city_pair(data):
    city_names = data.index
    city_pairs = []
    n = len(city_names)
    
    for i in range(n):
        for j in range(i + 1, n): 
            city_pairs.append((city_names[i], city_names[j], data.iloc[i, j]))
    city_pairs = sorted(city_pairs, key=lambda x: x[2], reverse=True)
    
    top_N_pairs = city_pairs[:10]
    return top_N_pairs

def get_least_sim_top10_city_pair(data):
    city_names = data.index
    city_pairs = []
    n = len(city_names)
    for i in range(n):
        for j in range(i + 1, n): 
            city_pairs.append((city_names[i], city_names[j], data.iloc[i, j]))
    city_pairs = sorted(city_pairs, key=lambda x: x[2])
    bottom_N_pairs = city_pairs[:10]
    return bottom_N_pairs


df2heatmap(data_semantic, 'semantic')
get_avg_sim(data_semantic)


## 词云

def single_color_func(word=None, font_size=None, position=None, orientation=None,
                      font_path=None, random_state=None, color=None):
    return color
    
def create_word_cloud(words, type, color, size, max_font_size):
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
                   random_state=2024,
                  ).generate(' '.join(words))
    plt.imshow(wc)  
    plt.axis('off')
    plt.savefig('../../Figs/similarity/wordcloud_lyrics_' + type + '.pdf', format='pdf', bbox_inches='tight', dpi=300)
    plt.show()


def tokenize(text):
    words = jieba.lcut(text)
    stop_words = set([' ', '的', '了', '和', '是', '在', '就', '不', '还', '把',
                      '我', '你', '我们', '着', '有', '啊', '呢', '让', '去', '陪',
                      '来', '啦', '就是', '吧', '它', '回', '大', '小', '上', '说', '打',
                      '他', '会', '想', '走', '到', '人', '要', '跟', '被', '没有',
                      '也', '都', '这', '那', '而', '与', '于', '哦'])
    return [word for word in words if word.strip() and word not in stop_words]

    
def show_word_cloud(df, type, color='#398A1D', size=(700, 100), max_font_size=100):
    df = df.drop_duplicates(subset=['content']).copy()
    df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w]', '', x))
    texts = ' '.join(df['content'].tolist())
    tokenized_words = tokenize(texts)

    create_word_cloud(tokenized_words, type, color, size, max_font_size)
    print(Counter(tokenized_words).most_common(70))

show_word_cloud(df, '全部2', color='#C02E22', size=(1200,200))