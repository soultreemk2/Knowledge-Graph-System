import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc

# 한글 폰트 지정
font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


# 방법1 - sub지정하면 관련 모든 rel, obj 제시

def draw_graph(data, sub):    
    data = data
    data = data[data['subject']==sub]
    
    G = nx.Graph()
    G.add_node(sub)  # subject
    
    relations = []
    for i in range(len(data)):
        relations.append(data['relation'].values[i])  # relation
        
    G.add_nodes_from(relations)
    
    objects = []
    for i in range(len(data)):
        objects.append(data['object'].values[i])  # relation
        
    G.add_nodes_from(objects)
    
    ### edge 연결 (sub - relation)
    edges = []
    for i in range(len(data)):
        edges.append((sub,data['relation'].values[i]))
    
    G.add_edges_from(edges)  # sub - relation

    ### edge 연결 (relation - objects)
    edges_2 = []
    for i in range(len(data)):
        edges_2.append((data['relation'].values[i] , data['object'].values[i]))
        
    G.add_edges_from(edges_2)
    
    ## 색깔 지정
    sub_color = {sub: 'yellow'}
    obj_color = {obj:'aqua' for obj in objects}
    rel_color = {rel:'green' for rel in relations}
    sub_color.update(obj_color)
    sub_color.update(rel_color)
    
    val_map = sub_color
    values = [val_map.get(node, 0.3) for node in G.nodes()]
    
    plt.figure(figsize=(8,6))
    nx.draw(G, with_labels=True,font_family=font_name, node_color=values,linewidths=2, node_size=1500, edge_cmap=plt.cm.Blues, pos=nx.spring_layout(G))
    plt.show()
