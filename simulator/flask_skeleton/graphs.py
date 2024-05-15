from pyvis.network import Network
from flask import Flask, request, render_template, session

def dematerialize_net(net):
    #print("Nodessss: ", net.get_nodes())
    graph_nodes = net.get_nodes()
    graph_colors = []
    graph_labels = []
    graph_shapes = []
    graph_titles = []
    for node in graph_nodes:
        node_details = net.get_node(node)
        graph_colors.append(node_details["color"])
        graph_labels.append(node_details["label"])
        graph_shapes.append(node_details["shape"])
        graph_titles.append(node_details["title"])
    #print("Labelsssss: ", graph_labels)

    graph_data= {
    "nodes": graph_nodes,
    "colors": graph_colors,
    "labels": graph_labels,
    "shapes": graph_shapes,
    "titles": graph_titles
    }
    edge_data = net.get_edges()

    session["network_nodes"] = graph_data
    session["network_edges"] = edge_data



def rematerialize_net():
    net = Network()
    net.add_nodes(session["network_nodes"]["nodes"], color=session["network_nodes"]["colors"], label=session["network_nodes"]["labels"], shape=session["network_nodes"]["shapes"], title=session["network_nodes"]["titles"])

    for edge in session["network_edges"]: 
        net.add_edge(edge["from"],edge["to"])

    return net

def run_automatic():
    net = rematerialize_net()
    for vertex in net.get_nodes():
        # Do something
        print(vertex)

def init_globals():
    session["turn_number"] = 0
    session["red_count"] = 0
    session["colored_count"] = 0
    session["instructions_history"] = []
    session["pik_pop"] = ['']

def color_node(node_idx):
    net = rematerialize_net()
    net.nodes[node_idx]['color'] = '#0b22b8'
    net.save_graph("templates/pik_graph.html")

def check_step(step_instructions):
    print("Instructions: ", step_instructions)

    net = rematerialize_net()

    # Assume valid until proven invalid
    step_valid = True

    all_nodes = net.get_nodes()
    for node_idx in all_nodes:
        if step_instructions[0] in net.get_node(node_idx)['label']:
            print("Neighbors ", net.neighbors(node_idx))
            print("Cur node ", node_idx)
            print("Movement ", int(step_instructions[1])-1)
            if (int(step_instructions[1])-1) not in net.neighbors(node_idx) and (int(step_instructions[1])-1) != node_idx: 
                step_valid = False
    
    if step_instructions[2] == "red" or step_instructions[2] == "blue":
        if net.nodes[(int(step_instructions[1])-1)]['color'] != '#f7f7f5':
            step_valid = False

    return step_valid

def execute_step(step_instructions):
    net = rematerialize_net()

    all_nodes = net.get_nodes()
    for node_idx in all_nodes:
        if step_instructions[0] in net.get_node(node_idx)['label'] :
            net.get_node(node_idx)['label'] = net.get_node(node_idx)['label'].replace(step_instructions[0], '')
            net.get_node(node_idx)['label'] = net.get_node(node_idx)['label'].strip()
        
        if net.nodes[node_idx]['title'] == str(step_instructions[1]):
            new_node_idx = node_idx
            net.get_node(new_node_idx)['label'] += " " + step_instructions[0]
            net.get_node(new_node_idx)['label'] = net.get_node(new_node_idx)['label'].strip()
    
    if step_instructions[2] == "red":
        #print("Ran red")
        net.nodes[new_node_idx]['color'] = '#f61709'
        new_pik_name = "Pik " + str(len(session["pik_pop"])+1)
        net.nodes[new_node_idx]['label'] += " " + new_pik_name
        net.get_node(new_node_idx)['label'] = net.get_node(new_node_idx)['label'].strip()

        session["pik_pop"].append(new_pik_name)

        session["red_count"] += 1
        session["colored_count"] += 1
    elif step_instructions[2] == "blue":
        #print("Ran blue")
        net.nodes[new_node_idx]['color'] = '#091df6'
        session["colored_count"] += 1

    net.save_graph("templates/pik_graph.html")
    dematerialize_net(net)

def check_completion():
    net = rematerialize_net()
    all_nodes = net.get_nodes()
    complete = True
    for node_idx in all_nodes:
        # If any node is colored grey, the game is not complete
        if net.nodes[node_idx]['color'] == '#f7f7f5':
            complete = False
    return complete

def load_n_node(n):
    net = Network()
    net.add_nodes(range(n))
    #for i in range(n):
    #    net.add_nodes([str(i)],color=['#222222'])
    net.save_graph("templates/pik_graph.html") 
    dematerialize_net(net)   
    return n

def init_pik(init_idx):
    net = rematerialize_net()

    session["turn_number"] = 0

    if init_idx != 0:
        init_idx = init_idx - 1

    # Clear out the labels of everything in the graph
    #for node_idx in range(len(net.get_nodes())):
    #    net.nodes[node_idx]['label'] = ''

    # Iniatlize the node we want with the label
    pik_name = 'Pik 1'
    net.nodes[init_idx]['label'] += ' ' + pik_name
    
    net.save_graph("templates/pik_graph.html")   
    dematerialize_net(net)

    set_pik_pop([pik_name])
    return([pik_name])
    #net.nodes[node_idx]['color'] = '#0b22b8'

def move_pik(cur_pik, move_loc):
    net = rematerialize_net()

    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        if net.nodes[node_idx]['label'] == cur_pik:
            net.nodes[node_idx]['label'] = ""

    # Iniatlize the node we want with the label
    net.nodes[move_loc]['label'] = cur_pik
    
    net.save_graph("templates/pik_graph.html")   
    dematerialize_net(net)

def load_path(n):
    session.clear()
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        net.nodes[node_idx]['label'] = "Vertex " + str(node_idx+1) + ": "
        if node_idx > 0:
            net.add_edge((node_idx-1),node_idx)
    net.save_graph("templates/pik_graph.html") 
    dematerialize_net(net)   
    init_globals()
    return n

def load_cycle(n):
    session.clear()
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        net.nodes[node_idx]['label'] = "Vertex " + str(node_idx+1) + ": "
        if n > 1:
            net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("templates/pik_graph.html")
    dematerialize_net(net)
    init_globals()
    return n

def load_star(n):
    session.clear()
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        net.nodes[node_idx]['label'] = "Vertex " + str(node_idx+1) + ": "
        if node_idx > 0:
            net.add_edge(0,node_idx)
    net.save_graph("templates/pik_graph.html")   
    dematerialize_net(net)
    init_globals() 
    return n

def load_wheel(n):
    session.clear()
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        net.nodes[node_idx]['label'] = "Vertex " + str(node_idx+1) + ": "
        if node_idx > 0:
            net.add_edge(0,node_idx)
        if n > 2:
            if ((node_idx+1)%n) == 0:
                net.add_edge(node_idx%n,1)
            else: 
                net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("templates/pik_graph.html")  
    dematerialize_net(net)
    init_globals()  
    return n

def load_complete(n):
    session.clear()
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        net.nodes[node_idx]['label'] = "Vertex " + str(node_idx+1) + ": "
        for node_idx_secondary in net.get_nodes():
            if node_idx_secondary != node_idx:
                net.add_edge(node_idx,node_idx_secondary)
    net.save_graph("templates/pik_graph.html")  
    dematerialize_net(net)  
    init_globals()
    return n

def set_turn(turn):
    session["turn_number"] += turn
    return session["turn_number"]

def increment_turn():
    session["turn_number"] += 1
    return session["turn_number"]

def set_pik_pop(new_pik_pop):
    session["pik_pop"] = new_pik_pop
    return session["pik_pop"]

def fetch_pik_pop():
    try:
        print("Cur Pik Pop? ", session["pik_pop"])
        return session["pik_pop"]
    except:
        return ['']

def fetch_red_count():
    try:
        return session["red_count"]
    except:
        return 0
    
def fetch_colored_count():
    try:
        return session["colored_count"]
    except:
        return 0
    
def fetch_instructions_history():
    try:
        return session["instructions_history"]
    except:
        return []
    
def fetch_size():
    try:
        net = rematerialize_net()
        return len(net.get_nodes())
    except:
        return 0
    
def fetch_turn():
    try:
        return session["turn_number"]
    except:
        return 0

def fetch_net():
    try:
        return rematerialize_net()
    except:
        return 

def init_net():
    net = Network()
    net.save_graph("templates/pik_graph.html") 
    dematerialize_net(net)
    return net