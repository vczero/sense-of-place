import pandas as pd
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import math
from threading import Lock
import os
import json

df = pd.read_csv('../get-data/get_data_v2/comments.csv')
df['idx'] = range(1, len(df) + 1)

def LLM_builder(content):
    ROLE = '你是情感分类专家，擅长进行评论级别（comment-level）的情感分类任务。'
    USER_CONTENT = '下面是音乐的用户评论，请对其进行情感分类，具体要求如下：\n '    
    USER_CONTENT += '1.情感分类分为3种：正向(Positive)、负向情感(Negative) 和中性的(Neutral)；\n ' 
    USER_CONTENT += '2.需要根据评论的主要情感，给出判定，也就是一个评论最后的情感只有一个类别；\n ' 
    USER_CONTENT += '3.直接返回结果，不需要任何解释；\n ' 
    USER_CONTENT += '4.下面的案例供你参考，例如：\n '
    
    USER_CONTENT += '案例1：\n '
    USER_CONTENT += '输入：期待下次的济南之行\n '
    USER_CONTENT += '输出：Positive \n '

    USER_CONTENT += '案例2：\n '
    USER_CONTENT += '输入：新县我永远的家\n '
    USER_CONTENT += '输出：Positive \n '

    USER_CONTENT += '案例3：\n '
    USER_CONTENT += '输入：前排好嘛\n '
    USER_CONTENT += '输出：Positive \n '
    

    USER_CONTENT += '案例4：\n '
    USER_CONTENT += '输入：通州的路过\n '
    USER_CONTENT += '输出：Neutral \n '    

    USER_CONTENT += '案例5：\n '
    USER_CONTENT += '输入：成都唱生活，无锡唱文化。\n '
    USER_CONTENT += '输出：Neutral \n '

    USER_CONTENT += '案例6：\n '
    USER_CONTENT += '输入：江苏哪里\n '
    USER_CONTENT += '输出：Neutral \n'
    

    USER_CONTENT += '案例7：\n '
    USER_CONTENT += '输入：我晕 这怎么变成vip了\n '
    USER_CONTENT += '输出：Negative \n '

    USER_CONTENT += '案例8：\n '
    USER_CONTENT += '输入：说到你痛处了，碍你啥事了辽源本来就搞破鞋的多又没88你\n '
    USER_CONTENT += '输出：Negative \n '

    USER_CONTENT += '案例9：\n '
    USER_CONTENT += '输入：你是傻逼吗\n '
    USER_CONTENT += '输出：Negative \n '

    
    USER_CONTENT += '下面是用户的评论内容：'
    USER_CONTENT += content
    messages = [{"role": "system", "content": ROLE}, {"role": "user", "content": USER_CONTENT}]
    return messages


def builder(model_name, df, split='1'):
    with open('./LLM-EMO-docs/' + model_name + '_' + str(split) + '.jsonl', 'w', encoding='utf-8') as fout:
        for i, row in df.iterrows():
            text = row['user_content']
            llm_bu = LLM_builder(text)
            body = {'model': model_name, 'messages': llm_bu, 'temperature': 0.1}
            request = {'custom_id': row['idx'], 'method': 'POST', 'url': '/v1/chat/completions', 'body': body}
            fout.write(json.dumps(request, separators=(',', ':'), ensure_ascii=False) + '\n')

total_rows = len(df)
chunk_size = 50000
for i in range(0, total_rows, chunk_size):
    start = i
    end = min(i + chunk_size, total_rows)  
    file_number = i // chunk_size + 1

    builder('qwen-turbo-latest', df[i:end], file_number)
    print(f"builder('qwen-turbo-latest', df[{start}:{end}], {file_number})")


from collections import Counter
def get_data_2csv(filename):
    file_path = './LLM-EMO-docs-results/' + filename
    with open(file_path, "r", encoding="utf-8") as file:
        data_list = [json.loads(line.strip()) for line in file]

    ds =[]
    for item in data_list:
        id = item.get('custom_id') 
        text = item.get('response').get('body').get('choices')[0].get('message').get('content')
        ds.append([id, text])
    t = pd.DataFrame(ds, columns=['idx', 'label'])
    return t



def get_response_ok():
    df_success = []
    for i in range(1, 24):
        filename = str(i) + '_success.jsonl'
        df_temp = get_data_2csv(filename)
        df_success.append(df_temp)
    temp = pd.concat(df_success)
    temp.to_csv('./LLM-EMO-docs-results/all_success.csv', index=None)
    return temp

rsp_ok = get_response_ok()



def get_error():
    df_error = []
    for i in [2, 5, 9, 12, 15, 18, 22]:
        filename = str(i) + '_error.jsonl'
        file_path = './LLM-EMO-docs-results/' + filename
        with open(file_path, "r", encoding="utf-8") as file:
            data_list = [json.loads(line.strip()) for line in file]
        ds =[]
        for item in data_list:
            id = item.get('custom_id') 
            ds.append([id])
        t = pd.DataFrame(ds, columns=['idx'])
        df_error.append(t)
    return pd.concat(df_error)


def save_success_output_error():
    labels = ['Positive', 'Negative', 'Neutral']
    # res-ok-success
    success = rsp_ok[rsp_ok.label.isin(labels)]
    success.to_csv('./LLM-EMO-temp/emo_success.csv', index=None)
    # res-ok-no
    no_success_idx = temp[~temp.label.isin(labels)][['idx']]
    error_idx = get_error()
    df_errs = pd.concat([no_success_idx, error_idx])
    df_errs.to_csv('./LLM-EMO-temp/emo_error.csv', index=None)
    return success

df_su = pd.read_csv('./LLM-EMO-temp/emo_success.csv')
df_final = pd.merge(df, df_su, on='idx')

df_final.to_csv('../../clean_data/comments.csv', index=None)