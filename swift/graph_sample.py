"""
graph_sampling_visualization.py

功能：
  - 从一段自然语言的图描述中识别图的类型（无向、有向、带权、带容量、二分匹配结构），
  - 构建对应的 networkx 图结构（改进：先从描述中预建节点，再添加边，以避免孤立节点被忽略），
  - 从指定根节点做 k-hop 邻居采样（BFS），
  - 使用 graphviz (python-graphviz) 将采样得到的子图渲染并保存为图片（PNG/SVG/…）。

函数接口：
  parse_sample_and_draw(description: str, root: int, hops: int) -> str
    - 返回保存的文件名（PNG）。

依赖：
  pip install networkx graphviz
  （同时需要系统安装 graphviz 可执行文件以便 graphviz.render 能够工作）

注意：
  - 对于带向的图，采样时会同时考虑入/出邻居（保证语义上的邻域更丰富），但渲染时边仍保持方向性；
  - 对于二分匹配的描述（hosts/tasks），会将 hosts 和 tasks 放在两个不同的集合并在节点属性上标注类型；
  - 如果解析不到明显的边描述，会抛出 ValueError（保留原意）。

已修改点：
  - 在解析过程中优先尝试从描述中提取“numbered from X to Y”这类节点范围，或 hosts/tasks 的范围描述，
    并预创建所有对应节点（包含孤立无边的节点）。
  - 之后再解析各种边描述并添加边。这样可以避免仅依据边来创建节点导致遗漏孤立节点的问题。

"""

import re
import os
from collections import deque
from typing import Tuple, List

import networkx as nx
import graphviz
import base64

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

def _find_integers(s: str) -> List[int]:
    return [int(x) for x in re.findall(r"\d+", s)]


def _create_nodes_from_range(G: nx.Graph, start: int, end: int, prefix: str = None, bipartite_side: int = None):
    """Helper: 在图 G 中根据范围 [start, end] 创建节点。
    - prefix 为 None 则创建整数节点（0,1,2,...），否则创建字符串节点 f"{prefix} {i}"。
    - bipartite_side 若为 0/1 则会把属性 'bipartite' 设为对应值并且设 label。
    """
    for i in range(start, end + 1):
        if prefix is None:
            if i not in G:
                G.add_node(i, label=str(i))
        else:
            name = f"{prefix} {i}"
            if name not in G:
                attrs = {"label": name}
                if bipartite_side is not None:
                    attrs["bipartite"] = bipartite_side
                G.add_node(name, **attrs)


def parse_description(description: str) -> Tuple[nx.Graph, dict]:
    """
    解析文本，返回 (graph, meta)。
    meta 包括: {'directed': bool, 'weighted': bool, 'capacity': bool, 'bipartite': bool}

    改进要点：先尝试从描述中提取节点范围（例如："nodes are numbered from 0 to 4" 或
    "hosts numbered from 0 to 9"），预创建这些节点；随后再解析边并将边加入图中。
    """
    text = description
    lower = text.lower()

    meta = {
        'directed': False,
        'weighted': False,
        'capacity': False,
        'bipartite': False,
    }

    # ---------- 先检测是否为二分图描述（出现 hosts 和 tasks 关键字） ----------
    is_bipartite_mentioned = bool(re.search(r"\bhosts?\b", text, re.IGNORECASE) and re.search(r"\btasks?\b", text, re.IGNORECASE))
    if is_bipartite_mentioned:
        meta['bipartite'] = True
        G = nx.Graph()

        # 1) 从类似 "hosts numbered from 0 to 9" 或 "hosts numbered 0 to 9" 中提取范围
        host_ranges = re.findall(r"\bhosts?\b\s*(?:are\s*)?(?:numbered\s*(?:from\s*)?)?(\d+)\s*(?:to|\.\.|-|–)\s*(\d+)", text, re.IGNORECASE)
        for s, e in host_ranges:
            _create_nodes_from_range(G, int(s), int(e), prefix='host', bipartite_side=0)

        task_ranges = re.findall(r"\btasks?\b\s*(?:are\s*)?(?:numbered\s*(?:from\s*)?)?(\d+)\s*(?:to|\.\.|-|–)\s*(\d+)", text, re.IGNORECASE)
        for s, e in task_ranges:
            _create_nodes_from_range(G, int(s), int(e), prefix='task', bipartite_side=1)

        # 2) 解析显式的 host-task 关系（例如 "Host 5 is interested in task 4"）并补充节点/边
        for m in re.finditer(r"Host\s*(\d+)\D+task\s*(\d+)", text, re.IGNORECASE):
            h = int(m.group(1))
            t = int(m.group(2))
            h_node = f"host {h}"
            t_node = f"task {t}"
            if h_node not in G:
                G.add_node(h_node, bipartite=0, label=h_node)
            if t_node not in G:
                G.add_node(t_node, bipartite=1, label=t_node)
            G.add_edge(h_node, t_node)

        # 3) 如果只是给了 "There are 10 hosts numbered from 0 to 9, and 7 tasks numbered from 0 to 6." 之类的，
        #    上面的 ranges 已经处理。若没有范围，但出现单独的 host/task 单词和编号，则也要补节点。
        single_host_mentions = re.findall(r"Host\s*(\d+)", text, re.IGNORECASE)
        for h in single_host_mentions:
            h_node = f"host {int(h)}"
            if h_node not in G:
                G.add_node(h_node, bipartite=0, label=h_node)

        single_task_mentions = re.findall(r"task\s*(\d+)", text, re.IGNORECASE)
        for t in single_task_mentions:
            t_node = f"task {int(t)}"
            if t_node not in G:
                G.add_node(t_node, bipartite=1, label=t_node)

        return G, meta

    # ---------- 非二分图情形 ----------
    # Detect directedness
    if ' directed ' in lower or 'should be visited before' in lower or re.search(r"from node", lower):
        meta['directed'] = True
        G = nx.DiGraph()
    else:
        meta['directed'] = False
        G = nx.Graph()
    # print(meta)
    # ---------- 先尝试从描述中提取节点范围并预创建节点 ----------
    # patterns like "nodes are numbered from 0 to 4" or "nodes numbered 0 to 4"
    node_ranges = re.findall(r"\bnodes?\b\s*(?:are\s*)?(?:numbered\s*(?:from\s*)?)?(\d+)\s*(?:to|\.\.|-|–)\s*(\d+)", text, re.IGNORECASE)
    for s, e in node_ranges:
        _create_nodes_from_range(G, int(s), int(e), prefix=None)

    # 提取单个 "node 5" 的提及，也预建这些节点（避免它们只在边描述中被遗漏）
    single_node_mentions = re.findall(r"\bnode\s*(\d+)\b", text, re.IGNORECASE)
    for n in single_node_mentions:
        val = int(n)
        if val not in G:
            G.add_node(val, label=str(val))

    # ---------- 再解析不同的边描述并添加边 ----------
    # 1) simple pair list like: (0,4) (1,4) ...
    pair_matches = re.findall(r"\((\d+)\s*,\s*(\d+)\)", text)
    if pair_matches:
        for a, b in pair_matches:
            u, v = int(a), int(b)
            if u not in G:
                G.add_node(u, label=str(u))
            if v not in G:
                G.add_node(v, label=str(v))
            G.add_edge(u, v)

    # 2) lines like "node 0 should be visited before node 2"
    for m in re.finditer(r"node\s*(\d+)\s*should be visited before\s*node\s*(\d+)", text, re.IGNORECASE):
        u, v = int(m.group(1)), int(m.group(2))
        if u not in G:
            G.add_node(u, label=str(u))
        if v not in G:
            G.add_node(v, label=str(v))
        G.add_edge(u, v)

    # 3) phrases describing "an edge between node 0 and node 4 with weight 4"
    for m in re.finditer(r"edge\s+(?:between|from)\s+node\s*(\d+)\s*(?:and|to)\s*node\s*(\d+)(?:.*?weight\s*(\d+))?", text, re.IGNORECASE):
        u, v = int(m.group(1)), int(m.group(2))
        w = m.group(3)
        if u not in G:
            G.add_node(u, label=str(u))
        if v not in G:
            G.add_node(v, label=str(v))
        if w is not None:
            meta['weighted'] = True
            G.add_edge(u, v, weight=float(w))
        else:
            G.add_edge(u, v)

    # 4) capacity edges: "an edge from node 0 to node 1 with capacity 3"
    for m in re.finditer(r"edge\s+from\s+node\s*(\d+)\s+to\s+node\s*(\d+).*?capacity\s*(\d+)", text, re.IGNORECASE):
        u, v, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        meta['capacity'] = True
        if u not in G:
            G.add_node(u, label=str(u))
        if v not in G:
            G.add_node(v, label=str(v))
        G.add_edge(u, v, capacity=int(c))

    # 5) "node X to node Y" (generic directed phrase without explicit 'edge')
    for m in re.finditer(r"node\s*(\d+)\s*to\s*node\s*(\d+)", text, re.IGNORECASE):
        u, v = int(m.group(1)), int(m.group(2))
        if u not in G:
            G.add_node(u, label=str(u))
        if v not in G:
            G.add_node(v, label=str(v))
        if not G.has_edge(u, v):
            G.add_edge(u, v)

    return G, meta


def k_hop_subgraph(G: nx.Graph, root: int, k: int) -> nx.Graph:
    """
    从 root 开始做广度优先搜索，收集到 k 跳内的节点并返回 induced subgraph。
    对于有向图，搜索时会同时考虑前驱和后继（以收集更完整的邻域）；但生成的子图保留方向。
    """
    if root not in G:
        return None
        # raise ValueError(f"根节点 {root} 不在图中。")

    visited = {root}
    q = deque([(root, 0)])
    while q:
        node, dist = q.popleft()
        if dist >= k:
            continue
        # neighbors: for DiGraph include both preds and succs; for undirected just neighbors()
        if isinstance(G, nx.DiGraph):
            nbrs = set(G.predecessors(node)) | set(G.successors(node))
        else:
            nbrs = set(G.neighbors(node))
        for nb in nbrs:
            if nb not in visited:
                visited.add(nb)
                q.append((nb, dist + 1))
    return G.subgraph(visited).copy()


def draw_graphviz(subG: nx.Graph, meta: dict, out_filename: str = 'sampled_graph.png') -> str:
    """
    使用 graphviz 渲染 subgraph 并保存为 PNG。
    返回最终保存的文件名。
    """
    name = os.path.splitext(out_filename)[0]
    # fmt = os.path.splitext(out_filename)[1].lstrip('.') or 'png'
    fmt = 'png'

    if isinstance(subG, nx.DiGraph):
        gv = graphviz.Digraph(name=name, format=fmt)
    else:
        gv = graphviz.Graph(name=name, format=fmt)

    gv.attr(edge="penwidth=2")
    colors = {1: 'black', 2: 'gray24', 3: 'darkred', 4: 'darkgreen', 5: 'darkolivegreen', 6: 'dodgerblue4',
              7: 'darkviolet', 8: 'darkslateblue', 9: 'darkorange4', 10: 'deeppink4', 11: 'goldenrod4', 12: 'brown'}

    # add nodes
    for n, data in subG.nodes(data=True):
        # print(n, data)
        label = data.get('label', str(n))
        if data.get('bipartite') == 0:
            gv.node(str(n), label=label, shape='ellipse', style='filled', fillcolor='grey')
        elif data.get('bipartite') == 1:
            gv.node(str(n), label=label, shape='box', style='filled', fillcolor='white', pencolor='red')
        else:
            # 默认：灰色填充
            if label.isdigit() and len(label) == 1:
                gv.node(str(n), label=label, shape="circle", style='filled', fillcolor='grey')
            else:
                gv.node(str(n), label=label, style='filled', fillcolor='grey')

            # gv.node(str(n), label=label, style='filled', fillcolor='grey')

    # add edges with labels if present
    colors_total = 12
    for i, (u, v, data) in enumerate(subG.edges(data=True)):
        lab = ''
        if 'weight' in data:
            lab = f"{int(data['weight'])}"
        if 'capacity' in data:
            lab = f"{int(data['capacity'])}"
        color_id = (i % colors_total) + 1
        if lab:
            gv.edge(str(u), str(v), label=lab, color=colors[color_id], fontcolor=colors[color_id])
        elif meta.get('bipartite'):
            gv.edge(str(u), str(v))
        else:
            gv.edge(str(u), str(v), color=colors[color_id])

    # out_path = gv.render(filename=name, cleanup=True)
    # return out_path
    binary = gv.pipe(format=fmt)  # 渲染为 bytes
    return base64.b64encode(binary).decode("utf-8")


def parse_sample_and_draw(description: str, root: int, hops: int, out_filename='sampled_graph.png') -> str:
    """
    主函数：解析、采样、绘制并保存。
    返回保存路径。
    """
    G, meta = parse_description(description)

    # If bipartite, nodes may be strings like 'host 0'/'task 1'; ensure root provided matches that format or try to coerce
    if meta.get('bipartite'):
        root_node = None
        if isinstance(root, int):
            candidate = f"host {root}"
            if candidate in G:
                root_node = candidate
            else:
                candidate2 = f"task {root}"
                if candidate2 in G:
                    root_node = candidate2
        else:
            root_node = str(root)
        if root_node is None:
            return None
            # print("在二分图中找不到匹配的根节点。请用例如 0 或 'host 0'/'task 0' 的根节点。")
            # raise ValueError("在二分图中找不到匹配的根节点。请用例如 0 或 'host 0'/'task 0' 的根节点。")
        subG = k_hop_subgraph(G, root_node, hops)
    else:
        subG = k_hop_subgraph(G, root, hops)
    if subG == None:
        return None
    out = draw_graphviz(subG, meta, out_filename=out_filename)
    return out


def draw_whole_graph(description: str, out_filename='sampled_graph.png') -> str:
    """
    解析并绘制整个图（不做采样）。
    """
    G, meta = parse_description(description)
    out = draw_graphviz(G, meta, out_filename=out_filename)
    return out


if __name__ == '__main__':
    example_undirected = "In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge.\nThe nodes are numbered from 0 to 15, and the edges are: (0,4) (1,4) (2,4)."
    example_directed = "In a directed graph with 5 nodes numbered from 0 to 4:\nnode 0 should be visited before node 2\nnode 1 should be visited before node 2\nnode 3 should be visited before node 2\nnode 4 should be visited before node 0\nnode 4 should be visited before node 2."
    example_bipartite = '''There are 10 hosts numbered from 0 to 9, and 7 tasks numbered from 0 to 6. Each host has a set of tasks that it is interested in: .'''

    # 绘制示例二分图（会在当前目录保存文件）
    out = draw_whole_graph(example_undirected)
    print("Saved:", out)
