import csv
import json
import pandas as pd
df = pd.read_csv('../../clean_data/comments.csv')

def landmark_builder(content):
    ROLE = '你是地址提取助手。'
    USER_CONTENT = '请从下面的用户评论中提取城市、县城、景点、道路、公园、广场、学校等地址名称。要求如下：\n'    
    USER_CONTENT += '1.直接返回结果，不需要任何解释；\n' 
    USER_CONTENT += '2.如果地名出现两次及多次，则只要提取一次；\n' 
    USER_CONTENT += '3.返回结果用逗号分割。例如：西湖,西溪湿地；\n' 
    USER_CONTENT += '4.没有提取到有效地址，则返回：N。\n'
    USER_CONTENT += '下面是用户的评论：'
    USER_CONTENT += content

    messages = [{"role": "system", "content": ROLE}, {"role": "user", "content": USER_CONTENT}]
    return messages

def food_builder(content):
    ROLE = '你是菜品名称提取助手。'
    USER_CONTENT = '请从下面的用户评论中提取菜品和饮食。要求如下：\n'    
    USER_CONTENT += '1.直接返回结果，不需要任何解释；\n' 
    USER_CONTENT += '2.如果菜名出现两次及多次，则只要提取一次；\n' 
    USER_CONTENT += '3.返回结果用逗号分割。例如：麻婆豆腐,火锅；\n' 
    USER_CONTENT += '4.没有提取到有效菜名，则返回：N。\n'
    USER_CONTENT += '下面是用户的评论：'
    USER_CONTENT += content

    messages = [{"role": "system", "content": ROLE}, {"role": "user", "content": USER_CONTENT}]
    return messages

def culture_builder(content):
    ROLE = '你是文化活动名称提取助手。'
    USER_CONTENT = '请从下面的用户评论中提取中华传统文化活动名称，例如戏曲等。要求如下：\n'    
    USER_CONTENT += '1.直接返回结果，不需要任何解释；\n' 
    USER_CONTENT += '2.如果名称出现两次及多次，则只要提取一次；\n' 
    USER_CONTENT += '3.返回结果用逗号分割。例如：京剧,瓷器；\n' 
    USER_CONTENT += '4.没有提取到有效名称，则返回：N。\n'
    USER_CONTENT += '下面是用户的评论：'
    USER_CONTENT += content

    messages = [{"role": "system", "content": ROLE}, {"role": "user", "content": USER_CONTENT}]
    return messages

def builder(model_name, df, func_builder, _dir,split='1'):
    
    with open('./CityDNA_docs/' + _dir + '/' + _dir + '_' + model_name + '_' + str(split) + '.jsonl', 'w', encoding='utf-8') as fout:
        for i, row in df.iterrows():
            text = row['user_content']
            llm_bu = func_builder(text)
            body = {'model': model_name, 'messages': llm_bu, 'temperature': 0.1}
            request = {'custom_id': row['idx'], 'method': 'POST', 'url': '/v1/chat/completions', 'body': body}
            fout.write(json.dumps(request, separators=(',', ':'), ensure_ascii=False) + '\n')


total_rows = len(df)
chunk_size = 50000
for i in range(0, total_rows, chunk_size):
    start = i
    end = min(i + chunk_size, total_rows)  
    file_number = i // chunk_size + 1

    builder('qwen-turbo-latest', df[i:end], landmark_builder, 'landmark', file_number)
    builder('qwen-turbo-latest', df[i:end], food_builder, 'food', file_number)
    builder('qwen-turbo-latest', df[i:end], culture_builder, 'culture', file_number)
    print(f"builder('qwen-turbo-latest', df[{start}:{end}], {file_number})")
    