from pyvis.network import Network

def add_node():
    cur_len = len(net.get_nodes())
    net.add_nodes([str(cur_len+1)],color=['#222222'])
    net.save_graph("app/templates/pik_graph.html")

def color_node(node_idx):
    global net
    net.nodes[node_idx]['color'] = '#0b22b8'
    net.save_graph("app/templates/pik_graph.html")

def check_completion():
    all_nodes = net.get_nodes()
    complete = True
    for node in all_nodes:
        print(node)
    return complete

def glimpse_network(): 
    net.show_buttons(['manipulation'])
    net.show("gameofthrones.html", notebook=False)

def load_n_node(n):
    net = Network()
    net.add_nodes(range(n))
    #for i in range(n):
    #    net.add_nodes([str(i)],color=['#222222'])
    net.save_graph("app/templates/pik_graph.html")    
    return n

def init_pik(init_idx):
    global net
    if init_idx != 0:
        init_idx = init_idx - 1
    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        net.nodes[node_idx]['label'] = ''

    # Iniatlize the node we want with the label
    net.nodes[init_idx]['label'] = 'Pik 1'
    
    net.save_graph("app/templates/pik_graph.html")   

    print(net.get_node(node_idx)["label"])
    return([net.get_node(node_idx)["label"]])
    #net.nodes[node_idx]['color'] = '#0b22b8'

def move_pik(cur_pik, move_loc):
    global net

    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        if net.nodes[node_idx]['label'] == cur_pik:
            net.nodes[node_idx]['label'] = ""

    # Iniatlize the node we want with the label
    net.nodes[move_loc]['label'] = cur_pik
    
    net.save_graph("app/templates/pik_graph.html")   

def load_cycle(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if n > 1:
            net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("app/templates/pik_graph.html")    
    return n

def fetch_size():
    try:
        return len(net.get_nodes())
    except:
        return 0

def fetch_net():
    try:
        return net
    except:
        return 

def init_net():
    global net 
    net = Network()
    return net