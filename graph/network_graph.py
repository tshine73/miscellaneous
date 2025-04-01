import csv

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import font_manager


def write_csv_from_dict(data_list, output_path):
    with open(output_path, 'w') as f:
        if len(data_list) > 0:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for data in data_list:
                writer.writerow(data)


def read_csv(file_name):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)


def read_node(file_name):
    rows = read_csv(file_name)
    return {row[0]: (row[1], row[2]) for row in rows}


def read_relationship(file_name):
    rows = read_csv(file_name)

    node_relationships = {}
    for row in rows:
        new_targets = row[1].split(",")
        targets = node_relationships.setdefault(row[0], [])
        targets.extend(new_targets)

    return node_relationships


def create_graph(nodes, node_relations):
    graph = nx.Graph()

    edge_id = 1
    for node, targets in node_relations.items():
        if node not in nodes:
            print(f"{node} is not in nodes csv, skip it.")
            continue

        graph.add_node(node, type=nodes[node][0], color=nodes[node][1])

        for target in targets:
            if target not in nodes:
                print(f"{target} is not in nodes csv, skip edge from {node} to {target}.")
                continue

            graph.add_node(target, type=nodes[target][0], color=nodes[target][1])
            graph.add_edge(node, target, edge_id=edge_id)
            edge_id += 1

    print("the graph has ", len(graph.nodes), " nodes and ", len(graph.edges), " edges")

    return graph


def calculate_coordinate(graph):
    # 計算 X, Y 座標，調整 k 參數來確保邊的可見性，並增加迭代次數
    pos = nx.spring_layout(graph, seed=42, k=0.3, iterations=500)  # 降低 k 值來減少節點間距

    # 找到 X 和 Y 座標中的最小值，並進行平移
    min_x, min_y = float('inf'), float('inf')
    for x, y in pos.values():
        min_x = min(min_x, x)
        min_y = min(min_y, y)

    # 平移座標，使得最小值變為 0
    for node in pos:
        pos[node] = (pos[node][0] - min_x, pos[node][1] - min_y)

    # 限制 Y 座標範圍，讓圖形從上到下展開
    y_values = [pos[node][1] for node in pos]
    max_y = max(y_values)
    min_y = min(y_values)

    # 強制 Y 座標在一定範圍內，這樣可以使圖從左到右發展
    for node in pos:
        pos[node] = (pos[node][0], pos[node][1] - min_y)

    # 重新調整 X 座標的範圍，確保左到右排列
    x_values = [pos[node][0] for node in pos]
    max_x = max(x_values)

    # 將 X 座標的範圍調整為從 0 到 max_x，讓圖從左到右分佈
    for node in pos:
        pos[node] = (pos[node][0] * 1.3, pos[node][1])

    return pos


def setup_font(font_path):
    font_manager.fontManager.addfont(font_path)
    font_manager._load_fontmanager()

    prop = font_manager.FontProperties(
        fname=font_path)
    plt.rcParams['font.sans-serif'] = prop.get_name()


def write_graph(graph, pos, output_path):
    output_list = []
    for node, adj_nodes in graph.adj.items():
        for adj_node, edge in adj_nodes.items():
            x, y = pos[node]
            output_list.append({
                'node': node,
                'edge_id': edge['edge_id'],
                "source_node": node,
                'target_node': adj_node,
                "source_type": graph.nodes[node]['type'],
                "target_type": graph.nodes[adj_node]['type'],
                "x": x,
                "y": y
            })

    print(f"write {len(output_list)} combined nodes to {output_path}")
    write_csv_from_dict(output_list, output_path)


def draw_graph(graph, pos):
    node_colors = [graph.nodes[node]['color'] for node in graph]

    # 更小的視窗，使得圖形更加緊湊
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_size=3000, font_size=10, edge_color="gray", width=2,
            node_color=node_colors)
    plt.show()


def main():
    nodes = read_node("node_type.csv")
    node_relations = read_relationship("node_relationship.csv")
    graph = create_graph(nodes, node_relations)

    pos = calculate_coordinate(graph)
    write_graph(graph, pos, "network_graph_output.csv")

    font_path = "/Users/steven.fanchiang/geek/engineering/Noto_Sans_TC/NotoSansTC-VariableFont_wght.ttf"
    setup_font(font_path)
    draw_graph(graph, pos)


if __name__ == "__main__":
    main()
