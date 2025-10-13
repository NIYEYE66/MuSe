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

def extract_call(output: str):
    """检测是否包含 <sample> ... </sample>"""
    match = re.search(r"<sample>(.*?)</sample>", output, re.DOTALL)
    return match.group(1).strip() if match else None

def parse_sample_call(call_str: str):
    """
    从 sample(G, root, hops) 字符串解析 root 和 hops
    """
    pattern = r"sample\(G\s*,\s*(\d+)\s*,\s*(\d+)\)"
    match = re.search(pattern, call_str)
    if not match:
        return None, None
    root, hops = int(match.group(1)), int(match.group(2))
    return root, hops

with open(f'./data/train_graph_sample.json', 'r') as f:
    total_data = json.load(f)  

for data in tqdm(total_data):
    messages = data['messages']
    image_idx = 0
    images = data['images']
    prompt = messages[0]['content']
    for msg in messages:
        if msg['role'] == 'assistant':
            call_expr = extract_call(msg['content'])
            if call_expr:

                r,h = parse_sample_call(call_expr)
                output_path = images[image_idx]

                out_path = parse_sample_and_draw(prompt,r,h,output_path)
                if out_path:
                    # saved_images.append(output_path)
                    image_idx = image_idx + 1

