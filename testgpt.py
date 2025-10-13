
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


# ====== 初始化对话 ======

def chat_with_gpt(user_message, messages, client):
    """发送消息到 GPT，获取输出"""
    messages.append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-4o",   # 或 gpt-4.1 / gpt-4o
        messages=messages
    )
    output = response.choices[0].message.content
    messages.append({"role": "assistant", "content": output})
    return output

def chat_with_gpt_image(image_path: str, messages, client, text_hint="Here is the sampled subgraph image"):
    """将图片作为 user 消息发给 GPT"""
    if image_path:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        image_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": text_hint},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
            ]
        }
    else:
        image_message = {
            "role": "user",
            "content": [
                {"type": "text", "text": "The selected root node does not exist, please try again."}
            ]
        }
    messages.append(image_message)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    output = response.choices[0].message.content
    messages.append({"role": "assistant", "content": output})
    return output

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

def get_openai_response(image_path, prompt, answer, api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.wlai.vip/v1/"
    )
    task = image_path.split('/')[3]
    # print(task)
    # example = example_list[task]
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(ground_truth=answer, example=example_list['connectivity'])},]
    output = chat_with_gpt(prompt,messages,client)
    # print("GPT:", output)
    # print(messages)
    sample_times = 0
    try_times = 0
    # 检查是否需要调用 sample
    saved_images = []
    while 'Answer' not in output:
        time.sleep(1)
        try_times = try_times + 1
        if try_times > 20:
            break
        call_expr = extract_call(output)
        if call_expr:
            # print("Detected call:", call_expr)
            r,h = parse_sample_call(call_expr)
            sample_times = sample_times + 1
            output_path = image_path[:-4] + '_' + str(sample_times) + '.png'
            # 假设我们生成了一张子图图片 sample.png

            out_path = parse_sample_and_draw(prompt,r,h,output_path)
            if out_path:
                saved_images.append(output_path)
            output = chat_with_gpt_image(out_path,messages,client)
            # print("GPT:", output)
    im_idx=0
    for msg in messages:
        if msg['role'] == 'user':
            if type(msg['content']) == str:
                continue
            for item in msg['content']:
                if item['type'] =="image_url":
                    item["image_url"] = saved_images[im_idx]
                    im_idx=im_idx+1

    return messages[1:]


def multi_thread_openai(prompts, answers, image_paths, api_key, batch_size=10, sleep_time=1):
    results = [None] * len(prompts)

    for batch_start in range(0, len(prompts), batch_size):
        batch_end = min(batch_start + batch_size, len(prompts))
        batch_prompts = prompts[batch_start:batch_end]
        batch_answers = answers[batch_start:batch_end]
        batch_images = image_paths[batch_start:batch_end]  # 按照批次切分图片路径
        print(f"Processing batch {batch_start} to {batch_end}")
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            # 提交任务，确保每个线程处理一张图片
            futures = [executor.submit(get_openai_response, image_path, prompt, answer, api_key) 
                       for prompt, answer, image_path in zip(batch_prompts, batch_answers, batch_images)]

            # 阻塞等待每个任务完成，按顺序获取结果
            for i, future in enumerate(futures):
                results[batch_start + i] = future.result()  # 将结果放到对应的位置

        # 一批发完，停1秒
        time.sleep(sleep_time)
    # print(results)
    return results

def main():
    api_key = ""

    img_dir = './GVLQA-AUGLY'
    base_dir = './GVLQA-AUGLY/data/'
    total_data = []
    datas = []
    new_datas = []
    rest_datas = []
    data = load_from_disk("./GVLQA-AUGLY-local")
    datas = data['train']
    num_dic = defaultdict(int) 
    use_text = True
    if os.path.exists('./data/train_graph_sample_next.json'):
        with open('./data/train_graph_sample_next.json', 'r', encoding='utf-8') as f:
            new_datas = json.load(f)
    else:
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
                if num_dic[name[0]+"_"+name[1]] <= 300:    
                    new_datas.append(new_item)
                else:
                    continue
                    rest_datas.append(new_item)
            else:
                num_dic[name[0]+"_"+name[1]] = num_dic[name[0]+"_"+name[1]] + 1
                if num_dic[name[0]+"_"+name[1]] <= 300:    
                    new_datas.append(datas[i])
                else:
                    rest_datas.append(datas[i])
        with open(f'./data/train_data_raw.json', 'w') as f:
            json.dump(new_datas, f)
        with open(f'./data/rest_train_data_raw.json', 'w') as f:
            json.dump(rest_datas, f)  
    if os.path.exists("./data/train_data_next_gpt_original.json"):
        with open("./data/train_data_next_gpt_original.json", 'r', encoding='utf-8') as f:
            total_data = json.load(f)
    large_batch = 10
    st = len(total_data)

    for batch_start in tqdm(range(st, len(new_datas), large_batch)):
        print(batch_start)
        batch_end = min(batch_start + large_batch, len(new_datas))
        batch_datas = new_datas[batch_start:batch_end]
          
        prompts = []
        answers = []
        for i, data in enumerate(batch_datas):
            prompts.append(data['conversations'][0]['value'])
            answers.append(data['conversations'][1]['value'])
        image_paths = [os.path.join(img_dir, data['image']) for data in batch_datas]

        results = multi_thread_openai(prompts, answers, image_paths, api_key, batch_size=10, sleep_time=1)
        # Preparation for inference
        for message in results:
            total_data.append(message)
        # if len(total_data)%large_batch==0:
        with open(f'./data/train_data_next_gpt_original.json', 'w') as f:
            json.dump(total_data, f, indent=2, ensure_ascii=False)  
    
# ====== 示例使用 ======
if __name__ == "__main__":
    # 第一个问题
    main()