from pyvis.network import Network

def run_automatic():
    global net
    for vertex in net.get_nodes():
        # Do something
        print(vertex)

def init_globals():
    global turn_count
    global red_count
    global colored_count

    turn_count = 0
    red_count = 0
    colored_count = 0

def color_node(node_idx):
    global net
    net.nodes[node_idx]['color'] = '#0b22b8'
    net.save_graph("app/templates/pik_graph.html")

def check_completion():
    all_nodes = net.get_nodes()
    complete = True
    for node in all_nodes:
        # If any node is colored grey, the game is not complete
        if node['color'] == '#f7f7f5':
            complete = False
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
    global turn_count

    turn_count = 0

    if init_idx != 0:
        init_idx = init_idx - 1

    # Clear out the labels of everything in the graph
    for node_idx in range(len(net.get_nodes())):
        net.nodes[node_idx]['label'] = ''

    # Iniatlize the node we want with the label
    net.nodes[init_idx]['label'] = 'Pik 1'
    
    net.save_graph("app/templates/pik_graph.html")   

    print(net.get_node(init_idx)["label"])
    set_pik_pop([net.get_node(init_idx)["label"]])
    return([net.get_node(init_idx)["label"]])
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

def load_path(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge((node_idx-1),node_idx)
    net.save_graph("app/templates/pik_graph.html")    
    init_globals()
    return n

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
    init_globals()
    return n

def load_star(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge(0,node_idx)
    net.save_graph("app/templates/pik_graph.html")   
    init_globals() 
    return n

def load_wheel(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        if node_idx > 0:
            net.add_edge(0,node_idx)
        if n > 2:
            if ((node_idx+1)%n) == 0:
                net.add_edge(node_idx%n,1)
            else: 
                net.add_edge(node_idx%n,(node_idx+1)%n)
    net.save_graph("app/templates/pik_graph.html")  
    init_globals()  
    return n

def load_complete(n):
    global net
    net = Network()
    net.add_nodes(range(n))
    for node_idx in range(n):
        net.nodes[node_idx]['color'] = '#f7f7f5'
        net.nodes[node_idx]['title'] = str(node_idx+1)
        for node_idx_secondary in net.get_nodes():
            if node_idx_secondary != node_idx:
                net.add_edge(node_idx,node_idx_secondary)
    net.save_graph("app/templates/pik_graph.html")    
    init_globals()
    return n

def set_turn(turn):
    global turn_count
    turn_count += turn
    return turn_count

def increment_turn():
    global turn_count
    turn_count += 1
    return turn_count

def set_pik_pop(new_pik_pop):
    global pik_pop
    pik_pop = new_pik_pop
    return pik_pop

def fetch_pik_pop():
    try:
        return pik_pop
    except:
        return ['']

def fetch_red_count():
    try:
        return red_count
    except:
        return 0
    
def fetch_colored_count():
    try:
        return colored_count
    except:
        return 0
    

def fetch_size():
    try:
        return len(net.get_nodes())
    except:
        return 0
    
def fetch_turn():
    try:
        return turn_count
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