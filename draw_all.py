import os
from pathlib import Path
from sample import draw_whole_graph
# 假设你已经有这个函数
# def draw_whole_graph(graph_content: str, out_filename: str):
#     ...

# 输入固定目录
# 'connectivity','cycle','flow','hamilton','matching','shortest_path',
for task in ['connectivity','cycle','flow','hamilton','matching','shortest_path','topology']:
    input_root = Path(f"./GVLQA-AUGLY/data/{task}/graph_description")
    # 输出根目录
    output_root = Path(f"./GVLQA-AUGLY/data/{task}/graph_visual/layout/dot")

    for dirpath, dirnames, filenames in os.walk(input_root):
        for filename in filenames:
            if filename.startswith("graph") and filename.endswith(".txt"):
                input_file = Path(dirpath) / filename
                
                # 读取图描述内容
                with open(input_file, "r", encoding="utf-8") as f:
                    graph_content = f.read()
                
                # 构建输出路径：保持相对路径，但放到 output_root 下
                relative_path = input_file.relative_to(input_root).parent  # graphxxx.txt 所在目录相对路径
                out_dir = output_root / relative_path
                out_dir.mkdir(parents=True, exist_ok=True)
                
                out_file = out_dir / (input_file.stem + ".png")

                # if os.path.exists(out_file):
                #     continue
                # else:
                #     print(out_file)
                draw_whole_graph(graph_content, str(out_file))
                # break
    print(f"Done: {task}")
