import json
from pathlib import Path
from sample import draw_whole_graph

def rebuild_images_from_json(json_path: str):
    json_path = Path(json_path)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        image_path = item.get("image")
        graph_content = item["conversations"][0]["value"]
    
        out_file = Path(image_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
    
        draw_whole_graph(graph_content, str(out_file))

if __name__ == "__main__":
    rebuild_images_from_json("data/LGVLQA.json")
