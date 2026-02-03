# Mining the Sense of Place in Chinese Cities Through Pop Music and LLMs

## Abstract
Sense of place is a significant topic in human geography, playing a critical role in cultural identity, urban planning, environmental protection, and sustainable tourism development. However, current research often relies on questionnaires and interviews that focus on specific communities or cities. This approach has limitations in covering a broader range of cities and does not support automated information extraction. To address these gaps, we propose an analytical framework that uses large language models (LLMs). First, we collect theme songs (pop music) and their associated comment data for 301 cities via NetEase Cloud Music, covering most prefecture-level cities in China. Next, we develop LLM-driven models, including a lyric similarity analysis model, a sentiment classification model, and a City DNA Extractor (focusing on landmarks, food, and cultural activities). In addition, we construct a city network to explore the relationships between cities. Finally, using these models and the constructed network, we analyze the sense of place both at a national scale and at the city level. Our study demonstrates the potential of music data and LLMs in sense-of-place research, revealing strong cultural identities and a deep sense of nostalgia among young people toward their hometowns, while offering a novel methodology and perspective for exploring this concept.

How to cite:     
```
Wang, L., S. Jiang, and P. Zhang. 2026. “ Mining the Sense of Place in Chinese Cities Through Pop Music and LLMs.” Transactions in GIS 30, no. 1: e70198. https://doi.org/10.1111/tgis.70198
```

BibTex Format
```
@article{https://doi.org/10.1111/tgis.70198,
author = {Wang, Lihua and Jiang, Shengyi and Zhang, Peihao},
title = {Mining the Sense of Place in Chinese Cities Through Pop Music and LLMs},
journal = {Transactions in GIS},
volume = {30},
number = {1},
pages = {e70198},
keywords = {City DNA, LLMs, place attachment, sense of place, urban communication},
doi = {10.1111/tgis.70198},
year = {2026}
}
```

## Sense-of-Place Project Directory Structure

- **1-get-data**  
  - Folder for data collection scripts  
- **2-pre-processing**  
  - Folder for data cleaning, transformation, and preparation scripts  
- **3-sentiment-analysis**  
  - Folder for scripts related to sentiment analysis  
- **4-lyrics-sim**  
  - Folder for analyzing similarity in lyrics  
- **5-city-networks**  
  - Folder for analyzing city networks  
- **6-CityDNA-Extractor**  
  - Folder for extracting city DNA  
- **7-evaluate**  
  - Folder for evaluation metrics and scripts  
- **QGIS**  
  - Folder for geospatial data visualization        
