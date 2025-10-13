from sample import parse_sample_and_draw
from prompt import *
import os
import json
import pandas as pd 
from openai import OpenAI
import base64
import re
from tqdm import tqdm
import ast
import warnings
from datasets import load_from_disk
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import time
# dataset = load_dataset("Yanbin99/GVLQA-AUGLY")

# save_path = "/root/paddlejob/workspace/env_run/chuxu/laoshu/GVLQA-AUGLY-local"
# os.makedirs(save_path, exist_ok=True)

# dataset.save_to_disk(save_path)

# dataset2 = load_from_disk(save_path)
# print(dataset2)

# from huggingface_hub import snapshot_download

# # 会把整个 repo 下载到本地
# local_dir = snapshot_download(repo_id="Yanbin99/GVLQA-AUGLY",local_dir="./GVLQA-AUGLY",   # 自定义目录
#     local_dir_use_symlinks=False,repo_type="dataset")
# print(local_dir)

img_dir = './GVLQA-AUGLY'
base_dir = './GVLQA-AUGLY/data/'
total_data = []
datas = []
new_datas = []
rest_datas = []
data = load_from_disk("./GVLQA-AUGLY-local")
datas = data['test']
num_dic = defaultdict(int) 
use_text = True

for i in range(0,len(datas), 6):
    name = datas[i]['id'].split('-')
    txt_dir = base_dir + name[0] + '/graph_description/' + name[1] + '/' + name[2] + '.txt'
    if use_text:
        num_dic[name[0]+"_"+name[1]] = num_dic[name[0]+"_"+name[1]] + 1
        with open(txt_dir, 'r', encoding='utf-8') as f:
            txt_content = f.read().strip()
        new_item = dict(datas[i])
        original_string = datas[i]['conversations'][0]['value']
        new_string = txt_content + original_string[len("<image>"):]
        new_item['conversations'][0]['value'] = new_string
        # print(new_item)
        # if num_dic[name[0]+"_"+name[1] :    
        new_datas.append(new_item)
        # else:
        #     rest_datas.append(new_item)
    else:
        num_dic[name[0]+"_"+name[1]] = num_dic[name[0]+"_"+name[1]] + 1
        if num_dic[name[0]+"_"+name[1]] <= 300:    
            new_datas.append(datas[i])
        else:
            rest_datas.append(datas[i])
print(num_dic)
with open(f'./data/test_data_raw.json', 'w') as f:
    json.dump(new_datas, f)  