### Visualize 1 - sub지정하면 관련 모든 rel, obj 제시

Input Data 형식:  
subject | relation | object 의 dataframe형식


```
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
```
![image](https://user-images.githubusercontent.com/50647833/117236899-ac8fcd00-ae64-11eb-97a2-e31c65bf3f62.png)


### Visualize 2 - sub지정하면 관련 모든 rel, obj 제시

```
# 방법2 - sub, relation 지정하면 관련 모든 obj 제시

def draw_graph_2(data, sub, rel):
    data = data
    data = data[data['subject']==sub]
    data = data[data['relation']==rel]
    
    G = nx.Graph()
    G.add_node(sub)  # subject
    G.add_node(rel)
    
    objects = []
    for i in range(len(data)):
        objects.append(data['object'].values[i])  # objects
        
    G.add_nodes_from(objects)
    
    ### edge 연결 (sub - relation)
    edges = [(sub,rel)]
    G.add_edges_from(edges)  # sub - relation

    ### edge 연결 (relation - objects)
    edges_2 = []
    for i in range(len(data)):
        edges_2.append((rel, data['object'].values[i]))
        
    G.add_edges_from(edges_2)
    
        ## 색깔 지정
    sub_color = {sub: 'yellow'}
    obj_color = {obj:'aqua' for obj in objects}
    rel_color = {rel:'green' for rel in relations}
    sub_color.update(obj_color)
    sub_color.update(rel_color)
    
    val_map = sub_color
    values = [val_map.get(node, 0.3) for node in G.nodes()]
    plt.figure(figsize=(7,5))
    nx.draw(G, with_labels=True,font_family=font_name, node_color=values,linewidths=2, node_size=1500, edge_cmap=plt.cm.Blues, pos=nx.spring_layout(G))
    plt.show()
```
![image](https://user-images.githubusercontent.com/50647833/117236943-c92c0500-ae64-11eb-8757-1ca31669dfb1.png)

### Visualize 3 - 문서 내 존재하는 모든 sub, rel, obj 제시

```
def draw_graph_total(data):    
    data = data

    G = nx.Graph()
    
    subjects = []
    for i in range(len(data)):
        subjects.append(data['subject'].values[i])  # subjects
        
    G.add_nodes_from(subjects)  # subject
    
    relations = []
    for i in range(len(data)):
        relations.append(data['relation'].values[i])  # relations
        
    G.add_nodes_from(relations)
    
    objects = []
    for i in range(len(data)):
        objects.append(data['object'].values[i])  # objects
        
    G.add_nodes_from(objects)
    
    ### edge 연결 (sub - relation)
    edges = []
    for i in range(len(data)):
        edges.append((data['subject'].values[i], data['relation'].values[i]))
    
    G.add_edges_from(edges)  # sub - relation

    ### edge 연결 (relation - objects)
    edges_2 = []
    for i in range(len(data)):
        edges_2.append((data['relation'].values[i] , data['object'].values[i]))
        
    G.add_edges_from(edges_2)
    
    ## 색깔 지정
    sub_color = {sub: 'yellow' for sub in subjects}
    obj_color = {obj:'aqua' for obj in objects}
    rel_color = {rel:'green' for rel in relations}
    sub_color.update(obj_color)
    sub_color.update(rel_color)
    
    val_map = sub_color
    values = [val_map.get(node, 0.3) for node in G.nodes()]
    
    plt.figure(figsize=(40,40))
    nx.draw(G, with_labels=True,font_family=font_name, node_color=values,linewidths=2, node_size=1000, edge_cmap=plt.cm.Blues, pos=nx.spring_layout(G))
    plt.show()
```


