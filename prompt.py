example_list = {
    'connectivity':'''messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge.\nThe nodes are numbered from 0 to 9, and the edges are:  (1,2) (1,5) (2,8) (2,5) (3,5) (3,7) (4,9) (5,6) (5,8) (5,7) (6,7).\nIs there a path between node 1 and node 6 in this undirected graph?"}
    ]},
    {"role": "assistant", "content": "<think> I need to check whether node 1 and node 6 are connected.  
First, I will sample the neighborhood of node 1 within 2 hops to see its connections. </think>  
<sample> sample(G, 1, 2) </sample>"}
    {"role": "user", "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/graph1.png"}}
    ]},
    {"role": "assistant", "content": "<think> From the sample I see that node 1 connects to node 5, and node 5 connects to node 6.  
This shows that a path exists. </think>  
Answer: Yes."}
]''', 
    'cycle':'''messages = [
    {
      "role": "user",
      "content": "In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge.\nThe nodes are numbered from 0 to 8, and the edges are: (5,2) (3,6) (1,0) (5,4) (3,1) (0,8) (6,7) (1,5) (0,5).\nIs there a cycle in this undirected graph?"
    },
    {
      "role": "assistant",
      "content": "<think> To determine if there is a cycle in an undirected graph, I'll need to traverse the graph and look for nodes that can be revisited (as part of the traversal), without revisiting the immediate predecessor.\n\nFirst, I will sample the neighborhood starting from any node, such as node 0, at 2 hops to get a sense of connections around it. This will allow me to analyze paths and potential revisit points. </think>  \n<sample> sample(G, 0, 2) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/cycle/graph_visual/layout/dot/easy/graph216_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, I observe several connections. I can use the subgraph to determine cycles by tracing paths:\n\n1. Starting point: Node 0 connects to nodes 1, 5, and 8. \n2. Node 1 connects to nodes 0, 3, and 5.\n3. Node 5 connects to nodes 0, 1, 2, and 4.\n\nI immediately notice there is a potential for cycles, as node 5 connects back to node 0 and node 1, both of which are already connected to other parts of the graph. For instance, if we trace around nodes 0 -> 1 -> 5 -> 0, there is already a cycle. \n\nThis reasoning suffices without further sampling. </think>  \nAnswer: Yes."
    }
  ]''',
  'flow':'''messages = [
    {
      "role": "user",
      "content": "In a directed graph, the nodes are numbered from 0 to 8, and the edges are:\nan edge from node 0 to node 5 with capacity 4,\nan edge from node 0 to node 2 with capacity 2,\nan edge from node 0 to node 8 with capacity 3,\nan edge from node 1 to node 4 with capacity 7,\nan edge from node 3 to node 5 with capacity 4,\nan edge from node 3 to node 0 with capacity 3,\nan edge from node 3 to node 8 with capacity 7,\nan edge from node 5 to node 6 with capacity 6,\nan edge from node 8 to node 5 with capacity 1,\nan edge from node 8 to node 3 with capacity 3,\nan edge from node 8 to node 7 with capacity 2.\nThis graphic illustrates a directed graph, with each edge's capacity indicated by a numerical label in close proximity.\nQ: What is the maximum flow from node 8 to node 6:"
    },
    {
      "role": "assistant",
      "content": "<think> To calculate the maximum flow from node 8 to node 6, we need to analyze all possible paths from node 8 to node 6 and their capacities, while considering the directed structure of the graph. We should also account for how capacities are distributed across these paths. \n\nFirst, I will sample the 2-hop neighborhood of node 8 to identify connections potentially leading to node 6. This will provide the immediate connections from node 8 and subsequent possibilities within one more step. </think>\n\n<sample> sample(G, 8, 2) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/flow/graph_visual/layout/dot/easy/graph208_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, I see the outgoing connections from node 8, leading to nodes 5, 3, and 7 with respective capacities 1, 3, and 2. For node 6, it can only be reached directly from node 5 with a capacity of 6.\n\nTo determine all possible paths from node 8 to node 6 and calculate the maximum flow, I must evaluate:\n- Paths from node 8 to node 5 and further to node 6.\n- Paths from node 8 to node 3, then possibly to node 5 and finally to node 6.\n\nThe goal will be to aggregate the bottleneck capacities of these paths while adhering to edge constraints. I now have sufficient information to compute the maximum flow. </think>\n\nAnswer: The maximum flow from node 8 to node 6 is determined by the following paths:\n- Path1: 8 -> 5 -> 6, with a bottleneck capacity of min(1, 6) = 1.\n- Path2: 8 -> 3 -> 5 -> 6, with a bottleneck capacity of min(3, 4, 6) = 3.\n\nAggregating these flow contributions gives a maximum flow of 1 + 3 = 4.\n\nAnswer: 4."
    }
  ]''',
  'hamilton':'''messages = [
    {
      "role": "user",
      "content": "In an undirected graph, (i,j) means that node i and node j are connected with an undirected edge.\nThe nodes are numbered from 0 to 9, and the edges are: (3,8) (9,0) (2,3) (6,7) (4,8) (1,7) (9,2) (6,2) (4,2) (3,6) (6,1) (5,1) (4,9) (3,5) (3,7) (8,5) (4,7).\nQ: Begin with node 0, what is the path in this graph that visits every node exactly once?"
    },
    {
      "role": "assistant",
      "content": "<think> The problem requires finding a path that visits every node exactly once, starting with node 0. This is a Hamiltonian path problem.\n\nTo solve this, I need to explore the connections of node 0 and then recursively map connections from other nodes while ensuring each node is visited only once.\n\nFirst, I will sample the neighborhood of node 0 within 1 hop to understand its immediate connections. </think>\n<sample> sample(G, 0, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 0 is directly connected to node 9. To explore a potential Hamiltonian path, I need to move to node 9 and explore its connections while ensuring I avoid revisiting nodes.\n\nNext, I will sample the neighborhood of node 9 within 1 hop to identify its connections. </think>\n<sample> sample(G, 9, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_2.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sample, I see that node 9 is connected to nodes 0, 2, and 4. We've already visited node 0, so we need to consider node 9's connections to nodes 2 and 4 for extending our path. \n  \nBoth nodes 2 and 4 could potentially lead to visiting all other nodes. I will explore node 2 next, as nodes with more connections might offer more pathways later in the process.\n\nI will sample the neighborhood of node 2 within 1 hop to identify its connections. </think>\n<sample> sample(G, 2, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_3.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 2 is connected to nodes 9 (already visited), 3, 4, and 6. Among these, node 4 is already visible from node 9's connections, so a logical next step is to move to node 3 as it progresses us toward unvisited nodes.\n\nNext, I will sample the neighborhood of node 3 within 1 hop to examine its connections. </think>\n<sample> sample(G, 3, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_4.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 3 is connected to nodes 2 (already visited), 6, 7, 5, and 8. The unvisited nodes here are 6, 7, 5, and 8. To maximize path continuity, I will proceed to node 6 next, as it directly connects with other unvisited nodes.\n\nNext, I will sample the neighborhood of node 6 within 1 hop to explore its connections. </think>\n<sample> sample(G, 6, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_5.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 6 is connected to nodes 3 (already visited), 2 (already visited), 7, and 1. The unvisited nodes here are 7 and 1. I will proceed to node 7 next, as it connects to other unexplored parts of the graph.\n\nNext, I will sample the neighborhood of node 7 within 1 hop to examine its connections. </think>\n<sample> sample(G, 7, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_6.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 7 is connected to nodes 3 (already visited), 4, 6 (already visited), and 1. The unvisited nodes here are 4 and 1. To move toward completing the path, I will proceed to node 4, as it connects us to fewer remaining unexplored nodes.\n\nNext, I will sample the neighborhood of node 4 within 1 hop to examine its connections. </think>\n<sample> sample(G, 4, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_7.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 4 is connected to nodes 9 (already visited), 2 (already visited), 7 (already visited), and 8. The only unvisited node here is node 8.\n\nI will proceed to node 8 next, as it is the only option left to complete the path.\n\nFinally, I will confirm the connections of node 8 within 1 hop. </think>\n<sample> sample(G, 8, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_8.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 8 is connected to nodes 4 (already visited), 3 (already visited), and 5. The only unvisited node here is node 5.\n\nI will now proceed to node 5, which completes the visit to all nodes. </think>\n<sample> sample(G, 5, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/hamilton/graph_visual/layout/dot/easy/graph208_9.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled result, I see that node 5 is connected to nodes 3 (already visited), 8 (already visited), and 1. The only unvisited node here is node 1.\n\nBy moving to node 1, we complete the Hamiltonian path, as all nodes will have been visited exactly once. The path can now be constructed based on the visited sequence. </think>\n\nAnswer:0->9->2->3->8->4->7->6->1->5."
    }
  ]''',
  'matching':'''messages = [
    {
      "role": "user",
      "content": "There are 4 hosts numbered from 0 to 3, and 4 tasks numbered from 0 to 3. Each host has a set of tasks that it is interested in: \nHost 1 is interested in task 1.\nHost 1 is interested in task 3.\nHost 0 is interested in task 3.\nHost 2 is interested in task 2.\nHost 1 is interested in task 2.\nHost 2 is interested in task 1..\nThere are 4 hosts numbered from 0 to 3, and 4 tasks numbered from 0 to 3. Each host has a set of tasks that it is interested in, represented by arrows from a host to a task in the diagram. However, each host is capable of solving only one task, and similarly, each task can be resolved by just one host.\nQ:  What is the maximum number of hosts that can be assigned a task they are interested in?"
    },
    {
      "role": "assistant",
      "content": "<think> This problem can be modeled as a bipartite graph matching problem. In the bipartite graph, one partition contains the hosts (0 to 3), and the other partition contains the tasks (0 to 3). An edge exists between a host and a task if the host is interested in that task.\n\nTo solve this, we need to find the maximum matching in the bipartite graph where each host can be matched to at most one task, and each task can be matched to at most one host.\n\nFirst, I will construct the graph and then explore the connections starting from each node to check possible matchings. I will sample from any host to explore its neighbors to find the matches. I will start with host 0. </think>\n<sample> sample(G, 0, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/matching/graph_visual/layout/dot/easy/graph56_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, host 0 is interested in task 3. Now I need to explore the interests of the other hosts to determine possible matches. I will sample the neighbors of host 1 next. </think>  \n<sample> sample(G, 1, 1) </sample>  "
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/matching/graph_visual/layout/dot/easy/graph56_2.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, host 1 is interested in tasks 1, 2, and 3. I'll continue exploring the neighbors of the next host, host 2, to uncover more potential assignments. </think>  \n<sample> sample(G, 2, 1) </sample>  "
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/matching/graph_visual/layout/dot/easy/graph56_3.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, host 2 is interested in tasks 1 and 2. Now I need to explore the neighbors of the final host, host 3, to complete the graph exploration. </think>  \n<sample> sample(G, 3, 1) </sample>  "
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/matching/graph_visual/layout/dot/easy/graph56_4.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> Host 3 does not have any interests, which means it cannot be matched to any task. Now, I have all the information regarding the hosts and their interests in tasks:\n\n- Host 0 is interested in task 3.\n- Host 1 is interested in tasks 1, 2, and 3.\n- Host 2 is interested in tasks 1 and 2.\n- Host 3 has no interests.\n\nUsing this information, I need to compute the maximum matching in the bipartite graph. I will assign tasks to hosts in such a way that no host or task is assigned more than once:\n\n1. Assign task 3 to host 0 (as it uniquely matches host 0).\n2. Assign task 2 to host 1.\n3. Assign task 1 to host 2.\n\nThis results in a total of 3 hosts assigned tasks they are interested in. Hosts 0, 1, and 2 are matched, while host 3 remains unmatched (due to lack of interest). </think>\n\nAnswer: 3."
    }
  ]''',
    'shortest_path':'''messages = [
    {
      "role": "user",
      "content": "In a undirected graph, the nodes are numbered from 0 to 6, and the edges are:\nan edge between node 0 and node 1 with weight 3,\nan edge between node 3 and node 0 with weight 4,\nan edge between node 0 and node 2 with weight 1,\nan edge between node 0 and node 6 with weight 1,\nan edge between node 1 and node 5 with weight 1,\nan edge between node 1 and node 3 with weight 1,\nan edge between node 1 and node 4 with weight 1,\nan edge between node 6 and node 1 with weight 3,\nan edge between node 5 and node 2 with weight 3,\nan edge between node 3 and node 2 with weight 2,\nan edge between node 4 and node 2 with weight 1,\nan edge between node 2 and node 6 with weight 2,\nan edge between node 3 and node 5 with weight 1,\nan edge between node 3 and node 4 with weight 1,\nan edge between node 3 and node 6 with weight 4,\nan edge between node 5 and node 4 with weight 3,\nan edge between node 6 and node 4 with weight 3,\nan edge between node 5 and node 6 with weight 2.\nThis graphic illustrates an undirected graph, with each edge's distance or length indicated by a numerical label in close proximity.\nQ: What is the shortest path from node 5 to node 0?"
    },
    {
      "role": "assistant",
      "content": "<think> In order to find the shortest path from node 5 to node 0 in this graph, I should use Dijkstra's algorithm since the graph has weighted edges, and the weights are non-negative. To do this, I need to explore the graph starting from node 5 and determine the shortest path towards node 0. I will begin by sampling the neighborhood of node 5 to inspect its directly connected nodes and their distances. </think>\n<sample> sample(G, 5, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/shortest_path/graph_visual/layout/dot/easy/graph169_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, I can see the following neighbors and respective edge weights for node 5:\n\n- Node 6 with a weight of 2.\n- Node 4 with a weight of 3.\n- Node 1 with a weight of 1.\n- Node 3 with a weight of 1.\n- Node 2 with a weight of 3.\n\nTo find the shortest path to node 0, I need to continue exploring the graph, starting with these neighboring nodes based on their distances. I will sample further from relevant nodes to construct the complete shortest path. I will next sample the neighborhood of node 6, as it is directly connected to node 5 and may provide the shortest route towards node 0 or other intermediate nodes. </think>\n<sample> sample(G, 6, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/shortest_path/graph_visual/layout/dot/easy/graph169_2.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, I can now see the following neighbors and edge weights for node 6:\n\n- Node 0 with a weight of 1.\n- Node 1 with a weight of 3.\n- Node 2 with a weight of 2.\n- Node 4 with a weight of 3.\n- Node 5 with a weight of 2.\n\nSince node 0 is directly connected to node 6 with a weight of 1, it shows a potential direct path from node 5 to node 0 through node 6 with a total weight of \\(2 (from\\ 5\\ to\\ 6) + 1 (from\\ 6\\ to\\ 0) = 3\\). \n\nTo ensure this is the shortest path, I need to confirm if there are any shorter paths to node 0 through other intermediate nodes (e.g., node 1 or node 3). Next, I will sample the neighbors of node 1 as it is also directly connected to node 5. Sampling node 1 may reveal alternate shorter routes to node 0. </think>\n<sample> sample(G, 1, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/shortest_path/graph_visual/layout/dot/easy/graph169_3.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> From the sampled subgraph, I can see that the neighbors and edge weights for node 1 are as follows:\n\n- Node 0 with a weight of 3.\n- Node 3 with a weight of 1.\n- Node 4 with a weight of 1.\n- Node 5 with a weight of 1.\n- Node 6 with a weight of 3.\n\nNow, evaluating paths to node 0:\n- The path from node 5 -> node 1 -> node 0 has a total weight of \\(1 (from\\ 5\\ to\\ 1) + 3 (from\\ 1\\ to\\ 0) = 4\\).\n- This is heavier than the earlier discovered path from node 5 -> node 6 -> node 0 with a total weight of 3.\n\nThus, the shortest path remains 5 -> 6 -> 0. No further sampling is needed as we have identified the path with the minimal cost. </think>\n\nAnswer:3."
    }
  ]''',
    'topology':'''messages = [
    {
      "role": "user",
      "content": "In a directed graph with 7 nodes numbered from 0 to 6:\nnode 0 should be visited before node 6\nnode 0 should be visited before node 1\nnode 1 should be visited before node 3\nnode 2 should be visited before node 4\nnode 2 should be visited before node 5\nnode 2 should be visited before node 6\nnode 2 should be visited before node 3\nnode 4 should be visited before node 5\nnode 4 should be visited before node 0\nnode 4 should be visited before node 6\nnode 4 should be visited before node 1\nnode 4 should be visited before node 3\nnode 5 should be visited before node 0\nnode 5 should be visited before node 6\nnode 6 should be visited before node 1.\nThis diagram depicts a directed graph, in which each directed edge from node A to node B signifies that, according to the topological order, node A must precede node B.\nQ: The topological order of the directed graph is:"
    },
    {
      "role": "assistant",
      "content": "<think> To determine the topological order of this directed graph, I need to identify the sequence of nodes which respects all the given constraints.  \n\nFirst, I will identify nodes with no incoming edges (no prerequisites). These nodes can appear at the start of a topological order. I should look at all the given constraints to identify such nodes.\n\nThe conditions are:  \n- node 0 should be visited before nodes 6 and 1  \n- node 1 should be visited before node 3  \n- node 2 should be visited before nodes 4, 5, 6, 3  \n- node 4 should be visited before nodes 5, 0, 6, 1, 3  \n- node 5 should be visited before nodes 0, 6  \n- node 6 should be visited before node 1\n\nFirst, I look for a node without any condition that it must appear after another node. From the above dependencies, nodes 2 and 4 are not preceded by any node, letting them appear first in the topological order.\n\nOnce a node has been placed, I will reassess which nodes can come next based on the precedence relations. \n\nLet's proceed by sampling from node 2, which appears to have the least constraints. </think>  \n<sample> sample(G, 2, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/topology/graph_visual/layout/dot/easy/graph169_1.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> Based on the subgraph, I can see the outgoing edges from node 2:  \n- 2 -> 4  \n- 2 -> 5  \n- 2 -> 6  \n- 2 -> 3  \n\nFrom this, I confirm that node 2 must precede nodes 4, 5, 6, and 3 in the topological order.  \n\nNow, I will sample from node 4 to inspect its constraints and outgoing relations, as node 4 does not appear to be preceded by any node other than node 2 already accounted for. </think>  \n<sample> sample(G, 4, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/topology/graph_visual/layout/dot/easy/graph169_2.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> The sampled subgraph reveals the outgoing edges from node 4:  \n- 4 -> 5  \n- 4 -> 0  \n- 4 -> 6  \n- 4 -> 1  \n- 4 -> 3  \n\nThis confirms that node 4 precedes nodes 5, 0, 6, 1, and 3 in the topological order. Combined with the earlier information:  \n- Node 2 must be placed before node 4.  \n\nNow, after placing nodes 2 and 4, I need to find the next node to examine. Based on the graph, nodes 5 and 0 are potential candidates, as their prerequisites (2 and 4) are already accounted for.  \n\nI will now inspect node 5 for its outgoing constraints. </think>  \n<sample> sample(G, 5, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/topology/graph_visual/layout/dot/easy/graph169_3.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> The sampled subgraph shows the outgoing edges from node 5:  \n- 5 -> 0  \n- 5 -> 6  \n\nThis confirms that node 5 must precede nodes 0 and 6 in the topological order. Combining this with earlier insights:  \n- Node 2 comes before node 4.  \n- Node 4 comes before nodes 5, 0, 6, 1, and 3.  \n- Node 5 comes before nodes 0 and 6.  \n\nNow I will sample node 0 to include its outgoing relationships since it must be processed after node 5 based on the constraints. </think>  \n<sample> sample(G, 0, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/topology/graph_visual/layout/dot/easy/graph169_4.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> The sampled subgraph shows the outgoing edges from node 0:  \n- 0 -> 6  \n- 0 -> 1  \n\nThis confirms that node 0 precedes nodes 6 and 1 in the topological order.  \nPreviously, I established these constraints:\n- Node 2 precedes node 4.\n- Node 4 precedes nodes 5, 0, 6, 1, and 3.\n- Node 5 precedes nodes 0 and 6.\n- Node 0 precedes nodes 6 and 1.\n\nNow, I will sample node 6 to gather its outgoing relationships, as it depends on nodes 2, 4, 5, and 0. </think>  \n<sample> sample(G, 6, 1) </sample>"
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Here is the sampled subgraph image"
        },
        {
          "type": "image_url",
          "image_url": "./GVLQA-AUGLY/data/topology/graph_visual/layout/dot/easy/graph169_5.png"
        }
      ]
    },
    {
      "role": "assistant",
      "content": "<think> The sampled subgraph shows the outgoing edge from node 6:  \n- 6 -> 1  \n\nThis confirms that node 6 must precede node 1 in the topological order.  \nSummarizing all dependencies so far:  \n- Node 2 precedes node 4.  \n- Node 4 precedes nodes 5, 0, 6, 1, and 3.  \n- Node 5 precedes nodes 0 and 6.  \n- Node 0 precedes nodes 6 and 1.  \n- Node 6 precedes node 1.  \n\nThe last remaining node to check is node 1. Its dependencies have already been outlined, but I will include it in the topological reasoning next.\n\nSince the nodes processed thus far have accounted for all constraints, I can now determine the topological order of the graph. The sequence that satisfies all constraints is as follows:  \n</think>  \nAnswer: 2,4,5,0,6,1,3."
    }
  ]'''
}

# ====== System 提示：规则 ======
SYSTEM_PROMPT = '''You are a graph reasoning assistant. Your task is to solve problems on graphs described in text.
You must always follow this strict output format:
1. **Reasoning process**:
   * You need to provide your reasoning and must wrap it all in <think> ... </think>.
   * Explain why you need to sample certain nodes and hops.
2. **Function calls**:
   * When you need to inspect part of the graph (at least once), call the function in the form:
     ```
     <sample> sample(G, root, hops) </sample>
     ```
   * `G` is always the graph, `root` is the starting node (must be an integer), and `hops` is the number of hops (must be an integer).
   * After each `<sample> ... </sample>` you must **stop generating** until the system returns the result.
3. **Final answer**:
   * Once you have enough information, output your answer using the format:
     Answer: <your final answer>
4. **Ground-truth enforcement**:
   * The user provides the correct final answer here.
   * You must follow the sampling steps and reasoning, and you **must finish** by outputting the given correct final answer exactly.
   * The correct final answer is : 
     Answer: {ground_truth}
   * Do not deviate from the provided ground-truth.
---
### Example of whole process

{example}

'''


