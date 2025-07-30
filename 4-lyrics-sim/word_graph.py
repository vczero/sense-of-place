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

from itertools import combinations
import networkx as nx

df = pd.read_csv('../../clean_data/lyrics_clean.csv')

def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set([line.strip() for line in f])
    return stopwords

stopwords_file = 'stopwords.txt'
stopwords = load_stopwords(stopwords_file)

def tokenize(text, stopwords):
    words = jieba.lcut(text)
    return [word for word in words if word not in stopwords and len(word) > 1]

df['tokens'] = df['content'].apply(lambda x: tokenize(x, stopwords))

co_occurrence = Counter()
for tokens in df['tokens']:
    for pair in combinations(set(tokens), 2): 
        co_occurrence[frozenset(pair)] += 1

co_occurrence_df = pd.DataFrame(
    [(list(pair)[0], list(pair)[1], count) for pair, count in co_occurrence.items()],
    columns=['keyword1', 'keyword2', 'weight']
)

threshold = 20
co_occurrence_df = co_occurrence_df[co_occurrence_df['weight'] >= threshold]


G = nx.Graph()


for _, row in co_occurrence_df.iterrows():
    G.add_edge(row['keyword1'], row['keyword2'], weight=row['weight'])


# plt.figure(figsize=(12, 12))
# node_size = [G.degree(node) * 100 for node in G.nodes()]
# edge_width = [G[u][v]['weight'] for u, v in G.edges()]
# pos = nx.spring_layout(G, seed=42)  
# nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='skyblue', alpha=0.7)
# nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.6)
# nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# plt.title("Keyword Co-occurrence Network", fontsize=16)
# plt.axis('off')
# plt.show()

# Keyword Co-occurrence Network
nx.write_gexf(G, "keyword_cooccurrence_network.gexf")